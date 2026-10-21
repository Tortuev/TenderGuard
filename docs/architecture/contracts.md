# Architecture integration contracts

These contracts specify the intended interaction between the frontend, backend,
retrieval/agent modules, worker and Inference Gateway. They accompany the
[architecture](architecture.md); they do not describe an already running API.
Names of existing SQL fields are retained where applicable. Proposed persistence
extensions must be implemented with reviewed forward migrations.

## Request context and roles

FastAPI authenticates the caller and derives the user identity from a verified
session. A route organization ID is accepted only after active membership and
role checks. The resulting internal context contains `user_id`, `organization_id`,
`role`, request correlation ID and the applicable policy reference. An LLM,
uploaded file, request body or browser header cannot supply trusted versions of
these fields. Sessions and service credentials must not be embedded in prompts.

`member` and `owner` can create evidence, runs, questions and reviews. `viewer`
can read permitted results and sources. Only `owner` can administer membership
and organization policy. Worker/service identities are scoped operational
identities, not unrestricted product owners. Revalidate authorization for delayed
jobs and model dispatch when membership or policy may have changed.

## Proposed HTTP surface

All paths below have the prefix `/api/v1/organizations/{organization_id}`.
Listing and lookup endpoints are organization-scoped; knowledge of a UUID does
not grant access. IDs in responses identify persisted resources, not public URLs.

| Method and path | Input / response contract | Role and implementation boundary |
| --- | --- | --- |
| `POST /tenders` | Validated title; returns tender ID | Member/owner; tenant derived from checked context |
| `POST /documents` | Multipart text-based PDF/DOCX, logical document target and classification request; returns version ID and ingestion job ID | Member/owner; validate bytes, limits and ownership, assign effective classification server-side; reject unsupported/unsafe files |
| `POST /tenders/{tender_id}/documents` | Attach an authorized document version to the tender | Member/owner; same-organization reference checked before inserting `tender_documents` |
| `POST /company-profiles/{profile_id}/versions` | Attributes and authorized evidence-version IDs; returns a sealed profile version | Member/owner; immutable attributes, atomically selected evidence and profile seal |
| `POST /analysis-runs` | Tender ID, exact profile version, selected tender versions, selected company-evidence IDs and an allowed analysis configuration | Member/owner; successful ingestion required; atomically assemble, seal and enqueue; return `202` with run/job IDs |
| `GET /jobs/{job_id}` | Safe state, stage/progress if known, error code and retry guidance | Any active member permitted to read the related resource; no stack traces, prompts or provider secrets |
| `GET /analysis-runs/{run_id}` | Immutable input manifest, execution state and completed report if available | Any authorized active member; partial artifacts clearly separated from completed results |
| `POST /analysis-runs/{run_id}/questions` | Bounded question and permitted selected evidence scope; returns supported answer, insufficient evidence or blocked processing | Member/owner; same retrieval/gateway policy; never modifies existing findings |
| `POST /analysis-runs/{run_id}/reviews` | Finding reference, review action and comment; returns a new review-event ID | Member/owner; append only; a correction requiring reanalysis creates a new run |
| `GET /documents/{document_version_id}/source` | Validated locator or chunk reference; returns authorized excerpt/view data | Any active member permitted to read the underlying document; no unrestricted storage key or public path |
| `GET /audit-events` and policy/member administration | Bounded, paginated safe audit reads and validated administrative commands | Owner only; policy changes cannot retroactively rewrite a run's recorded inputs or audit |

Creation requests use an organization- and operation-scoped idempotency key with
a canonical request fingerprint. A matching retry returns the same resource;
a different payload with the same key is a conflict. The database's current
organization/key uniqueness is only a foundation, not this complete API contract.

Initial QA is a bounded synchronous request: a supported answer or insufficient
evidence returns `200`; a policy block returns `409` with a safe policy code;
provider unavailability or a deadline failure returns a safe `503` outcome.
Timeout, input-size and model-call budgets are configuration decisions to confirm
with the evaluation protocol. QA is not silently assigned a nonexistent job kind
in the current ingestion/analysis-only job schema.

| Outcome | Intended HTTP behaviour |
| --- | --- |
| Missing or invalid authentication | `401` |
| Insufficient role within a permitted organization | `403` |
| Unknown or unauthorized organization/resource | `404`, without exposing another organization's existence |
| Invalid input schema / locator | `422` |
| Oversized or unsupported upload | `413` / `415` |
| Inputs not ready, sealed-version mutation, or idempotency conflict | `409` with a safe machine-readable code |
| Accepted asynchronous work | `202` with resource and job references |
| Job later blocked, failed or cancelled | Resource lookup returns its explicit state; never a fabricated successful report |

Upload creation spans file storage and PostgreSQL. Validate and stage bytes under
an organization-scoped temporary key, persist metadata/enqueue atomically, then
publish the durable object reference using a recoverable protocol. Reconcile
orphaned staged files after interruption. Do not claim a single database
transaction can atomically commit filesystem writes.

## Citation and retrieval contract

An evidence reference contains `organization_id` internally, document role
(`tender`, `company` or approved `reference`), exact `document_version_id`,
`chunk_id`, source locator and a supporting quote. The backend resolves IDs from
the manifest; model-generated IDs are checked against the supplied candidates.

| Locator | Meaning and validation |
| --- | --- |
| PDF page | One-based `page_number` plus optional extraction-block locator; the referenced text must resolve in that immutable file version |
| DOCX paragraph | Zero-based stable `paragraph_index` in the recorded extraction order |
| DOCX table cell | Zero-based `table_index`, `row_index`, `column_index` and optional paragraph index within the cell |
| Canonical text span | Unicode-code-point `char_start` inclusive and `char_end` exclusive in the parser's recorded canonical text; not byte offsets |

Initial chunks should remain within a resolvable page/paragraph/cell boundary.
Record parser and normalization settings; never use offsets from a different
extraction or document revision. Check quote support and bounds server-side;
database foreign keys alone cannot validate them.

Retrieval takes verified organization context, a sealed run manifest, query,
document role, language and bounded ranking parameters. The allowed candidate
set is the intersection of active permissions and selected inputs. Apply that
boundary to lexical, dense and reranked candidates, including cached results.
Company evidence outside the selected profile/run, later document revisions and
another organization's chunks must not enter the candidate set. Return evidence
references and retrieval scores, not a claim that a score establishes compliance.

Embedding results include model/artifact identity, dimensions and preprocessing
settings. Query and stored vectors must use compatible configurations; changing
them requires a new index/configuration, not mixing incompatible vectors. Dense
retrieval yielding too few authorized candidates must be visible and measured;
never relax access filters to fill the requested result count.

## Stage contracts

All stages receive bounded typed inputs and return validated outputs. An agent
can propose a finding; it cannot grant access, select a different organization,
perform arbitrary network requests or write to unrelated resources.

| Stage / interface | Required input | Required output and invariant |
| --- | --- | --- |
| Ingestion | Authorized immutable document version, effective classification and parser/chunker configuration | Parsed text, language, source locators and chunks; optional embeddings only through the permitted gateway route. Unsupported scans produce an explicit unsupported outcome. |
| Requirement extraction | Selected tender evidence references and extraction configuration | Atomic label/text, type, applicable condition, value/unit where present, language and tender citation. Unresolvable or unsupported requirements are not silently accepted. |
| Documentary matching | Validated requirement and selected applicable company evidence | `met`, `unmet` or `unknown`; short supported explanation; tender citation and any applicable company citations. Both met and unmet require company evidence, matching current SQL. |
| Risk and report | Validated requirements/findings, input manifest and explicit risk rules | Requirement/evidence matrix, unknowns, bounded risk flags and preparation actions. Deterministic counts and prioritization are distinguishable from model wording. No award probability or blanket legal approval. |
| Question answering | Authorized question and a permitted subset of run evidence | Supported answer with resolvable citations, or `insufficient_evidence`. A policy block or model error is a separate processing outcome. |
| Inference Gateway | Authenticated internal caller, server-verified run/policy scope, operation, configured schema/model preference and classified context | Permitted route/model reference, validated result envelope and safe audit reference, or a typed blocked/error result. The response remains untrusted for factual support. |

For illustration, a matching output can have this shape. It is a proposed
interface example, not an experimental result or an existing SQL row:

```json
{
  "requirement_label": "delivery-01",
  "status": "unknown",
  "explanation": "No applicable delivery commitment was found in the selected company evidence.",
  "tender_citations": [
    {
      "document_version_id": "11111111-1111-4111-8111-111111111111",
      "chunk_id": "22222222-2222-4222-8222-222222222222",
      "locator": {"kind": "pdf_page", "page_number": 2},
      "quote": "Delivery within 10 calendar days."
    }
  ],
  "company_evidence_id": null,
  "company_citations": [],
  "legal_status": "legal_unknown"
}
```

For met/unmet, require a non-null selected `company_evidence_id` and supporting
company citations. Missing evidence alone does not prove unmet. A supported
seven-day commitment is met against the example only if it applies to the same
goods and calendar-day conditions; an incompatible minimum of fourteen days is
unmet. Preserve ambiguity as unknown. Legal applicability remains a separate
field with its own evidence/rules, not an alternative value in the SQL finding
status enum.

## Execution and persistence

1. Validate and ingest every selected input; do not seal a run over unresolved
   upload or parsing jobs.
2. In one database transaction, verify active scope, select exact tender and
   company evidence, insert the immutable run/configuration and associations,
   seal the input set, and enqueue the job. Mutation and sealing must share a
   locking/constraint protocol that closes concurrent-insert races.
3. Claim ready work in a short transaction; record a lease and fencing token.
   Perform parsing/model calls outside that transaction. Heartbeat or expire the
   lease according to a bounded worker policy.
4. Process stages using only the sealed inputs and configured pipeline. Persist
   intermediate artifacts with explicit stage/attempt identity; they are not
   completed findings. Check routing again for each call and retry.
5. Publish the complete validated result in a transaction conditional on the
   current lease, active execution and unchanged input seal. Stale workers cannot
   publish after another worker takes over. Do not repeat provider side effects
   blindly after an ambiguous timeout; account for any repeated calls/costs.
6. New input, configuration or corrected analysis creates a new run. A human
   review appends an event and does not overwrite the original machine finding.

Proposed run-execution states are `assembling`, `queued`, `running`, `completed`,
`failed`, `blocked` and `cancelled`. Progress lives outside immutable `analysis_runs`.
The current job enum is only `queued`, `running`, `completed`, `failed`, `cancelled`.
Until an explicit migration changes it, represent a policy-blocked job as `failed`
with a safe `POLICY_BLOCKED` code and a separate blocked execution state. Do not
insert `blocked` into the existing job enum. Retrying an operational failure
does not authorize a new data route or silently change the frozen model policy.

A run configuration must capture the selected input manifest hash, parser/chunker,
embedding, retrieval, prompt/schema, model, pipeline/baseline, policy and risk-rule
references. Hashes/identifiers must resolve to retained permitted configuration
artifacts; recording a model name alone does not make a run reproducible.

## Gateway decision and audit contract

The gateway independently validates its internal caller and server-owned context.
It determines the allowed route from the effective policy, not a model-provided
URL. Classify the complete outgoing payload, including quoted snippets, earlier
stage outputs and the question itself. Personal-data masking is one possible
transformation and does not automatically declassify commercial information.

If no approved route exists, return a typed block without sending context.
Use the intersection of the run's recorded permissions and the current policy;
a stricter current rule can block a run, while a configuration change requires
an explicit new run rather than silent relaxation of its recorded policy.
Restricted local processing cannot silently fall back to hosted processing.
Retries, schema repairs, embeddings and evaluations follow the same rule.
Local placeholder mappings, if used, are organization/run-scoped, access-controlled
and expired by policy; do not send them to the provider or restore values into
another run. Error payloads from providers are treated as potentially sensitive.

Safe audit records contain organization, permitted actor/service reference, run,
stage, operation, policy/configuration reference, selected route/model, outcome,
call correlation, event timestamp, latency and usage where provided. Raw confidential
prompts, documents, credentials and mapping values do not belong in ordinary
application logs. Controlled synthetic payload capture for evaluation is separate
from production logging and has its own restricted retention.

## Contract acceptance and handoff

| Check | Expected evidence / owner |
| --- | --- |
| Authorization is independent of the browser/model | Two organizations, inactive membership and viewer-write negative cases; Ramazan with Rassul |
| Inputs and citations remain version-bound | New revision, later-added evidence, bad quote/locator and foreign chunk cases; Rassul with Daniyar |
| Sealing and retries are safe under concurrency | Concurrent insert/seal, lease expiry, stale worker, cancellation and changed-payload idempotency cases; Rassul |
| Unknown differs from failure and unmet | Missing/ambiguous evidence, supported mismatch and blocked-model fixtures; Daniyar with Rassul |
| Every model route enforces policy | Captured embedding, generation, retry and local-to-hosted output cases; Ramazan |
| UI reflects the same resource and outcome fields | Walkthrough of upload, report, both citation sides, unknown and blocked states; Ramazan with all members |
| Baselines are comparable | Fixed permitted manifests, configuration records and separate RU/KK results; Daniyar |

These are implementation acceptance cases to be exercised by later tasks, not
tests claimed to have passed for the unimplemented platform. Team review must
confirm model-specific limits, exact persistence extensions and API schemas
before implementation is presented as accepted.
