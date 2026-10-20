import hashlib
import os
from concurrent.futures import ThreadPoolExecutor

import psycopg
import pytest
from psycopg import sql

from app.db.migrate import MigrationError, load_migrations, migrate, migration_status


def test_sources_have_contiguous_versions_and_stable_checksums(tmp_path):
    source = tmp_path / "0001_example.sql"
    source.write_bytes(b"SELECT 1;\r\n")
    windows = load_migrations(tmp_path)[0]
    source.write_bytes(b"SELECT 1;\n")
    linux = load_migrations(tmp_path)[0]
    assert windows.checksum == linux.checksum == hashlib.sha256(b"SELECT 1;\n").hexdigest()


@pytest.mark.parametrize(
    "filename, content",
    [
        ("0002_gap.sql", "SELECT 1;"),
        ("unversioned.sql", "SELECT 1;"),
        ("0001_empty.sql", "   \n"),
    ],
)
def test_invalid_migration_sources_are_rejected(tmp_path, filename, content):
    (tmp_path / filename).write_text(content, encoding="utf-8")
    with pytest.raises(MigrationError):
        load_migrations(tmp_path)


def test_missing_migrations_are_rejected(tmp_path):
    with pytest.raises(MigrationError, match="No SQL migrations"):
        load_migrations(tmp_path)


@pytest.mark.database
def test_clean_setup_and_repeat_apply(connection):
    filenames = [migration.filename for migration in load_migrations()]
    assert migration_status(connection) == [(name, "pending") for name in filenames]
    assert migrate(connection) == filenames
    assert migrate(connection) == []
    assert migration_status(connection) == [(name, "applied") for name in filenames]
    tables = {
        row[0]
        for row in connection.execute(
            "SELECT tablename FROM pg_tables WHERE schemaname = current_schema()"
        )
    }
    assert tables == {
        "schema_migrations",
        "organizations",
        "users",
        "memberships",
        "tenders",
        "documents",
        "document_versions",
        "tender_documents",
        "company_profiles",
        "company_profile_versions",
        "company_evidence",
        "chunks",
        "analysis_runs",
        "analysis_run_documents",
        "requirements",
        "findings",
        "processing_jobs",
    }


@pytest.mark.database
@pytest.mark.parametrize("tamper", ["checksum", "filename", "version", "extra"])
def test_modified_or_unknown_history_is_rejected(connection, tamper):
    migrate(connection)
    if tamper == "extra":
        connection.execute(
            "INSERT INTO schema_migrations (version, filename, checksum) "
            "VALUES (9999, '9999_unknown.sql', %s)",
            ("0" * 64,),
        )
    else:
        value = {"checksum": "0" * 64, "filename": "0001_renamed.sql", "version": 99}[tamper]
        connection.execute(
            sql.SQL("UPDATE schema_migrations SET {} = %s WHERE version = 1").format(
                sql.Identifier(tamper)
            ),
            (value,),
        )
    with pytest.raises(MigrationError, match="history differs"):
        migrate(connection)
    with pytest.raises(MigrationError, match="history differs"):
        migration_status(connection)


@pytest.mark.database
def test_failed_batch_rolls_back_schema_and_history(connection, tmp_path):
    (tmp_path / "0001_start.sql").write_text("CREATE TABLE example (id integer);", encoding="utf-8")
    (tmp_path / "0002_fail.sql").write_text("SELECT * FROM nonexistent_table;", encoding="utf-8")
    with pytest.raises(psycopg.errors.UndefinedTable):
        migrate(connection, tmp_path)
    assert connection.execute("SELECT to_regclass('example')").fetchone()[0] is None
    assert connection.execute("SELECT to_regclass('schema_migrations')").fetchone()[0] is None


@pytest.mark.database
def test_failed_upgrade_preserves_previously_applied_migrations(connection, tmp_path):
    (tmp_path / "0001_start.sql").write_text("CREATE TABLE example (id integer);", encoding="utf-8")
    migrate(connection, tmp_path)
    (tmp_path / "0002_fail.sql").write_text(
        "ALTER TABLE example ADD COLUMN name text; SELECT * FROM nonexistent_table;",
        encoding="utf-8",
    )
    with pytest.raises(psycopg.errors.UndefinedTable):
        migrate(connection, tmp_path)
    assert connection.execute("SELECT version FROM schema_migrations").fetchall() == [(1,)]
    assert connection.execute(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_schema = current_schema() AND table_name = 'example'"
    ).fetchall() == [("id",)]


@pytest.mark.database
def test_concurrent_runners_apply_each_migration_once(connection):
    schema = connection.execute("SELECT current_schema()").fetchone()[0]

    def run():
        with psycopg.connect(os.environ["TEST_DATABASE_URL"], autocommit=True) as other:
            other.execute(sql.SQL("SET search_path TO {}").format(sql.Identifier(schema)))
            return migrate(other)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: run(), range(2)))
    assert sorted(map(len, results)) == [0, len(load_migrations())]
    assert connection.execute("SELECT count(*) FROM schema_migrations").fetchone()[0] == 2


@pytest.mark.database
def test_runner_rejects_an_existing_transaction(connection):
    with connection.transaction(), pytest.raises(MigrationError, match="fresh autocommit"):
        migrate(connection)
