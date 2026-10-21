# TenderGuard architecture

TenderGuard is designed as a web application for checking a tender package against
an SME's own documentary evidence. It preserves source locations, distinguishes
supported conclusions from missing evidence, and controls which context can reach
a model provider. This package supplies the architectural description, diagrams,
data model and integration contracts for TG-R04 and predefence component 7.

The [proposal](../project-proposal/proposal.md) defines the intended product.
The repository currently implements the [relational database foundation](../database/database.md),
migration runner and database checks. The interface, authentication, RLS, parsing,
retrieval, worker, agents and Inference Gateway below are **planned components**.
A completed design is not evidence that their runtime controls already work.

## Package contents

The six diagrams are editable Mermaid code blocks in this document and render
directly in its GitHub preview. This is their single source of truth. Vector
exports remain available for the report and predefence submission.

| View | Mermaid diagram | SVG export | Purpose |
| --- | --- | --- | --- |
| System context | [View diagram](#system-context) | [context.svg](export/context.svg) | Users, external systems and the external model boundary |
| Use cases | [View diagram](#actors-and-use-cases) | [use-cases.svg](export/use-cases.svg) | Actors and requirement-linked actions |
| Components | [View diagram](#component-responsibilities) | [components.svg](export/components.svg) | Responsibilities, interfaces and the four processing stages |
| Entity relationships | [View diagram](#data-model-and-required-evolution) | [data-model.svg](export/data-model.svg) | Existing tables and tenant-aware relationships |
| Analysis sequence | [View diagram](#processing-and-failure-semantics) | [analysis-flow.svg](export/analysis-flow.svg) | Ingestion, sealed inputs, policy checks and result publication |
| Deployment | [View diagram](#deployment-boundary) | [deployment.svg](export/deployment.svg) | Private services, file storage and controlled model egress |

[Integration contracts](contracts.md) define the proposed API, stage inputs,
citations, outcomes and lifecycle. The refinements below explain how the supplied
supervisor architecture is adapted to the company-evidence workflow and current
repository implementation.

## Refinements of the supplied architecture

| Design area | TenderGuard decision and reason |
| --- | --- |
| Main request path | Retain browser, Caddy, Next.js, FastAPI, PostgreSQL, processing stages and a Privacy Gateway. Call the gateway **Inference Gateway** consistently in these diagrams; it includes the privacy policy boundary. |
| Company-specific analysis | Add explicit company-profile versions and supporting document versions alongside tender inputs. A tender summary alone cannot establish a supplier's documentary fit. |
| Execution | Use a durable worker and transactional PostgreSQL job enqueue for the first integrated workflow. In-process background tasks are insufficient for the proposed crash-recovery contract. No Redis or general workflow framework is required by this design. |
| Privacy | Require policy authorization of the complete context, not just identifier replacement. Masking personal identifiers does not automatically permit commercially sensitive content to leave. |
| Gateway placement | Plan a small internal Inference Gateway service so provider credentials and permitted external model access have one boundary. The API and worker use its scoped interface; the stages remain modules in one worker, not separate microservices. |
| Models | Local embeddings form the proposed retrieval baseline; model and dimensions need selection. Local generative inference and adaptation are optional. Hosted open-weight models still count as external processing. Routing is decided per call, not permanently by agent name. |
| Legal flags | Separate documentary matching from legal applicability. An unverified reference corpus or applicability rule yields `legal_unknown`; no unrestricted legal audit is promised. |
| Storage | Retain PostgreSQL 17 and private file references. Vectors, RLS, audit, sealing and review persistence require later migrations; they are not present merely because a diagram includes them. |
| Project tooling | GitHub stores code, reviewed documents and evidence; Notion coordinates tasks. Neither GitLab nor YouTrack is required. |

The supervisor's illustrated fixed embedding dimension, hosting cost, workload
capacity and partial implementation labels are not adopted as measured facts.
Technology benchmarking remains a separate deliverable under component 5.

## Scope and consistency matrix

The `AR-*` identifiers below are **working architecture references** derived from
the proposal's core workflow and objectives. They provide traceability while the
separate requirements specification is being prepared; they are not a claim of
supervisor approval. Reconcile them with component 6 without losing the mapping.
Core references must remain covered by both a use case and a component.

| Reference and required behaviour | Use cases | Responsible components | Data / verification anchor |
| --- | --- | --- | --- |
| AR-01 Active membership and role-based actions | UC-01, UC-08 | Identity and authorization; Next.js interface; Caddy | `users`, `memberships`; anonymous, inactive and viewer-write cases |
| AR-02 Company-profile and evidence versions | UC-02 | Document and company service; Private FileStore | `company_profile_versions`, `company_evidence`; applicability and exact-version references |
| AR-03 Validated text-based PDF/DOCX ingestion | UC-03 | Document and company service; Job runner; ingestion | `document_versions`, `chunks`; invalid, oversized, empty and unsupported-file outcomes |
| AR-04 Atomic requirements with tender citations | UC-04 | Requirement extraction; Authorized retrieval | `requirements`, `analysis_run_documents`; every citation belongs to a selected input |
| AR-05 Company-specific met/unmet/unknown findings | UC-04 | Documentary matching; Authorized retrieval | `findings`; met/unmet require applicable company evidence |
| AR-06 Inspectable reports and both sides of evidence | UC-05 | Run / report / review service; Next.js interface | Authorized run, finding, document and source-locator reads |
| AR-07 Grounded answers with insufficient-evidence handling | UC-06 | Question-answer service; Authorized retrieval; Inference Gateway | Run-scoped evidence references; unsupported answer withheld |
| AR-08 Human review and new runs after revisions | UC-07 | Run / report / review service; Document and company service | Immutable versions/results; planned review events and sealed run selections |
| AR-09 Organization isolation and controlled processing | UC-04, UC-06, UC-08 | Identity and authorization; Inference Gateway; PostgreSQL; Private FileStore; safe audit | Foreign-organization denial, blocked routes and observed outbound payload checks |
| AR-10 Durable processing and visible non-success states | UC-04 | Job runner; Run / report / review service; Next.js interface | `processing_jobs`; planned lease fencing, run lifecycle and retry cases |
| AR-11 Russian/Kazakh document processing | UC-03, UC-04, UC-06 | Ingestion; Authorized retrieval; requirement extraction; Question-answer service | Language-labelled fixtures and separate quality measurements |
| AR-12 Bounded risk flags and separate legal uncertainty | UC-04, UC-05 | Documentary matching; risk and report | Evidence-backed flags, transparent aggregation, `legal_unknown` when unresolved |
| AR-13 Reproducible baseline and staged evaluation | UC-09 | Offline evaluation harness; same worker, retrieval and gateway contracts | Frozen permitted inputs, model/configuration manifest, metrics and retained failures |

Automatic bid submission, payments, digital signatures, market-wide crawling,
award prediction and every procurement category are outside the core scope.
OCR, downloadable reports, model adaptation and local generation are extensions
with their own acceptance checks; none may silently bypass the core controls.

## System context

<!-- diagram:context -->

```mermaid
flowchart LR
    analyst["SME analyst<br/>member or owner"]
    viewer["Manager / viewer"]
    owner["Organization owner"]
    researcher["Research evaluator"]
    portal["Procurement portals<br/>manual sourcing"]
    system["TenderGuard<br/>company evidence + tender analysis<br/>cited reports + controlled processing"]
    hosted["Approved hosted model provider<br/>outside operator control"]
    portal -->|Public tender download| analyst
    analyst -->|Tender files, company evidence, questions| system
    system -->|Findings, citations, unknowns, job state| analyst
    viewer -->|Authorized read requests| system
    system -->|Permitted reports and evidence| viewer
    owner -->|Membership and processing policies| system
    system -->|Safe audit and route decisions| owner
    researcher -->|Permitted fixed evaluation fixtures| system
    system -->|Supported outputs and measurements| researcher
    system -->|Only permitted minimal context via Inference Gateway| hosted
    hosted -->|Untrusted model output| system
```

The analyst obtains documents through permitted channels and uploads them; no
automated integration with procurement portals is assumed. Authorized managers
read reports, owners control membership and policy, and the evaluator runs
permitted research fixtures. Hosted inference is the explicit external processing
boundary. Browser delivery of an authorized report is a separate access decision;
permission to read a document is not permission to send it to a model provider.

## Actors and use cases

<!-- diagram:use-cases -->

```mermaid
flowchart LR
    analyst["«actor»<br/>SME analyst<br/>member or owner"]
    viewer["«actor»<br/>Manager / viewer"]
    owner["«actor»<br/>Organization owner"]
    researcher["«actor»<br/>Research evaluator"]
    subgraph system["TenderGuard — proposed use cases"]
      direction TB
      UC01(["UC-01 Sign in and select organization<br/>AR-01"])
      UC02(["UC-02 Maintain company evidence versions<br/>AR-02"])
      UC03(["UC-03 Upload and inspect tender documents<br/>AR-03, AR-11"])
      UC04(["UC-04 Run evidence-based analysis<br/>AR-04, AR-05, AR-09, AR-10, AR-11, AR-12"])
      UC05(["UC-05 Read report and inspect citations<br/>AR-06, AR-12"])
      UC06(["UC-06 Ask a cited question<br/>AR-07, AR-09, AR-11"])
      UC07(["UC-07 Review findings and create a new run<br/>AR-08"])
      UC08(["UC-08 Manage members, policy and audit<br/>AR-01, AR-09"])
      UC09(["UC-09 Evaluate fixed baselines<br/>AR-13"])
    end
    analyst --> UC01 & UC02 & UC03 & UC04 & UC05 & UC06 & UC07
    viewer --> UC01 & UC05
    owner --> UC01 & UC08
    researcher --> UC09
```

Actor boxes use the UML `actor` stereotype and use cases use oval shapes. An owner
may also act as an analyst; a viewer has read access only. Every action rechecks
active membership server-side. The research evaluator uses a controlled harness
and permitted fixtures; this role does not grant unrestricted production access.

| Role | Permitted product actions | Boundary |
| --- | --- | --- |
| `member` | Manage permitted company/tender evidence, start analysis, ask questions, review findings and read reports | Cannot manage organization membership or processing policy |
| `viewer` | Read permitted reports and resolve their cited sources | Cannot upload, start runs, create reviews or change policy; persisted QA creation is an analyst action |
| `owner` | Analyst actions plus membership, policy and permitted audit administration | Administrative changes remain auditable; owner is not the database superuser |

## Component responsibilities

<!-- diagram:components -->

```mermaid
flowchart TB
    browser["Browser<br/>untrusted client"]
    proxy["Caddy<br/>TLS / same-origin routing"]
    web["Next.js interface<br/>forms, report, citations, job state"]
    subgraph api["FastAPI process — proposed modular backend"]
      auth["Identity and authorization<br/>active membership + role checks"]
      evidence["Document and company service<br/>validation + immutable versions"]
      runs["Run / report / review service<br/>sealed inputs + authorized reads"]
      qa["Question-answer service<br/>run-scoped evidence"]
    end
    subgraph worker["Durable worker process — proposed"]
      jobs["Job runner<br/>claim, lease, retry, fenced commit"]
      ingest["Stage 1: ingestion<br/>parse, locate, chunk, embed"]
      extract["Stage 2: requirement extraction<br/>atomic cited requirements"]
      match["Stage 3: documentary matching<br/>met / unmet / unknown"]
      report["Stage 4: risk and report<br/>bounded flags + deterministic summary"]
      retrieval["Authorized retrieval<br/>manifest filter + lexical/dense fusion"]
    end
    gateway["Inference Gateway service — proposed<br/>policy + minimization + adapters<br/>all embedding and generation calls"]
    local["Local embedding runtime — planned core<br/>optional local generative runtime"]
    hosted["Approved hosted model API<br/>permitted contexts only"]
    db[("PostgreSQL 17<br/>relational foundation implemented<br/>RLS / vectors / lifecycle extensions planned")]
    files[("Private FileStore<br/>validated keys + access checks<br/>planned")]
    audit[("Safe model / access audit<br/>tenant-scoped records<br/>planned")]
    evaluation["Offline evaluation harness<br/>same retrieval and gateway contracts"]
    browser --> proxy
    proxy --> web
    proxy --> auth
    web -->|Same-origin API requests| auth
    auth --> evidence & runs & qa
    evidence --> files
    api -->|Authorized metadata and result transactions| db
    runs -.->|Enqueue and claim through PostgreSQL| jobs
    jobs --> ingest --> extract --> match --> report
    worker -->|Manifest-scoped reads and fenced publication| db
    ingest --> files
    extract & match & qa --> retrieval
    worker -->|All stage and embedding calls| gateway
    qa -->|Question generation and query embedding| gateway
    gateway -->|Approved internal route| local
    gateway -->|Approved external route only| hosted
    gateway --> audit
    gateway -->|Read effective policy and active scope| db
    audit --> db
    auth & runs --> audit
    evaluation -.-> jobs
    evaluation -.-> qa
```

FastAPI hosts the application modules; a separate worker performs durable
processing. Stage 1 is a technical ingestion stage and does not require an LLM
agent. Stages 2–4 use bounded extraction, matching and reporting interfaces.
Authorized retrieval is shared with question answering. The Inference Gateway
handles embedding and generation requests, including repair and evaluation calls.
The chart shows logical stores and modules, not a separate container for every box.

| Component | Responsibility and boundary | Implementation lead / proposed location |
| --- | --- | --- |
| Caddy and Next.js interface | Same-origin routing; profile/upload/report screens; citations and job states; no provider secrets in the browser | Ramazan coordinates `frontend/`; each member implements their feature screens |
| Identity and authorization | Verified session, active membership, role checks and server-derived organization context | Ramazan, `backend/app/auth/` |
| Document and company service | File validation, version creation, evidence selection and authorized file access | Rassul, `backend/app/documents/`, `backend/app/company/` |
| Run / report / review service | Atomic run assembly, authorized result reads and append-only human reviews | Rassul, `backend/app/analysis/` |
| Question-answer service | Bound questions to authorized evidence and validate supported answers | Daniyar with Rassul, `backend/app/qa/` |
| Job runner | Transactional enqueue, claim/lease, retries, cancellation and fenced publication | Rassul, `backend/app/jobs/` |
| Ingestion and Authorized retrieval | Parsing, canonical text, locators, local embeddings and filtered lexical/dense retrieval | Daniyar, `backend/app/ingestion/`, `backend/app/rag/` |
| Requirement extraction | Atomic values/conditions with verifiable tender references | Daniyar; Rassul integrates typed stages in `backend/app/agents/` |
| Documentary matching; risk and report | Apply company evidence, preserve unknowns and assemble traceable findings | Rassul with Daniyar, `backend/app/agents/`, `backend/app/analysis/` |
| Inference Gateway and local adapters | Enforce routes, minimize context, validate destinations and capture safe audit; local runtime is isolated from public access | Ramazan with Daniyar, `backend/app/privacy/`, `backend/app/providers/` |
| PostgreSQL and Private FileStore | Relational integrity, restricted reads, immutable references and private bytes | Rassul owns persistence; Ramazan owns runtime isolation and deployment |
| Safe audit | Actor, organization, run, policy, route and result code without raw confidential payloads | Ramazan with Rassul, `backend/app/audit/` |
| Offline evaluation harness | Fixed baselines and development/test separation; same controls as the application | Daniyar coordinates `backend/evaluation/`; all members supply subsystem evidence |

Locations are proposed module boundaries, not directories already implemented.
The gateway can reuse the backend package in a separate process. Avoid introducing
an agent framework, message broker or additional datastore without a demonstrated
requirement and a component-5 decision.

## Data model and required evolution

<!-- diagram:data-model -->

```mermaid
erDiagram
    organizations ||--o{ memberships : has
    users ||--o{ memberships : joins
    organizations ||--o{ tenders : owns
    organizations ||--o{ documents : owns
    documents ||--o{ document_versions : versions
    tenders ||--o{ tender_documents : includes
    document_versions ||--o{ tender_documents : attached_as
    organizations ||--o{ company_profiles : owns
    company_profiles ||--o{ company_profile_versions : versions
    company_profile_versions ||--o{ company_evidence : supports
    document_versions ||--o{ company_evidence : provides
    document_versions ||--o{ chunks : parsed_into
    tenders ||--o{ analysis_runs : analyzed_in
    company_profile_versions ||--o{ analysis_runs : evaluated_in
    memberships ||--o{ analysis_runs : requests
    analysis_runs ||--o{ analysis_run_documents : selects
    tender_documents ||--o{ analysis_run_documents : available_input
    analysis_run_documents ||--o{ requirements : source_document
    chunks ||--o{ requirements : source_chunk
    requirements ||--o| findings : evaluated_as
    analysis_runs ||--o{ findings : produces
    company_evidence o|--o{ findings : supports
    organizations ||--o{ processing_jobs : owns
    analysis_runs o|--o{ processing_jobs : analysis_target
    document_versions o|--o{ processing_jobs : ingestion_target
```

This ER view reflects the existing migration tables. Every tenant-owned reference
retains `organization_id`; global users are linked to organizations by membership.
An analysis run selects a specific profile version and exact tender document
versions. Requirements point to selected tender chunks. A finding's company
evidence must belong to the run's profile version. The optional job-target edges
are exclusive: the SQL check permits a document ingestion target or an analysis
run target, never both. Infrastructure migration history is omitted.

The [SQL migrations](../../db/migrations/) and
[database contract](../database/database.md) are authoritative for implemented
columns and constraints. Their immutable rows do not yet seal related collections,
restrict reads or establish factual citation support.

| Planned evolution | Why the existing schema is insufficient | Required invariant |
| --- | --- | --- |
| Profile evidence sealing | Evidence can currently be appended to an existing profile version | Atomically finish a profile version and its evidence, then seal it; insertion and sealing take the same parent lock so a concurrent insert cannot bypass the seal |
| Run company-evidence selection and sealing | The run currently selects tender documents but not an immutable list of company-evidence rows | Add a selected-evidence association and lifecycle seal; retrieve only those selected rows, with same-profile and same-organization constraints |
| Mutable run-execution record | `analysis_runs` is immutable and has no execution state | Store operational state separately; never update an immutable run to mark progress |
| Lease fencing and request fingerprints | Expiry and idempotency fields alone do not stop stale workers or changed-payload key reuse | Add a fencing token and request fingerprint; publish only under the current lease and reject a reused key with a different request |
| Structured requirement/risk fields | Current requirements and findings contain only the initial evidence/explanation fields | Add validated condition/value/unit/language and bounded risk data through forward migrations, preserving existing rows |
| Multiple finding citations | A current finding has one primary company-evidence reference, not a full set of evidence passages | Keep the primary anchor and add citation rows for tender/company passages; validate every referenced chunk against the sealed inputs |
| Human reviews, QA records and safe audit | These persistence models are not yet implemented | Append new review/QA/audit records with actor and access context; never overwrite machine findings or log private prompts |
| RLS, vectors and model configuration | Neither RLS nor vector columns/indexes currently exist | Use restricted runtime roles and server-scoped transactions; choose embedding dimensions before creating an index, and test filtered retrieval |

These are migration requirements for later implementation tasks, not SQL changes
made by TG-R04. Exact table/column names for the new records remain an integration
decision. Do not edit applied migrations to make this diagram appear implemented.

## Processing and failure semantics

<!-- diagram:analysis-flow -->

```mermaid
sequenceDiagram
    actor Analyst
    participant API as FastAPI
    participant Store as PostgreSQL + FileStore
    participant Worker as Durable worker
    participant Retrieve as Authorized retrieval
    participant Gateway as Inference Gateway
    participant Model as Selected local / hosted runtime
    Analyst->>API: Upload tender and company document versions
    API->>API: Authenticate, authorize, validate file limits/type
    API->>Store: Store private bytes and immutable metadata
    API->>Store: Enqueue ingestion transactionally
    Worker->>Store: Claim ingestion with lease / fencing token
    Worker->>Worker: Stage 1: parse, locate, chunk
    Worker->>Gateway: Classified embedding request
    Gateway->>Gateway: Check approved local embedding route
    Gateway->>Model: Permitted embedding request
    Model-->>Gateway: Embeddings
    Gateway-->>Worker: Validated embedding result
    Worker->>Store: Publish authorized chunks/index state
    Analyst->>API: Create run with exact profile and tender versions
    API->>Store: Atomically select evidence, seal manifest, enqueue
    API-->>Analyst: Accepted job reference
    Worker->>Store: Claim analysis and load sealed manifest
    Worker->>Retrieve: Retrieve only authorized selected inputs
    Retrieve-->>Worker: Evidence with source locators
    Note over Worker,Gateway: Stage 2 extract, stage 3 match, stage 4 report - every model call uses the gateway
    loop Each required model call while execution remains active
      Worker->>Gateway: Stage request + run scope + classified context
      Gateway->>Gateway: Verify policy, minimize, select permitted route
      alt No permitted route
        Gateway-->>Worker: Policy-blocked result with no model request
        Worker->>Store: Mark run blocked / job failed safely
      else Permitted route
        Gateway->>Model: Approved payload only
        Model-->>Gateway: Untrusted structured output
        Gateway-->>Worker: Validated envelope and safe audit reference
        Worker->>Worker: Validate citations, schema and stage invariants
      end
    end
    alt All required stages valid and current lease held
      Worker->>Worker: Assemble complete validated report
      Worker->>Store: Fenced transaction publishes complete findings
    else Blocked, failed, cancelled or stale lease
      Worker->>Store: Preserve explicit outcome without a completed report
    end
    Analyst->>API: Poll state and read completed report and citations
    API->>Store: Recheck membership and authorize each referenced source
    Store-->>API: Permitted result or explicit failed / blocked state
    API-->>Analyst: Report with met / unmet / unknown, or processing outcome
```

Uploads and analysis are separate jobs. Analysis requires successfully ingested
inputs, an exact profile version and an atomically sealed selection. Each stage
validates its input and output; documents and model responses are untrusted data.
An unknown compliance finding is a valid analytical outcome. A blocked route,
parser failure, exhausted retry or invalid model response is a processing outcome
and must not be presented as a completed unknown-filled report.

Workers claim jobs in a short transaction and release database locks before model
calls. A lease/fencing check protects final publication from a stale worker.
Only one complete, validated set of findings is published as a completed run;
partial stage artifacts remain distinguishable from a final report. The detailed
[stage and lifecycle contracts](contracts.md#execution-and-persistence) define
the required transitions and the mapping to current job statuses.

The single-prompt RAG baseline and staged pipeline use the same permitted frozen
inputs and gateway policy. Differences in retrieval settings, model budget or
hardware must be recorded rather than attributed to agent coordination alone.

## Trust boundaries and privacy controls

| Boundary / threat | Required control | Verification evidence to obtain |
| --- | --- | --- |
| Browser to API: forged organization or role | Validate the session and active membership; a selected organization ID is a lookup key, not authority | Missing/expired session, inactive member, foreign organization and viewer-write requests |
| API/worker to PostgreSQL: unscoped reads | Non-owner runtime roles, no `BYPASSRLS`, fail-closed RLS and transaction-local verified organization context | Two-organization reads/writes, missing context and reused connection cases |
| Document to parser/model: hostile content | Type/resource limits, disabled external document fetches, isolated parsing, bounded tools and schema/citation validation | Oversized/archive-expansion cases, remote relationship links and prompt-injection fixtures |
| Retrieval to a stage: overbroad context | Organization, sealed manifest, selected company evidence and document-role filters; ranking never supplies authorization | Foreign chunk, unselected revision and later-added company-evidence cases |
| Application to hosted inference: private context disclosure | One Inference Gateway, independently checked route policy, minimized payload, server-controlled destination and no silent fallback | Capture every embedding/generation/repair/retry call; blocked fixtures must emit no forbidden payload |
| Local stage output to hosted stage | Propagate the highest applicable restriction to derived findings, summaries and citations | A local private match cannot enter a hosted report prompt merely because raw identifiers were removed |
| Report/citation to browser | Authorize each report, document and source resolver; restricted file store, no public object paths | Guessed run/file/chunk IDs, old membership and cross-organization citation requests |
| Operational data and backups | No raw prompts, secrets or restoration maps in ordinary logs; restricted backups and retention policy | Error-path inspection, permitted audit access and database/file restore checks |

The current SQL classification is only `public` or `private`. Finer personal,
commercial and operational categories belong to the planned policy model; they
must not be described as existing enum values. Private input and derived private
output remain restricted unless an explicit approved transformation permits
transfer. Local processing still requires access controls, safe logging and
resource isolation.

## Deployment boundary

<!-- diagram:deployment -->

```mermaid
flowchart LR
    browser["Browser"]
    subgraph host["Operator-controlled deployment — target, not deployed"]
      caddy["Caddy<br/>only public HTTPS endpoint"]
      web["Next.js<br/>no model credentials"]
      subgraph private["Private application network / volumes"]
        api["FastAPI<br/>restricted runtime identity"]
        worker["Worker<br/>no direct Internet model access"]
        db[("PostgreSQL<br/>non-owner runtime roles + RLS planned")]
        files[("Private file volume<br/>not a static web directory")]
        local["Local embedding runtime<br/>optional local generation"]
      end
      gateway["Inference Gateway<br/>private authenticated endpoint<br/>sole model egress identity"]
      egress["Destination allowlist / egress controls<br/>redirect and retry policy"]
      backup[("Restricted backups<br/>compatible database + file snapshot")]
    end
    provider["Approved hosted provider<br/>external trust boundary"]
    browser -->|HTTPS| caddy
    caddy --> web
    caddy -->|API routes| api
    api --> db & files
    worker --> db & files
    api & worker -->|Scoped internal model requests| gateway
    gateway -->|Permitted local route| local
    gateway -->|Scoped policy and membership reads| db
    gateway --> egress
    egress -->|Only authorized minimized context| provider
    db & files -.-> backup
```

Caddy is the intended public entry point. PostgreSQL, workers, file storage,
model runtimes and the internal gateway endpoint are private. The gateway has the
approved model-egress identity; API and worker processes must not have a direct
provider route or provider credentials. Internal network attachment alone is not
proof of enforcement: destination allowlists, redirect handling, credentials and
host/container egress rules require explicit deployment checks under Ramazan's
tasks. Provision model artifacts through a controlled setup process rather than
enabling arbitrary worker downloads.

The existing Compose file provisions only PostgreSQL for local development.
This is a deployment target, not a runnable production topology. Hardware, model
memory, concurrency, backups and cost must be measured or confirmed before a
hosting commitment. Application rollback must remain compatible with forward
database migrations and the selected file snapshots.

## Integration decisions and review

| Decision / handoff | Owner and task | What must be confirmed |
| --- | --- | --- |
| Extraction, embedding and citation contract | Daniyar, retrieval/extraction tasks and TG-D01 | Model identity, dimensions, parser/locator rules, RU/KK development results and schema-compatible outputs |
| API, sealing and jobs | Rassul, TG-R07/TG-R08/TG-R09 | Supported authentication context, migration plan, worker fencing and atomic publication |
| Privacy and runtime boundary | Ramazan, TG-T03/TG-T06/TG-T07/TG-T09 | Data routes, role checks, retention, RLS and gateway/egress enforcement |
| UX representation | Ramazan with all members, TG-T04/TG-T08 | Fields and states in the report, both sides of citations and explicit blocked/unknown outcomes |
| Predefence integration | Rassul, TG-R05; Ramazan coordinates review | Consistency with completed requirements, technology choices and actual supervisor feedback |

The contracts are ready for team review; no agreement or supervisor approval is
invented. Changes from member reviews must update the relevant source, export,
contract and traceability row together. Architecture preparation can proceed
before all M0 outputs are finished; their final alignment is an integration step.

## Rebuilding diagrams

Run from the repository root with Python and Node.js/npm available:

```console
python docs/architecture/tools/render.py
```

The renderer invokes Mermaid CLI pinned to `12.0.0` and may download its tooling
and browser on first use. To use an existing CLI and Chrome installation:

```powershell
python docs/architecture/tools/render.py --mmdc "C:/path/to/mmdc.cmd" --browser "C:/Program Files/Google/Chrome/Application/chrome.exe"
```

The renderer reads the six named Mermaid blocks in this document and rebuilds
the SVGs in `export/`. Export tooling and styling are isolated in `tools/`;
there is no second copy of the diagram sources to maintain. Edit the Mermaid
blocks and rerender when an export is needed. Keep the ER block aligned with
the database document when the authoritative schema changes.

Initial tooling installation may need network access, independently of the
product's runtime network policy. GitHub preview requires no local renderer.
