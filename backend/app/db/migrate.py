"""Apply checked, ordered SQL migrations atomically (TG-R06).

Run from backend/: uv run python -m app.db.migrate [migrate|status]
The connection belongs to the migration owner, never to a future API runtime role.
"""

import argparse
import hashlib
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import psycopg
from psycopg.pq import TransactionStatus

MIGRATIONS_DIR = Path(__file__).resolve().parents[3] / "db" / "migrations"
# One transaction-scoped lock serializes migration runners within the database.
MIGRATION_LOCK = 764982163442601
FILE_PATTERN = re.compile(r"(?P<version>\d{4})_[a-z0-9_]+\.sql")


class MigrationError(Exception):
    """Migration history and the versioned sources disagree."""


@dataclass(frozen=True)
class Migration:
    version: int
    filename: str
    sql: str
    checksum: str


def load_migrations(directory: Path = MIGRATIONS_DIR) -> list[Migration]:
    paths = sorted(directory.glob("*.sql"))
    if not paths:
        raise MigrationError("No SQL migrations found")
    migrations = []
    for expected_version, path in enumerate(paths, start=1):
        match = FILE_PATTERN.fullmatch(path.name)
        if match is None or int(match["version"]) != expected_version:
            raise MigrationError("Migration filenames must form a sequence starting at 0001")
        # Normalize checkout line endings, so a Windows clone has the same checksum as CI.
        source = path.read_text(encoding="utf-8")
        if not source.strip():
            raise MigrationError("Empty SQL migration")
        migrations.append(
            Migration(
                expected_version,
                path.name,
                source,
                hashlib.sha256(source.encode("utf-8")).hexdigest(),
            )
        )
    return migrations


def _applied(conn: psycopg.Connection) -> list[tuple[int, str, str]]:
    exists = conn.execute(
        "SELECT EXISTS (SELECT FROM information_schema.tables "
        "WHERE table_schema = current_schema() AND table_name = 'schema_migrations')"
    ).fetchone()
    if not exists or not exists[0]:
        return []
    return conn.execute(
        "SELECT version, filename, checksum FROM schema_migrations ORDER BY version"
    ).fetchall()


def _validate_history(migrations: list[Migration], applied: list[tuple[int, str, str]]) -> None:
    expected = [(m.version, m.filename, m.checksum) for m in migrations[: len(applied)]]
    if applied != expected:
        raise MigrationError("Applied migration history differs from the checked-in SQL files")


def migrate(conn: psycopg.Connection, directory: Path = MIGRATIONS_DIR) -> list[str]:
    """Apply the entire pending batch or roll back the entire batch on any error."""
    if not conn.autocommit or conn.info.transaction_status != TransactionStatus.IDLE:
        raise MigrationError("Migrations require a fresh autocommit connection")
    migrations = load_migrations(directory)
    completed = []
    with conn.transaction():
        conn.execute("SELECT pg_advisory_xact_lock(%s)", (MIGRATION_LOCK,))
        conn.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations ("
            "version integer PRIMARY KEY, filename text NOT NULL UNIQUE, "
            "checksum char(64) NOT NULL, applied_at timestamptz NOT NULL DEFAULT now())"
        )
        applied = _applied(conn)
        _validate_history(migrations, applied)
        for migration in migrations[len(applied) :]:
            conn.execute(migration.sql, prepare=False)
            conn.execute(
                "INSERT INTO schema_migrations (version, filename, checksum) VALUES (%s, %s, %s)",
                (migration.version, migration.filename, migration.checksum),
            )
            completed.append(migration.filename)
    return completed


def migration_status(conn: psycopg.Connection) -> list[tuple[str, str]]:
    migrations = load_migrations()
    applied = _applied(conn)
    _validate_history(migrations, applied)
    return [(m.filename, "applied" if m.version <= len(applied) else "pending") for m in migrations]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["migrate", "status"], nargs="?", default="migrate")
    args = parser.parse_args()
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("Set DATABASE_URL to the migration-owner connection URL.", file=sys.stderr)
        return 2
    try:
        with psycopg.connect(
            database_url, autocommit=True, connect_timeout=5, application_name="tenderguard-migrate"
        ) as conn:
            if args.command == "migrate":
                completed = migrate(conn)
                print("Applied: " + ", ".join(completed) if completed else "Schema is up to date.")
            else:
                for filename, state in migration_status(conn):
                    print(f"{state:7} {filename}")
    except MigrationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except psycopg.Error as exc:
        # DSNs, credentials and server messages containing row data must not be logged.
        print(
            f"Database operation failed (SQLSTATE {exc.sqlstate or 'connection'}).", file=sys.stderr
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
