# TenderGuard: Dataset Plan and Annotation Guide

## 1. Purpose and relation to the evaluation

TenderGuard needs reference data that connects each tender condition to the company evidence used to assess it. A summary of the tender is insufficient for this purpose: the reference record must show the exact obligation, the relevant company fact and the reason for assigning `met`, `unmet` or `unknown`.

This guide defines collection, document grouping, annotation and quality checks for the experiments in the [verification and evaluation plan](../evaluation-plan/evaluation-plan.md). Retrieval experiments use annotated passages and complete evidence sets. Extraction and assessment experiments use atomic requirements, company facts, reference statuses and source locations. The three synthetic cases in Section 8 illustrate these rules; they are separate from the planned natural-document corpus.

The initial scope is text-based Russian and Kazakh PDF and DOCX documents from one pilot category. IT and office equipment is the candidate category in the [project proposal](../project-proposal/proposal.md), subject to confirmation through user findings and document availability. Scanned documents requiring OCR remain outside the core corpus unless that extension is implemented and evaluated separately.

## 2. Dataset composition

### 2.1. Evaluation units and collection targets

A package contains a particular tender-document set and a selected company-profile version with its supporting documents. A requirement assessment refers to one atomic obligation within that package. Several assessments from the same tender are related observations; they do not count as independent tender families.

The collection targets follow the evaluation plan:

| Partition | Provisional target | Intended use |
| --- | --- | --- |
| Development | 18 independent tender families | Annotation-guide refinement, chunking, retrieval selection and prompt development |
| Feasibility pilot | 6 families within the development partition | Estimate collection and annotation effort and check language and class coverage |
| Held-out test | 12 independent tender families, aiming for at least 120 atomic assessments | Final comparison after configurations and scoring rules are fixed |
| Synthetic diagnostics | The three cases in this guide, with additional controlled variants prepared as needed | Check labels, thresholds, dates and unresolved evidence without counting them as natural families |

The overall target is 30 independent tender families with approximately equal Russian and Kazakh coverage. These figures are planning targets, not collected counts or a statistical power calculation. Feasibility findings may justify a smaller corpus or revised allocation. Any revision must be recorded before final test access and reflected in both documents.

Natural tenders paired with synthetic company profiles will be distinguished from packages containing authorized real company evidence. Results from the two groups will be reported separately. Constructed company profiles make controlled comparisons possible, but they do not establish performance on real SME records.

### 2.2. Inclusion and exclusion

Include documents when their origin and use basis are recorded, their text and material tables are readable, their versions can be identified and they contain assessable obligations in the pilot category. An included tender must have enough context to interpret the selected clauses, including applicable attachments and amendments where available.

Exclude or quarantine unreadable scans, corrupted files, documents with unresolved use restrictions and incomplete packages whose missing context prevents reliable interpretation. Retain the exclusion reason. A requirement must not be removed merely because it is difficult, produces an inconvenient class or causes a model failure.

An unclear company fact normally produces `unknown` and remains useful evaluation data. An unclear tender obligation requires a different decision: retain it as `unknown` only when the obligation itself can still be defined and the uncertainty can be documented. If its applicability requires unresolved legal interpretation, keep it in a separate specialist-review list rather than inventing a reference answer.

### 2.3. Russian and Kazakh coverage

Record the language of each document and annotated passage. Retrieval queries also need their own language field, allowing Russian queries over Kazakh documents and the reverse to be identified. Mixed-language packages must retain passage-level language information.

Original Russian and Kazakh wording will remain the annotation source. An English gloss can help discussion, but it must not replace the original quotation. Reviewers competent in the relevant language must check negation, threshold operators, technical terms and calendar wording before an annotation becomes part of the reference set.

Report family, document, query and assessment counts by language and partition, together with status distributions. Do not force natural documents into an artificial class balance. If one language or class is scarce, report the limitation and use separate synthetic diagnostics to examine the missing behavior. Translated copies are derived material, not additional independent Kazakh or Russian tender families.

## 3. Provenance and permitted processing

Each acquired document needs a manifest entry before annotation. The manifest records what the file is, where it came from, which version is being used and which processing routes are permitted.

| Field group | Required information |
| --- | --- |
| Identity | `document_id`, `document_version`, `package_id`, `family_id`, `organization_id` and document role: tender, amendment, company evidence or profile |
| Origin | Source URL or controlled reference, acquisition date, original filename and acquisition method |
| Use basis | Public-source terms or recorded permission, intended use, restrictions on redistribution and permitted processing destinations |
| Content | Language, file type, category and whether the document is natural, synthetic or a derived translation |
| Integrity | SHA-256 of the acquired bytes, parsing version and a separate hash for any normalized text used in duplicate detection |
| Applicability | Effective dates where stated, amendment or supersession links, and the profile or product scope to which the evidence applies |
| Storage and partition | Restricted storage reference, access scope, retention decision and development, test or diagnostic assignment |

Public availability does not by itself establish permission to republish a document or send its contents to a hosted model. Collection permission and provider-transfer permission must be recorded separately. Missing approval blocks that processing route; it does not change the company's documentary status.

Real company documents, identifiable contacts and restricted annotation records remain in controlled storage. Public Git files contain this guide, clearly marked synthetic examples and aggregate results. Public manifests must also be checked for identifying metadata; private source paths and sensitive identifiers must not be exposed through evidence links.

External translation, annotation assistance, embedding, evaluation and retry calls are subject to the same processing policy as generation. If no approved route is available, preserve a processing-blocked record and use permitted material for development. A local failure does not permit an automatic hosted fallback.

## 4. Document families and prevention of test leakage

A document family groups a tender with its amendments, attachments, duplicate downloads, translations and derived variants. Related company-profile variants and reused evidence that could reveal the assessed answers also need to be considered when forming split groups. Every resulting connected group belongs to one partition.

Grouping will precede model development:

1. Assign stable package, document and family identifiers and retain exact file hashes.
2. Inspect exact duplicates, near-duplicate passages, shared tender identifiers and explicit amendment or translation links.
3. Review shared templates and reused company evidence. Similar boilerplate alone does not make two tenders identical, but distinctive copied conditions or repeated answer-bearing evidence can create leakage.
4. Join connected families where separation would reveal test wording or answers. Record the grouping reason and resulting number of independent groups.
5. Assign groups to development or test while checking language and category coverage. Save the split manifest and its hash.

If grouping leaves too few independent families, collect additional material or reduce the evaluation claim. Do not break a connected group merely to meet the planned sample size.

All chunks from a source remain in that source's partition. Translations, synthetic variants and paraphrases derived from a test item cannot be used as development examples. The synthetic cases published in this guide are diagnostic material and cannot later be claimed as unseen test data.

Only development data may guide retrieval settings, prompts, model selection or annotation-rule revisions. A custodian can prepare the test reference data, but its contents must not be used by the person tuning the system. Any prior exposure by team members must be recorded. Test labels, assessment rationales and gold evidence sets remain outside runtime retrieval indexes; the system receives only the permitted source documents.

Before the final experiment, freeze the manifest, annotations, source hashes and scoring revision. A suspected contamination incident requires an exposure record and a new uncontaminated test partition or a narrower claim. Corrected reference labels must retain their history, reason and reviewer, and all configurations must be rescored consistently.

## 5. Annotation record and evidence locations

### 5.1. One assessable obligation per record

Split a clause such as “16 GB of RAM and a 24-month warranty” into two requirements. Preserve their shared source and parent-clause identifier. Keep alternatives, exceptions and conditional wording attached to the obligation they modify. A conditional requirement whose applicability cannot be established is `unknown`, with the unresolved condition recorded. A demonstrably inapplicable condition is recorded separately and excluded from the three-status assessment denominator with a reason.

Each assessment needs the following fields. This is a research annotation format; it does not assert that the application database already implements every field.

| Field group | Contents |
| --- | --- |
| Record identity | `assessment_id`, `requirement_id`, package and family IDs, company-profile version, annotation-guide version and partition |
| Tender obligation | Original quotation, passage language, tender references, parent clause and applicable scope or condition |
| Normalized constraint | Subject, operator, value or range, unit, quantity basis, date or duration, anchor, day type and counting convention where relevant |
| Company facts | Original quotations, separate company references, relevant product or capability, effective dates and known authority or supersession relationships |
| Evidence scope | Full authorized package or supplied evidence set, its version/hash, and the documents inspected |
| Judgment | `status`, rationale, missing fields, unresolved conflicts and the fact needed to resolve an unknown |
| Review | Independent annotator IDs, original labels, adjudicated label, decision reason and actual review dates |

Use arrays for references: a finding may require several tender passages and more than one company source. A missing value is explicitly absent, not zero. Unavailable review information stays unrecorded until the review occurs.

### 5.2. Separate tender and company citations

Tender references establish what is required. Company references establish the offered specification, commitment or supporting fact. A tender citation alone cannot prove that the company satisfies its own requirement.

A source reference identifies the document, immutable version and recoverable location. Use PDF page index and the printed page label where different; use DOCX paragraph, heading, table row and cell where appropriate. Retain a short exact quotation. Chunk IDs may be additional locators, but they must resolve to the original document version.

For genuine absence of company evidence, keep the company-reference list empty, identify the missing field and record the inspected document scope. Do not invent a company citation. For a conflict, retain all material sources and explain why no applicable version can be selected.

The source blocks in Section 8 are the complete invented excerpts for those examples. Their internal links are real locations in this Markdown file, not references to nonexistent PDF pages.

### 5.3. Full-package and supplied-evidence judgments

The end-to-end reference status uses the full selected, authorized package. The separate assessment diagnostic uses the evidence actually supplied to the model. Store the two judgments separately, each with its evidence scope. Never overwrite the full-package label when retrieval misses a decisive passage.

For example, the complete package may establish `met`, while the supplied passages justify only `unknown`. The diagnostic can credit the cautious assessment, while end-to-end scoring still records the failure to retrieve the needed evidence. Both systems in the fixed-evidence comparison use the same supplied evidence set and its hash.

## 6. Label rules and interpretation

| Label | Decision rule | Evidence needed |
| --- | --- | --- |
| `met` | Applicable company evidence establishes the complete atomic condition | Tender condition and supporting company fact, with compatible scope, units and dates |
| `unmet` | Applicable evidence establishes a violation of the condition | Tender condition and a company fact or commitment that conflicts with it |
| `unknown` | The available evidence cannot establish either satisfaction or violation | Tender condition, available relevant sources and an explicit missing fact, ambiguity or unresolved conflict |

A 36-month warranty against a minimum of 24 months supports `met`. An applicable 12-month commitment supports `unmet`. An unstated warranty period supports `unknown`; it does not establish that the company offers no warranty.

Apply the rules in this order: identify the obligation and its scope, locate the applicable company evidence, resolve documented version relationships, compare the complete condition, and assign the status with a short rationale. If both positive and negative evidence remain applicable-looking and no authority rule resolves them, use `unknown` and retain both.

Policy blocking, unreadable input, timeout and invalid model output are processing outcomes. They must not be stored as company-fit labels. Likewise, documentary status does not establish legal eligibility or certify a licence's authenticity. Any separate legal conclusion needs its own validated source and applicability rule.

## 7. Numeric, date and conflict rules

### 7.1. Numbers and units

Preserve the original operator. “At least 16” means `>= 16`; “more than 16” means `> 16`. Equality satisfies only the first. Record decimal separators, ranges and whether a quantity applies per item, per lot or to the whole delivery.

Normalize units only when the relationship is explicit and the measured property is the same. Record the conversion and retain the original value. Do not equate GB and GiB, advertised and usable capacity, RAM and storage, or VAT-inclusive and VAT-exclusive prices without the information needed for comparison. Do not round a failing value into compliance. Record any tolerance only when the tender provides one.

### 7.2. Dates and durations

Distinguish an absolute deadline from a duration. For durations, record the anchor event, anchor date if known, calendar or working days, inclusion of the anchor date and the relevant cutoff or time zone where it affects the outcome. An unambiguous duration-to-duration comparison can be made without an absolute date when both statements use the same anchor and counting rule.

Working days cannot be converted to calendar days without the applicable start date and working-day calendar. Months and years must not be replaced with fixed numbers of days. If an ambiguous date format or missing counting rule could change the decision, use `unknown` and record the unresolved field. The explicit counting convention in SYN-02 is part of the invented source, not a general legal rule.

Certificate or document validity must be checked for the relevant product, holder and assessment date stated by the requirement. A source that proves only an earlier period is insufficient for a later one. If the current position is unestablished, use `unknown`; use `unmet` only when the applicable evidence establishes failure of the required validity condition.

### 7.3. Contradictions and amendments

Resolve an apparent conflict only through a documented relationship, such as an applicable amendment explicitly replacing a clause or a confirmed offer revision replacing an earlier offer. File modification time, a filename containing “final” or a more favorable value is insufficient.

Retain superseded material and the reason it was not used. If authority remains unresolved, cite the conflicting passages, set the conflict flag and identify the confirmation required. Do not average competing values or silently select one source.

## 8. Three annotated synthetic cases

All documents and facts in this section are invented. The English excerpts demonstrate annotation and arithmetic; they are not natural tender data, model predictions or evidence of Russian/Kazakh performance. Any later localized versions need language review and remain in the same diagnostic families as their originals.

The comparison below brings the two sides of each assessment together. The detailed records that follow retain their separate tender and company references.

| Case | Tender condition | Company evidence | Expected status | Decisive point |
| --- | --- | --- | --- | --- |
| **SYN-01: RAM** | At least **16 GB** of installed RAM per laptop | **32 GB** of installed RAM per laptop | **`met`** | Same property and unit; the value satisfies the minimum |
| **SYN-02: delivery** | Last permitted date: **11 November 2026** | Offered completion: **13 November 2026** | **`unmet`** | A documented commitment exceeds the deadline by two calendar days |
| **SYN-03: warranty** | At least **24 months** from acceptance | Competing offers: **12 months** and **36 months**; neither established as applicable | **`unknown`** | The applicable offer must be established before comparison |

*Expected statuses are reference judgments for synthetic examples. They are not outputs from an implemented TenderGuard model.*

### 8.1. SYN-01: minimum RAM requirement

#### SYN-T01-v1: tender excerpt

> The supplied laptop must include at least 16 GB of RAM. The quantity refers to installed RAM in each laptop, using the GB unit stated in this specification.

#### SYN-C01-v1: company excerpt

> Our offer for this tender specifies 32 GB of installed RAM in each laptop, using the same GB unit as the tender specification.

| Annotation field | Value |
| --- | --- |
| Assessment and family | `SYN-01-R01`; `SYN-F01` |
| Origin, language and partition | Synthetic; English; diagnostic |
| Evidence scope | Full synthetic package: `SYN-T01-v1` and `SYN-C01-v1`; profile `SYN-P01-v1` |
| Atomic requirement | Each offered laptop must have at least 16 GB of installed RAM |
| Normalized constraint | Subject: installed RAM per laptop; operator: `>=`; value: `16`; unit: `GB` |
| Tender reference | [SYN-T01-v1, excerpt paragraph 1](#syn-t01-v1-tender-excerpt) |
| Company reference | [SYN-C01-v1, excerpt paragraph 1](#syn-c01-v1-company-excerpt) |
| Company fact | 32 GB of installed RAM per offered laptop |
| Reference status | `met` |
| Rationale | `32 >= 16`; the two sources describe the same property, unit and item scope |
| Missing fields and conflict | None needed for this comparison; conflict: false |

Exactly 16 GB would also satisfy this requirement. An offer describing 32 GB of storage without a RAM value would leave the RAM assessment `unknown`.

### 8.2. SYN-02: calendar-day delivery deadline

#### SYN-T02-v1: tender excerpt

> Delivery must be completed within 10 calendar days after the contract is signed. For this offer comparison, the contract signing date is fixed at 1 November 2026. The signing date is excluded: 2 November is day 1. Completion on day 10 is permitted. No adjustment to working days applies.

#### SYN-C02-v1: company excerpt

> For the contract signed on 1 November 2026, our offer commits to completing delivery on 13 November 2026.

| Annotation field | Value |
| --- | --- |
| Assessment and family | `SYN-02-R01`; `SYN-F02` |
| Origin, language and partition | Synthetic; English; diagnostic |
| Evidence scope | Full synthetic package: `SYN-T02-v1` and `SYN-C02-v1`; profile `SYN-P02-v1` |
| Atomic requirement | Complete delivery no later than calendar day 10 after the stated signing date |
| Normalized constraint | Anchor: `2026-11-01`; anchor excluded; duration: `<= 10 calendar days`; last permitted completion date: `2026-11-11` |
| Tender reference | [SYN-T02-v1, excerpt paragraph 1](#syn-t02-v1-tender-excerpt) |
| Company reference | [SYN-C02-v1, excerpt paragraph 1](#syn-c02-v1-company-excerpt) |
| Company fact | Offered completion date: `2026-11-13` |
| Reference status | `unmet` |
| Rationale | 2 November is day 1, 11 November is day 10 and 13 November is day 12. The offered completion exceeds the permitted date by two calendar days |
| Missing fields and conflict | None needed for this date-level comparison; conflict: false |

The result follows from an explicit company commitment. If the offer stated only “10 working days,” the calendar-day limit could not be checked without the applicable working-day calendar and counting details.

### 8.3. SYN-03: unresolved warranty commitments

#### SYN-T03-v1: tender excerpt

> Each supplied laptop must have a full hardware warranty lasting at least 24 months from acceptance. The warranty duration must be confirmed in the applicable company offer.

#### SYN-C03-A-v1: first company excerpt

> For the laptops in this tender, our offer provides a full hardware warranty lasting exactly 12 months from acceptance.

#### SYN-C03-B-v1: second company excerpt

> For the laptops in this tender, our offer provides a full hardware warranty lasting exactly 36 months from acceptance.

The synthetic package contains both offer excerpts. Neither identifies the other as superseded, and no recorded confirmation establishes which offer applies. Both describe the same laptops and warranty scope.

| Annotation field | Value |
| --- | --- |
| Assessment and family | `SYN-03-R01`; `SYN-F03` |
| Origin, language and partition | Synthetic; English; diagnostic |
| Evidence scope | Full synthetic package: `SYN-T03-v1`, `SYN-C03-A-v1` and `SYN-C03-B-v1`; profile `SYN-P03-v1` |
| Atomic requirement | Full hardware warranty of at least 24 months from acceptance |
| Normalized constraint | Subject: full hardware warranty per laptop; operator: `>=`; value: `24`; unit: `months`; anchor: acceptance |
| Tender reference | [SYN-T03-v1, excerpt paragraph 1](#syn-t03-v1-tender-excerpt) |
| Company reference A | [SYN-C03-A-v1, excerpt paragraph 1](#syn-c03-a-v1-first-company-excerpt) |
| Company reference B | [SYN-C03-B-v1, excerpt paragraph 1](#syn-c03-b-v1-second-company-excerpt) |
| Company facts | Two competing full-warranty durations: exactly 12 months and exactly 36 months |
| Reference status | `unknown` |
| Rationale | Offer A would fail the requirement and offer B would satisfy it, but the applicable offer is not established. Selecting either would require an unsupported assumption |
| Missing field and conflict | Confirmation of the applicable offer or a documented supersession relationship; conflict: true |
| Next action | Obtain confirmation identifying the applicable offer; retain the original unknown assessment and create a new assessment if the evidence scope changes |

An absent warranty statement would also produce `unknown`, with no company citation invented. It would be recorded as missing evidence rather than as a contradiction. These two reasons for uncertainty remain distinct in error analysis.

### 8.4. Controlled variations: the numeric boundary

The RAM example also supports a direct check of the decision boundary. Keep [SYN-T01-v1](#syn-t01-v1-tender-excerpt) unchanged and replace only its company excerpt with one of the alternatives below. Each row is a separate diagnostic package, not an additional source to combine with the original 32 GB offer. The laptop scope and the stated GB convention remain unchanged.

The quoted cell is the complete synthetic company excerpt for its variant document. Its locator is this table's row identified by the document ID. All variants remain in `SYN-F01` and in the diagnostic partition.

| Variant company document | Company excerpt | Expected status | Annotation reason |
| --- | --- | --- | --- |
| `SYN-C01-EQ-v1` | “Each offered laptop includes **16 GB of installed RAM**.” | **`met`** | Equality satisfies “at least 16 GB” |
| `SYN-C01-BELOW-v1` | “Each offered laptop includes **15 GB of installed RAM**.” | **`unmet`** | The applicable stated value is below the minimum |
| `SYN-C01-MISSING-v1` | “The **RAM capacity is not specified** in this offer.” | **`unknown`** | The required value is absent; it must not be interpreted as zero |
| `SYN-C01-STORAGE-v1` | “Each offered laptop includes **32 GB of SSD storage**. RAM capacity is not specified.” | **`unknown`** | A storage value cannot establish the amount of RAM |

Together with the original 32 GB case, these variations check whether an assessment respects the operator, detects a violation, preserves uncertainty and matches the correct hardware property. A changed company fact does not alter the tender quotation or its source reference.

### 8.5. Controlled variations: the calendar boundary

For SYN-02, retain the tender's stated counting convention. The timeline makes the boundary explicit:

| Signing date | First counted day | Day 9 | **Day 10** | Day 11 | Day 12 |
| --- | --- | --- | --- | --- | --- |
| 1 Nov 2026 | 2 Nov 2026 | 10 Nov 2026 | **11 Nov 2026** | 12 Nov 2026 | 13 Nov 2026 |
| Excluded from count | Counting begins | Within limit | **Last permitted date** | One day late | Two days late |

Use the following alternative company excerpts against the unchanged [SYN-T02-v1](#syn-t02-v1-tender-excerpt). Each row replaces the original company excerpt in its own package. The row's document ID is its source locator; all variants remain in `SYN-F02` and the diagnostic partition.

| Variant company document | Company excerpt | Expected status | Comparison |
| --- | --- | --- | --- |
| `SYN-C02-EARLY-v1` | “For the contract signed on 1 November 2026, our offer commits to completing delivery on **10 November 2026**.” | **`met`** | Day 9 is within the ten-day limit |
| `SYN-C02-EQ-v1` | “For the contract signed on 1 November 2026, our offer commits to completing delivery on **11 November 2026**.” | **`met`** | Completion on day 10 is explicitly permitted |
| `SYN-C02-LATE-v1` | “For the contract signed on 1 November 2026, our offer commits to completing delivery on **12 November 2026**.” | **`unmet`** | Day 11 exceeds the limit by one calendar day |

These cases isolate the completion date. They do not introduce a different day type, signing date or counting rule. A model that counts the signing date as day 1 would incorrectly reject the equality case.

### 8.6. Resolving an unknown without discarding evidence

SYN-03 checks a different issue: more evidence is useful only when it resolves the relevant uncertainty. The competing warranty offers remain visible in all three scenarios below. A confirmation is accepted for this synthetic exercise only when its authority to identify the applicable company offer is established as part of the fixture context.

| Scenario | Additional evidence | Expected status | Reason |
| --- | --- | --- | --- |
| Original SYN-03 | No confirmation; both offers remain unresolved | **`unknown`** | Neither 12 nor 36 months can be selected as applicable |
| `SYN-C03-CONF-A-v1` | Authorized company confirmation: “For this tender, **offer SYN-C03-A-v1 is applicable and replaces SYN-C03-B-v1**.” | **`unmet`** | The applicable offer now establishes exactly 12 months, below the required 24 |
| `SYN-C03-CONF-B-v1` | Authorized company confirmation: “For this tender, **offer SYN-C03-B-v1 is applicable and replaces SYN-C03-A-v1**.” | **`met`** | The applicable offer now establishes exactly 36 months, satisfying the required 24 |

The quoted confirmation in each row is its complete synthetic source excerpt, located by the row's document ID. The two confirmations are alternative diagnostic scenarios; they are never included together. They remain in `SYN-F03` and retain [SYN-T03-v1](#syn-t03-v1-tender-excerpt) as the tender source.

A resolved assessment cites the tender, the applicable warranty offer and the confirmation that establishes its authority. The earlier offer is retained with its superseded status. The original `unknown` finding belongs to the earlier evidence set and is preserved; the revised evidence produces a new assessment.

### 8.7. Using the cases in implementation

The three base cases and their controlled variants provide a small, inspectable diagnostic set. They are related examples within three families, not independent natural observations or a balanced performance benchmark.

When the analysis workflow is available, record the actual status, cited source IDs, explanation and processing outcome for each variant beside its expected annotation. A check succeeds only when the status and its evidence agree. A correct label based on the wrong property, wrong date rule or unsupported choice of offer does not satisfy the case. Record failed calls as processing failures instead of changing the reference label.

Use the same variant packages for the single-prompt and staged workflows. Preserve the original model outputs before correction. Their comparison can then show whether an error concerns arithmetic, evidence selection, missing information or document authority. No actual model results are recorded in these tables.

## 9. Annotation quality and preparation for experiments

Two annotators will first work independently on the six-family development pilot without model predictions. They will identify atomic requirements, source passages, company facts and statuses. An alignment step will establish corresponding obligations before measuring status agreement; extraction disagreements and unmatched obligations will be reported separately.

For matched assessments, report the number of paired labels, class counts, raw agreement and Cohen's kappa before adjudication. A small or highly imbalanced sample can make agreement statistics unstable; if kappa is undefined, report it as undefined with the counts. Resolve disagreements through the written rules, retaining both original labels and the decision reason. Unresolved specialist questions remain outside the scored reference set with a documented exclusion.

The finalized reference set will use independent annotation and recorded adjudication. After a material guide revision, revisit affected development annotations. Test preparation must use the fixed guide, and later corrections must follow the versioning rule in Section 4.

For retrieval, annotate relevant passages and acceptable complete evidence sets, including tender and company passages where both are needed. Use the evaluation plan's proposed grades of 0 for irrelevant, 1 for partially relevant and 2 for directly relevant, subject to pilot review. Record unanswerable queries separately. Reference queries are permitted in the retrieval benchmark; they must not silently become queries for the end-to-end workflow.

Before release, check that every assessment has a recoverable tender citation, that each cited company fact exists in its recorded version, and that the status agrees with the normalized condition. Review empty evidence lists, contradictions, conversions and calendar calculations explicitly. Check that no family overlaps development and test, no reference labels appear in retrieval text and no private evidence is included in the public export.

Daniyar maintains the corpus and annotation guide. Rassul reviews the rules, examples and integration needs. Ramazan coordinates permission and processing-policy questions within his privacy responsibilities. Independent annotation assignments and actual review evidence must be recorded when the work is performed.

Natural corpus acquisition, permissions, language review and annotation agreement remain to be established through collection and the pilot. The present deliverable provides the dataset design, annotation rules and three worked synthetic cases; their expected labels are authored reference examples, not measured model results or completed independent adjudication.
