# TenderGuard requirements and acceptance criteria

**Version:** 1.0, 21 October 2026. **Task:** TG-R01. **Owner:** Rassul Akhmetov. **Reviewer:** Ramazan Talgatov, with Daniyar Kairatov reviewing ML criteria. **Status:** specification ready for review; implementation and approval are assessed separately.

These requirements implement the scope of the [project proposal](proposal.md). They describe the target core version rather than a completed product. Must requirements define the core release; Should requirements are extensions that do not block it. Numeric limits below are proposed engineering decisions, not university-mandated thresholds.

## Basis, assumptions and priorities

| Basis | Status | Effect on requirements |
| --- | --- | --- |
| Team decisions | Confirmed in project planning | Three members, GitHub, RU/KK document scope, Daniyar leading ML, Rassul and Ramazan leading backend/platform work |
| Supervisor architecture | Supplied design baseline | Four processing stages, web interface, API, worker and PostgreSQL-based persistence; refinements require review |
| Data and user hypotheses | Pending TG-T01 validation | Candidate category is IT and office equipment; manual effort, missing evidence and sharing restrictions require actual user findings |
| Model deployment | Core/extension boundary | Hosted processing is allowed only for permitted data; local inference and fine-tuning are optional extensions |
| First-predefence rubric | Documentation requirement | This specification provides priorities and verifiable criteria; actual results and implementation evidence belong to later acceptance records |

Each criterion below is a required future check, not a claim that a test has passed. “Reject” means a safe response without private content or a false completed analysis. “Evidence” means a versioned source and a resolvable locator whose content supports the associated claim. An existing file ID alone is insufficient.

## Functional requirements

### FR01 Organization access and roles

**Priority:** Must. **Lead:** Ramazan. **Tasks:** TG-T06, TG-T07, TG-T17.

The server must authorize actions using verified organization membership. The proposed owner/administrator, member/analyst and viewer capabilities must be mapped explicitly to stored roles.

- An owner can manage membership and policy; an analyst can maintain evidence and run analyses; a viewer has read access only to permitted material.
- A direct write request by a viewer is rejected even if the interface hides the action.
- Replacing a document, profile, run or job identifier with one from a second organization does not disclose its contents or permit a change. The tenant is not trusted merely because it appears in the request.

### FR02 Versioned company profiles and evidence

**Priority:** Must. **Lead:** Rassul. **Tasks:** TG-R10, TG-R16.

- An analyst can create a profile version containing company facts and attach supporting document versions, provenance and validity dates where applicable.
- Changing facts or supporting evidence creates a new version. A previous run continues to resolve to the profile and evidence it used.
- An unsupported fact can be stored as an unverified declaration, but cannot by itself produce a supported `met` or `unmet` finding. Cross-organization profile access is rejected.

### FR03 Tender workspaces and validated uploads

**Priority:** Must. **Lead:** Rassul; Daniyar integrates ingestion. **Tasks:** TG-R09, TG-D09.

- An analyst can create a tender and attach multiple text-based PDF/DOCX files with recorded type, size, content hash and version.
- The proposed initial limit is 20 MiB per file: larger files receive HTTP 413; unsupported types receive HTTP 415. Extension, file signature and parser outcome are checked, including mislabeled and malformed inputs.
- Originals are stored outside the public web root. Download requires organization authorization; a storage path supplied by a client cannot escape the authorized file store.

### FR04 Parsing and stable source locations

**Priority:** Must. **Lead:** Daniyar. **Tasks:** TG-D06, TG-D07.

- Text-based PDF fixtures retain page and span references; DOCX fixtures retain stable paragraph/table identifiers and offsets within the document version. DOCX page numbers are not invented.
- Clicking a citation resolves to the exact stored version and supporting passage. Supported table cases and unsupported layouts are documented in parser fixtures.
- Empty, corrupted or image-only inputs cannot produce a successful substantive analysis. A scan needing OCR receives an explicit `needs_ocr` outcome, and mixed/unsupported content is disclosed.

### FR05 Authorized search and cited questions

**Priority:** Must. **Lead:** Daniyar. **Tasks:** TG-D10, TG-D11, TG-D15.

- A question searches only the selected tender and an explicitly permitted corpus, within the authorized organization context.
- A returned factual answer includes citations that resolve to the correct versions and support the answer. Missing relevant context produces an insufficient-evidence response.
- Both a valid supporting case and an unanswerable case are checked. Retrieval cannot expose another organization's text through results, counts, generated answers or cached context.

### FR06 Atomic requirement extraction

**Priority:** Must. **Lead:** Daniyar; Rassul owns stage contracts. **Tasks:** TG-D13, TG-R13.

- Each extracted record includes an identifier, requirement text, type, mandatory/optional/unspecified classification and source reference. Applicable conditions retain operator, value, unit, date and negation.
- Contract and reference validation reject malformed values and references outside the selected inputs. Unspecified conditions are not silently invented.
- Numeric, date, negation and multi-clause fixtures have inspectable expected outputs. Invalid model output after bounded repair results in partial or failed processing, not an accepted report.

### FR07 Company-specific documentary fit

**Priority:** Must. **Lead:** Rassul; Daniyar reviews semantic matching. **Tasks:** TG-R14, TG-D15.

- Each requirement receives `met`, `unmet` or `unknown`, with an explanation, tender citation and the company evidence used when available.
- `Met` needs evidence of satisfaction; `unmet` needs evidence of conflict. Missing, contradictory or unresolved information remains `unknown`; absence of a certificate in the profile is not proof that the company lacks it.
- Synthetic cases cover a 10-calendar-day condition versus supported 7-day and 14-day commitments, absent evidence, incompatible units and expired evidence. Incompatible or ambiguous values are not compared without an explicit valid normalization.

### FR08 Limited legal applicability

**Priority:** Must. **Lead:** Rassul. **Task:** TG-R15.

- Documentary findings and legal flags appear as separate fields.
- A legal flag requires a versioned normative source, an identifiable provision and human-validated applicability to the case. A benchmark paper or vendor description cannot supply a legal rule.
- Missing corpus approval, unresolved effective date or uncertain applicability produces `legal_unknown` and human review. This fallback is mandatory even before a validated legal corpus is available.

### FR09 Evidence-based reports and actions

**Priority:** Must. **Lead:** Rassul. **Task:** TG-R17.

- A report shows requirements, statuses, explanations, citations, missing evidence, recommended next actions and the risk rubric version.
- Confirmed risks and information completeness are shown separately. A high unknown count cannot be hidden by a low aggregate risk score.
- A reviewer can trace a reported risk to its underlying condition and evidence. Risk severity is derived from a documented rubric and is not presented as a probability of winning.

### FR10 Human review without rewriting predictions

**Priority:** Must. **Lead:** Rassul. **Task:** TG-R16.

- An authorized analyst can add a comment or correction with a reason.
- The original machine prediction, author, timestamp and subsequent review remain distinguishable. Unauthorized edits are rejected.
- Evaluation can retrieve the original machine output separately from a human-corrected view. A correction does not silently change historical evaluation inputs.

### FR11 Run history and input manifests

**Priority:** Must. **Lead:** Rassul; Daniyar owns evaluation artifacts. **Tasks:** TG-R16, TG-D23.

- A run records exact document, profile and corpus versions plus model, embedding, prompt, policy and code identifiers, decoding settings and execution metadata.
- Inputs are assembled and sealed before processing. A retry uses that sealed manifest rather than newly added evidence.
- New analysis creates a new run. Changing a source document or profile does not replace citations or outputs in an old report; unresolved historical references cause an explicit error.

### FR12 Policy-enforced model routing

**Priority:** Must. **Lead:** Ramazan. **Tasks:** TG-T09, TG-T10, TG-T13.

- All external model routes, including generation, embeddings, optional evaluation calls and retries, pass through server policy. Only permitted destinations receive minimized, permitted context.
- If private data is forbidden on hosted routes and an approved local route is unavailable, the stage is blocked with a clear reason. Local failure does not trigger an unauthorized hosted fallback.
- Policy, masking or required-audit failure cannot enable a bypass. Intermediate outputs and placeholder mappings retain their access restrictions; an agent cannot override policy through its generated instructions.

### FR13 Safe audit events

**Priority:** Must. **Lead:** Ramazan. **Tasks:** TG-T11, TG-T17.

- Upload, analysis, routing, block, evidence access and review events record actor, organization, relevant run, policy version, outcome and safe metadata where applicable.
- Raw private document text, credentials, complete prompts and reversible placeholder mappings do not appear in shared logs or audit output.
- Audit access is authorized by organization and role. Canary strings and cross-organization reads are checked against both normal and failure paths.

### FR14 Durable processing and truthful progress

**Priority:** Must. **Lead:** Rassul. **Tasks:** TG-R08, TG-R11, TG-R18.

- Accepted work persists independently of the API process; the user can inspect queued/running/finished or failed job state.
- Domain outcomes such as partial processing, blocked routing and `needs_ocr` are distinguishable from job lifecycle state. The UI offers the relevant next action instead of showing a successful complete report.
- Worker crash, expired lease and repeated submission are tested. A bounded retry recovers accepted work without publishing duplicate final reports or mixing run inputs.

### FR15 Optional local inference and hybrid stages

**Priority:** Should. **Leads:** Daniyar, Rassul and Ramazan. **Tasks:** TG-D25, TG-R25, TG-T25.

If selected, local inference records the model, runtime and hardware and supports the same typed stage contract. A local stage's private output cannot reach a hosted stage without a fresh policy decision. Acceptance includes actual outbound-request checks and quality/resource comparison against the permitted hosted configuration. Open weights alone do not establish local execution or suitable licensing.

### FR16 Optional model adaptation

**Priority:** Should. **Lead:** Daniyar; Rassul and Ramazan review data and operations. **Tasks:** TG-D26, TG-R26, TG-T26.

If selected, LoRA/QLoRA uses permitted training data separated from development/test families before adaptation. The base model and adapted version are evaluated on the same untouched test set. Adapter/configuration identifiers, resource use and limitations are recorded. A trained adapter is not accepted as evidence of improvement without this comparison.

### FR17 Optional OCR

**Priority:** Should. **Leads:** Daniyar, Rassul and Ramazan. **Tasks:** TG-D27, TG-R27, TG-T27.

If selected after assessing scan frequency, OCR is evaluated on RU/KK fixtures with source-location checks. Extracted text must still resolve to its document version and page. OCR failures are visible, and restored text does not bypass routing policy. Until then, FR04's explicit `needs_ocr` outcome remains required.

### FR18 Optional report export

**Priority:** Should. **Proposed lead:** Rassul; a separate implementation task requires backlog agreement.

If selected, a PDF/DOCX export contains the same run version, statuses, evidence and uncertainty as the report view. Download requires authorization and preserves source references. An in-app report is sufficient for the core version.

## Non-functional requirements baseline

Ramazan's TG-T03 refines the privacy and operational model. This baseline identifies the checks that must remain aligned with the functional scope.

| ID and priority | Requirement | Acceptance method | Lead |
| --- | --- | --- | --- |
| NFR01 Must | Organization isolation | Two-organization negative cases cover API, non-owner database roles/RLS, files, jobs, caches, retrieval references and mappings, including pooled-connection reuse. No unauthorized disclosure in the defined suite is a release gate; foreign-key consistency alone is insufficient. | Ramazan, with Rassul |
| NFR02 Must | Controlled egress | Capture outbound requests on normal, retry and failure paths. Prohibited context never appears in an external request in this suite. Permitted requests still succeed. Measure residual disclosure on annotated canaries rather than treating masking as a guarantee. | Ramazan |
| NFR03 Must | Safe files and secrets | Environment/secret-store credentials stay outside tracked files. Test path traversal, unauthorized download and canaries in logs/errors; validate the chosen expiry/access model for temporary files and download links. | Ramazan and Rassul |
| NFR04 Must | Reproducible evaluation | Dataset/split hashes, code/model/prompt/policy versions, hardware, outputs, errors and resource use are recorded. Re-scoring saved outputs reproduces the reported metrics. Private artifacts remain in restricted storage. | Daniyar |
| NFR05 Must | Recovery and consistency | Crash/retry tests preserve sealed inputs and avoid duplicate publication. A database-and-file-store restoration exercise preserves version hashes and rechecks access. Recovery procedures identify the tested environment and limitations. | Rassul and Ramazan |
| NFR06 Must | Russian and Kazakh handling | Parsing and quality reports separate RU/KK and disclose mixed-language support and sample counts. Fixtures cover Kazakh characters, negation, quantities, units and calendar/business-day differences. | Daniyar |
| NFR07 Must | Bounded execution | Configure provider timeouts, token ceilings and retry limits. Proposed starting caps are three job attempts and one output-repair attempt per model stage; pilot review can revise them. Exhaustion produces an explicit failure/partial outcome and no infinite agent loop. | Rassul, with Daniyar |
| NFR08 Should | Measured interactive performance | Proposed starting target for light API calls is p95 at most 500 ms at 5 requests/s for 10 minutes after 60 seconds warm-up, with authentication enabled and hardware/data/cache conditions recorded. Report inference, queue delay and full-analysis time separately. Validate or revise the target after a deployment pilot. | Rassul and Ramazan |
| NFR09 Must | Inspectable, understandable results | A user can upload, select a profile, run analysis, inspect unknowns and open evidence without knowing the ML internals. States have text labels, not color alone. Task-based walkthroughs record completion and difficulties; blocked/partial states explain what can be done next. | All workflow owners |

## Workflow and verification traceability

| Scenario | Requirements | Main components | Planned verification evidence |
| --- | --- | --- | --- |
| UC1 Upload a tender package | FR03, FR04, FR14; NFR01, NFR05, NFR06 | Documents API, private file store, ingestion worker and upload UI | Valid/invalid upload fixtures, parser outputs, exact-version source resolution and crash cases |
| UC2 Ask a tender question | FR05, FR12; NFR01, NFR02, NFR06, NFR07 | Retrieval, QA, policy gateway and source viewer | Answerable/unanswerable queries, retrieval labels, supported citations and forbidden-route captures |
| UC3 Compare company evidence | FR02, FR06, FR07, FR08, FR14 | Profile API, extraction, matching, legal-source boundary and worker | Typed output checks, met/unmet/unknown fixtures, legal_unknown cases and sealed inputs |
| UC4 Inspect and review a report | FR09, FR10, FR11, FR13; NFR04, NFR09 | Report API, review history, evidence viewer and audit | Evidence on both sides, original/corrected outputs, historical citations and user walkthrough |
| UC5 Manage access and policy | FR01, FR12, FR13; NFR01, NFR02, NFR03 | Authentication, membership, database policies, gateway and audit | Direct API denials, two-tenant tests, outbound canaries and safe audit access |
| UC6 Update company evidence | FR02, FR11; NFR01, NFR05 | Profile versions, evidence store and input manifests | New version/new run with old results preserved, plus authorization checks |

Acceptance cases verify system behavior. Research metrics measure quality on a sample and do not replace access or egress tests. TG-D01 must specify the extraction precision/recall/F1 calculation, finding-status macro-F1 and confusion matrix, retrieval metrics, citation support, completeness, latency and cost accounting. Numerical quality thresholds and corpus size remain open until pilot calibration; they are not silently assumed to have been achieved.

The B1/B2 comparison uses identical permitted document/profile versions and, for the primary staging experiment, a frozen evidence pack and model. All calls, repairs, retries, failed runs and resource use count toward each configuration. A later adaptive-retrieval variant or local-model comparison must be reported separately.

## Review, validation gaps and change control

TG-T01 must provide actual user findings. The proposed category, workflow pain points and 20 MiB upload limit are currently design assumptions, not interview conclusions. After interviews, record the chain `finding ID -> requirement ID -> implementation task -> acceptance evidence` in the relevance and implementation records. Do not invent respondent statements to fill that chain.

Before team acceptance, Rassul checks all functional criteria, Daniyar checks extraction/retrieval and evaluation feasibility, and Ramazan checks privacy, priorities and unresolved dependencies. Supervisor comments and decisions belong in the separate supervisor-feedback material once received. The supervisor field, pilot category, supported table layouts, model/provider choice, legal corpus, later milestone dates and measured resource limits remain subject to confirmation.

For a change, record the rationale, affected requirement IDs, priority, scenarios, components and acceptance checks. Link the reviewed repository commit or PR to the existing tracker task. Only the project manager changes Notion task status. A merged specification does not by itself mean that the specified platform features are implemented or that the team has obtained supervisor approval.
