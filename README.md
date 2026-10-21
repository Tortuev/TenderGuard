# TenderGuard

A diploma project to build a privacy-preserving multi-agent RAG platform for automated
tender document and compliance risk analysis for SMEs.

**Current implementation:** the PostgreSQL database foundation for **TG-R06**.
This repository does not yet provide a web application, HTTP API, working agents or
privacy enforcement. Use synthetic data for development.

## Team

| Member | Responsibility |
| --- | --- |
| Daniyar Kairatov | ML, retrieval and evaluation |
| Rassul Akhmetov | Backend, database, agent orchestration and analysis workflows |
| Ramazan Talgatov | Platform, privacy, DevOps and UI integration |

TG-R06 belongs to Rassul; Ramazan is the planned reviewer. Completed implementation
still requires peer review before merging into `main`.

## Included in TG-R06

- Organizations, users and memberships.
- Tenders, uploaded document versions and company profile/evidence versions.
- Chunks with source locators, analysis runs, input manifests, requirements and findings.
- Processing-job records with tenant-scoped idempotency and valid target constraints.
- Ordered, checksummed SQL migrations with atomic rollback and concurrent-run protection.
- Immutable version/result rows, an [ER diagram and database contract](docs/database.md),
  and integration tests against PostgreSQL 17.

## Local setup

Prerequisites: Git, Docker Compose, [uv](https://docs.astral.sh/uv/getting-started/installation/)
and Python 3.13. `uv sync --python 3.13` can provision Python if it is not installed.

In PowerShell, starting in the repository root:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and replace `POSTGRES_PASSWORD`. These values are local development
credentials. The database binds only to `127.0.0.1:55432` by default; change
`POSTGRES_PORT` in `.env` if that port is in use.

```powershell
docker compose up -d --wait db
Set-Location backend
uv sync --locked --python 3.13
```

Set `DATABASE_URL` in the current shell using the same user, password, port and database
as `.env`. The following prompts for the password so it does not appear in command history:

```powershell
$databaseCredential = Get-Credential -UserName tenderguard_owner -Message "Local PostgreSQL password"
$encodedPassword = [uri]::EscapeDataString($databaseCredential.GetNetworkCredential().Password)
$env:DATABASE_URL = "postgresql://tenderguard_owner:${encodedPassword}@127.0.0.1:55432/tenderguard"
Remove-Variable databaseCredential, encodedPassword
uv run python -m app.db.migrate status
uv run python -m app.db.migrate
uv run python -m app.db.migrate status
```

Adjust the connection example if you changed the defaults. The migration CLI reads
`DATABASE_URL` from the shell; it does not automatically load the root `.env` file.
First application reports both SQL files; a repeat reports `Schema is up to date.`

For Bash, use `cp .env.example .env`, `cd backend`, and `export DATABASE_URL=...` with
your local credentials; the uv and migration commands are the same.

Stop the local database from the repository root with `docker compose down`.
Its named volume is preserved between restarts.

## Verification

From `backend/`:

```powershell
uv run ruff check .
uv run ruff format --check .
$env:TEST_DATABASE_URL = $env:DATABASE_URL
uv run pytest
```

Use a **disposable development/test database**, never a production database.
Integration tests create randomly named `tg_test_*` schemas and drop only those
schemas during cleanup. They need an account with permission to create schemas.
The normal `public` application schema is not reset. Without `TEST_DATABASE_URL`,
database tests are skipped; that is not a complete verification. The GitHub Actions
workflow supplies a fresh PostgreSQL 17 service and runs the complete suite.

Coverage includes clean and repeat migrations, modified migration history, atomic
failure rollback, concurrent runners, cross-organization foreign references, wrong
document/profile associations, immutable rows, evidence-required findings and jobs.

## Repository layout

```text
.github/workflows/backend.yml   Database integration and lint checks
backend/app/db/migrate.py       Migration command
backend/tests/                 Migration and schema tests
backend/uv.lock                Locked development/runtime dependencies
db/migrations/                 Ordered PostgreSQL SQL files
docs/database.md               ER diagram, data contracts and limitations
docs/research/literature-review.md  Shared literature review
compose.yaml                   Local PostgreSQL 17 service
```

## Next integration tasks

- **TG-T06 / TG-T07:** authentication, runtime roles, RLS and organization read isolation.
- **TG-R07:** typed FastAPI endpoints and server-validated organization context.
- **TG-R08:** durable processing, input sealing, leases and retries.
- **TG-R09:** validated upload and private file storage.
- **TG-D08 / TG-D14:** embeddings and vector retrieval contracts.

Database constraints alone do not enforce privacy. See the
[security boundary and dependencies](docs/database.md#security-boundary-and-remaining-dependencies)
before connecting any real company documents.

## Documentation

- [Database foundation and ER diagram](docs/database.md)
- [Project proposal](docs/proposal.md)
- [Requirements and acceptance criteria](docs/requirements.md)
- [Literature review](docs/research/literature-review.md)
- [Existing systems comparison: CIS platforms](docs/comparisons/existing-systems.md)

The proposal and requirements define the target scope for TG-R01, with priorities,
acceptance criteria and unresolved decisions. Team and supervisor approval are pending.
The literature review contains four scientific source discussions, a synthesis and
proposed design/evaluation decisions. It is ready for team review; approval remains pending.
The other predefence materials will be added under `docs/` as their tasks are completed.

Store detailed research and predefence materials under `docs/` and link them here.
Notion holds tasks, discussion and evidence links; reviewed repository versions
provide the submission record. Each member commits their own work and obtains
another member's review.

## Predefence documents

Linked documents are available for review. Paths shown as code are planned destinations;
add working links as those materials become available.

| Criterion | Material | Document or planned path |
| --- | --- | --- |
| 1 | Project proposal and scope | [Proposal](docs/proposal.md) |
| 2 | Relevance findings and permitted interview evidence | `docs/relevance.md` |
| 3 | Literature review and separate regulatory analysis | [Literature review](docs/research/literature-review.md); `docs/research/regulatory-review.md` planned |
| 4 | Existing systems comparison | [Five CIS systems, ten criteria and observation evidence](docs/comparisons/existing-systems.md) |
| 5 | Technology comparisons and decisions | `docs/comparisons/technologies.md` |
| 6 | Functional and non-functional requirements | [Requirements](docs/requirements.md) |
| 7 | Architecture, editable diagrams and readable exports | `docs/architecture/` |
| 8 | UX prototype link, screens and scenarios | `docs/ux/` |
| 9 | Verification and evaluation protocol | `docs/evaluation-plan.md` |
| 10 | Responsibilities, milestones, risks, dependencies and tracker | `docs/project-management.md` |
| 11 | Actual supervisor comments and resulting changes | `docs/supervisor-feedback.md` |

Keep private interview recordings, contact details and confidential company files
in restricted storage. Repository documentation should contain anonymized findings
and authorized evidence links. Do not commit paid paper copies or confidential
datasets as supporting material.
