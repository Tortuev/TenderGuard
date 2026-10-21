# TenderGuard — Research Questions and Evaluation Protocol

**Task:** TG-D01 — Define research questions and the evaluation protocol  
**Owner:** Daniyar Kairatov — ML and retrieval  
**Reviewer:** Rassul Akhmetov — review pending  
**Milestone:** M0 — First predefense, 24 October 2026  
**Version:** 1.0, prepared for review on 21 October 2026

This document defines planned evaluation. It contains no measured TenderGuard model results, user-study observations or approval claims.

## Purpose and project alignment

TenderGuard is a proposed platform for SMEs that compares tender requirements with company documents and returns source-linked documentary findings. This protocol operationalizes the proposal's four research questions and the target workflow: ingestion, requirement extraction, compliance analysis, and risk scoring/reporting. Ingestion is technical processing and need not be an LLM agent.

The literature review under TG-D02 motivates the method; TG-D03 develops the corpus and annotation rules; TG-D04 documents the technology comparison. This protocol specifies experiments and scoring conditions. It does not assert implementation of parsing, retrieval, model invocation or privacy enforcement.

## Research-question overview

| ID | Research question | Experiment and comparator | Data source | Main outcomes | Owner and coordination |
| --- | --- | --- | --- | --- | --- |
| RQ1 | Which retrieval configuration best finds supporting evidence? | Lexical baseline versus BGE-M3 dense versus multilingual E5-base; combined retrieval as a separately tuned variant | Authorized tender/company packages with adjudicated passage relevance | Recall@5/@10, complete-evidence success@5/@10, nDCG@10, latency | Daniyar; Rassul reviews |
| RQ2 | Does staged analysis improve supported company-specific findings? | Paired B1 versus B2-fixed; gold-requirement classification and end-to-end analysis scored separately | Held-out requirements, company evidence, labels and source locators | Status macro-F1, extraction/joint F1, citation support, false passes, cost | Daniyar; Rassul coordinates contracts |
| RQ3 | Do controls enforce the intended processing boundary? | Authorized and adversarial requests across two synthetic organizations; allowed versus blocked routes | Synthetic canaries, policy decisions and access/request logs | Unauthorized disclosures, prohibited transmissions, useful authorized processing | Daniyar defines ML-boundary cases; Ramazan/Rassul coordinate subsystem checks |
| RQ4 | Can users inspect findings and identify the next action? | Defined task-based walkthrough against a frozen success rubric | Permitted demonstration packages and actual consenting participants | Task completion, time, citation inspection, correct label interpretation | Daniyar supplies the ML rubric; Ramazan coordinates UX/user evidence, subject to team agreement |

RQ3 and RQ4 are project-level interfaces; this protocol does not transfer platform, security or participant-recruitment responsibilities to the ML owner. Numeric/calendar robustness, contradictions and missing evidence are RQ2 evaluation slices, consistent with the ML literature review.

## Units and documentary labels

A **package** is a selected, versioned tender-document set paired with a selected company-evidence/profile version. A **document family** groups originals, amendments, duplicates, translations and derived variants that must stay in the same data partition. An **atomic requirement** expresses one assessable obligation. A **gold label** is a human-adjudicated reference judgment established independently of system predictions.

| Label | Decision rule | Evidence requirement |
| --- | --- | --- |
| `met` | Applicable company evidence establishes satisfaction of the complete atomic condition | Cite the tender obligation and company evidence |
| `unmet` | Applicable evidence establishes a violation of the atomic condition | Cite the tender obligation and conflicting company commitment/capability |
| `unknown` | Evidence is missing, ambiguous, incomparable or materially conflicting without a resolution rule | Cite the tender and available relevant sources; identify the unresolved field or conflict |

Missing company evidence alone cannot establish `unmet`. Policy blocking, parser errors, invalid output and timeouts are processing outcomes, not company-fit labels. Documentary fit does not establish legal eligibility.

## B1 and B2: a fair primary comparison

**B1:** shared deterministic ingestion/retrieval followed by exactly one generation call producing atomic requirements, company-fit statuses, citations and a report in the agreed schema. No hidden generative planning, extraction or repair call forms part of B1. Shared deterministic validation may reject malformed output.

**B2-fixed:** the same permitted evidence pack, with typed generation stages for requirement extraction, compliance assessment and reporting. Each later stage receives only authorized original evidence and its preceding typed output. It cannot introduce new documents or external knowledge as company evidence. Deterministic validation is the same as B1. Each generated risk category requires an agreed rubric and evidence; no unexplained risk score is a primary quality endpoint.

The evidence pack is selected deterministically from the same organization-scoped, versioned tender/company pool. Before final runs, specify its query templates, retrieval settings, ordering and token limits. Queries must not come from gold test requirements or a hidden LLM. Freeze the serialized pack and hash, and confirm every scheduled chunk is accessible within each system's actual input limits. Oversized packages need a predefined segmentation/exclusion rule applied equally and reported with counts. Segmentation creates a separately labelled multi-call workflow rather than quietly changing the one-call B1 definition.

Use the same pinned generative model, shared embedding/retrieval configuration, input document/profile versions, output rubric and policy. B2 may have more calls and tokens; record the overhead and impose a declared total ceiling. Extra calls are not free. The primary comparison holds evidence fixed, not total compute.

**B2-adaptive**, if evaluated later, may retrieve new evidence per requirement from the same permitted pool. Report it as a separate end-to-end configuration. Its gains can reflect retrieval changes and cannot isolate staging. A separate gold-requirement assessment compares classification with identical evidence to distinguish extraction from assessment errors.

## RQ1 — Retrieval configuration and language

**Question:** Which retrieval configuration best finds supporting tender/company evidence?

**Experiment/comparators:** compare PostgreSQL lexical full-text search, BGE-M3 dense and multilingual E5-base dense on identical gold queries, chunks and corpus versions. BM25 is an optional separately implemented lexical comparator, not a claim about the existing PostgreSQL code. Evaluate lexical+dense fusion only with documented ranks, fusion rule and development tuning. Check both tokenizers for truncation on common chunks.

**Data:** authorized natural packages with adjudicated relevance/evidence sets, grouped by document family. Separate Russian and Kazakh query/document slices and cross-language cases. Report language pairs rather than assuming a single document language describes every query.

**Metrics:** passage recall@5/@10 over annotated relevant passages; complete-evidence success@5/@10 over queries with an answerable gold evidence set; ranking quality nDCG@10 where graded relevance labels exist; latency and index footprint. Success means at least one complete acceptable set, not merely one plausible passage. Queries lacking sufficient evidence are a separate unanswerable group and are excluded from answerable recall denominators with explicit counts.

**Privacy gate:** filter by organization/membership and selected document versions before retrieval. An unauthorized result is a security failure, regardless of its relevance.

**Owner:** Daniyar. Rassul reviews. **Limit:** incomplete relevance labels and small language samples constrain conclusions; multilingual benchmark coverage does not demonstrate Kazakh tender performance.

## RQ2 — Staging, company fit and evidence

**Question:** Does B2-fixed improve supported company-specific findings relative to B1?

**Experiment/comparators:** paired B1/B2-fixed runs on the held-out packages above. Separately run gold-requirement classification with the same evidence bundle. Preserve source quotations, intermediate outputs, errors and original predictions before human correction.

**Data:** tender obligations, company evidence, three-way labels and source locators from independent annotation and adjudication. Synthetic fixtures test boundary behavior but do not replace the natural test set.

**Primary outcome:** macro-F1 on met/unmet/unknown in gold-requirement assessment. Report per-class precision/recall/F1 and a confusion matrix. Treat missing/invalid predictions as a fourth prediction-only `processing_failure` outcome: they create a false negative for the gold class and receive no credit. Their columns remain visible in the confusion matrix; the macro average covers the three gold classes. If a gold class is absent, report fixed-label zero-division handling and also available-class scores, with the limitation explicit.

**Extraction:** match atomic predicted and gold requirements one-to-one by obligation, scope, operator, threshold, unit and deadline. A materially changed numeric/calendar constraint fails the match. Duplicate predictions are false positives, unmatched gold items false negatives. Anonymize system identity for disputed matching. Micro precision/recall/F1 are TP/(TP+FP), TP/(TP+FN) and 2PR/(P+R). Proposed scoring convention: return 0 when a scored precision/recall/F1 denominator is zero and report the underlying counts. Mark entirely inapplicable retrieval/citation subsets as N/A with counts instead of treating them as perfect. Review and freeze these conventions before final scoring.

**End-to-end quality:** joint requirement-and-status precision/recall/F1 uses a true positive only when extraction matches and status is correct. A wrong status contributes both a false positive and a false negative. Missed requirements and spurious findings remain in the denominator. Report false passes (gold unmet/unknown predicted met) and unknown recall alongside aggregate scores.

**Citations:** separately score locator validity, individual citation relevance/support, and complete support of an atomic finding by its cited set. Tender references establish the obligation and company references establish capability. Finding support coverage uses all evidence-dependent generated findings as the denominator, while gold-item supported coverage uses all gold obligations and gives credit only to a correctly extracted/classified finding with adequate support. Report both, so omission and verbosity cannot inflate a single score. Missing evidence cannot support unmet. For unknown, the rationale identifies a missing field or contradiction within the selected evidence scope rather than claiming universal absence.

**Efficiency:** total time, calls, retries, tokens, errors and cost per attempted/successful package. Reporting has no authority to override a failed semantic validation or change unsupported conclusions into successful reports.

**Privacy gate:** equivalent approved original information for both variants, including intermediate state, judge calls and retries. Blocked policy runs are processing outcomes, not unknown company-fit labels.

**Owner:** Daniyar, with Rassul coordinating run/output contracts. **Limit:** documentary fit is not legal eligibility. Staging may underperform, and a JSON-valid answer can still be false. A negative result is admissible.

## RQ3 — Privacy and isolation checks

**Question:** Do the controls enforce the defined processing boundary?

**Experiment/comparators:** positive authorized requests and negative fixtures across two synthetic organizations. Cover direct API access, SQL reads, files, jobs, caches, source-link resolution, document prompt injection, outgoing calls and derived intermediate outputs. Compare policy-allowed and policy-denied routes, not private hosted runs that violate policy. A policy decision cannot be delegated to document text or to an agent.

**Data:** synthetic documents/canaries and permitted test metadata. Real confidential data must not be used to test an unproven boundary.

**Metrics:** attempted unauthorized accesses versus observed disclosures; prohibited calls versus actual transmitted requests; allowed processing successes/failures; correct blocking and actionable error messages. Inspect requests and access logs within an approved environment. A canary test detects defined violations, not every form of leakage. PII masking alone is insufficient.

**Privacy gate:** no permitted route means block without hosted fallback. Runtime authorization, RLS, Gateway and egress controls must exist before these checks can pass; database foreign keys alone do not establish read isolation.

**Owner:** Daniyar owns ML-boundary test definitions and reporting here. Ramazan's platform/privacy area must confirm and execute its subsystem controls with Rassul. This is dependency coordination, not a claim of completed work or reassignment.

**Limit:** zero observed violations is a finite-test result, not proof of absolute privacy. These checks are not a legal-compliance certification.

## RQ4 — Inspection and resolving missing evidence

**Question:** Can users inspect findings and understand the next action?

**Experiment/comparator:** a defined workflow with report, requirement citation, company citation and an unknown case. Compare completion against a task success rubric; a manual-workflow comparison requires a separately agreed design. An internal rehearsal is labelled as such and is not a user study.

**Data:** permitted public/synthetic package and actual consenting participants recruited through TG-T01/TG-T04. No respondents or timings are asserted by this document.

**Metrics:** completed tasks/attempts, time, citation-opening success, correct interpretation of met/unmet/unknown and recorded difficulties. Freeze success criteria before observing participants. Do not infer customer demand from an internal walkthrough.

**Privacy gate:** approved participant context, minimal personal data and controlled recordings. **Owner:** Daniyar supplies the ML interpretation rubric; Ramazan's UX/user-evidence area coordinates participants, with team confirmation pending. **Limit:** convenience samples and learning effects restrict generalization; no baseline time-saving claim without a suitable comparator.

## Dataset freeze and annotation

TG-D03 will specify provenance, grouping, annotation and synthetic cases; the rules below are the minimum required by this protocol. Begin with a development-only feasibility pilot. Confirm natural package counts and language/class balance after permission and annotation assessment. No sample count has been achieved. Final sample sizes, provider, hardware and spend cap are open decisions, not hidden commitments.

Independent annotators label a shared pilot without system predictions. Record pre-adjudication agreement, label counts and Cohen's kappa where suitable. Resolve disagreements using a documented rule or qualified domain review. Keep unresolved legal labels out of documentary ground truth. Split related tenders, amendments, duplicates, derived translations and company variants as groups before tuning. Hash/freeze the test manifest; rebuild after contamination rather than tuning to the contaminated test.

## Provisional targets and interpretation

Planning targets proposed for review: macro-F1 ≥0.80, complete-evidence success@5 ≥0.85 and gold-item supported coverage ≥0.80. These numbers are provisional design targets, not measured results, task-card thresholds or promises to the committee. Confirm/revise them with development evidence and the supervisor before final-test freeze. Do not choose thresholds after viewing test outcomes. B2 has no assumed improvement margin.

No unauthorized external transfer is permitted. That policy invariant is not a negotiable statistical target.

Freeze model/tokenizer revisions, prompts, pack ordering/hash, splitter and retrieval configuration, scoring rules/code revision, dataset manifests, temperature/seed where supported, retry ceiling and price snapshot. Log every call; provider nondeterminism can persist even at temperature zero. Treat repeat executions as repeats, not new independent packages. Use package/family-level paired resampling for uncertainty when sample size permits; disclose unstable intervals. Report median latency and p95 only with sample size and computation method. Preserve failures and exclusions.

## Run record and completion evidence

Proposed run record: code revision, dataset/split hash, organization-scoped package IDs, input/profile versions, evidence-pack hash, model/prompt/retrieval configuration, route decision, predictions, locators, validation errors, elapsed time, tokens, retries, unit-price snapshot and total cost. Store private text in controlled storage. Do not publish model reasoning traces as a requirement; retain sufficient structured decisions and tool/evidence outcomes for audit.

Store the run record in a versioned evaluation export and controlled application storage as appropriate. Map its fields to the reviewed backend/API schema before implementation; this protocol does not establish that every required field or control already exists.

## Planned execution sequence

1. Complete TG-D03's provenance/annotation guide and run a development-only feasibility pilot. Confirm permission, language coverage and annotator capacity.
2. Group document families, assign partitions and adjudicate labels independently of model predictions. Record all exclusions and unresolved cases.
3. Compare RQ1 configurations on development data. Select settings without consulting held-out test outcomes.
4. Freeze the test manifest and the configuration checklist below. Verify equivalent evidence availability and policy permissions for B1 and B2.
5. Run paired B1/B2-fixed comparisons and the separate gold-requirement assessment. Retain original outputs, failed attempts and costs. Use a declared repeat count and alternate/randomize run order where provider/load effects matter.
6. Evaluate privacy fixtures with the responsible subsystem owners. Run a separate user walkthrough only with an agreed task rubric and actual participants.
7. Publish aggregate results, denominators, uncertainty, exclusions and error categories. Retain private evidence in controlled storage. Compare findings with the provisional targets without changing targets after seeing the test.

## Configuration decisions to freeze before final evaluation

| Decision | Required record | M0 status |
| --- | --- | --- |
| Corpus and sample size | Package/family counts by partition, language pair and status; inclusion/exclusion rules | Pending feasibility pilot and permissions; no achieved sample count claimed |
| Ground truth | Annotation-guide version, annotators, adjudication and pre-adjudication agreement | Planned under TG-D03; execution pending |
| Retrieval | Lexical configuration, embedding/tokenizer revisions, chunking, k, fusion rule if used | Candidates defined; development selection pending |
| Generator | Exact model/provider revision, context limits and approved processing route | Pending TG-D04 and policy review |
| Prompts and outputs | Prompt/schema versions, evidence-pack hashes and deterministic validation rules | Must be pinned before final runs |
| Resources | Hardware/runtime versions, timeout, call/token/retry ceilings, budget and price snapshot | Pending feasibility measurement and team agreement |
| Repeats and scoring | Repeat count, run order, scorer revision, matching rules and zero-denominator conventions | Must be frozen before final runs |
| User walkthrough | Participant recruitment, consent/context, task rubric and success criteria | Team coordination pending; no observations claimed |

Pending choices are explicitly tracked. They do not permit unrestricted experiment changes: resolve them using development evidence and record a protocol revision before final-test access. If corpus permissions or Kazakh coverage remain insufficient, narrow the evaluation claim and report the limitation.

## TG-D01 acceptance and review record

| Task-card criterion | Evidence in this protocol |
| --- | --- |
| Each research question has an experiment, comparator, data source, metric and owner | Overview table and RQ1–RQ4 sections |
| Each question specifies a privacy gate and interpretation limit | Privacy-gate and limitation paragraphs within RQ1–RQ4 |
| Numeric targets are explicitly provisional | Provisional targets and interpretation section |
| Baseline and staged comparisons use equivalent permitted inputs | B1/B2-fixed definitions, frozen-pack rules and run records |

**Document verification:** all four research questions have the required planning fields; B1/B2 inputs and differences are specified; language slices, missing/invalid outputs, leakage, privacy and interpretation limits are covered. These are document checks, not executed model or security tests.

**Outstanding review:** Rassul Akhmetov's review date, substantive comments, requested corrections and acceptance are pending. Confirm the cross-team RQ3/RQ4 interfaces with Ramazan and Rassul. Keep task status at the appropriate in-progress/review state until the actual task-card acceptance and review requirements are met.

M0 deliverable: this evaluation protocol v1. Final corpus collection, model training, completed security tests and final model experiments are later work; this document must not be presented as their execution evidence.
      
