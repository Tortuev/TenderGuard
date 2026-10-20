"""Integration fixtures: every test owns a fresh schema in a disposable database."""

import os
from types import SimpleNamespace
from uuid import uuid4

import psycopg
import pytest
from psycopg import sql
from psycopg.types.json import Jsonb

from app.db.migrate import migrate


def insert(conn, table, **values):
    """Insert a test record using quoted identifiers and bound values."""
    return conn.execute(
        sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING id").format(
            sql.Identifier(table),
            sql.SQL(", ").join(map(sql.Identifier, values)),
            sql.SQL(", ").join(sql.Placeholder() for _ in values),
        ),
        tuple(Jsonb(value) if isinstance(value, dict) else value for value in values.values()),
    ).fetchone()[0]


@pytest.fixture
def connection():
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Set TEST_DATABASE_URL to a disposable PostgreSQL database")
    schema = "tg_test_" + uuid4().hex
    with psycopg.connect(url, autocommit=True, connect_timeout=5) as conn:
        conn.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
        conn.execute(sql.SQL("SET search_path TO {}").format(sql.Identifier(schema)))
        try:
            yield conn
        finally:
            # Only the randomly named schema created by this fixture is removed.
            conn.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))


@pytest.fixture
def db(connection):
    migrate(connection)
    return connection


@pytest.fixture
def tenant_factory(db):
    def create():
        organization = insert(db, "organizations", name="Synthetic test organization")
        user = insert(db, "users", external_subject="test:" + uuid4().hex)
        db.execute(
            "INSERT INTO memberships (organization_id, user_id, role) VALUES (%s, %s, 'owner')",
            (organization, user),
        )
        tender = insert(db, "tenders", organization_id=organization, title="Synthetic tender")
        document = insert(db, "documents", organization_id=organization, title="Tender PDF")
        version = insert(
            db,
            "document_versions",
            organization_id=organization,
            document_id=document,
            version=1,
            filename="synthetic.pdf",
            media_type="application/pdf",
            size_bytes=100,
            sha256="a" * 64,
            storage_key=f"{organization}/{uuid4()}.pdf",
            data_class="public",
        )
        db.execute(
            "INSERT INTO tender_documents VALUES (%s, %s, %s)",
            (tender, organization, version),
        )
        profile = insert(db, "company_profiles", organization_id=organization, name="SME")
        profile_version = insert(
            db,
            "company_profile_versions",
            organization_id=organization,
            company_profile_id=profile,
            version=1,
            attributes={"synthetic": True},
        )
        evidence = insert(
            db,
            "company_evidence",
            organization_id=organization,
            company_profile_version_id=profile_version,
            document_version_id=version,
            label="Synthetic certificate",
        )
        chunk = insert(
            db,
            "chunks",
            organization_id=organization,
            document_version_id=version,
            chunker_version="test-v1",
            ordinal=0,
            content="A valid certificate is required.",
            char_start=0,
            char_end=32,
            source_locator={"page": 1},
        )
        run = insert(
            db,
            "analysis_runs",
            organization_id=organization,
            tender_id=tender,
            company_profile_version_id=profile_version,
            requested_by=user,
            configuration={"pipeline_version": "test-v1"},
        )
        db.execute(
            "INSERT INTO analysis_run_documents VALUES (%s, %s, %s, %s)",
            (run, organization, tender, version),
        )
        requirement = insert(
            db,
            "requirements",
            organization_id=organization,
            run_id=run,
            label="REQ-01",
            text="Provide a valid certificate",
            source_document_version_id=version,
            source_chunk_id=chunk,
            source_quote="A valid certificate is required.",
        )
        finding = insert(
            db,
            "findings",
            organization_id=organization,
            run_id=run,
            requirement_id=requirement,
            company_profile_version_id=profile_version,
            company_evidence_id=evidence,
            status="met",
            explanation="Synthetic test evidence supports this result.",
        )
        return SimpleNamespace(
            organization=organization,
            user=user,
            tender=tender,
            document=document,
            version=version,
            profile=profile,
            profile_version=profile_version,
            evidence=evidence,
            chunk=chunk,
            run=run,
            requirement=requirement,
            finding=finding,
        )

    return create
