# TenderGuard requirements

This specification defines the proposed functional scope for predefence component 6.
It develops the [project proposal](../project-proposal/proposal.md) into individually
verifiable requirements and maps them to the [architecture](../architecture/architecture.md)
and [integration contracts](../architecture/contracts.md). Rassul Akhmetov owns the
functional contribution under TG-R01; Ramazan Talgatov supplies the privacy and
non-functional contribution under TG-T03. Daniyar Kairatov reviews ML feasibility
and the evaluation conditions. Team and supervisor approval remain pending.

The functional specification is prepared for review. The complete component still
requires Ramazan's contribution and reconciliation with user findings. Only the
[database foundation](../database/database.md) is implemented; the acceptance
checks below are planned verification, not reported test results.

## Scope and priorities

The core product is an organization-scoped web application for comparing a tender
package with an SME's selected company evidence. The initial pilot category is
provisionally IT and office equipment, subject to user and corpus confirmation.
Core inputs are text-based Russian and Kazakh PDF/DOCX files. Documents are
uploaded manually; procurement portal integrations are outside the core scope.

| Priority | Meaning |
| --- | --- |
| Must | Required for the core diploma platform and its evaluation. This does not mean implementation must be finished for the first predefence. |
| Should | An extension considered after the core workflow works; omission must be recorded. |
| Could | Optional research or product work, conditional on resources and demonstrated need. |

## Actors

| Actor | Product actions |
| --- | --- |
| Member / analyst | Maintain company evidence and tenders, upload documents, start analysis, ask questions, review findings and read permitted reports. |
| Viewer / manager | Read permitted reports and cited sources; cannot create or change analysis inputs, questions or reviews. |
| Organization owner | Analyst actions plus membership, processing-policy and permitted audit administration. |
| Research evaluator | Execute the controlled offline evaluation harness on permitted fixtures; this is not an unrestricted production account. |

Role enforcement and organization isolation require the detailed security
requirements from TG-T03. The functional permissions above follow the architecture
and must remain consistent with that contribution.

## Core functional requirements

### FR-01 — Sign in and select an organization

**Priority:** Must. **Actor:** all product users.

The system shall authenticate users, display their active organizations and apply
the selected organization's role to subsequent actions.

**Acceptance:** a fixture user with memberships in two organizations can select
either and sees the corresponding workspace. A viewer can read a permitted report
but cannot upload or create a run. An unauthenticated user cannot open a protected
workspace. No membership is inferred from a user-supplied organization identifier.

### FR-02 — Maintain a tender workspace

**Priority:** Must. **Actor:** member or owner.

The system shall create and list tender workspaces with a title and stable
identifier, attach selected document versions, and show their processing state.

**Acceptance:** creating a tender with a valid title returns its identifier and
makes it visible in the active organization's list. A blank title is rejected.
Attaching two permitted document versions displays both exact versions; an
unavailable or foreign-organization version cannot be attached.

### FR-03 — Maintain company profiles and evidence versions

**Priority:** Must. **Actor:** member or owner.

The system shall create company profiles and immutable profile versions containing
applicable identity, goods/services, qualifications, delivery and warranty facts.
Material claims shall link to supporting document versions and locators when
available. The user shall be able to select the evidence relevant to a run.

**Acceptance:** a synthetic profile records a product, a delivery commitment and
its source. Saving a revised commitment creates a new profile version. Selecting
the old version still returns its original facts and evidence. A missing fact can
remain unspecified; it must not be silently filled with a model-generated claim.

### FR-04 — Upload and process document versions

**Priority:** Must. **Actor:** member or owner.

The system shall validate uploaded file bytes and configured size limits, retain
immutable PDF/DOCX versions, and expose ingestion status. Parsing shall preserve
source locations. A requested data classification shall be checked server-side
against the effective policy defined by TG-T03.

**Acceptance:** one text PDF and one DOCX fixture each produce a version identifier,
an ingestion reference and retrievable text after successful processing. A revised
upload creates a distinct version. A corrupt, oversized or unsupported file has an
explicit rejected/failed outcome. An image-only scan without supported OCR has an
explicit unsupported outcome and cannot appear as a successfully parsed empty file.

### FR-05 — Resolve evidence to the original source

**Priority:** Must. **Actor:** any user permitted to read the underlying document.

The system shall resolve a citation to an exact document version, supporting quote
and stable PDF page or DOCX paragraph/table-cell location, following the locator
conventions in the integration contracts.

**Acceptance:** prepared PDF-page, DOCX-paragraph and DOCX-table-cell references
open the matching passage in the correct version. An out-of-bounds locator or
unknown chunk is rejected. A revised file does not change an old citation's target.
Resolving a citation rechecks permission to its source.

### FR-06 — Start analysis with a fixed input selection

**Priority:** Must. **Actor:** member or owner.

The system shall accept a tender, an exact company-profile version, selected tender
versions, selected company evidence and an allowed analysis configuration. It shall
seal that selection, enqueue processing and return run/job identifiers.

**Acceptance:** a valid selection of successfully ingested inputs creates one run
with a readable manifest. An unprocessed input or evidence from another profile is
rejected before analysis starts. Later-added evidence cannot enter an existing run.
A repeated creation request with the same scoped idempotency key and payload returns
the same run; the same key with a changed payload is rejected as a conflict.

### FR-07 — Extract structured tender requirements

**Priority:** Must. **Actor:** analysis pipeline on an analyst's request.

The system shall extract atomic requirements with a label, text, type, language,
applicable conditions, values and units where present, and at least one supporting
tender citation. It shall preserve distinctions such as calendar/business days and
product-specific conditions.

**Acceptance:** controlled fixtures cover delivery, product specifications and
certificate conditions. Valid stage outputs retain the annotated values, units and
resolvable tender references. Outputs containing missing mandatory fields or an
unselected/unresolvable citation cannot be published as validated requirements.
Empirical extraction quality is measured separately under TG-D01/TG-D03; passing
schema checks alone does not establish extraction accuracy.

### FR-08 — Match requirements against company evidence

**Priority:** Must. **Actor:** analysis pipeline on an analyst's request.

For each validated requirement, the system shall return `met`, `unmet` or `unknown`,
an explanation and tender citations. Both `met` and `unmet` shall also have applicable
company evidence and company citations. Missing, contradictory or ambiguous evidence
shall remain `unknown` unless an explicit supported rule resolves it.

**Acceptance:** against a requirement for delivery within 10 calendar days for the
same goods, an applicable commitment within 7 calendar days produces `met`, a
documented minimum of 14 calendar days produces `unmet`, and an absent commitment
produces `unknown`. A business-day commitment without a supported conversion remains
`unknown`. A candidate met/unmet finding without selected company evidence fails
validation. These are synthetic acceptance fixtures, not measured platform results.

### FR-09 — Present an inspectable report and bounded risks

**Priority:** Must. **Actor:** any authorized report reader.

The system shall display the input manifest, requirement/evidence matrix, status
counts, explanations, unknowns, risk flags and preparation actions. Readers shall
be able to filter findings by status and inspect both sides of the evidence.
Risk flags shall identify their supporting findings and rule/configuration reference.

**Acceptance:** a fixture report containing one finding per status shows counts of
one met, one unmet and one unknown; filtering returns the corresponding finding.
Each met/unmet row opens tender and company sources. A missing-certificate action
links to its requirement and evidence gap. With no approved applicable legal source
and rule, the legal field is `legal_unknown`. Documentary fit is not presented as
legal approval or an award probability. Aggregate counts are computed from stored
findings rather than generated independently by a model.

### FR-10 — Ask evidence-grounded questions

**Priority:** Must. **Actor:** member or owner.

The system shall answer questions using the permitted selected evidence of a run,
returning resolvable citations or `insufficient_evidence`. Question answering shall
not change the run's findings or expand its input selection.

**Acceptance:** a question about a fixture's explicit delivery condition returns
the supported value and citation. An answer absent from the fixture returns
`insufficient_evidence`. Retrieval cannot introduce a later revision or unselected
company document. A policy block or provider failure is displayed as a processing
outcome rather than an unsupported answer or an evidence-insufficiency claim.

### FR-11 — Record human reviews without overwriting findings

**Priority:** Must. **Actor:** member or owner.

The system shall append review events for a finding, including reviewer identity,
action and comment, and distinguish the human assessment from the machine output.

**Acceptance:** accepting, disputing and commenting on a fixture finding produce
separate attributable events. The report shows those events while preserving the
original status, explanation and citations. A viewer cannot create a review.
Changes to input facts or a corrected machine analysis require a new run.

### FR-12 — Reanalyse revisions while preserving history

**Priority:** Must. **Actor:** member or owner.

The system shall allow a new analysis using revised tender/company evidence or a
changed allowed configuration, while retaining access to previous permitted runs
and their exact inputs.

**Acceptance:** replacing the fixture's 14-day commitment with a documented 7-day
commitment creates a new profile version and run. The old run still resolves to
the 14-day source; the new run resolves to the 7-day source. Neither review nor
reanalysis mutates the old report. A run records its parser, retrieval, prompt/schema,
model, pipeline and policy configuration references as defined in the contracts.

### FR-13 — Show processing outcomes and support safe recovery

**Priority:** Must. **Actor:** analyst monitoring a job.

The system shall expose queued, running, completed, failed, blocked and cancelled
execution outcomes as applicable, with a stage when known and a safe reason/action.
It shall support cancellation of active work and bounded retries of recoverable
failures without publishing duplicate or partial completed reports.

**Acceptance:** injected parser failure, provider failure, policy block and
cancellation each produce the corresponding visible outcome. A policy block sends
no prohibited request and cannot silently fall back to another route. Cancellation
prevents subsequent result publication; it need not undo a provider call already
dispatched. In a worker-interruption fixture, recovery publishes at most one complete
result, and the stale worker cannot publish. Unknown compliance is distinct from
failed processing. The current job enum has no `blocked` value: the proposed mapping
uses a failed job with `POLICY_BLOCKED` and a separate blocked execution state.

### FR-14 — Administer membership, processing policy and audit views

**Priority:** Must. **Actor:** organization owner.

The system shall let an owner manage member roles and active access, select among
approved processing-policy options, and inspect permitted audit events. A normal
member shall not administer these settings.

**Acceptance:** an owner changes a test user's member role to viewer; the next
write request is denied. Revoking membership denies subsequent protected reads.
A member's administrative request is denied. A policy change affects subsequent
dispatch checks without rewriting a run's recorded policy. An owner can inspect
the actor, action and outcome of the change without receiving confidential prompts
or credentials. Exact policy options and audit retention are defined by TG-T03.

### FR-15 — Process Russian and Kazakh evidence

**Priority:** Must. **Actor:** analyst.

The core upload, extraction, matching, source inspection and QA workflow shall
accept text-based Russian and Kazakh inputs while preserving source language and
text. Interface localization and automatic translation are not prerequisites.

**Acceptance:** language-labelled fixtures in both languages can traverse the
workflow without a language-based format rejection or corrupted citations. The
unit/condition cases in FR-07/FR-08 are included in both sets. Extraction, retrieval
and matching quality are reported separately by language under TG-D01/TG-D03;
no equality of quality or unmeasured numeric threshold is claimed here.

### FR-16 — Execute reproducible baseline comparisons

**Priority:** Must. **Actor:** research evaluator, using the offline harness.

The system shall support B1 single-prompt RAG and B2 staged analysis using the same
permitted frozen evidence and comparable recorded model configurations. It shall
retain outputs, failures and measurements required by the evaluation protocol.

**Acceptance:** one controlled fixture executes both paths with recorded input
hashes, configuration references, outputs, elapsed time and model usage when
available. A failed/blocked attempt remains in the experiment record. Retrieval
changes are recorded as separate variants; development and test inputs remain
distinguishable. Model, hardware or budget differences are reported as experimental
conditions. This requirement does not require B2 to outperform B1.

## Optional functional extensions

| ID | Priority | Capability | Acceptance if selected |
| --- | --- | --- | --- |
| EXT-01 | Should | Download a report | An authorized export contains the same run manifest, counts, findings and source references as the on-screen report. |
| EXT-02 | Could | Process scans with OCR | A labelled scan fixture produces source-resolvable text; OCR failures are visible and quality is evaluated separately. |
| EXT-03 | Could | Compare tender revisions | A fixture with an altered delivery clause identifies the changed clause and links to both exact revisions. |
| EXT-04 | Could | Add local generation or model adaptation | A resource-feasible local runtime follows the same contracts and route controls; any adapted model has documented permitted training data, a held-out comparison and retained base-model results. |

Local embeddings are part of the proposed retrieval baseline. Local generative
inference, a local/hosted combination and fine-tuning remain conditional extensions;
using a hosted open-weight model is still external processing. Optional work cannot
relax the core data policy. Automatic bid submission, payments, signatures,
market-wide crawling and unrestricted legal advice are outside scope.

## Traceability to architecture and implementation responsibility

The architecture's existing `AR-*` references are retained so its diagrams need no
duplicate requirement numbering. This table maps every core functional requirement
to a use case and responsible component. Leads refer to implementation ownership,
not to a claim that the corresponding task or feature is complete.

| Requirement | Architecture reference | Use case | Responsible component | Lead / integration |
| --- | --- | --- | --- | --- |
| FR-01 | AR-01, AR-09 | UC-01 | Identity and authorization; shared interface | Ramazan |
| FR-02 | AR-03 | UC-03 | Document and company service | Rassul |
| FR-03 | AR-02, AR-08 | UC-02, UC-07 | Document and company service | Rassul |
| FR-04 | AR-03, AR-10, AR-11 | UC-03 | Document service; ingestion; Job runner | Rassul with Daniyar |
| FR-05 | AR-06, AR-09 | UC-05 | Source resolver; ingestion; interface | Rassul with Daniyar and Ramazan |
| FR-06 | AR-02, AR-08, AR-10 | UC-04 | Run service; Job runner | Rassul |
| FR-07 | AR-04, AR-11 | UC-04 | Requirement extraction; Authorized retrieval | Daniyar with Rassul |
| FR-08 | AR-05 | UC-04 | Documentary matching; Authorized retrieval | Rassul with Daniyar |
| FR-09 | AR-06, AR-12 | UC-05 | Risk and report; Run service; interface | Rassul with Ramazan |
| FR-10 | AR-07, AR-09, AR-11 | UC-06 | Question-answer service; retrieval; Inference Gateway | Daniyar with Rassul and Ramazan |
| FR-11 | AR-08 | UC-07 | Run / report / review service; interface | Rassul with Ramazan |
| FR-12 | AR-08 | UC-07 | Document and company service; Run service | Rassul |
| FR-13 | AR-09, AR-10 | UC-04 | Job runner; Run service; Inference Gateway; interface | Rassul with Ramazan |
| FR-14 | AR-01, AR-09 | UC-08 | Identity and authorization; policy; safe audit | Ramazan |
| FR-15 | AR-11 | UC-03, UC-04, UC-06 | Ingestion; extraction; retrieval; QA | Daniyar with Rassul |
| FR-16 | AR-13 | UC-09 | Offline evaluation harness | Daniyar; all members contribute subsystem checks |

The full specification is jointly owned: documenting authentication, routing and
administration here defines their observable product behaviour without transferring
Ramazan's security implementation tasks to Rassul.

## Verification and review

For each core requirement, retain its ID, fixture/input references, configuration,
expected result, observed result and reviewer evidence when implementation is tested.
Use public or synthetic documents for initial checks. Include positive, invalid-input
and unauthorized cases where relevant. The acceptance examples establish deterministic
behaviour on controlled fixtures; broader model quality and user usefulness require
the separate evaluation protocol and actual user findings.

Remaining work before component 6 can be considered complete:

| Contribution | Required result | Owner / related task |
| --- | --- | --- |
| Privacy and non-functional requirements | Unique SEC/NFR identifiers, priorities, acceptance criteria and verification methods for classification, organization isolation, route policy, retention/deletion, audit/secrets, reliability and justified performance/resource targets | Ramazan, TG-T03 |
| User validation | Connect requirements to actual anonymized findings; revise the pilot category and priorities where justified | Ramazan, TG-T01; Rassul integrates |
| ML feasibility and evaluation alignment | Confirm language fixtures, annotation rules, dataset conditions and measurable quality targets without inventing results | Daniyar, TG-D01/TG-D03/TG-D04 |
| Joint review | Resolve overlaps between functional and SEC/NFR requirements, confirm Must scope, and record actual team/supervisor feedback | All members; TG-R05 integrates |

Detailed SEC/NFR requirements are pending; they are not replaced by these functional
checks. Retention/deletion rules must explicitly resolve their effect on historical
reports and citations. File limits, call budgets, concurrency, recovery targets and
latency thresholds must be agreed with a stated workload and deployment environment
rather than supplied as unsupported performance claims.
