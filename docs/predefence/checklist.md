# First-predefence assembly checklist

This TG-R05 record assembles evidence for all eleven components. Its labels describe
artifact readiness, not Notion statuses or approval. Rassul owns integration;
Ramazan reviews and coordinates team dependencies. The team confirms that member contributions are complete and this summary is agreed. The repository audit still distinguishes supplied artifacts from evidence not yet published.

| Component and expected evidence | Related tasks | Available artifact | Remaining acceptance work |
| --- | --- | --- | --- |
| 1. Proposal: problem, users, aim, objectives, outcomes and scope | TG-R01 | [Proposal](../project-proposal/proposal.md) | Confirm supervisor details, pilot scope and substantive review. |
| 2. Relevance: 3–5 user discussions or a substantive actual-client agreement | TG-T01 | [Three transcripts](../relevance/expert-interviews.md), [recommendations](../relevance/experts-recommendations.md) | Confirm actual collection context, respondent roles, consent/use basis and permitted supporting records. Reconcile the recommendations' scenario wording with the transcript evidence. |
| 3. Literature: at least 12 meaningfully used sources, including 8 scientific publications | TG-D02, TG-R02, TG-T02 | [Shared review](../literature-review/literature-review.md), with 12 scientific records | Confirm interpretations and synthesis. Legal applicability needs its own sourced analysis before making legal conclusions. |
| 4. Systems: 3–5 systems and 6–10 consistent criteria | TG-R03 | [Five systems and ten criteria](../system-comparison/existing-systems.md), [evidence](../system-comparison/evidence/checks.md) | Kontur's source still announces advanced features from 23 October 2026; paid operation is untested. Recheck before presentation. |
| 5. Technologies: at least 3 decisions with 2–3 alternatives each | TG-D04; TG-R04/TG-T03 contribute constraints | [ML decisions](../technology-comparison/ml-technologies.md): embeddings, B1/B2 workflow and hosted/local generation each compare two alternatives; retrieval is also discussed | Review integration, policy and resource assumptions. Candidate specifications and budgets are not measurements. |
| 6. Requirements: functional/NFR scope, priorities and verifiable Must acceptance | TG-R01, TG-T03 | [16 functional requirements](../requirements/requirements.md) | Add SEC/NFR identifiers, routing/data policy, retention/deletion, performance/recovery targets and verification methods. |
| 7. Architecture: context, use cases, component draft and consistent explanation | TG-R04; TG-T03/TG-D04 review | [Six Mermaid views, SVGs and contracts](../architecture/architecture.md) | Align with completed SEC/NFR requirements and team decisions. |
| 8. UX: key scenarios and understandable interaction | TG-T04 | [Prototype](../ux/prototype/index.html), [walkthrough](../ux/walkthrough.md) | Record actual feedback/accessibility checks. Resolve category, TXT acceptance, role labels, C3 label and proposed size limit. |
| 9. Evaluation: tests, metrics, conditions and baseline | TG-D01, TG-D03; all subsystem owners | [Protocol](../evaluation-plan/evaluation-plan.md), [annotation guide and synthetic cases](../dataset/dataset-and-annotation.md) | Confirm feasibility and reviewed thresholds; dataset collection and experiments are later work. |
| 10. Management: repository, tracker, roles, milestones, risks and dependencies | TG-T05; TG-R05 integrates | [Management record](../project-management/project-management.md), [Notion](https://app.notion.com/p/3fc6f6d6a08b8017a7cfc44ac2f981d4?v=3fc6f6d6a08b8069a70b000c2915ece9&source=copy_link) | Confirm access and retained peer-review evidence; set the submission tag at the accepted commit. |
| 11. Supervision: actual key-deliverable comments and resulting improvements | TG-R05 | [Known guidance and response record](../supervisor-feedback/supervisor-feedback.md) | Obtain substantive supervisor comments and link resulting revisions. Organizational guidance alone does not establish approval. |

## M0 task evidence in the repository

“Prepared” means that the expected document or prototype is present. Review,
rehearsal and validation can still prevent acceptance. This table does not change
or reproduce live Notion status fields.

| Owner | Task | Repository finding |
| --- | --- | --- |
| Daniyar | TG-D01 | Evaluation protocol prepared. |
| Daniyar | TG-D02 | Contribution integrated into the shared literature review. |
| Daniyar | TG-D03 | Dataset/annotation design and three synthetic diagnostics prepared. |
| Daniyar | TG-D04 | ML decisions prepared; substantive team review pending. |
| Daniyar | TG-D05 | [Research PDF and editable text/notes](research/research-slides.md) retained and integrated into the shared narrative; explanation/rehearsal remains open. |
| Rassul | TG-R01 | Proposal and functional specification prepared; supervisor confirmation and full SEC/NFR contribution pending. |
| Rassul | TG-R02 | Contribution integrated into the shared literature review. |
| Rassul | TG-R03 | Systems comparison and evidence prepared. |
| Rassul | TG-R04 | Architecture, contracts, Mermaid sources and six SVGs prepared. |
| Rassul | TG-R05 | Documentation assembly completed for the agreed scope: checklist, presentation, guidance record and README. New supervisor comments are excluded from this request; no rehearsal evidence is invented. |
| Ramazan | TG-T01 | Three supplied transcripts exist; provenance/consent validation remains open. |
| Ramazan | TG-T02 | Contribution integrated into the shared scientific review; no applied legal analysis is claimed. |
| Ramazan | TG-T03 | No complete SEC/NFR specification found in the merged repository. |
| Ramazan | TG-T04 | HTML prototype exists; actual user-test evidence and scope reconciliation remain open. |
| Ramazan | TG-T05 | Tracker and repository management snapshot available; PM maintains statuses. |

TG-R06 is implemented database-foundation work beyond the M0 documentation package.
It does not establish an implemented platform API or RAG workflow.

## Shared presentation and rehearsal

[Presentation content and speaker notes](presentation.md) connect the proposal,
research module, architecture, UX and project plan. The team has agreed on the summary. This confirmation does not establish an unrecorded rehearsal or formal supervisor approval.

| Rehearsal check | Evidence needed | Current record |
| --- | --- | --- |
| All members participate | Actual participants and session record | Not supplied. |
| Everyone explains B0/B1/B2 and unknown versus failure | Questions, responses and corrections | Not supplied. |
| UX and architecture agree | Walkthrough issues and resulting changes | Open issues listed above. |
| Timing and handoffs work | Actual duration and speaking handoffs | Not measured; presentation allocation is proposed. |

## Submission checks

- Publish the completed privacy/NFR contribution and validate the relevance records; a full SEC/NFR artifact was not found in this repository audit.
- Confirm supervisor identity/affiliation; retain actual review evidence when available. Obtaining new comments is outside this assembly request.
- Retain actual peer comments and revisions; a merge or CI success is not peer review.
- Confirm committee/supervisor repository and evidence access.
- Review the shared deck and perform the three-person rehearsal.
- Choose the accepted commit, then create `pre-defense-1`; never move a previously submitted tag.
- Provide repository/tag links, completed-work summary, limitations and outstanding tasks.

The inspected baseline's database CI passed. It covers database migrations/schema
and lint, not model quality or privacy enforcement. No open PRs or formal review
entries on PRs 8–13 were found in the audit. Review evidence held elsewhere should
be linked by the team rather than inferred from merge history.
