# TenderGuard

**Design and Implementation of a Privacy-Preserving Multi-Agent RAG Platform for Automated Tender and Compliance Analysis for SMEs**

TenderGuard is a diploma project for helping an SME compare a tender package with its own company documents. The proposed platform extracts requirements, identifies supporting or conflicting evidence, and presents an inspectable compliance matrix with citations and explicit uncertainty. A human specialist makes the participation decision.

**Current stage:** first-predefence analysis and design, a clickable synthetic UX prototype, and an implemented PostgreSQL database foundation. The repository does not yet contain an application API, working RAG/agent pipeline or enforced privacy gateway. Prepared documents describe the target platform and planned experiments.

**Project tracking:** [TenderGuard in Notion](https://app.notion.com/p/3fc6f6d6a08b8017a7cfc44ac2f981d4?v=3fc6f6d6a08b8069a70b000c2915ece9&source=copy_link).

## Problem and target users

Tender conditions can be distributed across specifications, attachments and amendments. A supplier must identify each obligation, locate the appropriate company document, check its applicability and determine what remains unresolved. Summarizing the tender alone leaves this company-specific verification to the specialist.

The initial users are SME tender specialists and bid managers in Kazakhstan. Company managers need a readable decision record; organization owners need control over access to company evidence and permitted model-processing routes. The proposed pilot category is IT and office equipment, subject to corpus and user confirmation. The document-language scope is Russian and Kazakh.

The repository contains [three interview transcripts and their findings](docs/relevance/expert-interviews.md), covering tender specialists and a process organizer. They motivate requirement extraction, document matching, visible evidence gaps and human verification. These are preliminary team-supplied records: collection context, consent and respondent validation still need confirmation. They establish neither representative demand nor a measured reduction in preparation time.

## Aim and objectives

The aim is to design, implement and evaluate an evidence-grounded tender analysis platform that compares requirements with company records while enforcing access and data-processing boundaries.

| Objective | Expected outcome |
| --- | --- |
| Establish the user problem and realistic scope | User findings linked to prioritized, verifiable requirements. |
| Justify the method | A critical literature review and evidenced comparisons of systems and technologies. |
| Prepare evaluation data | A permitted, versioned RU/KK corpus, annotation rules and separate development/test families. |
| Implement ingestion and retrieval | Parsed PDF/DOCX evidence with resolvable source locations and authorized search. |
| Implement company-specific analysis | Atomic requirements, supported findings, explicit unknowns and human review history. |
| Enforce controlled processing | Organization isolation, approved inference routes, safe failure and audit evidence. |
| Evaluate the proposed method | Fair single-prompt/staged comparisons, error analysis and measurements of quality and resource use. |
| Deliver the diploma platform | A reproducible core workflow, demonstration and documented limitations. |

The [project proposal](docs/project-proposal/proposal.md) contains the full project identity, multilingual diploma titles, objectives, boundaries and unresolved decisions.

## Core platform workflow

1. An analyst signs in and selects an organization.
2. The analyst creates a versioned company profile and selects supporting documents.
3. The analyst uploads a tender package; ingestion validates and parses its files.
4. A run records the exact tender versions, company evidence and processing configuration.
5. The pipeline extracts atomic requirements and assesses them against selected evidence.
6. The report shows each finding, its explanation, tender/company citations and outstanding actions.
7. The analyst inspects sources, records a review and creates a new run when inputs change.

| Finding | Meaning |
| --- | --- |
| `met` | Applicable company evidence supports the complete requirement. |
| `unmet` | Applicable company evidence demonstrates a violation. |
| `unknown` | Evidence is missing, ambiguous, incomparable or conflicting without a supported resolution. |

Missing evidence alone does not prove `unmet`. Both `met` and `unmet` require company evidence as well as a tender citation. A blocked model route, parsing error or timeout is a **processing outcome**, not a compliance finding. Legal applicability is separate: unresolved applicability remains `legal_unknown`.

For example, against a 10-calendar-day delivery condition, a supported applicable 7-day commitment is `met`, a documented minimum of 14 days is `unmet`, and no applicable commitment is `unknown`. This is a synthetic acceptance example.

## Features and scope

The core includes company evidence versions, validated text-based PDF/DOCX upload, source-aware retrieval, cited requirement extraction, documentary matching, a report with unknowns and preparation actions, bounded cited questions, human reviews and versioned reanalysis. Membership checks and controlled model calls apply throughout. The [functional specification](docs/requirements/requirements.md) defines 16 Must requirements, their acceptance checks and architecture mappings.

OCR, downloadable report export, tender-revision comparison, local generative inference and fine-tuning are conditional extensions. Local embeddings are part of the proposed retrieval baseline. The project does not include automatic bid submission, payments, digital signatures, award prediction, unrestricted legal advice or an aggregator covering every procurement portal.

## Research approach

The [shared literature review](docs/literature-review/literature-review.md) discusses 12 scientific publications, linking methods and limitations to design decisions. Topics include multilingual retrieval, agent handoffs, citation support, legal reasoning boundaries, context position, privacy leakage and prompt injection.

The main hypothesis is that typed extraction, assessment and reporting stages may improve supported company-specific findings compared with single-prompt RAG. Extra stages also add cost and failure opportunities, so improvement is an experimental question rather than an assumed benefit of using multiple agents.

| Research question | Planned comparison and evidence |
| --- | --- |
| RQ1: Which retrieval method finds the necessary evidence? | Lexical search, BGE-M3 and multilingual E5-base on common annotated inputs; Recall@5/@10, complete-evidence success and ranking quality. |
| RQ2: Does staged analysis improve company-specific findings? | B1 single generation call versus B2 typed stages with the same original evidence and generator; extraction/status quality, false passes, citation support, latency and total model use. |
| RQ3: Do privacy controls enforce the intended boundaries? | Authorized and adversarial requests across two synthetic organizations and permitted/blocked routes; disclosures, forbidden transmissions and useful permitted operations. |
| RQ4: Can users inspect findings and resolve missing evidence? | Task-based walkthroughs; completion, correct status interpretation, citation inspection and observed difficulties. |

B0 names the lexical **retrieval-only** reference and does not produce compliance statuses. Development/test splits use document families, including related amendments and company variants. RU/KK results will be reported separately.

The [evaluation plan](docs/evaluation-plan/evaluation-plan.md) and [dataset/annotation guide](docs/dataset/dataset-and-annotation.md) define conditions, metrics, provisional collection targets and three annotated synthetic diagnostics. The targets are plans; no model-quality, time-saving or privacy-enforcement results have yet been measured for the working platform.

## Existing systems and proposed contribution

The [existing-systems comparison](docs/system-comparison/existing-systems.md) assesses Tenderbot, Tenderplan, Kontur.Zakupki, BiCoTender and UZEX eTender using 10 consistent criteria. UZEX is a transaction-platform comparator rather than a direct supplier-analysis product. Claims distinguish vendor documentation, observed public interactions, announced functions and unspecified capabilities.

The proposed contribution combines company-specific evidence matching, explicit unknowns, version-bound review, RU/KK evaluation and controlled confidential-context routing. The comparison does not establish market exclusivity or equivalent competitor accuracy. Summaries, cited answers and risk reports already overlap with vendor offerings; they are insufficient as a standalone novelty claim.

## Architecture and technology choices

The target is a modular application with a browser interface, API and a separate durable worker. Ingestion is a technical stage; extraction, assessment and reporting use bounded interfaces. Every embedding or generation request passes through the Inference Gateway. A hosted open-weight model still crosses an external trust boundary, and a local deployment alone does not prove privacy.

| Area | Proposed technology | Repository status |
| --- | --- | --- |
| Interface | Next.js, React, TypeScript | Target stack; current UX is standalone HTML/CSS/JavaScript. |
| API and stage contracts | Python, FastAPI, Pydantic, explicit Python stages | Designed; no application API or agents implemented. |
| Persistence | PostgreSQL 17, psycopg, ordered SQL migrations | Relational schema, migration tooling and tests implemented. |
| Retrieval | PostgreSQL lexical search and pgvector; BGE-M3 compared with multilingual E5-base | Candidates and comparison protocol documented; search/vector additions pending. |
| Parsing | pypdf and python-docx | Planned local text extraction; OCR optional. |
| Execution | PostgreSQL-backed durable jobs and a separate worker | Job records exist; execution, sealing, retries and fencing pending. |
| Inference | Provider adapters behind a policy-enforcing gateway | Designed; generator selection requires policy, resource and RU/KK checks. |
| Operations | Docker Compose, Caddy, GitHub Actions | Local database Compose and database CI exist; application deployment pending. |

The [technology comparison](docs/technology-comparison/ml-technologies.md) examines embedding, retrieval/persistence, analysis workflow and hosted/local generation decisions. Candidate properties do not establish TenderGuard performance.

The [architecture package](docs/architecture/architecture.md) includes context, use cases, components, data model, analysis sequence and deployment views, with editable Mermaid sources and SVG exports. [Integration contracts](docs/architecture/contracts.md) define source references, stages, processing states and handoffs. Dependencies should point from adapters toward application/domain contracts, keeping inference, storage and HTTP concerns outside the evidence-assessment rules.

## Team and project coordination

| Member | Primary responsibility |
| --- | --- |
| Daniyar Kairatov | Parsing, retrieval, embeddings, requirement extraction, corpus/annotation and ML evaluation. |
| Rassul Akhmetov | Backend, database, durable jobs, company-evidence workflows, orchestration, reports and predefence integration. |
| Ramazan Talgatov | Project management, privacy, authentication, DevOps, shared UI and UX coordination. |

**Supervisor:** Almas Ospanov, as recorded in the proposal. Formal spelling, affiliation and scope approval remain to be confirmed with the supervisor.

The Notion task tracker holds assignments, priorities, dependencies and acceptance criteria. GitHub retains deliverables and contribution history. The [project-management plan](docs/project-management/project-management.md) records responsibilities, milestones, risks and dependencies. The team confirms that all three members have completed their contributions and agreed on the project summary. Repository coverage below refers to the artifacts available in the merged baseline. Task status updates remain with project manager Ramazan.

## First-predefence materials and current coverage

The package is for **24 October 2026**. “Prepared” means an artifact exists for review; it does not mean supervisor approval or completed implementation.

| Component | Repository evidence | Current coverage |
| --- | --- | --- |
| 1. Project proposal | [Proposal](docs/project-proposal/proposal.md) | Prepared; supervisor confirmation pending. |
| 2. Evidence of relevance | [Interview records](docs/relevance/expert-interviews.md), [recommendations](docs/relevance/experts-recommendations.md) | Three supplied transcripts; collection/consent validation remains open. |
| 3. Literature review | [One shared review](docs/literature-review/literature-review.md) | 12 scientific source discussions and synthesis prepared; regulatory applicability is not established. |
| 4. Existing systems | [Five systems, ten criteria and evidence](docs/system-comparison/existing-systems.md) | Prepared; announced/untested functions remain qualified. |
| 5. Technology comparison | [ML technology decisions](docs/technology-comparison/ml-technologies.md) | Alternatives and selection conditions prepared; joint stack review pending. |
| 6. Requirements | [Functional requirements](docs/requirements/requirements.md) | Functional contribution prepared; detailed SEC/NFR artifact not published in this baseline. |
| 7. Architecture | [Description, Mermaid diagrams and SVGs](docs/architecture/architecture.md) | Prepared; final alignment with SEC/NFR requirements pending. |
| 8. UX / prototype | [Walkthrough](docs/ux/walkthrough.md), [HTML prototype](docs/ux/prototype/index.html) | Clickable synthetic workflow available; user-test evidence pending. |
| 9. Verification and evaluation | [Protocol](docs/evaluation-plan/evaluation-plan.md), [annotation guide](docs/dataset/dataset-and-annotation.md) | Plans and synthetic diagnostics prepared; experiments pending implementation. |
| 10. Management and risks | [Plan and tracker](docs/project-management/project-management.md) | Responsibilities, stages, risk and dependency records assembled; review/access/submission checks remain. |
| 11. Supervisor feedback | [Feedback record](docs/supervisor-feedback/supervisor-feedback.md) | Supplied organizational guidance recorded; substantive deliverable review and resulting corrections still required. |

The [TG-R05 assembly checklist](docs/predefence/checklist.md) maps each component to its tasks, evidence and remaining work. The [shared presentation](docs/predefence/presentation.md) provides the committee narrative and speaker allocation. The team has agreed on this summary; no rehearsal session or formal supervisor approval is inferred from that agreement.

The implemented database foundation includes two SQL migrations, version/evidence relationships, integrity constraints and automated migration/schema checks. It does not implement read isolation, authentication, parsing, retrieval or a production worker. The UX prototype simulates these flows with synthetic records and no backend or model calls. Its illustrative category, data-class labels and file limits need alignment with the final requirements.

## Repository organization

```text
backend/                       Database migration code and automated tests
db/migrations/                 Ordered SQL schema migrations
.github/workflows/             Database verification in CI
compose.yaml                   Local database configuration
docs/
  project-proposal/            Problem, objectives and scope
  relevance/                   Interview records and findings
  literature-review/           Canonical shared literature review
  system-comparison/           CIS comparison and supporting evidence
  technology-comparison/       Alternatives and technology decisions
  requirements/               Functional specification and TG-T03 handoff
  architecture/                Description, contracts, Mermaid sources and SVG exports
  database/                    Implemented schema and its limitations
  dataset/                     Corpus plan, annotation rules and synthetic cases
  ux/                          Walkthrough and standalone prototype
  evaluation-plan/             Experiments, metrics and test conditions
  project-management/          Responsibilities, milestones, risks and dependencies
  supervisor-feedback/         Actual guidance, response decisions and open review
  predefence/                  Submission checklist, shared deck and research module
```

Detailed deliverables stay in their component folders; this README introduces the project and links to the evidence. Private source documents, respondent contacts, credentials and confidential datasets belong in restricted storage.

## Next steps

For submission, ensure the detailed privacy/NFR contribution and permitted relevance evidence are included in the repository, resolve the documented UX differences, and confirm access to all materials. Keep any actual review and rehearsal evidence linked to the package. Identify the accepted submission with the required `pre-defense-1` tag; no submitted tag should later be moved. Obtaining new supervisor comments is outside the current assembly request.

After predefence, implement authentication and read isolation, upload/ingestion, sealed inputs and durable jobs, then retrieval and B1 before the staged workflow. Measure feasibility on development data, freeze the configuration and run held-out evaluation. Optional local generation or adaptation follows a permitted dataset, resource check and error analysis.
