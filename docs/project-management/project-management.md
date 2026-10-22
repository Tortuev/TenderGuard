# Project management, responsibilities and risks

[GitHub](https://github.com/Tortuev/TenderGuard) holds deliverables and implementation
history. The [Notion tracker](https://app.notion.com/p/3fc6f6d6a08b8017a7cfc44ac2f981d4?v=3fc6f6d6a08b8069a70b000c2915ece9&source=copy_link)
holds assignments, priorities, deadlines and live statuses. The supervisor allows
a convenient tracker; YouTrack is not mandatory. Ramazan manages statuses. This
document is the committee-facing plan, not a second live tracker.

## Responsibilities and review

| Member | Primary work | Main handoffs |
| --- | --- | --- |
| Daniyar Kairatov | Corpus, annotation, parsing, embeddings, retrieval, extraction and evaluation | Source locators and structured outputs to Rassul; model/runtime needs to Ramazan. |
| Rassul Akhmetov | Proposal, functional specification, comparisons, persistence, API, jobs, orchestration, matching and reports | Data/stage contracts with Daniyar; authorization/gateway integration with Ramazan; predefence assembly. |
| Ramazan Talgatov | PM, interviews, privacy/NFRs, authentication, isolation, DevOps and shared UX | Policy, roles and retention boundaries to both members; shared UI and delivery coordination. |

Feature owners provide their workflow UI; Ramazan coordinates the common shell.
Another team member reviews substantive changes and records comments and revisions.
Assignment does not establish approval. The Notion account mapping is Daniyar →
`kairatov300100`, Rassul → `Kojizz`, Ramazan → `Ramazan Talgatov`. Each student uses
their own identifiable Git account.

## Milestones and exit conditions

The confirmed first-predefence deadline is 24 October 2026. Later calendar
commitments require team/supervisor agreement; these stages define delivery order.

| Stage | Outcome | Exit condition |
| --- | --- | --- |
| M0: first predefence | Analysis, research, design, UX and evaluation/delivery plan | Eleven components reviewed, substantive supervisor feedback addressed and shared presentation rehearsed. A full application is not required. |
| Foundation | Authorized persistence, storage, ingestion and durable execution | Organization access, source resolution, sealed-input and recovery tests pass on synthetic data. |
| First complete workflow | Upload, retrieval, B1 analysis, report and citations | A fixture traverses the actual application; unknown, blocked and failed outcomes remain distinct. |
| Core completion | Typed B2 stages, reviews, revised runs, QA and controlled inference | Core FR and SEC/NFR acceptance evidence; measured resource feasibility. |
| Frozen evaluation | Held-out measurements and error analysis | Frozen data/configuration, paired B1/B2 runs, failures, RU/KK slices and privacy/user-study evidence retained. |
| Final defence | Reviewed platform, demonstration and diploma report | Reproducible delivery, accepted limitations and supervisor review; extensions do not displace core work. |

## Dependencies

| Dependency | Reason | Lead |
| --- | --- | --- |
| TG-T01/TG-T03 → final requirements | Scope and privacy acceptance must reflect actual needs and permitted use. | Ramazan; Rassul integrates. |
| Requirements → architecture/API/UX agreement | Roles, states, classifications, citations and limits must agree. | All members. |
| Authentication/runtime grants/RLS → private access | Foreign keys prevent invalid links but do not isolate reads. | Ramazan, TG-T06/TG-T07. |
| Parsing → chunks/retrieval/citations | Findings require stable source locations. | Daniyar; Rassul integrates upload/storage. |
| Sealing/jobs → run execution | Later input changes and stale workers must not corrupt results. | Rassul, TG-R08/TG-R09. |
| Gateway → every model operation | All calls and retries require a permitted route. | Ramazan with both members. |
| Data/annotation and B1 → B2 comparison | A reference set and simpler comparator precede staging claims. | Daniyar with Rassul. |
| Development measurements → freeze → held-out tests | Selecting configurations on test data contaminates results. | Daniyar. |

## Risks

| Risk | Consequence | Mitigation / evidence | Owner |
| --- | --- | --- | --- |
| Unclear interview provenance/consent | Relevance or public-sharing claims cannot be defended. | Confirm collection/use basis; anonymize public records and restrict contacts. | Ramazan |
| Incomplete privacy/NFRs | No agreed processing or operational acceptance boundary. | Complete TG-T03; reconcile deletion with historical citations. | Ramazan |
| Unsupported or false-pass findings | Users rely on an unsubstantiated conclusion. | Both evidence sides, explicit unknowns, false-pass measures and human review. | Rassul with Daniyar |
| RU/KK imbalance or data leakage | Aggregate quality is misleading. | Family splits, class/language counts and explicit limitations. | Daniyar |
| Model costs or hardware exceed resources | Extensions displace core delivery. | Bounded B1 pilot, full call/memory accounting and resource gates. | Daniyar with Ramazan |
| Cross-organization or external disclosure | Confidential information leaves its boundary. | Scoped authorization, RLS, egress controls and negative/positive tests. | Ramazan with Rassul |
| Retry/concurrency corrupts provenance | Duplicate or changing completed reports. | Sealed inputs, request fingerprints, fenced leases and atomic publication. | Rassul |
| UX differs from scope | Demo implies unsupported policies/features. | Resolve category, TXT, role, classification and limit discrepancies. | Ramazan with Rassul |
| Competitor capabilities change | Differentiation becomes misleading. | Qualified evidence and pre-submission source recheck. | Rassul |
| Missing review or rehearsal evidence | Prepared artifacts are mistaken for accepted work. | Actual comments, revisions and three-person rehearsal record. | Rassul integrates; Ramazan coordinates |

## Traceability and submission

Link each Notion task to its artifact and commit/PR. Direct commits still need
independent review evidence; CI and merging do not establish human approval.
The [assembly checklist](../predefence/checklist.md) records gaps, and the
[supervisor record](../supervisor-feedback/supervisor-feedback.md) separates known
guidance from substantive review still needed.

Confirm team, supervisor and committee access. Create `pre-defense-1` at the accepted
commit and retain that submitted tag unchanged. No tag or review approval is claimed
merely by preparing this management document.
