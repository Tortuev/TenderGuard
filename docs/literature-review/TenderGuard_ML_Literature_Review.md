# TenderGuard: ML Literature Review and Research Synthesis

**Task:** TG-D02 — Review four scientific papers on RAG and evaluation  
**Contributor:** Daniyar Kairatov — ML and retrieval  
**Reviewer:** Rassul Akhmetov; review pending  
**Milestone:** M0 — First predefense, 24 October 2026  
**Version:** 1.0, prepared for review on 21 October 2026

## 1. Purpose and scope

TenderGuard is a proposed web platform for small and medium-sized enterprises that compares tender requirements with company documents. Its outputs should identify documentary fit as `met`, `unmet` or `unknown` and link findings to source evidence. This review examines the research basis for retrieval, multilingual processing, evidence selection and evaluation.

The review contains four detailed publication records [1–4] and four supporting methodological records [5–8]. It is Daniyar's ML contribution to the team's literature review. It does not establish completion of the team's requirement for at least 12 meaningfully used sources, including at least eight scientific publications. Team contributions must be combined and deduplicated; regulatory research belongs in a separate, coordinated contribution.

## 2. Selection and review method

Selection was thematic rather than systematic. Three detailed records came from the supplied article archive; the fourth uses the primary publication of *Lost in the Middle*. Supporting sources were selected for their direct relevance to RAG, embedding alternatives and citation evaluation. This is not an exhaustive search or a PRISMA review.

Each detailed record examines the method, data, published findings, methodological limitations and a concrete implication for TenderGuard. Publisher records and primary texts are linked in the references. The archive's publication list and journal-quartile labels are not treated as independent verification. Reported scores belong to the original studies; no TenderGuard experiments were run for this review.

## 3. Detailed publication records

### 3.1. Domain adaptation: retrieval versus fine-tuning [1]

**Method and data.** Tugambayeva and Sakhipov compare FAISS retrieval with Mistral-7B over 238 aviation documents against T5-small adapted with LoRA using 920 context–question pairs. Automatic evaluation uses 116 examples; preliminary expert assessment uses 15 questions per approach.

**Findings.** Table 1 reports BLEU of 24.77% for fine-tuned T5 and 3.02% for RAG, while aviation-term coverage is 43.97% and 92.24%, respectively. The disagreement shows that reference similarity and domain terminology measure different properties.

**Critical assessment.** Model architecture, capacity and training change together: approximately 60 million versus seven billion parameters. The comparison cannot isolate the effect of retrieval. The small author-led expert assessment also limits generalization. Question generation differs from eligibility assessment.

**TenderGuard implication.** Begin with an evidence-retrieval baseline and justify any later fine-tuning through error analysis. Prioritize correct statuses and supporting citations over BLEU. Keep the generator and evidence fixed when comparing analysis workflows.

**Evidence locations:** Methods and evaluation, pp. 156–159; Table 1, p. 159; expert assessment, p. 160; discussion, pp. 160–162.

### 3.2. Multilingual adaptation for Kazakh QA [2]

**Method and data.** Tleubayeva and Shomanov examine multilingual question-answering models, adaptation and augmentation for Kazakh, including Kazakh sKQuAD evaluation. Their results section combines analysis with findings from another study; it should not be described as a wholly reproduced, controlled benchmark.

**Findings.** Table 3 reports mT5 F1 of 75.7213 after fine-tuning. However, mDeBERTa-v3-base-SQuAD2 is listed at 80.6928 before and 79.7787 after fine-tuning. The abstract's claim that mT5 has the highest F1 therefore does not describe the entire table consistently.

**Critical assessment.** Model conditions and result provenance require careful separation. QA token-overlap scores do not demonstrate correct tender citations or numeric reasoning. Translation and augmentation can also introduce related examples across data partitions.

**TenderGuard implication.** Evaluate Russian and Kazakh separately, retaining sample counts, checkpoint identifiers and data versions. Use human-reviewed numeric and calendar cases. Treat multilingual capability as a hypothesis to test, rather than selecting a model from the abstract's ranking.

**Evidence locations:** Methods, pp. 91–93; results and Table 3, pp. 93–95; discussion, pp. 95–96.

### 3.3. Near-duplicate detection and dataset integrity [3]

**Method and data.** Kazagasheva and colleagues combine text canonicalization, lexical filtering, semantic embeddings and approximate-neighbor retrieval to reduce candidate comparisons. Their Kazakh academic-abstract dataset includes 11,851 pairs with authentic texts and controlled synthetic transformations.

**Findings.** The study reports computational savings relative to exhaustive comparison and a trade-off between candidate filtering and duplicate recall. Figures 12–13 present performance information. No exact speedup is adopted here without a clearly reproducible numeric comparison.

**Critical assessment.** Academic abstracts and synthetic paraphrases differ from tender amendments. Pair-level stratification alone does not establish independence between source families. Aggressive normalization can erase meaningful changes in amounts, deadlines or negation.

**TenderGuard implication.** Group original tenders, amendments, translations and derived examples before splitting development and test data. Use hashes and similarity candidates followed by review. Similarity may identify related documents, but it must not establish equivalence between obligations.

**Evidence locations:** Data, pp. 247–250; methodology, pp. 251–256; results and limitations, pp. 257–258. The publisher/PDF author order is used; a differing DOI-registration order was observed during preparation.

### 3.4. Evidence position in long contexts [4]

**Method and data.** Liu and colleagues vary the position of relevant information in multi-document question answering and synthetic key-value retrieval. The QA experiments use Natural Questions-derived examples with distractor documents.

**Findings.** Several tested models perform best when evidence appears near the beginning or end of the context and worse when it appears in the middle. A larger advertised context window does not ensure effective use of all included evidence.

**Critical assessment.** The controlled tasks do not estimate procurement accuracy or the behavior of every later model. The findings motivate context-construction tests; they do not prove that chunking or a multi-agent system resolves the problem.

**TenderGuard implication.** Version evidence ordering and truncation. Include long-document and distractor cases in development evaluation. Keep evidence content and order identical in the primary single-prompt versus staged comparison so context changes cannot explain an apparent staging benefit.

**Evidence locations:** Sections 2–3, especially Section 2.3; published article, pp. 157–173.

## 4. Supporting methodological literature

### 4.1. Retrieval-augmented generation [5]

Lewis and colleagues combine a dense retriever with a sequence-to-sequence generator, examining RAG-Sequence and RAG-Token on knowledge-intensive tasks. Table 1 reports Natural Questions exact match of 44.5 for RAG-Sequence against 41.5 for the listed DPR system. This supports investigating explicit document retrieval, but Wikipedia-based QA does not establish procurement correctness, faithful citations or privacy. TenderGuard should therefore measure retrieval separately and ground decisions in current company evidence. This 2020 foundational publication must be excluded if a mandatory recent-source window starts after 2020.

### 4.2. BGE-M3 as an embedding candidate [6]

Chen and colleagues investigate dense, sparse and multi-vector retrieval with self-knowledge distillation. Their evaluation includes MIRACL, MKQA and MLDR. Table 5 reports MIRACL development nDCG@10 of 69.2 with distillation versus 68.7 without it in dense mode. This ablation supports considering the method, rather than assuming a universal ranking. TenderGuard should first test BGE-M3's dense mode on its own frozen queries and chunks; hybrid modes require separate evidence that their added complexity is worthwhile. The cited version is an arXiv technical paper.

### 4.3. Multilingual E5 as a controlled comparator [7]

Wang and colleagues describe contrastive pretraining on approximately one billion multilingual pairs followed by supervised refinement. Table 4 reports multilingual E5-base nDCG@10 of 62.3 and Recall@100 of 93.1, averaged over 16 MIRACL development languages. These scores cannot be directly compared with a number from a differently configured paper to declare a TenderGuard winner. E5-base is a concrete dense comparator: use identical project queries and chunks, documented query/passage formatting, and measured resource consumption. Base and large are distinct checkpoints. The source is a technical report.

### 4.4. Citation evaluation with ALCE [8]

Gao and colleagues introduce ALCE using ASQA, QAMPARI and ELI5 to evaluate generated answers with citations. The study separates fluency, correctness and citation quality and examines automated entailment and human judgments. Its findings show why fluent text and plausible-looking references are insufficient evidence of support. For TenderGuard, check source-location validity separately from whether the cited passage supports the claim. Automated entailment may assist evaluation but needs human calibration for Russian/Kazakh numeric and calendar constraints. Sections 3–5 provide the evaluation framework and experimental discussion.

## 5. Cross-study synthesis and research gap

The literature identifies separate failure points across the evidence-processing chain. Retrieval can expose relevant information [5–7], but information may be poorly used because of context position [4]. Reference similarity can disagree with domain usefulness [1], and answer quality can differ from citation support [8]. Language-specific data and evaluation conditions matter [2]; related-document contamination can further distort apparent quality [3].

None of these studies, individually or together, demonstrates reliable Russian/Kazakh comparison of tender requirements with SME company evidence under TenderGuard's processing policy. This is the project-specific evaluation gap. It supports an empirical engineering study, rather than a claim that TenderGuard introduces an unprecedented algorithm.

| Literature finding | Proposed TenderGuard choice | Check to implement |
| --- | --- | --- |
| Different metrics reward different behavior [1, 8] | Separate status correctness, citation support and cost | Human-adjudicated labels and claim–evidence checks |
| Multilingual scores depend on task and data [2, 6, 7] | Compare embedding candidates on project data | Per-language retrieval scores and sample counts |
| Related texts can contaminate partitions [3] | Split by document family before tuning | Duplicate and amendment audit |
| Evidence position can change answers [4] | Freeze evidence ordering and limits | Paired comparison with identical evidence packs |
| Retrieval and generation are distinct components [5] | Evaluate both independently | Retrieval recall and downstream status errors |

## 6. Proposed approach and evaluation questions

Authorized ingestion should produce versioned text with stable source locations. Local lexical and dense retrieval should select tender requirements and company evidence. The analysis should retain atomic conditions, including operators, quantities, units, dates and deadline anchors, and produce supported documentary findings.

The primary comparison should use two configurations:

- **B1 — Single-prompt RAG:** one analysis generation after shared ingestion and retrieval.
- **B2 — Staged analysis:** typed requirement extraction, company-evidence comparison and reporting after the same ingestion and retrieval.

Both configurations should receive the same frozen evidence pack, model version and permitted input. Record total calls, retries, tokens, elapsed time and failures under a declared resource ceiling. Any adaptive retrieval variant should be evaluated separately. More calls and higher cost must remain visible when interpreting a quality difference.

The resulting research questions are:

1. **Retrieval:** How do a lexical baseline, BGE-M3 dense retrieval and multilingual E5-base differ in evidence retrieval on Russian and Kazakh project cases?
2. **Analysis structure:** Does staged analysis improve documentary status accuracy and citation support relative to single-prompt RAG under equivalent evidence and processing permissions, and at what cost?
3. **Robustness:** How do missing evidence, contradictory records, numeric thresholds and calendar constraints affect errors and uncertainty?

TG-D01 should specify the experiments, denominators, baselines and measurement conditions. TG-D03 should define provenance, document-family partitions and annotation rules. TG-D04 should compare candidate technologies using language coverage, licenses, privacy, resources and budget. TG-D05 should present the findings and proposed evaluation without claiming results that have not been measured.

Candidate outcomes include retrieval Recall@k and nDCG@k; extraction precision/recall/F1; status macro-F1 and a confusion matrix; citation support and coverage; erroneous-pass counts; latency, tokens and cost. Define k, relevance judgments, citation units and failure accounting before measurement. Report language slices and uncertainty where the sample supports it. Numerical success thresholds remain provisional until pilot calibration.

## 7. Interpretation and privacy boundaries

`Met` requires evidence supporting the stated condition. `Unmet` requires evidence of a failure to satisfy it. Missing or unresolved evidence should produce `unknown`, rather than an invented contradiction. For example, a synthetic 24-month warranty requirement with an explicit 36-month company offer supports `met`; an explicit 12-month offer supports `unmet`; an absent warranty statement supports `unknown`. Cite the tender and company evidence separately.

These labels describe documentary fit. Legal applicability and legal conclusions require a separate validated basis. Private documents must pass the core Privacy Gateway policy before any permitted external processing, including evaluation calls. Tenant isolation remains a core requirement. Local generation, fine-tuning and OCR are optional extensions; this review does not establish their necessity or completion.

## 8. Conclusion and review status

The reviewed evidence supports evaluating a controlled, source-linked workflow with multilingual retrieval, explicit uncertainty and separate measurements for retrieval, status decisions and citations. It does not establish that staging will outperform a simpler baseline. A negative or mixed result should inform the final design.

This document is ready for substantive team review. Rassul Akhmetov's review date, comments and resulting corrections have not yet been recorded. Task completion and committee approval are not asserted. Before presentation, the contributor should be able to explain the four detailed papers, their limitations and the decisions derived from them.

## References

[1] Tugambayeva, A., & Sakhipov, A. (2026). AI-based question generation for aviation training: Comparing retrieval-augmented generation and fine-tuned models. *Scientific Journal of Astana IT University, 25*. https://doi.org/10.37943/25VYNZ9998. [Publisher record](https://journal.astanait.edu.kz/index.php/ojs/article/view/967).

[2] Tleubayeva, A., & Shomanov, A. (2024). Comparative analysis of multilingual QA models and their adaptation to the Kazakh language. *Scientific Journal of Astana IT University, 19*, 89–97. https://doi.org/10.37943/19WHRK2878. [Publisher record](https://journal.astanait.edu.kz/index.php/ojs/article/view/626).

[3] Kazagasheva, V., Kuchanskyi, O., Biloshchytska, S., & Kantayeva, D. (2026). Scalable near-duplicate detection in Kazakh scientific texts via semantic embeddings and optimized candidate filtering. *Scientific Journal of Astana IT University, 25*. https://doi.org/10.37943/25NVVS5297. [Publisher record](https://journal.astanait.edu.kz/index.php/ojs/article/view/1029).

[4] Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2024). Lost in the middle: How language models use long contexts. *Transactions of the Association for Computational Linguistics, 12*, 157–173. https://doi.org/10.1162/tacl_a_00638. [Primary publication and full text](https://aclanthology.org/2024.tacl-1.9/).

[5] Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-t., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems, 33*, 9459–9474. [Author full text, version 4](https://arxiv.org/html/2005.11401v4).

[6] Chen, J., Xiao, S., Zhang, P., Luo, K., Lian, D., & Liu, Z. (2024). M3-embedding: Multi-linguality, multi-functionality, multi-granularity text embeddings through self-knowledge distillation. *arXiv technical paper*, arXiv:2402.03216, version 4. https://arxiv.org/html/2402.03216v4.

[7] Wang, L., Yang, N., Huang, X., Yang, L., Majumder, R., & Wei, F. (2024). Multilingual E5 text embeddings: A technical report. *arXiv*, arXiv:2402.05672, version 1. https://arxiv.org/html/2402.05672v1.

[8] Gao, T., Yen, H., Yu, J., & Chen, D. (2023). Enabling large language models to generate text with citations. *Proceedings of EMNLP 2023*, 6465–6488. https://doi.org/10.18653/v1/2023.emnlp-main.398. [Primary publication and full text](https://aclanthology.org/2023.emnlp-main.398/).
