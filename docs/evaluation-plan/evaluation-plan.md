# TenderGuard — Verification and Evaluation Plan

## 1. Evaluation purpose

TenderGuard compares tender requirements with a company's documents and presents the findings with supporting quotations and source references. The evaluation will examine whether the platform retrieves the necessary evidence, interprets the requirements correctly and produces an assessment that a tender specialist can check. It will also test whether organization access and processing policies remain effective throughout that workflow.

The main experimental question concerns the proposed staged RAG workflow. Separating requirement extraction, assessment and reporting may make errors easier to detect, but it also introduces additional model calls and opportunities to lose information between stages. A single-prompt RAG system provides the comparison needed to determine whether the additional structure is worthwhile.

The evaluation follows the objectives in the project proposal. Documentary fit is assessed against the supplied evidence; legal applicability requires its own validated basis.

| Project objective | Evidence and verification method | Measures |
| --- | --- | --- |
| O1: Establish the user problem and scope | Check interview records and the links from findings to proposed requirements | Number of actual user discussions; findings with identifiable supporting records; unresolved assumptions |
| O2: Justify the proposed approach | Review the literature synthesis and system/technology comparison against their stated criteria | Source coverage; evidence supporting comparison claims; decisions linked to research findings and limitations |
| O3: Prepare traceable research data | Audit document provenance, annotation and development/test separation | Manifest completeness; annotation agreement; unresolved labels; document-family overlap between partitions |
| O4: Implement ingestion and retrieval | Test parsing and source resolution; evaluate evidence retrieval and cited answers | Parser acceptance cases; locator validity; Recall@5/@10; complete-evidence retrieval; answer support |
| O5: Implement company-specific analysis | Compare extracted requirements, statuses and reports with human reference annotations | Extraction F1; status macro-F1; joint requirement/status F1; false passes; supported coverage |
| O6: Enforce controlled processing | Exercise authorized, unauthorized and policy-blocked requests | Unauthorized disclosures; prohibited outbound requests; correct blocking; successful authorized operations |
| O7: Evaluate the method fairly | Run paired baseline comparisons using fixed data and configurations | Paired quality differences; latency; model calls, tokens and cost; reproducibility of scoring |
| O8: Deliver an explainable prototype and report | Inspect the prototype, run the core workflow and repeat setup from the documentation | Task completion; citation inspection; retained review history; successful setup and smoke tests |

Documentation review verifies the analysis and design objectives. Model experiments and application tests will provide the implementation evidence as the corresponding functionality becomes available.

## 2. Research questions

| Question | Comparison and data | Main measurements | Responsibility |
| --- | --- | --- | --- |
| RQ1: Which retrieval configuration best finds the evidence needed for tender analysis? | Lexical retrieval, BGE-M3 dense retrieval and multilingual E5-base on the same annotated corpus and queries | Passage recall, complete-evidence success, ranking quality, retrieval time and index size | Daniyar Kairatov |
| RQ2: Does staged analysis improve company-specific findings compared with single-prompt RAG? | Paired runs on the same held-out tender/company packages, with a fixed generator and evidence set | Extraction and status quality, citation support, false passes, latency and total model use | Daniyar Kairatov; Rassul Akhmetov coordinates backend and orchestration integration |
| RQ3: Do the controls enforce the intended organization and data-processing boundaries? | Authorized and adversarial requests across two synthetic organizations, using permitted and prohibited processing routes | Observed disclosures, forbidden transmissions, correct blocking and successful permitted processing | Ramazan Talgatov; Rassul checks backend enforcement and Daniyar checks ML inputs and outputs |
| RQ4: Can users inspect a finding and identify how to resolve missing evidence? | Task-based walkthroughs using the prototype and, later, the working analysis interface | Completion, time, correct interpretation of statuses, citation inspection and difficulties encountered | Ramazan Talgatov; Daniyar prepares the assessment rubric and Rassul checks report behavior |

Russian and Kazakh results will be reported separately. Numeric thresholds, calendar constraints, contradictory documents and missing evidence will be examined within RQ2 because these cases directly affect the reliability of an application decision.

## 3. Evaluation data and reference annotations

### 3.1. Corpus composition

The basic evaluation unit is a tender package paired with a particular version of a company profile and its supporting documents. The corpus will cover text-based PDF and DOCX files in Russian and Kazakh. The pilot category will follow the approved project scope; the initial proposal identifies IT and office equipment as a candidate.

Tender documents will come from public sources or be used with permission. Company evidence will use authorized records where these are available. Clearly labelled synthetic company documents will provide controlled cases when access to real records is restricted. Results from real company evidence and synthetic profiles will be reported separately, since success with constructed profiles does not establish performance on real SME records.

Each document will have a manifest entry recording its source, use basis, language, document type, version, acquisition date, organization scope and file hash. Private records will remain in controlled storage. The repository will contain the annotation rules, permitted examples, evaluation configuration and aggregate results.

For planning, the study will aim for 30 independent tender families, with approximately equal Russian and Kazakh coverage. Eighteen families will be assigned to development and twelve to the held-out test set. An initial six-family feasibility pilot will be drawn from the development partition. The held-out set will aim to contain at least 120 atomic requirement assessments across its twelve families. These are provisional collection targets, not achieved counts or a statistical power calculation. The allocation will be revised after the pilot if permissions, document quality or annotation effort make it unsuitable, and fixed before final testing.

The corpus report will state the actual number of families, documents, queries and assessed requirements in every partition, together with language and class distributions. A shortage of Kazakh documents or a rare status class will be reported directly rather than concealed through an overall average.

### 3.2. Document families and data separation

A document family includes a tender and its amendments, duplicates, translations and related company-profile variants. Connected families will remain in one partition. This prevents a development example from revealing the wording or answer of a test case. Exact hashes, near-duplicate candidates and shared templates will be reviewed before the split is finalized.

Development data will be used to select chunking, retrieval settings, prompts and model parameters. Test data will be used only after those decisions and the scoring rules have been fixed. If test material is exposed during tuning, the affected evaluation will be documented and a new uncontaminated test partition prepared before another final run.

Fully synthetic boundary cases will form a separate diagnostic set. They will cover equality at numeric thresholds, incompatible units, calendar versus working days, unresolved amendments, missing values and conflicting company commitments. They support controlled testing but will not be counted as natural tender families.

### 3.3. Annotation procedure

Each annotation will represent one atomic obligation. Annotators will preserve the original text and record its subject, operator, threshold, unit, product scope and applicable date or deadline. The tender citation and company-evidence citation will be stored separately, with document versions and page, paragraph or table-cell locations.

| Status | Annotation rule | Example |
| --- | --- | --- |
| `met` | Applicable company evidence supports the complete requirement | A tender requires at least 24 months of warranty and the applicable offer promises 36 months |
| `unmet` | Applicable evidence demonstrates a violation | The same requirement is paired with an applicable 12-month warranty commitment |
| `unknown` | Evidence is missing, ambiguous, incomparable or conflicting without a rule resolving the conflict | No warranty period is stated, or two applicable-looking offers give different periods and neither supersedes the other |

Missing information alone will not be labelled `unmet`. Working days will not be converted to calendar days without the necessary anchor date and calendar. Material differences in units, thresholds or scope will be retained. A file's name or upload date will not by itself establish which document is authoritative.

Two team members will annotate the pilot independently before inspecting model predictions. Agreement and Cohen's kappa will be reported before adjudication, together with class counts. Disagreements will be used to refine the guide. Final reference labels will be established through independent annotation and documented adjudication; unresolved cases requiring legal interpretation will be kept outside the documentary reference set or recorded separately for specialist review.

Two evidence scopes will be distinguished. End-to-end reference labels use the full authorized package. The separate classification experiment uses labels based on the evidence actually supplied to the model. If retrieval misses a decisive company document, a justified `unknown` can be correct for the supplied evidence while remaining an end-to-end failure. The original full-package label will be retained so that retrieval errors are not hidden by relabelling.

## 4. Baselines and experimental design

### 4.1. Retrieval comparison

RQ1 will compare PostgreSQL lexical full-text search with BGE-M3 dense retrieval and multilingual E5-base dense retrieval. Lexical search provides an interpretable baseline for exact terms and identifiers; dense retrieval tests whether semantic matching improves retrieval of paraphrased requirements. The embedding comparison is motivated by the multilingual retrieval study in [Chen et al. (2024)](https://aclanthology.org/2024.findings-acl.137/), while selection between the candidates will depend on project data.

All configurations will use the same corpus versions, chunk boundaries, query set and organization filters. Tokenizer truncation will be checked for each embedding model. Query language and document language will be recorded separately, including cross-language cases. Annotators will identify relevant passages and acceptable complete evidence sets for each query. Queries with no supporting evidence in the corpus will be evaluated as a separate unanswerable group.

Lexical–dense fusion will be tested as a retrieval ablation after its combination rule and parameters have been selected on development data. Its effect will be reported separately from the comparison of analysis workflows.

### 4.2. Single-prompt and staged analysis

The primary comparison will use two configurations:

| Configuration | Processing after shared ingestion and retrieval | Output |
| --- | --- | --- |
| B1: single-prompt RAG | One generation call receives the selected tender and company passages | Atomic requirements, statuses, explanations and citations in the agreed output schema |
| B2: staged RAG | Separate extraction, assessment and reporting stages exchange structured outputs and retain access to the same permitted source passages | The same final output schema, with intermediate requirements and assessments available for analysis |

B1 is a practical lower-complexity alternative. B2 will be considered useful only if any improvement in supported findings justifies its additional latency, model use and integration effort. The relevance of explicit support checking is informed by [Asai et al. (2024)](https://proceedings.iclr.cc/paper_files/paper/2024/hash/25f7be9694d7b32d5cc670927b8091e1-Abstract-Conference.html). TenderGuard will evaluate its own structured workflow; reproducing Self-RAG's training procedure is outside this comparison.

The two configurations will use the same generator revision, source-document versions, company profile and permitted original information. Their retrieved evidence will be serialized and hashed before the paired run. Ordering, token limits and truncation rules will be identical. B2's intermediate outputs are part of its processing method and will be retained for error analysis.

Shared retrieval will use predefined queries derived from the user request and available document metadata. Human reference requirements will not be used to select evidence for the end-to-end experiment. Reference-based queries are permitted in the separate retrieval benchmark, where retrieval itself is the object of measurement.

No generative planning or repair calls will be hidden inside B1. Both configurations will use the same deterministic schema and reference validation. Invalid output will be retained as a processing failure. Packages exceeding the input limit will follow a common exclusion or segmentation rule fixed before testing; segmented multi-call processing will be reported as a separate configuration.

An additional assessment experiment will provide both systems with the same human-annotated requirements and evidence. Comparing this result with end-to-end performance will help distinguish extraction failures from assessment failures. Adaptive retrieval that searches for further passages during analysis will also be reported separately, because it changes the evidence available to the system.

### 4.3. Diagnostic comparisons

A development ablation will compare the staged workflow with and without an explicit support-check instruction in the assessment stage. The original evidence, generator and stage structure will be held constant. Server authorization and mandatory output validation will remain enabled. This comparison will test whether the support check reduces false passes or merely increases omissions.

A second diagnostic will move the same decisive passage to the beginning, middle and end of an otherwise fixed evidence set. Status and citation-support changes will be measured. This follows the context-position problem examined by [Liu et al. (2024)](https://aclanthology.org/2024.tacl-1.9/). The main B1/B2 experiment will subsequently use one fixed ordering so that position changes cannot explain a difference between configurations.

## 5. Quality measures

### 5.1. Retrieval

Passage Recall@5 and Recall@10 will measure how much annotated relevant evidence appears among the highest-ranked results. For each answerable query, recall is the number of relevant retrieved passages divided by the number of relevant reference passages. Scores will be averaged across queries and reported with their denominators.

Complete-evidence success@5 and success@10 will measure the proportion of answerable queries for which the retrieved results contain at least one complete acceptable evidence set. This is necessary because retrieving a tender clause without the associated company evidence may be insufficient for an assessment.

Where graded relevance annotations are available, nDCG@10 will measure ranking quality. Proposed relevance grades are 0 for irrelevant, 1 for partially relevant and 2 for directly relevant passages, using gain `2^grade − 1` and discount `log2(rank + 1)`. These definitions will be settled during annotation. Unanswerable queries will be reported separately rather than assigned a recall value with an empty denominator.

### 5.2. Extraction and status assignment

Predicted requirements will be matched one-to-one with reference obligations using their meaning, scope and normalized conditions. A changed threshold, unit or deadline that affects the decision will invalidate the match. Duplicate predictions will count as false positives; missed obligations will count as false negatives. Disputed matches will be reviewed without revealing the producing configuration.

Extraction precision, recall and F1 will be calculated as:

`Precision = TP / (TP + FP)`  
`Recall = TP / (TP + FN)`  
`F1 = 2TP / (2TP + FP + FN)`

The primary classification measure will be macro-F1 across `met`, `unmet` and `unknown` in the reference-requirement experiment. Per-class precision, recall and F1, class counts and the confusion matrix will accompany it. A prediction-only `processing_failure` column will retain invalid or missing answers; these count as false negatives for their reference classes. Undefined scored precision/recall/F1 values will be set to zero, with the underlying counts reported. If a reference class is absent, both the fixed three-class score and the score over represented classes will be shown.

End-to-end requirement-and-status F1 will count a true positive only when both the obligation and its status are correct. A matched obligation with a wrong status contributes one false positive and one false negative. This prevents high classification scores from concealing missed requirements.

False passes will receive separate attention. The false-pass rate is the number of reference `unmet` or `unknown` cases predicted as `met`, divided by all reference `unmet` and `unknown` cases. The report will also show the erroneous-pass share among predicted `met` findings and recall for `unknown` cases.

Any reported risk category will be checked against a written rubric and human reference judgments. Category agreement and disagreements will be reported separately from documentary status. A numerical risk score will be evaluated only if its meaning, reference scale and acceptance conditions have been defined.

### 5.3. Citations and cited answers

Citation evaluation will distinguish a reference that opens correctly from evidence that supports the associated claim. This distinction follows the evaluation approach in [Gao et al. (2023)](https://aclanthology.org/2023.emnlp-main.398/).

| Measure | Scoring unit and denominator |
| --- | --- |
| Locator validity | Citation links resolving to the intended document version and location, divided by all generated citation links |
| Citation precision | Individually useful supporting citations, divided by all generated citations; a redundant or irrelevant reference receives no credit |
| Finding support | Atomic evidence-dependent findings fully supported by their cited set, divided by all generated evidence-dependent findings; missing citations receive no credit |
| Supported gold coverage | Reference obligations correctly extracted and classified with adequate support, divided by all reference obligations |

For `met` and `unmet`, support must establish both the tender condition and the relevant company fact. For `unknown`, the explanation must identify the unresolved field or conflict within the assessed evidence scope. Automatic entailment scoring may assist review only after calibration against human labels on development cases; it will not define the reference labels.

Cited question answering will use a separate set of answerable and unanswerable questions. Human assessment will record factual correctness, supporting citations and whether the answer adds unsupported claims. The question set will include requests about quantities, delivery periods, warranty terms and document references. Questions without sufficient evidence should receive an explicit explanation of what is missing.

### 5.4. Efficiency

For every attempted package, measurements will include elapsed time, model calls, input/output tokens, retries and cost. Failed runs will remain in the accounting. Ingestion and indexing time will be reported separately from analysis time so that repeated use of an existing index does not conceal initial processing costs. The report will distinguish application processing time from provider response time where the instrumentation permits it.

## 6. Application verification

Each test case will identify the functional or non-functional requirement it verifies, its inputs, expected outcome and observable evidence. The test inventory will use the requirement identifiers adopted in the consolidated specification, allowing a reviewer to trace a requirement through its component and test.

| Test level | TenderGuard behavior to verify | Expected evidence |
| --- | --- | --- |
| Unit | File validation; paragraph/table extraction; source-locator mapping; numeric operators; unit and date handling; label rules; schema validation; policy decisions | Repeatable fixtures with expected values and explicit error outcomes |
| Integration | Upload → parsed text → chunks → retrieval; profile version → assessment; stage handoffs → persisted findings; citations → original source; Privacy Gateway → provider adapter | Tests showing that document versions, organization context and evidence references remain consistent across boundaries |
| End-to-end | Sign in, select an organization, upload documents, select a profile, run analysis, inspect findings and record a review; rerun with revised evidence | A repeatable scenario demonstrating the core workflow and preserved previous run history |
| Security | Unauthorized API/database/file access; cross-tenant jobs, search and caches; forged identifiers; indirect prompt injection; prohibited external routes | Allowed/denied test records, controlled outbound observations and an incident record for any disclosure |
| Recovery | Invalid files, unsupported scans, provider failure, timeout and worker interruption | Safe failure states, bounded retries and recovery without mixing tenants or replacing the original run record |
| Load | Concurrent uploads, queued analyses and report access | Request/job counts, completion and error rates, response/queue times and resource use under a declared workload |

Security tests will use two synthetic organizations with distinct documents and recognizable test strings. A successful test must show both that prohibited access is blocked and that the corresponding authorized request succeeds. The same checks apply to derived outputs and retries. Document removal, retention and access changes will also be checked against the agreed requirements for indexes, caches, jobs and logs. Restricted information must not be transmitted when the processing policy blocks the selected route; failure of a local route must not authorize an external fallback.

For the initial load test, workloads of one, three and five concurrent users are proposed, with twenty job attempts at each level. A stubbed provider with documented behavior will first isolate application and queue overhead. Real-provider analysis latency will be measured separately within the available budget. Median and maximum times will be reported with sample counts; any p95 estimate will state the sample size and calculation method. A particular latency limit will be adopted only after the requirements and pilot measurements establish a defensible value.

Coverage will be used to identify untested code paths alongside scenario-based tests. The team's longer-term target of at least 95% coverage will be tracked with the selected coverage definition and scope; a coverage percentage will not substitute for evidence that access restrictions, citations or assessment rules behave correctly.

## 7. User evaluation

Prototype walkthroughs will first involve at least two people outside the team, in line with the prototype requirement. A later evaluation of the working interface will aim to recruit five representatives of the intended users, subject to availability and consent. These activities will be reported separately from the interviews used to establish the project problem.

Participants will complete four tasks: locate a tender requirement, inspect the associated company evidence, explain one reported status and identify the information needed to resolve an `unknown` finding. Task completion will require the correct source or explanation, rather than simply reaching the right screen. The study will record completion, time, assistance required and observed difficulties. Participants will use public or synthetic material rather than confidential company records.

A manual-workflow comparison will be made only if equivalent tasks and a defined order/counterbalancing procedure can be arranged. Without that comparison, recorded time will describe usability and will not be interpreted as time saved. Results from a small convenience sample will be used to identify design problems, with participant characteristics and limitations stated.

## 8. Measurement conditions and analysis

Before final testing, the corpus manifest, annotations, chunking, retrieval settings, prompts, output schema and scoring procedure will be fixed. The experiment record will identify the generator and embedding revisions, tokenizer, sampling parameters, supported seed settings, context limits, timeout/retry ceilings and permitted processing route. Local measurements will record CPU, GPU, memory, software versions and model precision. Hosted measurements will record the model identifier, measurement period and available provider information.

B1 and B2 will each be run three times on every held-out package using the same sampling settings. Run order will be alternated or randomized within repetitions to reduce systematic effects from provider load. Scores will be calculated for each full repetition and then summarized; repeated executions will not be counted as additional independent packages. Retrieval warm-up and cache conditions will be documented and kept comparable.

Paired differences will be reported because both configurations process the same packages. Where the sample supports it, uncertainty will be estimated through family-level paired bootstrap resampling, retaining the related requirements and repetitions within their families. Small language/class subsets and unstable intervals will be identified explicitly.

Every run will retain its configuration, document/profile versions, evidence-set hash, original predictions, citations, validation outcomes, timing and model-use records. Private source text will stay in controlled storage. The evaluation export will contain enough permitted information to reproduce scoring and trace a reported finding to the assessed input.

Paid experiments will use the remaining allocation within the team's stated $0–50 project budget. Expected token use and charges will be estimated before the final run, and a maximum run budget enforced. The exact generator, resource ceilings and final corpus allocation will be settled from the development pilot and recorded before the held-out test is accessed.

## 9. Success criteria and interpretation

The initial planning targets are status macro-F1 of at least 0.80, complete-evidence success@5 of at least 0.85 and supported gold coverage of at least 0.80. These are provisional engineering targets to review against the pilot, rather than thresholds established by the cited studies. They will be finalized before testing and reported alongside false passes, class/language results and processing failures.

All defined unauthorized-access and prohibited-transfer cases are expected to be blocked, with authorized control cases remaining usable. Any observed disclosure will require correction and re-testing. Passing these scenarios supports the tested processing boundary; it does not establish protection against every possible attack.

The final analysis will explain where errors originate: parsing, evidence retrieval, requirement extraction, numeric/calendar interpretation, status assignment, citation support or inter-stage reporting. Quality gains will be considered together with their resource cost. Higher precision accompanied by lower supported coverage will be reported as a trade-off, and similar quality at lower cost may favor the simpler baseline.

The evaluation will support conclusions within the selected tender category, languages, document types and evidence conditions. Performance on synthetic company profiles, limited Kazakh samples or a small participant group will not be generalized to all procurement settings. Negative and inconclusive findings will remain part of the results and will inform the final system design.
