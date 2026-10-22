# Shared first-predefence presentation

[Editable PowerPoint](presentation.pptx)

This TG-R05 deck integrates the committee narrative with Daniyar's [research module](research/research-slides.md). The team confirms completion of member contributions and agreement on the summary. Speaker allocation and timing still need confirmation through actual rehearsal. Full evidence stays in the component documents. Substantive supervisor approval is pending.

## Slide 1: TenderGuard

**Presenter:** All members

### On-slide content

- Tender and company-evidence analysis for SMEs
- Daniyar Kairatov · Rassul Akhmetov · Ramazan Talgatov
- First predefence: analysis, design and prototype

### Speaker notes

Official topic: Design and Implementation of a Privacy-Preserving Multi-Agent RAG Platform for Automated Tender and Compliance Analysis for SMEs. Supervisor recorded in the proposal: Almas Ospanov; formal details and approval remain to be confirmed. Introduce the committee to the target platform and clearly separate it from the currently implemented database and synthetic prototype.

### Evidence

- [proposal.md](../project-proposal/proposal.md)

## Slide 2: Problem and users

**Presenter:** Ramazan Talgatov

### On-slide content

- SME tender specialists must check obligations against their own company evidence.
- Conditions and supporting documents can be distributed across files and revisions.
- Three supplied transcripts motivate extraction, matching, visible gaps and human review.
- Collection context and consent still require confirmation. Time savings are not measured.

### Speaker notes

The initial context is Kazakhstan, Russian and Kazakh documents, with IT and office equipment as the provisional pilot. The records describe two tender specialists and a process organizer. Do not describe the transcripts as representative validation or invent interview timing, client agreement or quantified savings. Public records use P01–P03.

### Evidence

- [expert-interviews.md](../relevance/expert-interviews.md)
- [experts-recommendations.md](../relevance/experts-recommendations.md)

## Slide 3: Aim and expected outcomes

**Presenter:** Rassul Akhmetov

### On-slide content

- Design, implement and evaluate an evidence-grounded tender analysis platform.
- Extract requirements and compare them with selected company documents.
- Preserve citations, uncertainty and the history of inputs and human reviews.
- Enforce access and processing boundaries, then measure quality and resource use.

### Speaker notes

The expected engineering outcome is a core platform, not just a document summarizer. Research and requirements precede implementation. Corpus design, justified technology decisions, controlled experiments and an explainable interface are separate objectives with their own evidence.

### Evidence

- [proposal.md](../project-proposal/proposal.md)

## Slide 4: Core workflow

**Presenter:** Rassul Akhmetov

### On-slide content

- An analyst selects an organization, company profile and supporting evidence.
- The platform ingests a tender and records exact document versions for a run.
- Extraction, assessment and reporting produce a requirement/evidence matrix.
- The analyst inspects sources, records a review and starts a new run for revised inputs.

### Speaker notes

These are planned platform actions. The standalone UX simulates the interaction without backend or model calls. Ingestion is a technical processing stage and need not be an LLM agent. Profiles and sealed run inputs prevent later evidence from silently changing an earlier analysis.

### Evidence

- [proposal.md](../project-proposal/proposal.md)
- [contracts.md](../architecture/contracts.md)

## Slide 5: Findings and uncertainty

**Presenter:** Rassul Akhmetov

### On-slide content

- Met: applicable company evidence supports the requirement.
- Unmet: applicable evidence demonstrates a violation.
- Unknown: evidence is missing, ambiguous, incomparable or unresolved.
- Blocked or failed processing remains separate from company compliance.

### Speaker notes

Synthetic example: delivery within 10 calendar days. An applicable 7-day commitment supports met; a documented minimum of 14 days supports unmet; no applicable commitment supports unknown. Both met and unmet require company citations plus the tender citation. Missing evidence is not proof of violation. Legal applicability is a separate field; unresolved applicability is legal_unknown.

### Evidence

- [requirements.md](../requirements/requirements.md)
- [dataset-and-annotation.md](../dataset/dataset-and-annotation.md)

## Slide 6: Requirements and scope

**Presenter:** Rassul Akhmetov

### On-slide content

- Sixteen Must functional requirements have acceptance checks and architecture mappings.
- Core inputs are text-based Russian and Kazakh PDF/DOCX documents.
- The core includes cited analysis, bounded questions, reviews and versioned reanalysis.
- Detailed SEC/NFR evidence must be published. OCR, export, local generation and training are extensions.

### Speaker notes

Must means required for the core diploma platform, not a finished application at first predefence. Exclusions include automatic submission, payments, signatures, award prediction and unrestricted legal advice. Ramazan supplies TG-T03: data classes, routes, isolation, retention/deletion and measurable operational targets.

### Evidence

- [requirements.md](../requirements/requirements.md)

## Slide 7: Research foundation

**Presenter:** Daniyar Kairatov

### On-slide content

- One shared review discusses twelve scientific publications and their limitations.
- Retrieval and citation studies motivate complete-evidence and support measurements.
- Agent-failure and security studies motivate bounded handoffs and explicit validation.
- The proposed staged method must justify its additional cost against a simpler baseline.

### Speaker notes

The review includes ReAct, MAST, LegalBench, RAGAs, RAG privacy/poisoning/injection studies, BGE-M3, Self-RAG, ALCE and Lost in the Middle. Do not transfer their scores to RU/KK tenders. The retained research module has fuller study-specific notes. Fine-tuning does not resolve missing evidence or authoritative-document ambiguity.

### Evidence

- [literature-review.md](../literature-review/literature-review.md)
- [research-slides.md](research/research-slides.md)

## Slide 8: Regional systems comparison

**Presenter:** Rassul Akhmetov

### On-slide content

- Five systems: Tenderbot, Tenderplan, Kontur.Zakupki, BiCoTender and UZEX eTender.
- Ten consistent criteria distinguish discovery, analysis, evidence, workflow and processing controls.
- Cited answers and risk summaries overlap with vendor offerings.
- The proposed contribution combines company evidence, unknowns, versioned review and controlled routing.

### Speaker notes

The complete five-by-ten matrix and primary sources remain in the comparison document. UZEX is a contextual transaction-platform comparator. Unspecified means not established by reviewed sources, not absent. Kontur still announces advanced rollout from 23 October 2026; paid operation has not been tested. BiCo recheck was restricted. These observations do not prove uniqueness or comparative accuracy.

### Evidence

- [existing-systems.md](../system-comparison/existing-systems.md)
- [checks.md](../system-comparison/evidence/checks.md)

## Slide 9: Technology decisions

**Presenter:** Daniyar Kairatov

### On-slide content

- Proposed application: Next.js/TypeScript, Python/FastAPI and Pydantic contracts.
- PostgreSQL stores relational evidence. Lexical search and pgvector retrieval are planned.
- Compare BGE-M3 with multilingual E5-base and B1 with typed B2 stages.
- Generator choice passes policy, resource and RU/KK checks. Local generation remains optional.

### Speaker notes

The ML technology record compares alternatives for embeddings, pipeline structure and hosted/local generation, with further retrieval design discussion. Model properties are candidate specifications. Parsing, embeddings, vector indexes, stage schemas and generator adapters are not yet integrated into the backend. Hosted open-weight inference still sends context outside the operator boundary.

### Evidence

- [ml-technologies.md](../technology-comparison/ml-technologies.md)
- [architecture.md](../architecture/architecture.md)

## Slide 10: Architecture and dependency direction

**Presenter:** Rassul Akhmetov

### On-slide content

- Browser interface and API coordinate a separate durable processing worker.
- Domain rules define evidence and findings. Application use cases depend on narrow ports.
- HTTP, database, parser and provider adapters implement those ports.
- Six Mermaid views and SVG exports align scenarios, components, data and deployment.

### Speaker notes

Use the linked context, use-case and component diagrams during questions. The API is modular; do not present every logical module as a microservice. The architecture also includes the ER view, sequence and deployment. Dependency direction complements runtime authorization and egress enforcement; it does not replace them. Current code implements migration tooling, not these future layers.

### Evidence

- [architecture.md](../architecture/architecture.md)
- [contracts.md](../architecture/contracts.md)

## Slide 11: Privacy boundary

**Presenter:** Ramazan Talgatov

### On-slide content

- Each read and action checks active organization membership and role.
- Every embedding and generation call uses the Inference Gateway.
- Prohibited routes block processing without an unapproved hosted fallback.
- Local inference alone does not prove privacy. Enforcement tests remain future work.

### Speaker notes

TG-T03 is still incomplete in the repository. Confirm classification, permitted routes, derived-output restrictions, audit/secrets, retention/deletion and operational acceptance targets. The current SQL public/private class is not the prototype C3 vocabulary. Foreign keys prevent invalid references but do not implement read isolation. Use synthetic data until the runtime controls are implemented and verified.

### Evidence

- [contracts.md](../architecture/contracts.md)
- [requirements.md](../requirements/requirements.md)
- [database.md](../database/database.md)

## Slide 12: UX prototype

**Presenter:** Ramazan Talgatov

### On-slide content

- The clickable prototype illustrates company evidence, upload, reports, citations and reviews.
- It also illustrates revised runs, questions, blocked routes and model unavailability.
- All records and results are synthetic. No backend, authentication or model is connected.
- Walkthrough feedback and scope alignment remain open.

### Speaker notes

Follow the UX walkthrough in the repository rather than treating this slide as a working system demonstration. Resolve roadworks versus IT pilot, TXT acceptance, role labels, C3 classification and the proposed 25 MB limit. Record actual participant observations and accessibility checks after the session.

### Evidence

- [walkthrough.md](../ux/walkthrough.md)
- [index.html](../ux/prototype/index.html)

## Slide 13: Evaluation design

**Presenter:** Daniyar Kairatov

### On-slide content

- B0 is lexical retrieval only. B1 uses one generation call. B2 uses typed stages.
- B1 and B2 share original evidence, generator and validation rules.
- Measure retrieval, extraction/status quality, false passes, citations and total resource use.
- Split connected document families and report RU/KK separately. Retain failures.

### Speaker notes

RQ1 concerns retrieval; RQ2 concerns supported documentary findings; RQ3 concerns privacy controls; RQ4 concerns user interpretation. Status scores do not apply to B0. The corpus and numeric targets are provisional plans. Three authored synthetic diagnostics exist; they are not held-out natural-document results. Count every B2 stage and retry, and report different compute or evidence scopes explicitly.

### Evidence

- [evaluation-plan.md](../evaluation-plan/evaluation-plan.md)
- [dataset-and-annotation.md](../dataset/dataset-and-annotation.md)
- [research-slides.md](research/research-slides.md)

## Slide 14: Team and delivery stages

**Presenter:** Ramazan Talgatov

### On-slide content

- Daniyar leads ML/data/evaluation. Rassul leads backend/analysis and integration.
- Ramazan leads PM/privacy/DevOps and shared UX.
- Delivery proceeds from M0 design to foundation, core workflow and frozen evaluation.
- Notion coordinates work. GitHub preserves deliverables, contributions and review evidence.

### Speaker notes

All members contribute UI for their workflow and review each other. Authentication, isolation and source contracts precede private-data integration. B1 and development measurements precede the staged comparison and final freeze. Main risks are unsupported findings, privacy disclosure, corpus imbalance/leakage, resource overruns and incomplete review evidence. Later dates require agreement.

### Evidence

- [project-management.md](../project-management/project-management.md)

## Slide 15: Current evidence and remaining work

**Presenter:** Rassul Akhmetov

### On-slide content

- Prepared: proposal, twelve-source review, comparisons, functional requirements and architecture.
- Available: evaluation/annotation plans, three transcripts, synthetic UX and database foundation.
- Repository follow-up: publish SEC/NFR evidence, validate interview provenance and resolve UX differences.
- The team confirms completed contributions and agrees on the summary. Published evidence remains traceable.

### Speaker notes

The eleven-component checklist maps all M0 tasks to artifacts and gaps. Do not equate a merged document, a Notion status or passing database CI with accepted platform functionality. There is no measured model improvement or completed privacy enforcement. The shared package is prepared for review, not supervisor approved.

### Evidence

- [checklist.md](checklist.md)
- [supervisor-feedback.md](../supervisor-feedback/supervisor-feedback.md)

## Slide 16: Next steps

**Presenter:** All members

### On-slide content

- Confirm scope, publish the detailed SEC/NFR contribution and review the assembled materials.
- Keep actual review decisions and resulting changes linked to deliverables.
- Rehearse together, confirm committee access and tag the accepted submission.
- Implement the controlled core workflow, then measure it against the frozen baseline.

### Speaker notes

The team confirms completion of member contributions and agreement on this summary. New supervisor comments are excluded from the current assembly request. Known guidance concerns document storage and the supplied architecture; it does not establish formal approval. Retain any actual review and rehearsal evidence without inventing a session, approval or measurement. Preserve the accepted pre-defense-1 tag unchanged.

### Evidence

- [supervisor-feedback.md](../supervisor-feedback/supervisor-feedback.md)
- [checklist.md](checklist.md)
