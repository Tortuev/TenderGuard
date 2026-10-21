# TenderGuard project proposal

TenderGuard is a proposed web platform that helps an SME check a tender against its own company profile and supporting documents. It will extract requirements, show whether the available evidence supports compliance, and explain missing information and risks with citations. The project will evaluate whether a controlled multi-agent RAG workflow improves this analysis compared with a simpler single-prompt RAG baseline, while enforcing access and data-transfer policies.

## Project identification

| Field | Proposal |
| --- | --- |
| Product and repository | [TenderGuard](https://github.com/Tortuev/TenderGuard) |
| English diploma title | Design and Implementation of a Privacy-Preserving Multi-Agent RAG Platform for Automated Tender and Compliance Analysis for SMEs |
| Russian diploma title | Проектирование и разработка мультиагентной RAG-платформы с сохранением конфиденциальности для автоматизированного анализа тендерной документации и комплаенс-рисков для МСБ |
| Kazakh diploma title | МСБ үшін тендерлік құжаттаманы автоматты талдауға және комплаенс-тәуекелдерді бағалауға арналған, құпиялылықты сақтайтын көп агентті RAG платформасын жобалау және әзірлеу |
| Team | Daniyar Kairatov, Rassul Akhmetov, Ramazan Talgatov |
| Supervisor field | Almas Ospanov, as named in the existing planning material; official spelling, position and affiliation require team confirmation before formal submission |
| Initial market context | SMEs preparing tender applications in Kazakhstan; Russian and Kazakh documents |
| Proposed pilot category | IT and office equipment; provisional until user discussions and document availability confirm a manageable category |
| First predefence | 24 October 2026 |

The proposal follows the supplied first-predefence requirements, the team assignment, the supervisor's architecture and the team's subsequent scope decisions. The task tracker assigns TG-R01 to Rassul and its review to Ramazan. The separate requirements and acceptance criteria specification is planned at `docs/requirements/requirements.md`.

## Problem statement

A decision to enter a tender requires more than a summary. A supplier must identify the relevant conditions across specifications and attachments, compare them with its capabilities and supporting documents, and determine which conclusions are justified. A statement such as “a certificate is required” is useful only when the reviewer can find the requirement, inspect the company's certificate and check its relevance and validity.

The team's problem hypotheses are that fragmented documents increase manual checking effort, incomplete company records create uncertainty, and restrictions on sharing company documents constrain the use of hosted AI services. Their frequency, cost and importance to actual SMEs have not yet been established by evidence included in this repository. TG-T01 must supply actual interview findings before the proposal can claim customer validation.

The engineering problem is to preserve the relationship between a finding and its evidence throughout parsing, retrieval, model calls, inter-stage handoffs and reporting. The platform must also prevent an otherwise useful analysis from exposing another organization's data or sending restricted information to an unauthorized provider.

## Users and decision boundaries

| User | Main need | Planned permitted actions |
| --- | --- | --- |
| SME tender specialist or analyst | Check suitability and prepare a list of documents or issues to resolve | Maintain company evidence, upload tender files, run analysis, ask questions, inspect citations and record review comments |
| Company manager or authorized viewer | Review the basis for an application decision | Read permitted reports, evidence and outstanding actions; a viewer cannot change data |
| Organization owner or administrator | Control membership and processing policy | Manage organization access and approved data routes |

The system supports a human decision about preparation and participation. It does not submit an application, promise eligibility, predict a win or replace a qualified legal assessment. Documentary fit and legal applicability remain separate outputs.

## Aim and objectives

The aim is to design, implement and experimentally evaluate a platform that turns tender documents and company evidence into a traceable compliance analysis, with explicit uncertainty and enforceable privacy controls.

| Objective | Expected deliverable | Verification | Lead |
| --- | --- | --- | --- |
| O1 Establish the user problem and scope | Interview findings, pilot category and requirements linked to findings | Recorded respondent context and actual answers; hypotheses distinguished from observations | Ramazan, with all members participating |
| O2 Justify the proposed approach | Critical literature review and consistent comparison of relevant CIS platforms | Primary evidence, limitations and links from findings to design choices; literature criterion completed under its own tasks | Daniyar and Rassul; Ramazan contributes privacy sources |
| O3 Prepare traceable research data | Versioned tender corpus, company profiles, annotation guide and separated development/test data | Source permissions, document-family separation, citation labels and independent annotation checks | Daniyar |
| O4 Implement ingestion and retrieval | Validated PDF/DOCX upload, source locators, authorized search and cited answers | Parser and source-resolution cases; retrieval measurements by language | Daniyar, with Rassul providing API and storage integration |
| O5 Implement company-specific analysis | Typed requirements, evidence matching, explicit statuses, reports and review history | Deterministic acceptance cases and annotated end-to-end evaluation | Rassul, with Daniyar responsible for extraction quality |
| O6 Enforce controlled processing | Membership checks, organization isolation, policy gateway and safe audit | Direct API, database, file, worker and outbound-request negative tests | Ramazan, with Rassul |
| O7 Evaluate the proposed method fairly | Baseline comparisons, cost/latency results and error analysis | Frozen inputs, versioned configurations, retained failures and reproducible scoring | Daniyar coordinates; all members own their subsystem evidence |
| O8 Deliver an explainable prototype and report | Runnable core workflow, installation guide, demo scenario and diploma materials | Another member follows setup and traces a reported finding to its inputs | All members |

## Core workflow and company profile

1. An authenticated analyst selects an organization and creates a company-profile version with supporting evidence.
2. The analyst creates a tender workspace and uploads its text-based PDF/DOCX package.
3. Ingestion validates and parses the files, retaining document versions and resolvable source locations.
4. Extraction creates atomic requirements with conditions, values, units, dates and citations where applicable.
5. Analysis compares each requirement with the selected company-profile version and its evidence.
6. The analyst inspects a report, opens both sides of the evidence, reviews unknowns and records comments or corrections.
7. New evidence or document revisions produce a new analysis run; previous findings remain linked to their original inputs.

The profile is an evidence-backed record rather than an unrestricted text biography. Its initial fields are defined below; fields outside the selected pilot category may be omitted.

| Profile area | Initial contents | Evidence treatment |
| --- | --- | --- |
| Identity | Company identifier, display name and authorized organization membership | Access is controlled; identity alone does not prove eligibility |
| Goods and services | Product/service categories, relevant specifications and capabilities | Link each material claim to a document version and source locator |
| Qualifications | Certificates, licences or experience required by the pilot tenders | Record issuer, reference and validity dates when provided; unresolved relevance remains unknown |
| Delivery and warranty | Supported delivery conditions, durations and warranty commitments | Preserve units, calendar/business-day meaning and applicable product scope |
| Evidence inventory | Documents, versions, effective dates and links to supported facts | Missing, expired or ambiguous evidence is visible; profile edits do not rewrite prior runs |

**Illustrative acceptance case:** a synthetic tender requires delivery within 10 calendar days. A company document confirming a minimum of 14 calendar days supports `unmet`; a supported commitment within 10 days supports `met`. An absent or ambiguous commitment supports `unknown`. Every comparison cites its tender condition and available company evidence. This example is a proposed test fixture, not an interview result or legal rule.

## Scope and priorities

The core version must support one approved pilot category, text-based Russian and Kazakh PDF/DOCX documents, organization access, company evidence, cited question answering, atomic requirement extraction, documentary matching, a transparent report, human review, versioned runs, durable processing and controlled model calls. Detailed priorities and acceptance criteria will be maintained in the planned requirements specification at `docs/requirements/requirements.md`.

Legal analysis is bounded. A legal flag requires an identified source edition and a human-validated applicability rule within a limited corpus. If the corpus or applicability is unresolved, the platform reports `legal_unknown` and requests human review. It must not silently convert documentary fit into a legal conclusion.

Optional extensions are local generative inference, a policy-controlled local/hosted combination, LoRA/QLoRA adaptation, OCR, downloadable report export and comparison of tender revisions. They follow the core workflow and receive separate acceptance and evaluation. Under the team's latest scope decision, a locally fine-tuned LLM is desirable rather than a mandatory core deliverable.

Excluded from the core diploma implementation are automatic bid submission, electronic signatures, payments, award-probability predictions, coverage of every procurement category or portal, and an unrestricted legal audit. These exclusions keep the three-person project testable within the diploma schedule.

## Architecture and technology baseline

The proposed request path follows the supervisor's architecture: browser, Caddy reverse proxy, Next.js interface, FastAPI service, a durable worker, PostgreSQL and a private file store. PostgreSQL with pgvector is the planned retrieval store; embedding dimensions and index choices follow the selected model contract.

The analysis pipeline has four stages: ingestion, requirement extraction, compliance analysis, and risk scoring/reporting. Ingestion is a technical stage and need not be an LLM agent. The proposed agents have typed inputs and outputs, bounded tools and explicit completion checks. More agents are not assumed to improve quality; that is an experimental question.

| Area | Proposed baseline | Decision boundary |
| --- | --- | --- |
| UI | Next.js, React and TypeScript; shared components | Each member implements the UI for their own workflow; Ramazan coordinates the shared shell |
| API and orchestration | Python, FastAPI, Pydantic and explicit Python stages | Start with a controlled fixed pipeline; introduce another agent framework only for a demonstrated requirement |
| Persistence | PostgreSQL, psycopg and ordered SQL migrations | Preserve organization context, document versions and consistent evidence references |
| Retrieval | Local multilingual embeddings, PostgreSQL lexical search and pgvector | BGE-M3 and multilingual E5 are candidates; select and tune on development data |
| Parsing | pypdf and python-docx | Text-based files first; unsupported scans receive an explicit outcome |
| Execution | PostgreSQL-backed durable jobs and a separate worker | Queue implementation requires a crash-recovery spike; a particular queue library is not yet approved |
| Model access | Provider adapter and server-enforced Privacy Gateway | Initial hosted inference uses permitted data only; provider, model ID and limits remain to be selected |
| Operations | Docker Compose, Caddy and GitHub Actions | Lock compatible versions during implementation; verify setup, migrations and deployment |

This is an implementation baseline rather than a completed technology benchmark. TG-D04, TG-R04 and TG-T03 must refine model choice, architecture and privacy design respectively. The [literature review](../literature-review/literature-review.md) explains the current scientific rationale and its limitations.

## Privacy and trust boundaries

The server derives organization access from verified membership. Client-supplied identifiers and instructions embedded in documents cannot grant permissions or select a different tenant. Isolation must cover API responses, SQL queries, files, jobs, caches and any placeholder mappings.

Every external AI request, including embedding, evaluation and retry calls, is subject to the same policy boundary. Data classification, permitted destination and context minimization are checked before a request. Masking personal information alone does not establish that commercial information is safe to disclose. Restricted content and derived private outputs remain restricted unless an explicit policy permits their transformation and transfer.

If hosted processing is prohibited and no approved local route exists, the relevant stage is blocked with an actionable explanation. A local failure does not authorize a hosted fallback. Early demonstrations therefore use public documents and permitted synthetic company profiles. Privacy claims are supported by observed tests against defined threats, not by the model's deployment label alone.

## Research questions and evaluation

| Question | Planned comparison | Outcomes and interpretation |
| --- | --- | --- |
| RQ1 Which retrieval configuration best finds supporting tender evidence? | Lexical, dense and combined retrieval on identical document splits | Recall@k and ranking quality, reported separately for RU/KK; tune only on development data |
| RQ2 Does staged analysis improve company-specific findings? | B1 single-prompt RAG versus B2 staged analysis with the same model, permitted inputs and frozen evidence pack | Extraction F1, status macro-F1, citation support, unknown handling, latency and total model use |
| RQ3 Do the controls enforce the intended privacy boundary? | Positive and adversarial requests across two organizations and permitted/blocked routes | Observed unauthorized disclosures, forbidden outbound requests, safe failure and useful permitted processing |
| RQ4 Can users inspect the findings and resolve missing evidence? | A defined task-based walkthrough using the core workflow | Completion, time, citation inspection and recorded difficulties; distinguish user study observations from internal checks |

The separate TG-D01 evaluation protocol must finalize dataset size, annotation rules, numeric targets, hardware and experiment configuration. No TenderGuard quality improvement or user time saving has yet been measured in this proposal. A result showing no benefit from staging is still an admissible research outcome if the comparison and error analysis are sound.

## Responsibilities, stages and dependencies

| Member | Primary implementation responsibility | Contribution to TG-R01 |
| --- | --- | --- |
| Daniyar Kairatov | Parsing, retrieval, embeddings, extraction, annotation and evaluation | Check ML feasibility, language scope and measurable quality criteria |
| Rassul Akhmetov | Backend, database, company evidence, jobs, orchestration and reports | Own the proposal and functional specification; maintain traceability and address review comments |
| Ramazan Talgatov | Project management, authentication, privacy, DevOps and shared UI | Review TG-R01, validate interviews and privacy assumptions, coordinate scope approval |

M0, due 24 October 2026, prepares the eleven predefence components: proposal, relevance evidence, literature, existing-system and technology comparisons, requirements, architecture, UX, evaluation plan, project management and supervisor feedback. A finished platform or completed final experiment is not claimed as an M0 deliverable. The proposal and requirements contribute to components 1 and 6; they do not complete the other components.

Subsequent delivery proceeds through foundation, a first end-to-end workflow, core feature completion, frozen evaluation and final defence preparation. Official dates after M0 require confirmation. TG-R01 depends on TG-T01 user findings and informs TG-R03 comparisons, TG-R04 architecture, TG-T03 privacy requirements and TG-T04 UX. TG-D01 supplies the research evaluation protocol. The [database foundation PR](https://github.com/Tortuev/TenderGuard/pull/1) is implementation work with its own review and acceptance.

## Risks and unresolved decisions

| Risk or open item | Consequence | Resolution and owner |
| --- | --- | --- |
| No validated user findings are included with this proposal | The chosen workflow or category may not match actual needs | Ramazan supplies TG-T01 findings; Rassul links findings to requirements and revises scope |
| Supervisor identity and formal approval are unconfirmed | The submission may contain incorrect metadata or an unapproved scope | Ramazan confirms the supervisor field and records dated feedback |
| Pilot corpus, permissions and language balance are unconfirmed | Dataset access or representative evaluation may be insufficient | Daniyar records provenance and sample counts; choose a smaller permitted pilot rather than claim unsupported coverage |
| RU/KK extraction or evidence matching is weak | A plausible report may contain unsupported findings | Daniyar measures components separately; Rassul preserves unknowns and prevents invalid outputs becoming completed reports |
| Privacy controls or provider policy are incomplete | Restricted content may be disclosed | Ramazan blocks prohibited routes and completes isolation/egress tests before private use |
| Agents, OCR or training exceed the available time or hardware | Optional work displaces the core system | All members prioritize the core workflow; decide extensions only after a runnable baseline and resource check |
