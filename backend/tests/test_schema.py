from uuid import uuid4

import psycopg
import pytest
from conftest import insert
from psycopg import sql

pytestmark = pytest.mark.database


def test_complete_synthetic_analysis_graph(db, tenant_factory):
    tenant = tenant_factory()
    row = db.execute(
        "SELECT f.status, r.source_quote, c.source_locator->>'page' "
        "FROM findings f JOIN requirements r ON r.id = f.requirement_id "
        "JOIN chunks c ON c.id = r.source_chunk_id WHERE f.id = %s",
        (tenant.finding,),
    ).fetchone()
    assert row == ("met", "A valid certificate is required.", "1")


@pytest.mark.parametrize(
    "relationship",
    [
        "document",
        "profile",
        "evidence",
        "chunk",
        "run_tender",
        "run_profile",
        "run_member",
        "manifest",
        "requirement",
        "finding",
        "job",
    ],
)
def test_cross_organization_references_are_rejected(db, tenant_factory, relationship):
    first, other = tenant_factory(), tenant_factory()
    org = first.organization
    operations = {
        "document": (
            "INSERT INTO document_versions (organization_id, document_id, version, filename, "
            "media_type, size_bytes, sha256, storage_key, data_class) "
            "VALUES (%s, %s, 2, 'test.pdf', 'application/pdf', 1, %s, %s, 'public')",
            (org, other.document, "b" * 64, f"{org}/new.pdf"),
        ),
        "profile": (
            "INSERT INTO company_profile_versions (organization_id, company_profile_id, "
            "version, attributes) VALUES (%s, %s, 2, '{}')",
            (org, other.profile),
        ),
        "evidence": (
            "INSERT INTO company_evidence (organization_id, company_profile_version_id, "
            "document_version_id, label) VALUES (%s, %s, %s, 'test')",
            (org, first.profile_version, other.version),
        ),
        "chunk": (
            "INSERT INTO chunks (organization_id, document_version_id, chunker_version, "
            "ordinal, content, char_start, char_end, source_locator) "
            "VALUES (%s, %s, 'v2', 0, 'test', 0, 4, '{}')",
            (org, other.version),
        ),
        "run_tender": (
            "INSERT INTO analysis_runs (organization_id, tender_id, company_profile_version_id, "
            "requested_by, configuration) VALUES (%s, %s, %s, %s, '{}')",
            (org, other.tender, first.profile_version, first.user),
        ),
        "run_profile": (
            "INSERT INTO analysis_runs (organization_id, tender_id, company_profile_version_id, "
            "requested_by, configuration) VALUES (%s, %s, %s, %s, '{}')",
            (org, first.tender, other.profile_version, first.user),
        ),
        "run_member": (
            "INSERT INTO analysis_runs (organization_id, tender_id, company_profile_version_id, "
            "requested_by, configuration) VALUES (%s, %s, %s, %s, '{}')",
            (org, first.tender, first.profile_version, other.user),
        ),
        "manifest": (
            "INSERT INTO analysis_run_documents VALUES (%s, %s, %s, %s)",
            (first.run, org, first.tender, other.version),
        ),
        "requirement": (
            "INSERT INTO requirements (organization_id, run_id, label, text, "
            "source_document_version_id, source_chunk_id, source_quote) "
            "VALUES (%s, %s, 'NEW', 'test', %s, %s, 'test')",
            (org, first.run, first.version, other.chunk),
        ),
        "finding": (
            "INSERT INTO findings (organization_id, run_id, requirement_id, "
            "company_profile_version_id, status, explanation) "
            "VALUES (%s, %s, %s, %s, 'unknown', 'test')",
            (org, first.run, other.requirement, first.profile_version),
        ),
        "job": (
            "INSERT INTO processing_jobs (organization_id, kind, run_id, idempotency_key) "
            "VALUES (%s, 'analysis', %s, 'test')",
            (org, other.run),
        ),
    }
    statement, params = operations[relationship]
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        db.execute(statement, params)


def test_source_chunk_must_belong_to_the_cited_document(db, tenant_factory):
    tenant = tenant_factory()
    document = insert(db, "documents", organization_id=tenant.organization, title="Other document")
    version = insert(
        db,
        "document_versions",
        organization_id=tenant.organization,
        document_id=document,
        version=1,
        filename="other.pdf",
        media_type="application/pdf",
        size_bytes=1,
        sha256="b" * 64,
        storage_key=f"{tenant.organization}/other.pdf",
        data_class="public",
    )
    chunk = insert(
        db,
        "chunks",
        organization_id=tenant.organization,
        document_version_id=version,
        chunker_version="v1",
        ordinal=0,
        content="Other text",
        char_start=0,
        char_end=10,
        source_locator={"page": 1},
    )
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        insert(
            db,
            "requirements",
            organization_id=tenant.organization,
            run_id=tenant.run,
            label="NEW",
            text="test",
            source_document_version_id=tenant.version,
            source_chunk_id=chunk,
            source_quote="test",
        )


def test_manifest_must_use_documents_attached_to_the_runs_tender(db, tenant_factory):
    tenant = tenant_factory()
    different_tender = insert(db, "tenders", organization_id=tenant.organization, title="Other")
    run = insert(
        db,
        "analysis_runs",
        organization_id=tenant.organization,
        tender_id=different_tender,
        company_profile_version_id=tenant.profile_version,
        requested_by=tenant.user,
        configuration={},
    )
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        db.execute(
            "INSERT INTO analysis_run_documents VALUES (%s, %s, %s, %s)",
            (run, tenant.organization, tenant.tender, tenant.version),
        )
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        db.execute(
            "INSERT INTO analysis_run_documents VALUES (%s, %s, %s, %s)",
            (run, tenant.organization, different_tender, tenant.version),
        )


def test_finding_cannot_use_evidence_from_a_different_profile_version(db, tenant_factory):
    tenant = tenant_factory()
    requirement = insert(
        db,
        "requirements",
        organization_id=tenant.organization,
        run_id=tenant.run,
        label="SECOND",
        text="test",
        source_document_version_id=tenant.version,
        source_chunk_id=tenant.chunk,
        source_quote="test",
    )
    profile_version = insert(
        db,
        "company_profile_versions",
        organization_id=tenant.organization,
        company_profile_id=tenant.profile,
        version=2,
        attributes={"synthetic": True},
    )
    evidence = insert(
        db,
        "company_evidence",
        organization_id=tenant.organization,
        company_profile_version_id=profile_version,
        document_version_id=tenant.version,
        label="v2",
    )
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        insert(
            db,
            "findings",
            organization_id=tenant.organization,
            run_id=tenant.run,
            requirement_id=requirement,
            company_profile_version_id=tenant.profile_version,
            company_evidence_id=evidence,
            status="met",
            explanation="test",
        )


@pytest.mark.parametrize("status", ["met", "unmet", "unknown"])
def test_missing_company_evidence_is_unknown(db, tenant_factory, status):
    tenant = tenant_factory()
    requirement = insert(
        db,
        "requirements",
        organization_id=tenant.organization,
        run_id=tenant.run,
        label="NEW",
        text="test",
        source_document_version_id=tenant.version,
        source_chunk_id=tenant.chunk,
        source_quote="test",
    )

    def create_finding():
        return insert(
            db,
            "findings",
            organization_id=tenant.organization,
            run_id=tenant.run,
            requirement_id=requirement,
            company_profile_version_id=tenant.profile_version,
            status=status,
            explanation="No usable company evidence.",
        )

    if status == "unknown":
        assert create_finding()
    else:
        with pytest.raises(psycopg.errors.CheckViolation):
            create_finding()


@pytest.mark.parametrize(
    "table, field",
    [
        ("document_versions", "version"),
        ("company_profile_versions", "profile_version"),
        ("company_evidence", "evidence"),
        ("chunks", "chunk"),
        ("analysis_runs", "run"),
        ("requirements", "requirement"),
        ("findings", "finding"),
    ],
)
@pytest.mark.parametrize("operation", ["update", "delete", "truncate"])
def test_snapshot_rows_cannot_be_rewritten(db, tenant_factory, table, field, operation):
    tenant = tenant_factory()
    identifier = sql.Identifier(table)
    with pytest.raises(psycopg.errors.ObjectNotInPrerequisiteState):
        if operation == "update":
            db.execute(
                sql.SQL("UPDATE {} SET id = id WHERE id = %s").format(identifier),
                (getattr(tenant, field),),
            )
        elif operation == "delete":
            db.execute(
                sql.SQL("DELETE FROM {} WHERE id = %s").format(identifier),
                (getattr(tenant, field),),
            )
        else:
            db.execute(sql.SQL("TRUNCATE {} CASCADE").format(identifier))


@pytest.mark.parametrize(
    "operation",
    [
        "UPDATE analysis_run_documents SET run_id = run_id WHERE run_id = %s",
        "DELETE FROM analysis_run_documents WHERE run_id = %s",
        "TRUNCATE analysis_run_documents CASCADE",
    ],
)
def test_run_input_rows_are_immutable(db, tenant_factory, operation):
    tenant = tenant_factory()
    with pytest.raises(psycopg.errors.ObjectNotInPrerequisiteState):
        db.execute(operation, (tenant.run,) if "%s" in operation else None)


def test_new_versions_can_be_added_without_changing_existing_results(db, tenant_factory):
    tenant = tenant_factory()
    new_version = insert(
        db,
        "company_profile_versions",
        organization_id=tenant.organization,
        company_profile_id=tenant.profile,
        version=2,
        attributes={"certificate": "new"},
    )
    db.execute("UPDATE company_profiles SET name = 'Renamed' WHERE id = %s", (tenant.profile,))
    assert new_version != tenant.profile_version
    assert (
        db.execute(
            "SELECT company_profile_version_id FROM findings WHERE id = %s", (tenant.finding,)
        ).fetchone()[0]
        == tenant.profile_version
    )


def test_document_version_requires_valid_metadata(db, tenant_factory):
    tenant = tenant_factory()
    valid = dict(
        organization_id=tenant.organization,
        document_id=tenant.document,
        version=2,
        filename="test.pdf",
        media_type="application/pdf",
        size_bytes=1,
        sha256="b" * 64,
        storage_key=f"{tenant.organization}/new.pdf",
        data_class="private",
    )
    for invalid in [
        {"sha256": "not-a-hash"},
        {"size_bytes": 0},
        {"version": 0},
        {"filename": " "},
        {"storage_key": f"{uuid4()}/wrong-organization.pdf"},
        {"storage_key": f"{tenant.organization}/../escape.pdf"},
        {"media_type": "application/x-executable"},
        {"data_class": "unspecified"},
    ]:
        with pytest.raises(psycopg.errors.CheckViolation):
            insert(db, "document_versions", **(valid | invalid))
    assert insert(db, "document_versions", **valid)
    with pytest.raises(psycopg.errors.UniqueViolation):
        insert(
            db, "document_versions", **(valid | {"storage_key": f"{tenant.organization}/dup.pdf"})
        )


def test_jobs_are_tenant_scoped_and_have_one_valid_target(db, tenant_factory):
    tenant, other = tenant_factory(), tenant_factory()
    values = dict(
        organization_id=tenant.organization,
        kind="analysis",
        run_id=tenant.run,
        idempotency_key="analysis:test",
    )
    job = insert(db, "processing_jobs", **values)
    with pytest.raises(psycopg.errors.UniqueViolation):
        insert(db, "processing_jobs", **values)
    assert insert(
        db,
        "processing_jobs",
        **(
            values
            | {
                "organization_id": other.organization,
                "run_id": other.run,
            }
        ),
    )
    for invalid in [
        {"run_id": None},
        {"document_version_id": tenant.version},
        {"kind": "ingestion"},
        {"attempt": 4},
        {"max_attempts": 0},
        {"status": "invented"},
    ]:
        with pytest.raises(psycopg.errors.CheckViolation):
            insert(db, "processing_jobs", **(values | {"idempotency_key": uuid4().hex} | invalid))
    db.execute("UPDATE processing_jobs SET status = 'running', attempt = 1 WHERE id = %s", (job,))
    assert db.execute(
        "SELECT status, attempt FROM processing_jobs WHERE id = %s", (job,)
    ).fetchone() == ("running", 1)
    assert insert(
        db,
        "processing_jobs",
        organization_id=tenant.organization,
        kind="ingestion",
        document_version_id=tenant.version,
        idempotency_key="ingestion:test",
    )
