# Existing systems comparison

## Purpose and scope

This comparison addresses predefence component 4: compare 3–5 relevant systems
against 6–10 consistent criteria and explain the need for the proposed solution
using evidence. It covers **five existing systems and ten criteria**, with
TenderGuard shown separately as a planned implementation.

The target workflow is an SME reviewing a tender package against its own company
documents before deciding how to prepare an application. The comparison considers
discovery and team workflow as well as documentary analysis; it does not assume
that every procurement service has the same purpose.

| System | Regional relevance | Reason for selection |
| --- | --- | --- |
| Tenderbot | Kazakhstan | Local tender discovery, monitoring and integration alternative closest to the initial market [S01, S02]. |
| Tenderplan | Russia | Supplier search and team workflow, including search within attachments [S03–S05]. |
| Kontur.Zakupki | Russia; vendor also claims CIS coverage | Established search and analytics, with an announced document assistant that overlaps with the proposed workflow [S06, S07]. |
| BiCoTender | Russia; vendor also claims CIS coverage | Supplier analytics, document preanalysis and tender relationship management [S08–S10]. |
| UZEX eTender | Uzbekistan | An official procurement transaction platform: a contextual comparator for discovery and participation, rather than a direct SME analysis product [S11, S12]. |

The sample represents Kazakhstan, Russia and Uzbekistan. It does not establish
coverage of every CIS market. UZEX is included to expose the difference between
an operator's transaction workflow and a supplier's internal analysis workflow.
TenderGuard is not intended to replace procurement operators or replicate a
commercial aggregator's entire database.

## Method and evidence rules

The review combines official product pages and documentation with two interactive
public-browser checks using the same Russian procurement query. The
[observation log and screenshots](evidence/checks.md) record
the actions, outcomes and access boundaries. Source access dates appear in the
[source register](#source-register).

Evidence labels used throughout the matrix:

- **D — Documented:** an official source describes the capability; its quality
  has not been independently established.
- **O — Observed:** a public interface or result was inspected in the recorded
  browser check; the label applies only to that observation.
- **A — Announced:** a supplier describes a future rollout; availability was not
  demonstrated.
- **NS — Not specified:** the reviewed material does not establish the capability
  at the stated level. This is not evidence that the capability is absent.
- **P — Planned:** a TenderGuard design commitment from the
  [project proposal](../project-proposal/proposal.md), not an implemented or measured advantage.

There is no numerical ranking. Unspecified capabilities cannot fairly be scored
as zero, and planned capabilities cannot be scored as delivered. Vendor marketing
claims about speed, completeness or business outcomes are not measurement results.

**Availability qualification:** S06 says advanced Kontur AI functions start on
**23 October 2026**, after the recorded checks. Its assistant and report are
therefore marked A. Smart search is described separately as already available on
paid plans other than Light. Recheck the rollout before presenting the matrix.

## Comparison matrix

Each criterion is applied to every system. A search filter, a company identifier
and a counterparty score do not by themselves establish matching against the
supplier's own supporting documents. Likewise, a Russian interface is not a
validated Russian/Kazakh document-processing benchmark.

| Criterion | Tenderbot | Tenderplan | Kontur.Zakupki | BiCoTender | UZEX eTender | TenderGuard — proposed |
| --- | --- | --- | --- | --- | --- | --- |
| **C1. Regional procurement scope** | D: Kazakhstan government, quasi-public and commercial sources [S01, S02]. | D: Russian government and commercial procurement [S03]. | D: Russia and CIS procurement coverage claimed; completeness not verified [S07]. | D: Russian/CIS tender coverage claimed; completeness not verified [S08]. | D/O: Uzbekistan tender/competition portal [S11, S12; T02]. | P: uploaded tender packages for a Kazakhstan pilot; comprehensive portal coverage excluded [proposal](../project-proposal/proposal.md). |
| **C2. Discovery and monitoring** | D/O: public keyword search and filters; email/Telegram monitoring advertised [S01; T01]. | D: saved search, filters and change notifications [S03, S04]. | D: search templates, filters and notifications [S07]. | D: filtered search and alerts [S09]. | O: public lots and filters; monitoring alerts NS in this review [S11; T02]. | P: analyse an uploaded package; market-wide discovery and alerts outside core scope [proposal](../project-proposal/proposal.md). |
| **C3. Document search and source-backed question answering** | O: documentation-search control visible, not executed; generated cited answers NS [S01; T01]. | D: keyword search within documents/archives and document viewer; generated cited answers NS [S03]. | A: assistant answers procurement questions and links to sources; not executed [S06]. | D: document preanalysis advertised; cited conversational answers NS [S08, S09]. | NS: document QA not established by public lots or participation guides [S11, S12]. | P: answers over permitted documents with resolvable citations and an insufficient-evidence outcome [proposal](../project-proposal/proposal.md). |
| **C4. Conditions, requirements and risk analysis** | D: procurement/supplier analytics; structured requirement extraction NS [S01]. | D: customer/competitor analytics; structured documentary compliance extraction NS [S04]. | A: report covering conditions, risks and preparation actions [S06]. | D: express document preanalysis of conditions and risks; model type and accuracy not established [S08, S09]. | NS: automated requirement/risk extraction not established in reviewed portal material [S11, S12]. | P: atomic requirements and bounded risk findings; documentary fit separated from legal applicability [proposal](../project-proposal/proposal.md). |
| **C5. Matching against the SME's own documentary evidence** | NS: supplier analytics/API do not establish two-sided evidence matching or explicit met/unmet/unknown [S01, S02]. | NS: own-file attachments and workflow do not establish this matching contract [S04]. | NS: company-based search personalization does not establish this matching contract [S06]. | NS: preanalysis/TRM descriptions do not establish this matching contract [S08, S09]. | NS: registration and participation documentation do not establish this matching contract [S11, S12]. | P: selected company-profile version; met/unmet/unknown with tender citations and supporting company evidence where available [proposal](../project-proposal/proposal.md). |
| **C6. Russian/Kazakh language evidence** | O: Russian search interface/query; Kazakh analysis quality NS [T01]. | D: Russian product material; Kazakh analysis quality NS [S03]. | D: Russian product material; Kazakh analysis quality NS [S06, S07]. | D: Russian product material; Kazakh analysis quality NS [S08, S09]. | O: locale controls and Uzbek interface; Russian switch not validated; Kazakh analysis quality NS [T02]. | P: RU/KK documents, evaluated separately; no achieved bilingual accuracy claim [proposal](../project-proposal/proposal.md). |
| **C7. Collaboration and traceability** | NS: public search/API pages do not establish internal review/history or immutable analysis inputs [S01, S02]. | D: assignees, comments, own attachments and processing history; immutable analysis manifest NS [S04]. | D: team board, comments, statuses and assignees; immutable analysis manifest NS [S07]. | D: comments/labels, multiple users and TRM by plan; immutable analysis manifest NS [S09]. | D: buyer/supplier participation workflows; internal SME review and analysis manifests NS [S12]. | P: human review and version-bound runs; profile/document edits must not rewrite earlier findings [proposal](../project-proposal/proposal.md). |
| **C8. Deployment and confidential-context controls** | NS: reviewed public service/API pages do not establish customer-controlled local inference or blocked external model routes [S01, S02]. | NS: API authentication documentation does not establish these processing controls [S05]. | NS: reviewed feature material does not establish these processing controls [S06, S07]. | NS: reviewed product/plan material does not establish these processing controls [S08, S09]. | NS: procurement portal/manuals do not establish these processing controls [S11, S12]. | P: organization isolation and policy-checked outbound calls; blocked analysis if no permitted route exists; local inference optional [proposal](../project-proposal/proposal.md). |
| **C9. Integration and export evidence** | D: JSON/Bearer API for CRM/ERP; not executed [S02]. | D/O: Swagger API documentation, OAuth/token access; endpoints not executed [S05; T03]. | NS: integration/export capability not established by the pages reviewed [S07]. | D: Excel export by plan; API/CRM integration documented in an older announcement, current operation unverified [S09, S10]. | O: Excel export control visible; download not executed [T02]. | P: REST service; downloadable report export optional; no production integration delivered [proposal](../project-proposal/proposal.md). |
| **C10. Access model and assessment boundary** | O/D: anonymous search; details partly subscription-gated; three-day trial advertised, not activated [S01; T01]. | D: free-start invitation and account registration; authenticated workflow not tested [S03, S04]. | D/A: paid smart-search access; advanced AI plan announced; no paid account tested [S06]. | D: tiered subscription, with preanalysis/TRM depending on plan; no paid workflow tested [S09]. | O/D: anonymous discovery; registration for participation; fees and bidding not evaluated [S11, S12; T02]. | P: research prototype; public/synthetic demo inputs; no commercial pricing or readiness claim [proposal](../project-proposal/proposal.md). |

## What the evidence supports

Existing services already address substantial parts of the workflow. Their
documented strengths include tender sourcing, monitoring, customer/supplier
analytics, team coordination and, for UZEX, procurement transactions. Rebuilding
these capabilities would widen the diploma beyond its proposed pilot. TenderGuard
can instead begin with packages obtained through permitted existing channels.

AI summaries and citations alone are an insufficient differentiation argument:
Kontur's announced assistant explicitly overlaps with cited answers, while BiCo
advertises documentary preanalysis. These observations narrow the proposed
contribution; they do not establish equivalent accuracy or end-to-end behaviour.

The reviewed public sources do **not establish the complete combination** of
company-document matching with explicit uncertainty, version-bound review,
RU/KK evaluation and enforceable confidential-context routing. This is a gap in
the available evidence, not proof that no competitor offers the combination.
Enterprise configurations, private demonstrations or a newer release could change
the assessment.

## Proposed contribution and how it will be evaluated

| Proposed capability | Practical reason | Planned verification, not a result |
| --- | --- | --- |
| Company-specific requirement/evidence matrix | A useful summary still leaves the SME to establish whether its own evidence supports a condition. | Annotated tender/company pairs; requirement extraction F1, status macro-F1 and citation support. Use the same inputs for single-prompt RAG and staged analysis. |
| Explicit uncertainty | Missing or ambiguous evidence should trigger clarification rather than a confident eligibility claim. | Include absent, expired, irrelevant and conflicting evidence; measure unsupported met decisions and correct unknown outcomes. |
| Version-bound findings and review | A reviewer must know which tender revision and company documents supported the decision. | Change an input, create a new run, and verify that the earlier run still resolves its original citations and review record. |
| Controlled processing routes | An organization may prohibit sending confidential context to a hosted provider. | Observe outbound requests, retries and fallbacks with synthetic restricted data; a prohibited route must receive no restricted payload. Test cross-organization access separately. |
| Measured Russian/Kazakh performance | Interface localization does not establish reliable extraction from bilingual documents. | Report retrieval, extraction and evidence-matching results separately by language on held-out document families. |

These are engineering and research hypotheses. More agents and a locally hosted
model are not assumed to improve quality or establish privacy automatically.
Local inference is an optional route; policy enforcement must also block unsafe
fallbacks. A bounded legal flag requires an applicable, identified legal source;
documentary matching alone is not a legal opinion.

A small acceptance fixture can make the proposed behaviour concrete: a synthetic
tender requires delivery within 10 calendar days; an applicable supported
seven-day commitment is met, an incompatible minimum of 14 days is unmet, and
missing or ambiguous evidence is unknown. The evaluator must first establish
that the company evidence applies to the same goods and conditions. This fixture
has **not** been run against vendor document-analysis services.

## Interactive checks and limitations

| Check | Common scenario and actual outcome | What it establishes |
| --- | --- | --- |
| [T01](evidence/checks.md#t01-tenderbot-public-search) | Search Tenderbot for `поставка компьютеров`; query and six displayed results observed, with some details subscription-gated. | Public discovery and an access boundary; not search accuracy or document-analysis quality. |
| [T02](evidence/checks.md#t02-uzex-public-search) | Submit the same query in UZEX's product/lot filter; no-data message observed while the catalogue counter remained populated. | Filter interaction and an inconsistent displayed result state; not a reliable zero-result count or a language-quality finding. |
| [T03](evidence/checks.md#t03-tenderplan-api-documentation) | Inspect Tenderplan's public Swagger documentation without authorization or endpoint execution. | Documented API surface and access requirements; not integration correctness. |

The two common-query checks are reproducible public-interface smoke tests, not an
equal-corpus benchmark. The systems index different jurisdictions and document
collections, so their result counts cannot be compared as precision, recall or
market coverage. No private company documents were uploaded, trial accounts
created, payments made or applications submitted. Paid document-analysis features
and provider data retention were not independently tested.

To assess vendor analysis quality later, obtain an authorized account and reuse
the same permitted synthetic tender/company pack, questions and scoring rules.
Record product plan, model/configuration if disclosed, citations, unknown handling,
failures and total cost. Until then, keep those matrix entries documented,
announced or unspecified rather than labelling them experimentally verified.

This comparison justifies a focused design and further investigation. It does
not establish SME demand or measured time savings; actual relevance evidence
belongs in the separate interview/relevance deliverable.

## Source register

Pages can change; source IDs and access dates make the evidence traceable.

| ID | Primary source | Accessed | Relevant evidence and qualification |
| --- | --- | --- | --- |
| S01 | [Tenderbot product and public search](https://tenderbot.kz/) | 2026-10-21 | Kazakhstan scope, monitoring and trial invitation; browser observation T01. |
| S02 | [Tenderbot API](https://tenderbot.kz/pages/api) | 2026-10-21 | Procurement feed and integration contract; vendor documentation, no API execution. |
| S03 | [Tenderplan search](https://tenderplan.ru/search) | 2026-10-21 | Regional scope, attachment search, filters and document viewing. |
| S04 | [Tenderplan product](https://tenderplan.ru/) | 2026-10-21 | Team workflow and history descriptions; landing-page examples are not account observations. |
| S05 | [Tenderplan API documentation](https://tenderplan.ru/api/doc/) | 2026-10-21 | JavaScript-rendered Swagger documentation checked in browser, T03. |
| S06 | [Kontur.Zakupki AI announcement](https://zakupki.kontur.ru/site/new-features/ai) | 2026-10-21 | Separates available search from announced advanced functions; [page capture](evidence/S06-kontur-announcement.png). |
| S07 | [Kontur.Zakupki features](https://zakupki.kontur.ru/site/features) | 2026-10-21 | Discovery, analytics, notifications and team workflow. |
| S08 | [BiCoTender product description](https://www.bicotender.ru/about.html) | 2026-10-21 | Coverage, analytics and preanalysis claims; a later automated refetch returned HTTP 403. |
| S09 | [BiCoTender search plans](https://www.bicotender.ru/tariffs-search.html) | 2026-10-21 | Plan-dependent preanalysis, TRM, collaboration and Excel export; advertised speed not independently timed. |
| S10 | [BiCoTender integration announcement](https://www.bicotender.ru/news/novoye_resheniye.html) | 2026-10-21 | Historical API/CRM announcement published 30 September 2020; current availability not verified; later refetch returned HTTP 403. |
| S11 | [UZEX eTender portal](https://etender.uzex.uz/) and [guides](https://etender.uzex.uz/docs) | 2026-10-21 | Public procurement interface and linked participation guidance; T02. |
| S12 | [UZEX supplier instruction](https://etender.uzex.uz/assets/file/e-tender-instruction-for-provider.pdf) | 2026-10-21 | Official participation instructions; does not establish SME document-analysis functions. |

## Predefence coverage and follow-up

The matrix supplies five systems, ten shared criteria, source references and an
explicit justification for the proposed approach. The evidence folder supplies
two interactive common-scenario logs and screenshots. Together these address
the existing-system comparison deliverable; they do not complete the separate
technology comparison, relevance study or final experimental evaluation.

Before submission, recheck the Kontur rollout, refresh any changed plan claims,
and obtain peer review of the interpretations. Do not replace NS with an absence
claim without stronger evidence. If a vendor demonstrates the proposed matching
and privacy workflow, revise the gap statement and retain the scientific
comparison as an evaluation question rather than a uniqueness claim.
