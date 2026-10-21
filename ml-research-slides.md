# TenderGuard: Research Slides and Speaker Notes

This contribution supports the shared first-predefence presentation. The six editable slides cover the research basis, four research questions, an annotated example, baseline comparison, evaluation measures and limitations. They follow the proposal and the prepared TG-D01 to TG-D04 documents.

[Open the editable research slides](TenderGuard_M0_Research.pptx)

## Integration into the shared presentation

Use these slides in the corresponding literature, research and evaluation sections of the team's presentation. Preserve the source paths and speaker notes when copying slides. If the shared deck already covers one topic, integrate the relevant material into that slide rather than repeating it. The complete team presentation still needs the other predefence components.

The suggested speaking time is about four to five minutes for this contribution, subject to the team's confirmed presentation format. Each slide includes its evidence path. The PowerPoint contains the same speaker notes as the sections below.

## Baseline terminology

B0 names the PostgreSQL lexical retrieval baseline already described in RQ1. This naming connects the TG-D05 task card with the existing protocol. It adds no generation call and does not introduce an additional status-classification experiment.

| Variant | Function | Appropriate comparison |
| --- | --- | --- |
| B0 | PostgreSQL lexical retrieval returning ranked passages | Retrieval recall, complete-evidence success and ranking quality against the dense alternatives |
| B1 | Shared deterministic ingestion/retrieval followed by exactly one generation call | Primary company-assessment comparator |
| B2 | The same original evidence with typed extraction, assessment and reporting stages | Primary staged candidate against B1 |

Status macro-F1 and supported finding coverage do not apply to B0, because it produces no company-fit findings. Do not enter zero for these inapplicable measures. B1 and B2 share the retrieval configuration selected on development data. This is distinct from the RQ1 retrieval experiment comparing lexical search, BGE-M3 and E5.

## Slide 1: Research basis

### On-slide content

| Study | Research concern | TenderGuard response |
| --- | --- | --- |
| BGE-M3 Chen et al., 2024 | Multilingual evidence retrieval | Compare lexical search, BGE-M3 and E5 on common chunks |
| Self-RAG Asai et al., 2024 | Whether evidence supports a generated claim | Add support checks and measure false passes |
| ALCE Gao et al., 2023 | Citation support and completeness | Check both source locations and support for each finding |
| Lost in the Middle Liu et al., 2024 | Sensitivity to evidence position | Test position on development data, then freeze ordering |

### Speaker notes

These four papers contribute to the shared literature review. BGE-M3 motivates a multilingual retrieval comparison. Self-RAG motivates explicit evidence-support checks, although our pipeline does not reproduce its training procedure. ALCE separates citation support from a citation simply existing. Lost in the Middle motivates a development test of evidence position. These studies use other tasks and datasets. Their results do not establish TenderGuard accuracy on Russian or Kazakh tenders.

### Evidence

- [docs/literature-review/literature-review.md](https://github.com/Tortuev/TenderGuard/blob/main/docs/literature-review/literature-review.md)
- [Primary paper: https://aclanthology.org/2024.findings-acl.137/](https://aclanthology.org/2024.findings-acl.137/)
- [Primary paper: https://proceedings.iclr.cc/paper_files/paper/2024/hash/25f7be9694d7b32d5cc670927b8091e1-Abstract-Conference.html](https://proceedings.iclr.cc/paper_files/paper/2024/hash/25f7be9694d7b32d5cc670927b8091e1-Abstract-Conference.html)
- [Primary paper: https://aclanthology.org/2023.emnlp-main.398/](https://aclanthology.org/2023.emnlp-main.398/)
- [Primary paper: https://aclanthology.org/2024.tacl-1.9/](https://aclanthology.org/2024.tacl-1.9/)

## Slide 2: Research questions

### On-slide content

| Question | What we ask | What we observe |
| --- | --- | --- |
| RQ1 | Which retrieval method finds the evidence needed for assessment? | Evidence recall and complete evidence sets |
| RQ2 | Does staged analysis improve supported company-specific findings? | Status quality, citations and resource use |
| RQ3 | Do controls enforce organization and processing boundaries? | Blocked violations and useful authorized processing |
| RQ4 | Can users inspect findings and resolve missing information? | Task completion and correct interpretation |

### Speaker notes

The main ML questions concern finding evidence and assessing the company against it. RQ1 compares the retrieval configurations. RQ2 compares one generation call with explicit extraction, assessment and reporting stages. RQ3 covers the project privacy boundary and requires work from Ramazan and Rassul as well as ML tests. RQ4 checks whether users understand the report and its evidence. We report language slices separately. Documentary fit supports a human decision and does not establish legal eligibility.

### Evidence

- [docs/evaluation-plan/evaluation-plan.md](https://github.com/Tortuev/TenderGuard/blob/main/docs/evaluation-plan/evaluation-plan.md)
- [docs/project-proposal/proposal.md](https://github.com/Tortuev/TenderGuard/blob/main/docs/project-proposal/proposal.md)

## Slide 3: Annotated example: warranty evidence

### On-slide content

| Company source | Quoted commitment | If confirmed applicable |
| --- | --- | --- |
| SYN-C03-A-v1 | “exactly 12 months from acceptance” | unmet |
| SYN-C03-B-v1 | “exactly 36 months from acceptance” | met |

Tender condition: full hardware warranty of at least 24 months from acceptance. The expected reference status is **unknown**, because the package does not establish which offer applies. The example is synthetic. Missing evidence also gives unknown. A policy block remains a processing outcome.

### Speaker notes

This example is synthetic and has an authored expected label. The tender requires at least 24 months from acceptance. Offer A promises exactly 12 months and offer B promises exactly 36 months. We cannot choose the better-looking offer without knowing which one applies. The correct reference label is unknown, with the tender citation and both company citations retained. If an authorized confirmation establishes offer A, the new assessment is unmet. If it establishes offer B, the new assessment is met. A missing warranty statement also gives unknown, but for a different reason. A timeout or policy block does not describe the company and stays a separate processing outcome.

### Evidence

- [docs/dataset/dataset-and-annotation.md#83-syn-03-unresolved-warranty-commitments](https://github.com/Tortuev/TenderGuard/blob/main/docs/dataset/dataset-and-annotation.md#83-syn-03-unresolved-warranty-commitments)
- [docs/dataset/dataset-and-annotation.md#86-resolving-an-unknown-without-discarding-evidence](https://github.com/Tortuev/TenderGuard/blob/main/docs/dataset/dataset-and-annotation.md#86-resolving-an-unknown-without-discarding-evidence)

## Slide 4: Baseline comparison

### On-slide content

| Variant | Method | Output | Comparison role |
| --- | --- | --- | --- |
| B0 | PostgreSQL lexical retrieval | Ranked source passages | Retrieval reference |
| B1 | Shared retrieval, then one generation call | Requirements, statuses and citations | Primary comparator |
| B2 | Same original evidence, then typed extraction, assessment and reporting | Same final schema with intermediate records | Primary candidate |

B1 and B2 share the generator snapshot, original evidence and validation rules. Count every stage, failure, retry and token in the resource record.

### Speaker notes

Here B0 names the PostgreSQL lexical retrieval baseline already included in RQ1. It returns passages, so status macro-F1 does not apply to B0. Compare its retrieval results with BGE-M3 and E5 under the same corpus and queries. The primary analysis experiment compares B1 and B2. They use the same selected retrieval configuration, generator snapshot, profile version and fixed original evidence pack. We freeze its ordering and hash. B1 has exactly one generation call and no hidden model repair. B2 adds stages and generated state. Fairness means equivalent original evidence and rules, not identical compute. We record the complete overhead. Adaptive retrieval and segmented multi-call baselines receive separate labels.

### Evidence

- [docs/evaluation-plan/evaluation-plan.md#41-retrieval-comparison](https://github.com/Tortuev/TenderGuard/blob/main/docs/evaluation-plan/evaluation-plan.md#41-retrieval-comparison)
- [docs/evaluation-plan/evaluation-plan.md#42-single-prompt-and-staged-analysis](https://github.com/Tortuev/TenderGuard/blob/main/docs/evaluation-plan/evaluation-plan.md#42-single-prompt-and-staged-analysis)
- [docs/technology-comparison/ml-technologies.md#5-adr-ml-03-typed-stages-and-the-single-prompt-baseline](https://github.com/Tortuev/TenderGuard/blob/main/docs/technology-comparison/ml-technologies.md#5-adr-ml-03-typed-stages-and-the-single-prompt-baseline)

## Slide 5: Evaluation measures and conditions

### On-slide content

| Measure | Target | Scoring unit |
| --- | --- | --- |
| Complete-evidence success@5 | At least 0.85 | Answerable queries with a complete acceptable evidence set |
| Status macro-F1 | At least 0.80 | Equal-weight F1 across met, unmet and unknown on reference requirements |
| Supported gold coverage | At least 0.80 | All gold obligations, crediting correct findings with adequate support |

The targets are provisional planning values. Also report false passes, processing failures, latency and total model cost. Keep document families in one partition and report RU/KK results separately.

### Speaker notes

These are provisional engineering targets, not measured results. Complete-evidence success requires at least one full acceptable evidence set among the first five passages. Macro-F1 gives each of the three status classes equal weight in the gold-requirement assessment. Supported gold coverage uses every reference obligation, so missing requirements cannot improve the score. Invalid or missing predictions remain failures and receive no credit. We also report per-class and language results, false passes and total resource use. The collection plan targets 30 independent tender families, split into 18 development and 12 test families, with a six-family development pilot. These counts are planned. Family grouping prevents related documents crossing partitions. We freeze configurations and run paired B1/B2 comparisons with three repetitions, without treating repeats as new independent packages.

### Evidence

- [docs/evaluation-plan/evaluation-plan.md#5-quality-measures](https://github.com/Tortuev/TenderGuard/blob/main/docs/evaluation-plan/evaluation-plan.md#5-quality-measures)
- [docs/evaluation-plan/evaluation-plan.md#8-measurement-conditions-and-analysis](https://github.com/Tortuev/TenderGuard/blob/main/docs/evaluation-plan/evaluation-plan.md#8-measurement-conditions-and-analysis)
- [docs/evaluation-plan/evaluation-plan.md#9-success-criteria-and-interpretation](https://github.com/Tortuev/TenderGuard/blob/main/docs/evaluation-plan/evaluation-plan.md#9-success-criteria-and-interpretation)
- [docs/dataset/dataset-and-annotation.md](https://github.com/Tortuev/TenderGuard/blob/main/docs/dataset/dataset-and-annotation.md)

## Slide 6: Limitations and optional fine-tuning

### On-slide content

Core evaluation

Pretrained models, evidence retrieval, validated outputs, separate RU/KK results

Fine-tuning after a permitted dataset, error analysis and resource check

Small samples and documentary/legal boundaries

### Speaker notes

Fine-tuning is optional because the core question can be tested with pretrained models, retrieval and controlled prompts. We first need a permitted corpus and an error analysis showing what adaptation should improve. Training would also require independent held-out data, hardware and time. A model can memorize published synthetic examples, so they cannot establish unseen-test improvement. Local generation and OCR also remain extensions. Our current contribution is the research and design package. Final model measurements follow implementation. Small samples, synthetic company profiles and limited Kazakh coverage restrict generalization. A negative result for staging remains valid if the comparison is fair and the evidence is retained.

### Evidence

- [docs/technology-comparison/ml-technologies.md#5-adr-ml-03-typed-stages-and-the-single-prompt-baseline](https://github.com/Tortuev/TenderGuard/blob/main/docs/technology-comparison/ml-technologies.md#5-adr-ml-03-typed-stages-and-the-single-prompt-baseline)
- [docs/evaluation-plan/evaluation-plan.md#9-success-criteria-and-interpretation](https://github.com/Tortuev/TenderGuard/blob/main/docs/evaluation-plan/evaluation-plan.md#9-success-criteria-and-interpretation)
- [docs/project-proposal/proposal.md#scope-and-priorities](https://github.com/Tortuev/TenderGuard/blob/main/docs/project-proposal/proposal.md#scope-and-priorities)

## Team explanation guide

Every member should be able to explain the following points without reading the slide.

**Why compare B0 with retrieval methods rather than status scores?** B0 returns evidence passages. Its relevant outcomes concern whether the needed evidence appears among its results. B1 and B2 add company assessment, so they receive extraction, status and citation measures. Combining these into one undifferentiated score would compare different tasks.

**What makes B1/B2 fair?** Both use the same generator snapshot, selected document/profile versions, retrieval configuration, original evidence pack, ordering and validation rules. B2 may produce more intermediate text and make more calls. Count that overhead. Keep adaptive retrieval and segmented multi-call baselines separate. B1 must not contain hidden model extraction or repair calls.

**When is unknown correct?** Use unknown when selected evidence is absent, ambiguous, incomparable or conflicting without a resolution rule. Missing evidence does not establish a violation. In SYN-03, selecting either warranty offer would require an unsupported assumption. Retain both citations and request confirmation of the applicable offer.

**How does unknown differ from blocked or failed?** Unknown describes what the available evidence establishes about one company requirement. A block, timeout or invalid output describes processing. Preserve those outcomes separately and retain failed attempts in the evaluation record.

**Why is fine-tuning optional?** The core workflow can be tested with pretrained models and retrieval. Adaptation needs a permitted training set, a measured error pattern, a comparison with the base model and a feasible resource budget. It cannot resolve a genuinely missing document or decide which conflicting offer is authoritative. Published synthetic cases are diagnostics and cannot establish unseen-test improvement.

**What can we claim at M0?** The team can present the documented method, annotated synthetic examples and planned measurements. Provisional targets and sample counts remain planning values. Measured quality, time saving, training gains and completed privacy controls require their own execution evidence.

## Review and rehearsal evidence

Rassul reviews the slide content against the proposal and protocol. Record actual comments and resulting changes in the PR. Keep B0's retrieval-only meaning visible when integrating the material into the shared deck.

Before closing TG-D05, each member explains baseline fairness, unknown outcomes and optional fine-tuning. Record the actual rehearsal date, participants, questions and corrections after that session. Link the final shared-deck version and review evidence in the task. Preparing this module alone does not establish that the team rehearsal or shared-deck integration has occurred.
