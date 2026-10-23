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

## Security, privacy and non-functional requirements
This section is the TG-T03 contribution (owner: Ramazan Talgatov; reviewer: Daniyar Kairatov). It specifies planned controls; implementation belongs to later milestones. It claims no implemented isolation and no zero-leakage result. Detailed design, threat register, acceptance cases and trust-boundary description are given in Appendix A and are maintained under docs/privacy/. Values marked proposed are unmeasured placeholders to agree with a stated workload and environment (decision D4).

## Policy definitions

**Data classes.** C0 public tender text; C1 personal data; C2 commercially sensitive company evidence (company profile, evidence documents, non-public tender annexes); C3 operational data (logs, audit records, prompts, credentials, mappings). Chunks, embeddings, extracted requirements, findings, reports, caches and evaluation records inherit the highest class of any source they derive from and are never downgraded automatically. A document whose class is unknown is treated as C2.

**Route outcomes.** HOSTED (allowed), TRANSFORM+HOSTED (allowed only after the stated transformation), LOCAL (must stay on a local route), BLOCKED (no outbound call; visible failed outcome with reason code POLICY_BLOCKED).

## Processing-policy options an owner can select (FR-14).

| Option | C0 | C1 | C2	| When no permitted route exists |
| LOCAL_ONLY	| LOCAL	| LOCAL	| LOCAL	| BLOCKED |
| HOSTED_PUBLIC_ONLY	| HOSTED	| LOCAL	| LOCAL	| BLOCKED for C1 and C2 |
| HOSTED_APPROVED_ROUTE	| HOSTED	| TRANSFORM+HOSTED on an approved route	| HOSTED only on an explicitly approved provider route	| BLOCKED |


The option HOSTED_APPROVED_ROUTE requires an explicit owner action and a matching entry in the provider route registry (SEC-16). A new organization starts with LOCAL_ONLY. Because matching needs company evidence (C2), a deployment without a local route can run the pilot only on synthetic or authorized public fixtures under an explicit option (decision D2). Masking alone does not establish confidentiality: pseudonymization reduces exposure of C1 but does not make C2 content safe to send. If no permitted local route exists, restricted analysis is blocked and never falls back silently to a hosted model. Local inference is optional; enforcement of the selected policy is a core requirement.

## Security and privacy requirements (SEC)

Owner is the lead for specification and verification; implementation owners follow the traceability table.
| ID	| Pri	| Requirement	Acceptance (planned verification)	| Verification method	| Owner |
| SEC-01	| Must	| The server derives the active organization and role from the authenticated session and membership records. | A client-supplied organization identifier is only a claim to verify	| A user with no membership in the supplied organization is denied; a user with two memberships sees only the selected organization's data; no membership is inferred from the identifier	| Automated negative tests; code review of org-context handling	| Ramazan |
| SEC-02 | Must | Organization isolation holds for API objects, database rows, files, retrieval indexes, caches and jobs. A foreign object and a nonexistent object produce the same denied response	| Organization A requesting a document, version, run, report, chunk or cache entry of organization B is denied and no row, file or entry of B is read	| Test suite across each store; database and storage access logs	| Ramazan with Rassul |
| SEC-03	| Must	| Roles follow the actor table: viewers read permitted reports and cited sources only; members manage evidence, tenders, runs, questions and reviews; owners add membership, policy and audit administration	| Viewer upload, run creation, question, review and delete are denied with no state change; member administrative requests are denied; role change and revocation apply from the next request	| Role-by-action test matrix	| Ramazan |
| SEC-04	| Must	| Every uploaded document receives a data class server-side: uploader declaration, personal-data detection (promotes to C1), unknown treated as C2. Derived data inherits the highest source class	| A fixture with an unmarked company contract is stored as C2; a fixture with planted personal data is promoted to C1; derived chunks, embeddings and reports carry the source class. Detector recall is measured and reported, not assumed	| Fixtures with known classes; detector evaluation with Daniyar	| Ramazan with Daniyar |
| SEC-05	| Must	| Every model, embedding, repair, retry and evaluation call is made through the Privacy Gateway, which checks class, organization policy and provider route before any network call	| A mock provider receives no request that lacks a recorded gateway decision; a direct provider call path does not exist in the code	| Code review; integration test with a mock provider	| Ramazan |
| SEC-06	| Must	| Routing follows the policy matrix for the organization's selected processing-policy option	| For each class and option, the observed route equals the matrix; a policy change affects subsequent dispatch checks and does not rewrite a stored run's recorded policy	| Route matrix test; run manifest inspection	| Ramazan |
| SEC-07	| Must	| If no permitted route exists for restricted data, analysis is blocked before any outbound request, with a visible reason; there is no silent fallback to another provider or route	| With the policy forbidding hosted processing and no local route, a restricted run ends failed with POLICY_BLOCKED and the mock provider receives 0 requests	| Fault and policy tests; gateway decision records	| Ramazan |
| SEC-08	| Must	| Retries, repairs and evaluation calls are re-evaluated under the same policy and never use a more permissive route than the original call	| A forced timeout, schema repair or judge call on C2 content never reaches a route the policy forbids; retries are bounded	| Fault injection; gateway log	| Ramazan with Daniyar |
| SEC-09	| Must	| Document content is untrusted input. Instructions inside a tender or evidence document are not followed; model outputs are validated against schema and permitted sources before use	| A fixture containing text that tells the model to ignore rules, reveal other data or call another route produces no foreign data, no extra outbound call and no changed policy; outputs citing unselected sources fail validation	| Hostile-document fixtures; canary check; output trace	| Ramazan with Daniyar |
| SEC-10	| Must	| Outbound payloads are checked against forbidden content: secrets, operational data and identifiers of other organizations	| A prompt containing a planted canary or secret pattern is blocked before the call	| Canary tests against the gateway	| Ramazan |
| SEC-11	| Must	| Files and results are never publicly addressable. Access is authorized per request, and citation resolution rechecks permission to the underlying source (FR-05)	| Direct or expired file URLs and cross-organization citation requests are denied	| Access tests; storage access log	| Ramazan with Rassul |
| SEC-12	| Must	| Logs, traces and error reports contain no document text, prompts, model outputs, extracted personal data, file contents or credentials. They may contain request, organization and user IDs, object IDs, class, route, model identifier, policy decision, token counts, latency, status and content hashes	| After a test run with canary strings in documents and prompts, no canary appears in any log, trace or error report	| Canary scan of all log sinks	| Ramazan |
| SEC-13	| Must	| Secrets are kept in a secret store or environment injection and never in the repository, images, prompts or logs. A rotation procedure is documented	| Secret scanning in CI reports no findings; log scan finds no credential	| CI scan; log scan; document review	| Ramazan |
| SEC-14	| Must	| Policy decisions, role and membership changes, policy changes, deletions and exports are recorded in an audit log readable by owners only, without confidential prompts or credentials. Audit retention period is set under decision D4	| Each tested action produces one audit event with actor, action, object and outcome; a member cannot read the audit log	| Test actions; audit inspection	| Ramazan |
| SEC-15	| Must	| Retention and deletion: deleting a document version removes its file, chunks, embeddings, cached answers and extracted requirements; historical reports and citations follow the rule in decision D1	| After deletion, the file, chunks and embeddings are not retrievable and citations behave as D1 specifies; removal from primary stores within the agreed time (proposed 24 hours)	| Delete then query each store; citation resolution test	| Rassul with Ramazan |
| SEC-16	| Must	| A provider route registry records provider, model, region, retention mode and allowed data classes. Only registered and approved routes can be used, and the route and model identifier are recorded per call	| An unregistered route or a class not allowed for a route is blocked; the run manifest records route and model	| Registry tests; manifest inspection	| Ramazan |
| SEC-17	| Must	| TLS protects all external traffic. Storage encryption is applied as far as the chosen deployment supports and any gap is recorded as a limitation	| Configuration checklist passed	| Configuration review	| Ramazan |
| SEC-18	| Must	| Uploaded file bytes are validated against the declared type (FR-04) and stored outside any web-served path	| Mismatched, malformed or encrypted files are rejected with an explicit outcome and are never served directly	| Upload tests	| Rassul with Ramazan |
| SEC-19	| Must	| The research evaluator account and offline harness run only on permitted fixtures and follow SEC-05 to SEC-08 like production calls	| A harness run on a fixture containing restricted content under a forbidding policy ends blocked and is recorded in the experiment record	| Harness test	| Daniyar with Ramazan |

## Non-functional requirements (NFR)

File limits, call budgets, concurrency, recovery targets and latency thresholds are to be agreed with a stated workload and deployment environment; they are not performance claims.
| ID	| Pri	| Requirement	Acceptance (planned verification)	| Verification method	| Owner |
| NFR-01	| Must	| Jobs survive a worker interruption or repeated submission without lost or duplicate complete reports (supports FR-06 and FR-13)	| Killing a worker mid-job results in at most one complete result, and the stale worker cannot publish; a repeated request with the same scoped idempotency key returns the same run	| Fault injection in the shared environment	| Rassul, reviewed by Ramazan |
| NFR-02	| Should	| Database and file backups can be restored, and the restoration is checked	| A restore drill passes an integrity check; recovery time is recorded (target to agree)	| Restore drill	| Ramazan |
| NFR-03	| Must	| Provider, parser and policy failures are shown as visible outcomes, never as an empty or successful report	| Injected parser failure, provider failure, policy block and cancellation each produce the visible outcome in FR-13	| Fault injection	| Rassul |
| NFR-04	| Must	| Upload limits: text-based PDF and DOCX only; other types, encrypted files and oversize files are rejected with a clear message	| Limits (proposed 20 MB and 200 pages) are confirmed after parser measurement on the authorized corpus; rejected inputs produce the message	| Upload tests; parser measurement	| Rassul with Daniyar |
| NFR-05	| Should	| Ordinary API calls (not analysis) respond within a stated time under a defined load	| Proposed p95 of 500 ms under a recorded workload and environment	| Load test with a fixed script and data set	| Rassul |
| NFR-06	| Must	| The time and resources for a standard package analysis are measured and reported with their conditions (measurement is Must; a numeric target is Should)	| Latency, calls and token usage are recorded per run; a target is set after the first end-to-end baseline and is reported together with the B1 and B2 comparison	| Timed runs under fixed model and settings	| Daniyar with Rassul |
| NFR-07	| Should	| A stated number of concurrent jobs per organization is handled without cross-organization effects	| Number and threshold to agree; no result mixing observed	| Concurrency test	| Rassul |
| NFR-08	| Must	| Cost and resource accounting: every run records provider calls, retries, tokens and elapsed time so that B1 and B2 are compared under a declared resource ceiling (supports FR-16)	| Run records contain the fields; failed and blocked attempts remain in the record	| Record inspection	| Daniyar |
| NFR-09	| Must	| Users can see why a run is blocked, failed or unknown and what to do next, and can see which processing policy applies	| Participants in the TG-T04 prototype test can state the reason for each outcome in their own words; thresholds are agreed before the test and results report the sample size	| UX test; UI review	| Ramazan with Daniyar |

## Retention and deletion versus historical reports and citations

Deletion necessarily overrides the immutability stated in FR-05 and FR-12 for the deleted document, so the exception is stated explicitly. Decision D1 chooses among these options.
| Option	| What happens to reports that cited the deleted document	| Effect |
| A Cascade	| Runs and reports that cite it are deleted too	| Strongest privacy; history is lost | 
| B Tombstone (proposed)	| Runs remain. Citations to the document resolve to a deleted-source notice with no quote. Quotes, explanations and company text derived from it are redacted. Affected findings are marked evidence_deleted and keep their status label. Reanalysis is possible only with new evidence	| Keeps counts, structure and review history without keeping the content |
| C Block deletion	| A document cited by any run cannot be deleted	| Keeps history; conflicts with a user's right to remove data |

Proposed rule (option B): deletion overrides FR-12 and FR-05 immutability for the deleted version only; human review events remain but any content copied into comments can be removed by an owner; audit events keep metadata only.

## Coverage of model calls by the Privacy Gateway

Every call in this table passes through the gateway under SEC-05 to SEC-08, with its class and route recorded. Daniyar reviews this coverage.
| Call	| Used by	| Typical input class	| Route rule |
| Embedding of tender or company text	| Ingestion, retrieval (FR-04, FR-10)	| C0, C1, C2	| Same as generation; local embeddings are part of the proposed retrieval baseline |
| Requirement extraction	| FR-07	| C0 and C1	| Per policy matrix |
| Documentary matching	| FR-08	| C0, C1 and C2	| Per policy matrix; the most restrictive class in the input decides |
| Question answering	| FR-10	| C0, C1 and C2	| Per policy matrix; a policy block is shown as a processing outcome, not as insufficient evidence| 
| Repair or format-fix call	| FR-07, FR-08	| Same as the call it repairs	| Same or stricter route |
| Retry	| All stages	| Same as the original	| Same or stricter route, bounded count |
| B1 and B2 evaluation runs	| FR-16	| Permitted frozen fixtures	| Same policy as production |
| Model-based judging (optional)	| Evaluation diagnostics	| Fixtures	| Same policy; versioned model and prompts |


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

SEC and NFR traceability. Architecture references for these items are to be confirmed against the existing AR-* numbering; no new AR identifiers are introduced here.
| Requirement	| Related functional requirements	| Responsible component	| Lead / integration |
| SEC-01, SEC-02, SEC-03	| FR-01, FR-02, FR-14	| Identity and authorization; shared interface	| Ramazan with Rassul |
| SEC-04	| FR-04	| Document service; ingestion; policy	| Ramazan with Daniyar |
| SEC-05 to SEC-08, SEC-10, SEC-16	| FR-07, FR-08, FR-10, FR-13	| Inference Gateway; policy; Job runner	| Ramazan |
| SEC-09	| FR-07, FR-08, FR-10	| Requirement extraction; matching; QA	| Ramazan with Daniyar |
| SEC-11, SEC-18	| FR-04, FR-05	| Document service; source resolver	| Rassul with Ramazan |
| SEC-12, SEC-13, SEC-17	| All	Logging; secrets; deployment	| Ramazan |
| SEC-14	| FR-14	| Safe audit	| Ramazan |
| SEC-15	| FR-03, FR-05, FR-12	| Document and company service; run service	| Rassul with Ramazan |
| SEC-19	| FR-16	 | Offline evaluation harness	| Daniyar with Ramazan |
| NFR-01, NFR-03	| FR-06, FR-13	| Job runner; run service	| Rassul with Ramazan |
| NFR-02, NFR-05, NFR-07	| None	| Platform and deployment	| Ramazan with Rassul |
| NFR-04	| FR-04	| Document service; ingestion	| Rassul with Daniyar |
| NFR-06, NFR-08	| FR-16	| Evaluation harness; Job runner	| Daniyar |
| NFR-09	| FR-09, FR-13	| Shared interface	| Ramazan with Rassul |


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

## Open decisions for joint review

| ID	| Decision	| Notes |
| D1	| Deletion versus historical reports and citations	| Option B (tombstone) proposed |
| D2	| Default processing policy for the pilot, given that matching needs company evidence	| New organizations start at LOCAL_ONLY; the pilot would use synthetic or authorized public fixtures under an explicit option unless a local route exists |
| D3	Legal applicability of cross-border transfer and localization, and provider terms (retention, region, training use)	| Legal question for the supervisor and a lawyer; not resolved here |
| D4	| Numeric values: file limits, latency, concurrency, recovery time, backup period, audit retention, deletion time, usability thresholds	| Agree with Daniyar after the first end-to-end baseline and a stated workload |
| D5	| Role names in the interface: owner, member, viewer in this specification versus administrator, analyst, viewer in the TG-T03 task brief	| This document uses owner, member (analyst), viewer |

## Appendix A. Privacy design (TG-T03)

This appendix holds the supporting design behind SEC-01 to SEC-19 and NFR-01 to NFR-09: data classes, route matrix, trust boundaries, roles, retention and logging policy, threat register, acceptance cases and links to the TG-T02 sources. The SEC and NFR tables in the section Security, privacy and non-functional requirements are the reference for requirement wording; this appendix explains and tests them. The same design is kept under docs/privacy/. Nothing here claims implemented isolation or zero leakage; every item is a planned control or a test to run.

**A.1 Data classes and examples**
| Class	| Examples	| Default handling |
| C0 Public tender text	| Published tender notice and its public annexes	| Org-scoped storage; hosted model allowed |
| C1 Personal data	| Names, contacts, signatures, specialist CVs, ID details inside any document	| Restricted: hosted only after transformation and org policy approval, otherwise local or blocked |
| C2 Commercially sensitive company evidence	| Company profile, financial statements, contracts, prices, certificates, internal policies, non-public tender annexes	| Restricted: local only by default; hosted only under an explicit approved provider route |
| C3 Operational data | Logs, audit records, job metadata, prompts, route decisions, credentials, pseudonym mappings	| Never sent to a model; content-free logging; secrets in a secret store |

**How a class is assigned.** (1) The uploader declares the document type (tender document or company evidence) and whether it is public; (2) a server-side detector flags probable personal data and promotes the document to C1; (3) any document whose class is unknown is treated as C2 until an organization owner confirms otherwise. The detector is a safeguard with unmeasured recall: it supports classification but never proves that a document contains no personal or sensitive data (SEC-04).

**A.2 Data-class / route matrix**
| Class	| Storage	| Retrieval	| Hosted model	| Local model	| If no permitted route	| Logs may contain |
| C0	| Org-scoped DB rows and files	| Org-filtered index	| HOSTED	| Allowed	 | Not applicable	| IDs, hashes, route, token counts |
| C1	| Org-scoped, access-controlled	| Org-filtered index; no cross-org index	| TRANSFORM+HOSTED only if org policy enables hosted processing and legal basis is confirmed (decision D3); transformation is pseudonymization with per-org scoped mapping	| Allowed	| BLOCKED	| IDs, hashes, route, class; never the personal data |
| C2	| Org-scoped, access-controlled	| Org-filtered index	| LOCAL by default; hosted only on an explicitly approved provider route that satisfies retention and no-training terms (decision D3)	| Allowed	| BLOCKED; no silent fallback to hosted	| IDs, hashes, route, class |
| C3 | Restricted store; secrets outside the repo	| Not indexed	| Never	| Never	| Not applicable	| Not applicable |
The three owner-selectable processing-policy options (LOCAL_ONLY, HOSTED_PUBLIC_ONLY, HOSTED_APPROVED_ROUTE) are defined in the section Policy definitions. Masking alone does not establish confidentiality: pseudonymization reduces exposure of C1 but does not make C2 content safe to send, because company names, prices and clauses remain identifying and sensitive after masking.

**A.3 Processing steps covered by the same policy**
| Step	| Rule |
| Prompts	| Built server-side from authorized context only; checked by the Privacy Gateway before every outbound call |
| Embeddings	| An embedding call on C1 or C2 text is a model call and follows the same route rules |
| Repairs (format or schema fixes)	| Re-evaluated as a new call; the same route or a stricter one, never a more permissive one |
| Retries	| Bounded count; each retry re-checks policy; a retry never switches to a more permissive route |
| Evaluation calls (including model-based judging)	| Treated as production calls: same classes, same routes, same logging rules |
| Derived outputs	| Inherit the class of the inputs; displayed only to authorized members of the same organization |
| Provider timeout or error	| Job ends as failed or partial with a visible reason; no automatic fallback to another provider or route |
Local inference is an optional extension. Enforcement of the selected policy is a core requirement and does not depend on it. If an organization has restricted data and no permitted local route exists, restricted analysis is blocked.
<img width="432" height="214" alt="image" src="https://github.com/user-attachments/assets/0e6cc164-fb15-4a6d-8cad-16b95374e66c" />
gateway decision for every model call · 3 checks, 3 outcomes
The same decision applies to prompts, embeddings, repairs, retries and evaluation calls (SEC-05 to SEC-08). The route outcomes follow the data-class matrix in A.2.

**A.4 Trust boundaries**
The diagram below shows trust boundaries B1 to B8 and the table after it states the control and failure outcome at each boundary. The diagram is to be added to the architecture deliverable (component 7).
<img width="432" height="257" alt="image" src="https://github.com/user-attachments/assets/d16c90e9-cee2-4a92-9878-f28da285b966" />
trust boundaries B1 to B8 · one policy gate before model providers

The Privacy Gateway is the only route from the server to model providers (B6); organization context comes from the session on the server (B1), and every data store is scoped by organization (B3 to B5).
| Boundary	| Crossing	| Control	| Failure outcome |
| B1 Browser to API	| Credentials, uploads, requests with object IDs	| Authentication; TLS; organization context taken from the session on the server, never from client input; IDs checked against membership	| Denied |
| B2 API to workers (queue)	| Job requests	| Job carries org ID and class set by the server; idempotency key; worker re-checks authorization	| Job rejected or failed visibly |
| B3 API and workers to PostgreSQL	| Rows, results	| Every query scoped by organization; database-level isolation as a second layer (agree design with Rassul, TG-R04)	| Query returns nothing; denied |
| B4 Application to file storage	| Uploaded files, exports	| Org-prefixed paths; short-lived access checked per request; no public URLs	| Denied |
| B5 Workers to retrieval index and caches	| Chunks, embeddings, cached answers	| Per-organization index or enforced per-organization filter; cache keys include org ID and data version	| Empty result; denied |
| B6 Privacy Gateway to providers	| Prompts and embedding inputs	| Policy decision on class, org policy and provider route before the network call; payload check against forbidden content	| Blocked before any request |
| B7 Application to logs and monitoring	| Events	| Content-free logging; scrubbing of known canary and secret patterns	| Event dropped or reduced to metadata |
| B8 Developers and CI to environments	| Secrets, deployments	| Secret store; no secrets in the repository or images; secret scanning in CI	| Build fails |

**A.5 Roles and access**
| Action	| Owner	| Member (analyst)	| Viewer | 
| Manage members and roles	| Yes	| No	| No |
| Set organization privacy policy (processing-policy option, provider route)	| Yes	| No	| No |
| Upload tender or company documents	| Yes	| Yes	| No |
| Delete documents and derived data	| Yes	| Own uploads only	| No |
| Run an analysis	| Yes	| Yes	 | No |
| Review and edit findings (human review)	| Yes	| Yes	| No |
| View reports and source citations	| Yes	| Yes	| Yes |
| Export reports	| Yes	| Yes	| Yes (if the policy permits) |
| View audit log	| Yes	| No	| No |
**Source of organization context.** The server derives the organization from the authenticated session and the membership table. Any organization identifier supplied by the client is only a claim to verify. A request for an object in a foreign organization and a request for a nonexistent object produce the same denied response, so object existence is not disclosed (SEC-01, SEC-02).

**A.6 Retention, deletion and logging policy**
| Topic	| Requirement |
| Retention of uploads	| Kept until deleted by an authorized user or the organization is deleted; no use for training or any purpose other than that organization's analysis |
| Deletion cascade	| Deleting a source document removes its files, chunks, embeddings, extracted requirements and cached answers. Reports and citations that depended on it follow decision D1; proposed rule: reports remain, citations resolve to a deleted-source notice with no quote, derived quotes and company text are redacted, and affected findings are marked evidence_deleted (SEC-15) |
| Deletion time (proposed)	| Removed from primary stores and indexes within 24 hours of the request; removal from backups at the end of the backup cycle (backup period to agree, decision D4) |
| Provider retention	| Whatever the provider stores is governed by its terms; the route registry records retention mode per provider and model (SEC-16); unresolved terms are decision D3 |
| Logged	| Request ID, timestamps, organization ID, user ID, action, object IDs, data class, route and model identifier, policy decision, token counts, latency, status, content hashes |
| Never logged	| Document text, prompts, model outputs, extracted personal data, file contents, tokens, passwords and API keys (SEC-12) |
| Secrets	| Kept in a secret store or environment injection; never in the repository, images, prompts or logs; rotation procedure documented (SEC-13) |
| Audit	| Policy decisions, role changes, deletions, exports and owner actions recorded and retained for a period to agree; reading the audit log requires the owner role (SEC-14) |


**A.7 Threat register**
Status of every row is planned: controls are specified, none is claimed as implemented.
| ID	| Threat	| Asset	| Boundary	| Planned control	| Requirement and test | 
| TH-01	| Access to another organization's data via guessed or foreign identifiers	 | All org data	| B1, B3	| Server-side org context; membership check on every object	| SEC-01, SEC-02; AC-01 |
| TH-02	| Authenticated user without membership acts on an organization	| All org data	| B1	| Membership required for every org-scoped route	| SEC-01; AC-02 |
| TH-03	| Viewer modifies or deletes data	| Documents, findings	| B1	| Role check on every write	| SEC-03; AC-03 |
| TH-04	| Direct access to files or results by URL	| Files, reports	| B4	| No public URLs; authorization per request	| SEC-11; AC-04, AC-05 |
| TH-05	| Cross-tenant leakage through a shared index or cache	| Chunks, embeddings	| B5	| Per-organization index or enforced filter; org ID in cache keys	| SEC-02; AC-01, AC-05 |
| TH-06	| Hostile instructions inside a tender document (prompt injection)	| Policy, other org data	| B6	| Document text treated as data; stages have no tools with side effects; outputs checked	| SEC-09; AC-06 |
| TH-07	| Extraction of retrieval content through crafted queries	| Company documents	| B1, B5	
 Org-level filtering; output checks; leakage tests with canaries	| SEC-02, SEC-09; AC-06 |
| TH-08	| Restricted content sent to a provider through misclassification, repair or retry	| C1 and C2 data	| B6	| Gateway check on every call; unknown class treated as C2; retries never more permissive	| SEC-04, SEC-05, SEC-08; AC-08 |
| TH-09	| Silent fallback to a hosted model after local failure or timeout	| C1 and C2 data	| B6	| No automatic fallback; visible failed or blocked state	| SEC-07; AC-07, AC-09 |
| TH-10	| Sensitive content or secrets in logs and traces	| C3, C1, C2	| B7	| Content-free logging; canary scan of logs	| SEC-12 |
| TH-11	| Incomplete deletion leaves orphan chunks or embeddings	| Derived data	| B3, B5	| Deletion cascade; post-deletion retrieval check	| SEC-15 |
| TH-12	| Lost or duplicated jobs after a crash or repeated submission	| Reports	| B2	| Durable queue; idempotency; bounded retries	| NFR-01 |
| TH-13	| Provider terms conflict with policy (retention, region)	| C1 and C2 data	| B6	| Route registry with retention mode and region; unapproved routes disabled	| SEC-16; decision D3 |
| TH-14	| Evaluation or judging calls send restricted data out	| C1 and C2 data	| B6	| Same Gateway policy for evaluation calls	| SEC-19; AC-08 |

**A.8 Acceptance cases (positive and negative)**
Outcome words: ALLOWED, DENIED (authorization failure), BLOCKED (policy stops an outbound call).
| ID	| Case	| Expected outcome	| Evidence to collect |
| AC-01	| User of organization | A requests a document, report or index entry by an identifier belonging to organization B	| DENIED; same response as for a nonexistent ID	| HTTP responses, database access log showing no row returned, audit entry |
| AC-02	| Valid user with no membership in the organization calls an org-scoped endpoint	| DENIED	| Response, audit entry |
| AC-03	| Viewer attempts to upload, edit a finding or delete a document	| DENIED; no state change	| Response, before and after database state |
| AC-04	| Request for a file by direct or expired URL, or from the wrong organization	| DENIED	| Response, storage access log |
| AC-05	| Request for another organization's analysis result or cached answer	| DENIED	| Response, cache key inspection |
| AC-06	| A tender document contains text telling the model to ignore rules, reveal other data or send content elsewhere	| ALLOWED as input; instruction not followed; no foreign data in output; no extra outbound call	| Output, canary check, gateway log, trace of calls |
| AC-07	| Provider times out or errors during a restricted analysis	| Bounded retries on the same route, then failed or partial; no other route used	| Job state, gateway log |
| AC-08	| Restricted content (C1 or C2) would be sent to a hosted provider that the organization policy does not permit, or a retry or repair would widen the route	| BLOCKED before the network call	| Mock provider shows 0 requests; gateway decision record |
| AC-09	| Restricted analysis requested with no permitted local route	| BLOCKED; visible reason; no hosted fallback	| Job state, gateway log, 0 outbound requests |
| AC-10	| Forbidden outbound payload: canary string from C3 or a secret pattern in a prompt	| BLOCKED	| Gateway decision record; canary absent from provider-side capture |
A pass means the observed outcome matches the expected one in the defined cases. It does not establish that no leakage exists outside those cases.

**A.9 Links to TG-T02 sources**
| Design choice	| Source and what it supports |
| Per-organization isolation at index and cache level; test extraction from the retrieval database	| Zeng et al., Findings of ACL 2024: black-box prompts extracted retrieval content from RAG systems; for example 250 untargeted prompts on the Enron set with GPT-3.5-turbo gave 112 exact matches of retrieved text. OWASP LLM08 names cross-tenant leakage and embedding weaknesses | 
| Do not rely on re-ranking, summarization or protective system prompts as the privacy control	| Zeng et al.: re-ranking gave almost no mitigation; summarization reduced untargeted extraction but not reliably targeted extraction and cut quality; the protective system prompts tested did not stop training-data extraction. Structural controls (isolation, routing, blocking) are therefore primary |
| Measure the privacy and utility trade-off	| Zeng et al.: a retrieval distance threshold reduced leakage but also reduced quality (average ROUGE-L on one dataset fell from about 0.39 without a threshold to about 0.27 at threshold 0.2). Results depend on their models and data and are not transferable as numbers |
| Document text as untrusted input; limited stage permissions	| OWASP LLM01 and LLM06 |
| No secrets or sensitive data in prompts; validated outputs	| OWASP LLM02, LLM05 and LLM07 |
| Route registry with provider retention mode, region and allowed classes; block when no route is permitted	| Provider data-retention documentation (TG-T02 source 4); localization and personal data rules (TG-T02 source 1) |

**A.10 Additional open questions and handoff**
Decisions D1 to D5 in the section Open decisions for joint review cover legal and provider terms (D3), numeric targets (D4) and role names (D5). Three further questions from the privacy design remain open:
| ID	| Question	| Who decides |
| Q4	| Whether a local inference route is feasible on available hardware	| Ramazan; hardware feasibility check |
| Q5	| Findings from TG-T01 interviews on what users would accept for uploads and hosted processing	| TG-T01 results |
| Q7	| Recall of the personal data detector used for classification	| Measured with Daniyar |
Handoff checklist:
•	TG-R04 (Rassul): align boundaries B2 to B5, the database isolation approach and the deletion cascade.
•	TG-T04: UX states for blocked, failed, partial and unknown, route and privacy settings visibility (NFR-09).
•	TG-T06, TG-T07, TG-T09: concrete requirements are SEC-01 to SEC-03, SEC-05 to SEC-08 and the acceptance cases AC-01 to AC-10.
•	Components 5, 7 and 9: the route matrix and policy rules feed technology and architecture decisions; the acceptance cases and NFR verification methods feed the verification plan.
•	Review by Daniyar: testability of each requirement and coverage of every model call (prompts, embeddings, repairs, retries, evaluation).
•	Task status: controlled by Ramazan.



