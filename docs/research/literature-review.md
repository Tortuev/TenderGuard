# TenderGuard literature review

TenderGuard uses evidence from tender documents and company records to assess requirements and explain compliance risks for SMEs. This review supports a controlled, testable analysis workflow: retrieve evidence, extract requirements, compare them with company evidence, and report supported findings with explicit uncertainty. The value of separating these stages must be measured against a simpler RAG baseline.

Project team: Daniyar Kairatov, Rassul Akhmetov and Ramazan Talgatov. Prepared: 21 October 2026. Peer review: pending.

## Scope and source selection

The four sources address tool-using agents, coordination failures, legal reasoning and evaluation of grounded answers. Selection is thematic rather than a systematic search of all research. The published editions date from 2023–2025 and fall within the rubric's recent-source window.

Publication status is supported by the conference header in the ReAct paper and the publisher records for MAST, LegalBench and RAGAs. The source locations below identify the methods and results used in each discussion. The records retain the shared review's identifiers L07, L14, L08 and L04 so they can be integrated without counting the same publication twice.

| Record | Publication | Research focus | TenderGuard design question |
| --- | --- | --- | --- |
| L07 | ReAct, ICLR 2023 | Tool use during reasoning | Which actions should an analysis stage be allowed to perform? |
| L14 | MAST, NeurIPS 2025 | Multi-agent failure analysis | How should handoffs, completion and verification be checked? |
| L08 | LegalBench, NeurIPS 2023 | Evaluation of legal reasoning | How should documentary fit and legal applicability be separated? |
| L04 | RAGAs, EACL 2024 | Automated RAG evaluation | Which quality checks need human reference judgments? |

This review currently contains four scientific publications. Component 3 requires at least 12 meaningfully used sources, including at least 8 scientific publications; further literature can be integrated into this same document. Applicable legislation belongs in a separate regulatory review; a legal-reasoning benchmark is not a normative legal source.

## ReAct and controlled tool use

**L07. Yao et al. (2023), ReAct: Synergizing Reasoning and Acting in Language Models. ICLR 2023.** [Paper, conference edition v3](https://arxiv.org/pdf/2210.03629v3). Evidence: Sections 2–4; Table 1, printed page 5; error analysis in Table 2, page 6.

**Method and evaluation.** ReAct alternates model-generated reasoning, actions and external observations. Experiments cover HotpotQA, FEVER, ALFWorld and WebShop. Table 1 uses PaLM-540B and compares standard, reasoning-only, action-only and combined prompting. ReAct obtains 27.4% exact match on HotpotQA against 29.4% for chain-of-thought, while FEVER accuracy is 60.9% against 56.3%. The mixed outcome matters: access to tools does not produce a universal quality improvement. The error analysis identifies unhelpful search and repetitive reasoning among remaining problems.

**Transfer limitation.** These tasks do not establish performance on Russian/Kazakh tenders, legal applicability or multi-agent coordination. ReAct itself is not evidence that four specialized agents outperform one prompt.

**Proposed decision.** Give stages a bounded set of read-only evidence tools; keep organization context and permissions server-controlled. Record tool outcomes and source references. Compare B1 and B2 under the controlled conditions below. Related tasks: TG-R13 and TG-R19.

## MAST and verification of agent handoffs

**L14. Cemri et al. (2025), Why Do Multi-Agent LLM Systems Fail? NeurIPS 2025, Datasets and Benchmarks Track.** [Publisher record](https://papers.nips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html). [Published paper](https://papers.nips.cc/paper_files/paper/2025/file/b1041e52d3be19f0a9bc491657488e4a-Paper-Datasets_and_Benchmarks_Track.pdf). Evidence: Section 3 and Table 1, pages 2–6; Sections 4–5, pages 7–9.

**Method and evaluation.** The conference edition presents 1,642 execution traces from seven frameworks. Grounded-theory analysis develops 14 failure modes grouped into system design, inter-agent misalignment and task verification. Human annotation is used to refine definitions; an LLM annotator supports scaling. The reported human-agreement coefficient of 0.88 belongs to an iterative annotation study, not all traces. Intervention studies show that workflow changes can improve particular systems while leaving failures unresolved.

**Transfer limitation.** Coding, mathematics and general-agent traces do not estimate procurement failure rates. Automated annotation and the selected systems constrain interpretation. The taxonomy is not claimed to be exhaustive.

**Proposed decision.** Validate handoff fields and evidence references, use explicit completion conditions, and inspect semantic errors even when JSON validates. Classify lost evidence, contradictory outputs and premature completion during error analysis. Related tasks: TG-R13, TG-D15 and TG-R21. This published edition supersedes the earlier draft's preprint classification.

## LegalBench and the boundary of compliance claims

**L08. Guha et al. (2023), LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models. NeurIPS 2023, Datasets and Benchmarks Track.** [Publisher record](https://proceedings.nips.cc/paper_files/paper/2023/hash/89e44582fd28ddfea1ea4dcb0ebbf4b0-Abstract-Datasets_and_Benchmarks.html). [Published paper](https://proceedings.nips.cc/paper_files/paper/2023/file/89e44582fd28ddfea1ea4dcb0ebbf4b0-Paper-Datasets_and_Benchmarks.pdf). Evidence: Sections 3–5; limitations in Section 4.1, printed pages 7–8; evaluation and Tables 2–3, pages 8–9.

**Method and evaluation.** LegalBench evaluates 20 models across 162 tasks organized around six reasoning categories. Legal professionals contribute tasks and grading guidance. Evaluation uses measures appropriate to the task, including balanced accuracy for classification, F1 for selected tasks and manual grading of rule application. Model performance varies across categories; correct conclusions and adequate legal analysis are evaluated separately.

**Transfer limitation.** The initial benchmark is English-only, skewed toward American law and contracts, and limited in long-document coverage. Its scores cannot establish Kazakhstan procurement compliance or expert agreement on ambiguous cases.

**Proposed decision.** Evaluate requirement extraction, company-evidence matching and legal applicability separately. A legal flag needs an identified rule version and validated applicability; unresolved applicability remains `legal_unknown`. Report documentary findings as `met`, `unmet` or `unknown`, with evidence from both sides. Related tasks: TG-R14, TG-R15 and TG-R20.

## RAGAs and calibration of automatic evaluation

**L04. Es, James, Espinosa Anke and Schockaert (2024), RAGAs: Automated Evaluation of Retrieval Augmented Generation. EACL System Demonstrations, pages 150–158.** [Publisher record and DOI](https://aclanthology.org/2024.eacl-demo.16/). [Published paper](https://aclanthology.org/2024.eacl-demo.16.pdf). Evidence: Section 3, printed pages 152–153; WikiEval in Section 4, page 153; Table 4, page 155; limitations, page 156.

**Method and evaluation.** RAGAs estimates faithfulness, answer relevance and context relevance using LLM-based scoring. Its WikiEval study uses 50 Wikipedia pages and two English-fluent annotators. Table 4 reports model–human pairwise agreement of 0.95, 0.78 and 0.70 respectively, outperforming the tested GPT Score and GPT Ranking baselines. These are agreement measurements, not tender-analysis accuracy. Reference-free scoring is still validated against human judgments in the paper.

**Transfer limitation.** A small English encyclopedia-based comparison does not validate numeric constraints, company eligibility or Russian/Kazakh performance. Scores depend on the evaluator and prompts; the weakest agreement is for context relevance.

**Proposed decision.** Use human-adjudicated labels and citation checks as primary outcomes. Treat automatic judging as optional diagnostics, calibrated on permitted development data. Version its model and prompts and apply the same data-routing policy as generation. Related tasks: TG-D19 and TG-D21.

## Synthesis and proposed TenderGuard method

The proposed method combines controlled stages with explicit evidence contracts. The research contribution to test is whether that structure improves a specific SME document-analysis workflow enough to justify its cost. The four studies inform the design questions above; they do not establish TenderGuard's eventual quality or the uniqueness of its feature set.

### Shared ingestion and stage contracts

Both experimental configurations receive the same authorized document versions and company-profile version. Ingestion retains document structure, chunk identifiers and source locations. Each requirement record identifies its condition, operator, value, unit and citation, together with an explicit missing-information state where needed.

The staged configuration follows the supervisor's architecture: ingestion, requirement extraction, compliance analysis, and risk scoring/reporting. Compliance consumes atomic requirements and company evidence. Reporting exposes the status, supporting quotations, uncertainty and recommended next action. Risk categories must follow an agreed rubric rather than an unexplained model score.

A valid handoff must preserve the requirement identifier and document version. A factual claim must remain linked to evidence that actually supports it. Structural validation checks fields and references; semantic review checks meaning, dates, units, contradictions and missing evidence. Failures remain visible as failed or incomplete processing instead of becoming a successful report.

### Controlled comparison of B1 and B2

**B1** is a single-prompt RAG analysis after shared ingestion and retrieval. **B2** separates extraction, compliance and reporting into explicit stages after the same ingestion. For the primary comparison, freeze the retrieved evidence pack so improved retrieval is not confused with the effect of staging. An adaptive-retrieval variant can be evaluated separately.

Keep the model identifier, data versions, retrieval configuration, permitted inputs and output rubric fixed. Record all calls, retries, tokens, elapsed time and failures. Use a declared total resource ceiling and report actual consumption for each method. More calls are part of the cost of B2, not an unreported advantage. A quality gain accompanied by higher latency or cost must be assessed as a trade-off.

The generative model can initially use an approved hosted route. Private context without a permitted route remains blocked. Local inference and fine-tuning are optional extensions and should receive separate comparisons. This design does not require training a model to complete the literature-review task.

### Illustrative documentary fit case

Consider a synthetic tender requiring at least 24 months of warranty. An offer explicitly promising 36 months supports `met`; an offer explicitly promising 12 months supports `unmet`. An absent or irrelevant warranty statement supports `unknown`. Each outcome must cite the tender requirement and, when available, the company offer. A missing document must not be treated as proof of a contradictory promise.

This illustration motivates separate measurement of evidence retrieval, condition extraction and status assignment. It is an example of the proposed method, not a completed experiment or a validated legal rule.

## Evaluation and traceability

The following checks turn the proposed method into testable work. Definitions and target values are finalized under TG-D01; final results require the frozen data and evaluation milestones.

| Proposed decision | Task links by ID | Verification to implement |
| --- | --- | --- |
| Bound stage actions and preserve evidence | TG-R13, TG-D15 | Reject invalid references; inspect support of each reported finding |
| Compare B1 with B2 fairly | TG-R19, TG-D21 | Fixed evidence pack and model; paired quality, latency and token measurements |
| Separate documentary fit from legal applicability | TG-R14, TG-R15, TG-R20 | Independently annotated cases; explicit applicability and unknown labels |
| Calibrate automatic judging | TG-D19, TG-D21 | Compare judge decisions with human labels on a separate development subset |

Report extraction precision/recall/F1 with field-level checks for quantities, units and dates. For company fit, report macro-F1 and the confusion matrix across `met`, `unmet` and `unknown`, including erroneous passes. Citation correctness is the proportion of checked citation links that support their associated claims. Evidence coverage measures correctly supported required items against all gold required items. Failed runs must remain in the accounting.

Split by document family and related company-profile variants before tuning, and report Russian and Kazakh results separately with sample counts. Preserve development/test separation. Evidence of privacy and organization isolation requires its own tests; an accurate answer alone does not demonstrate either property.

## References

1. Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., and Cao, Y. 2023. *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. [Conference paper v3](https://arxiv.org/pdf/2210.03629v3).
2. Cemri, M., et al. 2025. *Why Do Multi-Agent LLM Systems Fail?* Advances in Neural Information Processing Systems 38, Datasets and Benchmarks Track. [Publisher and citation](https://papers.nips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html). DOI: [10.52202/085713-4082](https://doi.org/10.52202/085713-4082).
3. Guha, N., et al. 2023. *LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models*. Advances in Neural Information Processing Systems 36, Datasets and Benchmarks Track. [Publisher and citation](https://proceedings.nips.cc/paper_files/paper/2023/hash/89e44582fd28ddfea1ea4dcb0ebbf4b0-Abstract-Datasets_and_Benchmarks.html). DOI: [10.52202/075280-1915](https://doi.org/10.52202/075280-1915).
4. Es, S., James, J., Espinosa Anke, L., and Schockaert, S. 2024. *RAGAs: Automated Evaluation of Retrieval Augmented Generation*. Proceedings of EACL 2024: System Demonstrations, 150–158. DOI: [10.18653/v1/2024.eacl-demo.16](https://doi.org/10.18653/v1/2024.eacl-demo.16).

## Review and integration

The review connects each publication's method, evaluation and limitations to a TenderGuard design decision. Team members confirm the interpretations for presentation; Ramazan coordinates peer review and records any requested corrections. Review approval and task statuses remain with the team.

Maintain one literature review under Component 3, retaining unique publication identifiers when adding research. Transfer the proposed decisions into the requirements, architecture and evaluation documents after team review. The Word document is a presentation copy of this Markdown source; update both together when incorporating review comments.
