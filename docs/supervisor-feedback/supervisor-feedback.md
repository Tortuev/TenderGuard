# Component 11 — Supervisor feedback record

| | |
| --- | --- |
| Project | Design and Implementation of a Privacy-Preserving Multi-Agent RAG Platform for Automated Tender and Compliance Analysis for SMEs (TenderGuard) |
| Team | Daniyar Kairatov · Rassul Akhmetov · Ramazan Talgatov |
| Supervisor | Almas Ospanov, Senior Lecturer, School of Software Engineering, Astana IT University |
| Reviews in this record | **R1** — written review of the full first-predefence package, 22 October 2026 (commit `608d167`) · **R2** — verification of the team's changes before the `pre-defense-1` tag, 23 October 2026 (commit `3489f5e`): repository check done; re-checked on 24 October 2026, no new commits; live part pending |
| Who writes what | The supervisor writes sections 1–3 and closes items in R2. The team writes only the *Team response* fields and the PR links. Ramazan Talgatov (project manager) keeps the summary table current. |

This record replaces the earlier "guidance and response record". Its three entries (FB-01 to FB-03) are kept in section 1. Nothing below is backdated: the repository was created on 17 October 2026, so no repository review could take place before then.

## How the team responds

1. For each comment, create a Notion task and use its ID everywhere: branch `TG-xx-sr1-yy-short-topic`, PR title `TG-xx: SR1-yy …`, commit messages `TG-xx: …`.
2. In the PR description, state the comment ID, what changed and how you checked it. Another team member reviews and approves the PR before it is merged with a merge commit.
3. Fill in the *Team response* line under the comment (decision, reason, PR link, date) and the matching row of the summary table.
4. Disagreeing is allowed. Write the reason; I decide in R2.
5. Do not mark anything *Closed*. Only the supervisor closes items, in R2.
6. Do not rewrite history: no force-push, no squashing of commits that are already on `main`.

## 1. Guidance given before the repository review (not counted as a review)

| Ref | Guidance | How the team used it | Supervisor note (22 Oct) |
| --- | --- | --- | --- |
| G-01 (was FB-01) | Keep proposal and research materials in separate repository folders; reference them from the README; summarise work in the tracker; explain methods and algorithms in Markdown files. | Component folders under `docs/`, linked from the [README](../../README.md). | Implemented. |
| G-02 (was FB-02) | Department requirements for pre-defense 1: an answer for each component, real feedback from potential users, a critical literature synthesis, an evidenced comparison of 3–5 systems against 6–10 criteria. | [Assembly checklist](https://github.com/Tortuev/TenderGuard/blob/608d1679ce56a91f1a618a8c2ba52da6ff25ae67/docs/predefence/checklist.md) (deleted on 23 October, link pinned to `608d167`) and the component documents. | Addressed in form. The substance is reviewed in R1 below; relevance evidence (SR1-06) is not yet sufficient. |
| G-03 (was FB-03) | Supervisor architecture baseline: diagram and module table (13 October 2026). | Retained the structure; refinements documented in [architecture.md](../architecture/architecture.md#refinements-of-the-supplied-architecture) and [ml-technologies.md](../technology-comparison/ml-technologies.md#2-alignment-with-the-supplied-architecture). | Refinements accepted, see decision D-03. |

## 2. Supervisor review R1 — 22 October 2026

**Scope.** The whole package on `main` at commit [`608d167`](https://github.com/Tortuev/TenderGuard/commit/608d167) (22 October 2026, 12:40 +05:00): README, the eleven components, the presentation, the database foundation, CI and the Git history.

**What I checked directly.**
- Read every document in `docs/`.
- Inspected the history of all branches.
- Ran the database test suite: 59 tests passed and `ruff` reported no issues. I ran it against PostgreSQL 16; CI runs it on PostgreSQL 17.
- Opened `presentation.pptx`.

### 2.1 Overall assessment

**Strengths.**
- The [evaluation plan](../evaluation-plan/evaluation-plan.md) and the [dataset/annotation guide](../dataset/dataset-and-annotation.md) are the strongest part of the package. They define:
  - a lexical retrieval reference (B0) and a single-prompt baseline (B1) against the staged pipeline (B2), with the same frozen evidence pack for B1 and B2;
  - document-family splits with Russian and Kazakh results reported separately;
  - retained failures and a planned bootstrap.
- The [requirements](../requirements/requirements.md) have concrete, testable acceptance criteria.
- The status semantics are sound and consistent across all documents: missing evidence is `unknown`, not `unmet`; a processing failure is not a compliance finding; legal applicability is separate (`legal_unknown`).
- The [existing-systems comparison](../system-comparison/existing-systems.md) labels its evidence honestly (Documented / Observed / Announced / Not specified), with screenshots.
- The database foundation is real and tested.
- Throughout the package you separate what exists from what is planned. Keep doing that.

**Main problems for 24 October** (details in the comments below):

1. **Process evidence (SR1-01).**
   - The repository was created on 17 October.
   - 52 of the 54 commits are dated 21–22 October.
   - 22 of the 35 commits on `main` were pushed directly, without a pull request.
   - Only 8 of the 38 non-merge commits mention a task ID.
   - No pull request shows a review by another member.

   The department requirement warns exactly against this pattern ("uploading the entire project immediately before a pre-defense does not demonstrate continuous development"). The past cannot be changed. It can only be explained honestly and corrected from now on.
2. **Relevance evidence (SR1-06).** The three interviews have no date, method, respondent context or consent record. The separate recommendations text refers to different roles and to "interview scenarios".
3. **Security, privacy and non-functional requirements are absent (SR1-10).** The diploma title promises a *privacy-preserving* platform, so this is the largest content gap.
4. **Submission basics (SR1-16).**
   - No `pre-defense-1` tag.
   - No submission note.
   - No setup/run/test section in the README.
   - `.env.example` was deleted although `compose.yaml` requires it.

**Readiness on 22 October:** not yet ready to tag. The design content is above the usual level for a first pre-defense. It becomes ready when the four blockers are resolved or honestly stated as limitations in the submission note.

### 2.2 Supervisor decisions

| Ref | Decision |
| --- | --- |
| D-01 | **Task tracker.** Notion is accepted instead of YouTrack for this project. Conditions: the committee gets read-only access to the board; every task shows the responsible member, priority, deadline and acceptance criteria; each task links to its branch/PR. State this decision on the project-management slide. |
| D-02 | **Supervisor details** for the proposal, README and title page: *Almas Ospanov, Senior Lecturer, School of Software Engineering, Astana IT University*. This closes the "supervisor field to be confirmed" items in the [proposal](../project-proposal/proposal.md) and README. |
| D-03 | **Architecture refinements accepted:** the "Inference Gateway" name; a durable PostgreSQL-backed worker instead of in-process tasks; a separate vector configuration per embedding model (the `vector(1024)`, cost and status labels in my diagram were illustrative); exact search before approximate indexing; OCR outside the core path; classification of the full payload rather than identifier masking alone. |
| D-04 | **Pilot category:** IT and office equipment is accepted provisionally for pre-defense 1. Confirm or change it after the 6-family feasibility pilot, before pre-defense 2. |
| D-05 | **Scope:** local generation and fine-tuning stay optional extensions, not core deliverables. The core must work with a permitted hosted route and synthetic or permitted data. |

### 2.3 Summary of R1 comments

Severity: **B** = blocker for the 24 October tag; **M** = major, fix by 24 October or list it as a known limitation with a date; **m** = minor, by pre-defense 2.

Status columns updated in R2 (23 October 2026, commit `3489f5e`) and confirmed in the re-check on 24 October 2026: no item changed status. A *PR / commit* entry shows where the supervisor found a related change; the team must still confirm it in its response (SR2-01).

| ID | Topic | Sev. | Owner | Team decision | PR / commit | Status after R2 |
| --- | --- | --- | --- | --- | --- | --- |
| SR1-01 | Continuous contribution and review evidence | B | All; Ramazan coordinates | Not recorded | — | Open |
| SR1-02 | Task IDs, branch names, commit messages | M | All | Not recorded | — | Open |
| SR1-03 | Git identities | m | Rassul | Not recorded | — | Open |
| SR1-04 | Disclosure of AI assistance | M | All; Rassul integrates | Not recorded | — | Open |
| SR1-05 | Proposal: measurable objectives, supervisor details | M | Rassul | Not recorded | `3489f5e` (title only) | Partly addressed |
| SR1-06 | Interview provenance and relevance synthesis | B | Ramazan | Not recorded | — | Open |
| SR1-07 | Literature: Kazakh, procurement and gateway sources | M | Daniyar (all contribute) | Not recorded | — | Open |
| SR1-08 | Existing systems: local portal and status-quo alternative | M | Rassul | Not recorded | — | Open |
| SR1-09 | Technology decisions outside ML | M | Ramazan | Not recorded | `9e42ec6` (partial) | Partly addressed |
| SR1-10 | Security, privacy and non-functional requirements | B | Ramazan; Rassul integrates | Not recorded | `9e42ec6` | Substantially addressed |
| SR1-11 | Requirement priorities, sources, verification method | M | Rassul | Not recorded | `9e42ec6` (NFR only) | Partly addressed |
| SR1-12 | Diagram exports and traceability to tests | m | Rassul | Not recorded | — | Open |
| SR1-13 | Prototype: outsider walkthroughs and alignment | M | Ramazan | Not recorded | PR #15 (`5c0a609`) | Partly addressed |
| SR1-14 | Evaluation feasibility details | m | Daniyar | Not recorded | — | Open |
| SR1-15 | Project management: Notion access, milestones, risks | M | Ramazan | Not recorded | — | Open |
| SR1-16 | Submission note, tag, setup/run/test, `.env.example` | B | Rassul; Ramazan tags after R2 | Not recorded | — | Open |
| SR1-17 | Presentation | M | All | Not recorded | `1fe5592` | Partly addressed |
| SR1-18 | Legal and data-protection context | M | Ramazan; Daniyar for the provider terms | Not recorded | `9e42ec6` (D3) | Partly addressed |
| SR1-19 | Every member explains every component | M | All | Not recorded | — | Live check |
| SR2-01 | This record and the links to changes | B | Ramazan (all respond) | | | Open (new in R2) |
| SR2-02 | New requirement tables do not render | M | Ramazan | | | Open (new in R2) |
| SR2-03 | Broken links after deletions | M | Rassul | | | Open (new in R2) |
| SR2-04 | Consistency between documents | M | Rassul; each author | | | Open (new in R2) |

### 2.4 R1 comments

#### SR1-01 · Process evidence · B · Owner: all (Ramazan coordinates)

**Finding.**
- History: the first commit is dated 17 October 2026 (`d5f30b1`). 42 commits are dated 21 October and 10 are dated 22 October.
- Direct pushes: the first-parent history of `main` has 35 commits. 12 are merges (10 GitHub pull requests) and 22 are direct pushes after the initial commit. Examples: `69bf61c` architecture, `5bcfebf` requirements, `c67de1e` interviews, `82f2613` research questions, `898e9e8` predefence package.
- Review evidence: the [assembly checklist](https://github.com/Tortuev/TenderGuard/blob/608d1679ce56a91f1a618a8c2ba52da6ff25ae67/docs/predefence/checklist.md) itself records that no formal review entries exist on PRs 8–13.
- Branch protection: the direct pushes show that `main` is either not protected or that the protection is bypassed.

**Why it matters.** The committee assesses the substance and *progression* of each member's contributions and peer review, not the final state alone.

**Required change.**
- **Protect `main` today:** require a PR with 1 approval from another member, block force-push and deletion, and add a tag ruleset so `pre-defense-1` cannot be moved.
- **PRs only from now on:** every change is a PR with a substantive review comment and an approval. A merge or a green CI is not a review.
- **Honest submission note:** in `docs/predefence/pre-defense-1.md`, state that the repository was assembled between 17 and 22 October. If earlier work exists in Notion (task creation dates, drafts), link it as evidence of continuity. Do not rewrite history.

**Done when.**
- A screenshot of the ruleset is in `docs/project-management/`.
- Every PR merged after this review has an approval and at least one review comment.
- The submission note contains the statement.

*Team response:* Decision ☐ Accept ☐ Accept with change ☐ Disagree — reason: … · PR: … · Date: …

#### SR1-02 · Task IDs and commit messages · M · Owner: all

**Finding.**
- Only 8 of the 38 non-merge commits mention a task ID.
- Several messages say nothing about the change: "clearing", "update research", "Add files via upload", "Readme update".
- Daniyar's PRs #8, #10–#13 come from web-editor branches `DaniyarK006-patch-1…5`. Each was merged by its author.

**Required change.**
- Use the format in "How the team responds" for every new branch, PR and commit.
- Optional: add a `commit-msg` hook and a CI check that rejects messages without a task ID.
- For the repository demo, each member prepares one task traced end to end, from the Notion task through branch, PR, review comment, revision and merge commit to the files. Use a PR created after this review.

**Done when.** Each member can show such a trace in under two minutes on 23 October.

*Team response:* Decision ☐ ☐ ☐ — … · PR: … · Date: …

#### SR1-03 · Git identities · m · Owner: Rassul

**Finding.** Rassul commits under two names, `ahmet` and `Kojizz`, with the same e-mail address.

**Required change.** Set one `user.name` (your real name) on every machine you use. Keep the account mapping in the [project-management](../project-management/project-management.md) document.

*Team response:* … · PR: … · Date: …

#### SR1-04 · Disclosure of AI assistance · M · Owner: all (Rassul integrates)

**Finding.** PRs #1 and #2 were merged from branches named `codex/TG-R06-database-foundation` and `codex/TG-R02-literature-review`. This indicates that an AI coding agent produced at least part of the database foundation and of the literature review. The uniform style across the documents suggests wider AI drafting. Using such tools is not forbidden. Concealing it, or being unable to defend the result, is an academic-honesty problem under ДП-AITU-05.

**Required change.** Add `docs/ai-assistance.md` that lists:
- the tools used;
- the artifacts they were used for;
- what each author verified or changed;
- for every literature source, confirmation that the author read the paper itself.

**Done when.** The file exists and each member confirms their part in the PR.

*Team response:* … · PR: … · Date: …

#### SR1-05 · Proposal · M · Owner: Rassul

**Finding.** Objectives O1–O8 have deliverables and verification methods, but no target values or dates, so they are not yet measurable. The supervisor field is marked "to be confirmed".

**Required change.**
- Add a target and a date to each objective, taken from the evaluation plan §9 or provisional. For example:
  - O4: Recall@10 measured on the development families by the pilot date;
  - O6: 0 disclosures in the defined cross-organization and prohibited-route test cases.
- Apply D-02.
- Add a short "complexity" paragraph: what makes this a three-person project.

**Done when.** Each objective has a target and a date, and D-02 is applied.

*Team response:* … · PR: … · Date: …

#### SR1-06 · Relevance evidence · B · Owner: Ramazan

**Finding.**
- There are three transcripts, which meets the minimum of 3 but not the target of 5.
- No transcript has a date, format, duration, interviewer, respondent's company type or size, the respondent's experience, the interview language, or a consent record.
- The answers are uniformly polished. It is not stated whether they are verbatim, summarised or translated.
- [experts-recommendations.md](../relevance/experts-recommendations.md) speaks of "three expert interview scenarios". Its roles ("procurement and bid manager", "operations manager") do not match P01–P03 (two tender specialists and one process organizer).
- A committee member can reasonably ask whether these interviews took place. You must be able to answer with evidence.

**Required change.**
- For each interview, add a metadata block with:
  - date and format;
  - duration;
  - interviewer;
  - respondent role and company category/size (anonymised);
  - language;
  - whether the text is verbatim or a summary;
  - where the consent and the contact are kept privately.
- Reconcile the recommendations file with the transcripts or delete it.
- **If any interview was not actually conducted, remove it and say so.**
- Add a findings table that marks each finding as verified or assumption and links it to the FR/SEC IDs it supports.
- Record scope decisions taken against user requests: deadline reminders, task assignment and report export were asked for by P02/P03 but are deferred or out of scope. Say why.
- Two further interviews may follow after 24 October. List them in the submission note with a date.

**Done when.** Each interview has its metadata block, the findings table exists and the recommendations file is reconciled.

*Team response:* … · PR: … · Date: …

#### SR1-07 · Literature review · M · Owner: Daniyar (all contribute)

**Finding.** The review covers twelve scientific sources from 2023–2025, each with method, transfer limitation and design decision; the ≥ 12 / ≥ 8 minimum is met. There are three gaps:
- no source on the procurement domain;
- no source on Kazakh-language NLP or retrieval, although RU/KK evaluation is one of your claimed contributions;
- no source on privacy middleware for LLM calls, which is your Inference Gateway.

**Required change.**
- Read and add at least three of these. I verified them on 10 October: the DOIs resolve and the full texts are open access.
  - 10.37943/19whrk2878 — multilingual QA adapted to Kazakh, AITU journal, 2024;
  - 10.37943/25nvvs5297 — Kazakh semantic embeddings, AITU journal, 2026;
  - 10.3390/electronics15163554 — privacy middleware for prompt injection and sensitive-data exposure, 2026;
  - 10.14569/ijacsa.2021.0120272 — review of procurement fraud detection, 2021;
  - 10.3390/info17010054 — review of prompt injection in agent systems, 2026.
- Keep normative sources (Law of the Republic of Kazakhstan No. 106-VIII "On public procurement", the personal-data law, the law on artificial intelligence) in a separate list. They are context for the final report, not research literature.
- Plan the path to ≥ 20 references with ≤ 30 % internet sources for the final report (ДП-AITU-19).
- Fix the summary table: rows L15–L18 show only the venue, not the title.
- Make sure the task IDs cited in the review (TG-R13, TG-D15 and others) exist in Notion.

**Done when.** At least three of the listed sources are discussed in the review and the summary table is fixed.

*Team response:* … · PR: … · Date: …

#### SR1-08 · Existing systems · M · Owner: Rassul

**Finding.** The method and evidence labelling are good. Two comparators that matter most for a Kazakhstan SME are missing:
- the official public-procurement portal of Kazakhstan (goszakup.gov.kz), which is the natural local transaction comparator instead of UZEX;
- the status quo many SMEs already use: a general-purpose AI assistant with file upload. It competes directly on criteria C3–C5 and is the alternative against which your privacy argument (C8) is strongest.

Kontur's announced AI functions start on 23 October, which is after your checks.

**Required change.**
- Replace UZEX with goszakup.gov.kz, or justify keeping it.
- Add the general AI assistant either as one of the five systems or as a separate "status-quo" column.
- Recheck Kontur on 23 October and update C3/C4.
- Keep the gap statement as "not established by the reviewed sources".

**Done when.** The matrix includes both comparators (or a written justification) and the Kontur cells are updated.

*Team response:* … · PR: … · Date: …

#### SR1-09 · Technology decisions · M · Owner: Ramazan

**Finding.** [ml-technologies.md](../technology-comparison/ml-technologies.md) records four ML decisions (ADR-ML-01 to ADR-ML-04); three of them compare two alternatives each, so the formal minimum is met. The README, however, presents a full stack (Next.js, FastAPI, Caddy, Docker Compose) for which no decision record exists. The privacy-critical decisions are missing: how payloads are classified and how personal or commercial data are detected before a hosted call, and the authentication/session approach.

**Required change.**
- By 24 October, add two short ADRs with 2–3 alternatives each and criteria taken from the requirements:
  - ADR "data classification and sensitive-data detection for the Inference Gateway": rule/class-based policy vs. NER-based detection (e.g. Presidio with RU support and custom KZ identifiers such as the IIN/BIN) vs. LLM-based classification;
  - ADR "authentication and sessions".
- Frontend, deployment and job-queue ADRs may follow by pre-defense 2.
- Record the retrieval date of the hosted-model price used in ADR-ML-04.

**Done when.** Both ADRs are merged.

*Team response:* … · PR: … · Date: …

#### SR1-10 · Security, privacy and non-functional requirements · B · Owner: Ramazan (Rassul integrates)

**Finding.** TG-T03 has not been published. The requirements contain 16 functional requirements and no SEC or NFR identifiers. The [requirements](../requirements/requirements.md) and the [checklist](https://github.com/Tortuev/TenderGuard/blob/608d1679ce56a91f1a618a8c2ba52da6ff25ae67/docs/predefence/checklist.md) acknowledge this.

**Required change.** At minimum, the Must SEC/NFR requirements, each with an ID, priority, acceptance criterion, verification method and source:

- **SEC-01 Organization isolation** across API, database (row-level security in addition to composite foreign keys), files, jobs, caches and placeholder mappings.
- **SEC-02 Route policy and egress.** No prohibited payload leaves the system; a failed local route never falls back silently to a hosted one; verified by observing outbound requests.
- **SEC-03 Data classification** of documents and of each outbound payload, including derived outputs.
- **SEC-04 Secrets and logging.** No credentials, prompts or document content in logs or error messages.
- **SEC-05 Retention and deletion**, including the effect on historical runs and citations.
- **SEC-06 Untrusted document content.** Defence against prompt injection; verified with a test set.
- **NFR — operations:** recovery and durability of jobs; a performance target with a stated workload (see SR1-14).
- **NFR — cost and use:** an enforced cost ceiling within the $0–50 project budget; RU/KK support; accessibility of the core screens.

**Done when.** The Must SEC/NFR items are merged into the specification and appear in the architecture traceability matrix (SR1-12).

*Team response:* … · PR: … · Date: …

#### SR1-11 · Requirement priorities and sources · M · Owner: Rassul

**Finding.**
- All 16 functional requirements are *Must*, so the priority scheme does not prioritise anything.
- No requirement cites its source (interview, literature, guidance or assumption); the interview IDs P01–P03 appear nowhere in the specification.
- The verification level (unit / integration / e2e / evaluation) is not stated per requirement.

**Required change.**
- Re-rank so that *Must* equals the minimal end-to-end workflow you will demonstrate at pre-defense 2. One candidate for *Should* is the administration and audit views of FR-14; decide the rest yourselves and record the reasons.
- Add *Source* and *Verification method* to each requirement.

**Done when.** Every Must has an acceptance criterion, a verification method and a source.

*Team response:* … · PR: … · Date: …

#### SR1-12 · Diagrams and traceability · m · Owner: Rassul

**Finding.** Six Mermaid views with SVG exports form a good package. Two things are missing:
- the report needs vector figures that LaTeX includes directly (ДП-AITU-19), and SVG is not one of them;
- the traceability matrix stops at a "verification anchor" without test IDs.

**Required change.**
- Add PDF (or EPS) exports to `docs/architecture/export/`.
- After SR1-10, add the SEC/NFR IDs and the planned test IDs to the matrix: requirement → use case → component → test.

**Done when.** The PDF/EPS exports exist and the matrix includes SEC/NFR IDs and test IDs.

*Team response:* … · PR: … · Date: …

#### SR1-13 · UX prototype · M · Owner: Ramazan

**Finding.** The HTML prototype exists and the [walkthrough](../ux/walkthrough.md) honestly lists six alignment issues:
- the Roadworks example vs. the IT pilot;
- TXT acceptance;
- the 25 MB limit;
- the C3 label;
- role labels;
- simulated privacy output.

No person outside the team has tried the prototype yet, and the committee has to download the HTML to see it.

**Required change.**
- Run two short walkthroughs with people outside the team, using the four tasks in evaluation plan §7, and record observations and the resulting changes.
- Resolve the alignment issues or label them in the prototype.
- Publish it on GitHub Pages and put the link in the README.

**Done when.** Two walkthrough records exist and the prototype link is in the README.

*Team response:* … · PR: … · Date: …

#### SR1-14 · Evaluation plan · m · Owner: Daniyar

The plan is rigorous; these points improve its defensibility.

- **(a) Kazakh coverage.** Check in the 6-family pilot whether enough Kazakh-language IT/office tender documentation exists. Many Kazakh versions are translations of Russian ones; you already put translations in one family, so state that the RU and KK results are then not independent.
- **(b) Sample size.** 120 held-out assessments in 12 families give wide intervals for a three-class macro-F1. Report the intervals and avoid claiming small differences.
- **(c) Load test.** The 1/3/5-concurrent-user load test needs a stated usage assumption. My guidance assumed 1 000 users/day, about 5 requests/s at peak. State your own figure and derive the test from it.
- **(d) Cost estimate.** Add a cost-estimate table for the 144+ B1/B2 calls under the proposed $10 pilot cap.
- **(e) Coverage tooling.** Configure `pytest-cov` now, so the coverage trend toward the ≥ 95 % target is visible from the first application code.

*Team response:* … · PR: … · Date: …

#### SR1-15 · Project management · M · Owner: Ramazan

**Finding.** Following D-01, the Notion board is the official tracker, but committee access is unverified. The milestones have no dates after M0. The risk register lacks the process-evidence risk (SR1-01).

**Required change.**
- Open the Notion link in a private browser window to confirm read access without a login.
- Make sure each task shows responsible member, priority, deadline, acceptance criteria and PR link.
- Add provisional dates for pre-defense 2 and the final pre-defense; mark them provisional until the department publishes the schedule.
- Add the SR1-01 risk with its mitigation.

**Done when.** Access is confirmed, the milestone dates are added and the risk is in the register.

*Team response:* … · PR: … · Date: …

#### SR1-16 · Submission basics · B · Owner: Rassul (Ramazan tags after R2)

**Finding.**
- There is no `pre-defense-1` tag and no `docs/predefence/pre-defense-1.md`.
- The README has no "Setup, run and test" section; the commands are only in [database.md](../database/database.md).
- `.env.example` was deleted in `17046bd`, although `compose.yaml` refuses to start without `POSTGRES_PASSWORD`.
- A fresh clone therefore cannot follow a documented path to run the 59 tests, which is step 5 of the repository demo.

**Required change.**
- Restore `.env.example`, with no real secrets.
- Add a README section: `docker compose up -d db`, set `TEST_DATABASE_URL`, `uv sync --locked`, `uv run pytest`.
- Write the submission note: repository and tag links, completed work, known limitations (including every R1 item carried over, with a date) and outstanding tasks with owners and dates.
- After R2, create the annotated tag `pre-defense-1` on the accepted commit and never move it.

**Done when.** Another member follows the README on a clean clone and the tests pass; the note exists; the tag points to the commit accepted in R2.

*Team response:* … · PR: … · Date: …

#### SR1-17 · Presentation · M · Owner: all

**Finding.** [presentation.pptx](https://github.com/Tortuev/TenderGuard/blob/608d1679ce56a91f1a618a8c2ba52da6ff25ae67/docs/predefence/presentation.pptx) has 16 text-only slides, with no diagram, screenshot or table. ДП-AITU-08 cl. 65 gives 8–10 minutes for a School pre-defense. Slide 1 has no supervisor and no topic in three languages. There is no supervisor-feedback slide. Slide 15 makes statements about team agreement that do not belong in front of a committee.

**Required change.**
- Reduce to about 12 slides.
- Show visuals: the context and component diagrams, the condensed comparison matrix, one prototype screen and one requirement → component → test trace.
- Slide 1: titles in EN/RU/KZ and the supervisor.
- Add a slide on R1 and the changes it caused.
- Rehearse with a timer and record the actual duration.

**Done when.** The revised deck is merged and the rehearsal duration is recorded.

*Team response:* … · PR: … · Date: …

#### SR1-18 · Legal and data-protection context · M · Owner: Ramazan (Daniyar for the provider terms)

**Finding.** No document mentions the law that governs the domain: Law of the Republic of Kazakhstan No. 106-VIII "On public procurement", in force since 1 January 2025. The privacy design does not yet address two points:
- the hosted provider's retention of request content, which your ADR-ML-04 itself notes (abuse-monitoring logs of up to 30 days);
- Kazakhstan's personal-data rules on where databases with citizens' personal data are stored and on cross-border transfer.

**Required change.**
- Name the procurement law as domain context in the proposal.
- In the SEC requirements, state as an explicit assumption to be verified that no real company or personal data reaches a hosted provider until the legal basis and the provider settings are confirmed. Until then, use synthetic or permitted data only (you already apply this in practice).
- Cite the current texts of the laws, with the date retrieved.

**Done when.** The proposal names the law and the SEC requirements contain the assumption.

*Team response:* … · PR: … · Date: …

#### SR1-19 · Every member explains every component · M · Owner: all

**Finding.** Ownership is clear: Daniyar ML, Rassul backend and integration, Ramazan PM, privacy and UX. The committee, however, will question any member on any component.

**Required change.** Each member studies the components they did not write. In R2 I will ask each of you two questions outside your own area, for example:
- Daniyar: why composite foreign keys do not isolate reads;
- Rassul: why B1 and B2 share a frozen evidence pack;
- Ramazan: why missing evidence is `unknown` rather than `unmet`.

**Done when.** Each member answers both questions in R2.

*Team response:* … · Date: …

## 3. Supervisor review R2 — 23 October 2026

| | |
| --- | --- |
| Date | 23 October 2026 |
| Commit reviewed | [`3489f5e`](https://github.com/Tortuev/TenderGuard/commit/3489f5ec8bc17d0593f1297ab6001f827ba0d839) on `main` (23 October 2026, 17:55 +05:00): 15 new commits since R1 (`608d167`) |
| Form | **Repository check: done, written below.** Live part (repository demo drill, cold questions, final verdict): to be completed by the supervisor with the team, section 3.5 |
| Re-check | 24 October 2026: `main` is still at `3489f5e`. No new commits, branches, pull requests (the latest is #15) or tags. Additional observations are in section 3.6. |

### 3.1 What changed since R1

**Content changes.**
- **Security, privacy and non-functional requirements** were added to [requirements.md](../requirements/requirements.md) in [`9e42ec6`](https://github.com/Tortuev/TenderGuard/commit/9e42ec63766b5389fd3e889bce372e341f8c0243) (Ramazan). They include:
  - SEC-01 to SEC-19 and NFR-01 to NFR-09;
  - data classes C0–C3, three processing-policy options and a route matrix;
  - eight trust boundaries, threat register TH-01 to TH-14 and acceptance cases AC-01 to AC-10;
  - deletion options and five open decisions (D1–D5).
- **UX:** a new prototype [TenderGuard.html](../ux/TenderGuard.html) (PR #15) and an overview PDF. The walkthrough link was fixed.
- **Presentation:** a new 15-slide deck, [tenderguard_presentation.pdf](../presentation/tenderguard_presentation.pdf), made in Canva, replaces `presentation.pptx` and `presentation.md`.
- **Proposal:** the Kazakh title was updated to the approved version (ШОБ instead of МСБ).
- **Deleted directly on `main`:**
  - `docs/predefence/checklist.md`;
  - `presentation.md` (with the speaker notes) and `presentation.pptx`;
  - `research-slides.md` and `research-slides.pdf`;
  - the old prototype `docs/ux/prototype/index.html`.

**Process facts.**
- Of the 14 new commits on the first-parent line of `main`, 13 were pushed directly.
- The only pull request, #15, was merged by its author six minutes after its single commit (01:45 → 01:51), with no review evidence.
- None of the 14 new non-merge commits mentions a task ID.
- This record was not committed and no *Team response* field is filled in. None of the changes above is therefore linked to an SR1 comment.

### 3.2 Result for each R1 item

Results: **Open** — not addressed; **Partly addressed**; **Substantially addressed** — closes once the listed remainder is fixed; **Live check** — cannot be judged from the repository.

| Item | Sev. | Result | Evidence and what remains |
| --- | --- | --- | --- |
| SR1-01 | B | Open | 13 more direct pushes, including 6 deletions. No evidence of branch protection or a tag ruleset. PR #15 shows no review. |
| SR1-02 | M | Open | 0 of 14 new non-merge commits mention a task ID. |
| SR1-03 | m | Open | `3489f5e` is still committed as `ahmet`. |
| SR1-04 | M | Open | `docs/ai-assistance.md` does not exist. |
| SR1-05 | M | Partly addressed | The Kazakh title is updated. D-02 is not applied: the proposal still says the supervisor field "requires team confirmation". Objectives still have no targets or dates. |
| SR1-06 | B | Open | `docs/relevance/` is unchanged: no metadata block, no reconciliation of the recommendations file, no findings table. |
| SR1-07 | M | Open | Literature review unchanged. |
| SR1-08 | M | Open | Comparison unchanged. The Kontur recheck due on 23 October is not recorded. |
| SR1-09 | M | Partly addressed | The classification approach is now specified (Appendix A.1: uploader declaration, personal-data detector, unknown treated as C2), but not as an ADR comparing alternatives. The authentication ADR is missing. |
| SR1-10 | B | **Substantially addressed** | The content meets the request and goes beyond it. The default-deny route policy, "no silent fallback", re-evaluation of retries and repairs, content-free logging, and the canary and mock-provider acceptance cases are exactly what a privacy-preserving diploma needs. Remaining: the tables do not render (SR2-02); `docs/privacy/` is referenced but does not exist; the two diagrams are external image attachments, not editable sources in the repository; the change went in without a reviewed PR, although Daniyar is named as reviewer. Also see section 3.6: there is no enforced cost ceiling and no accessibility requirement. |
| SR1-11 | M | Partly addressed | NFRs now use Should where justified. All 16 FRs and all 19 SEC items are still Must. No requirement has a *Source* column. FRs still have no verification method. |
| SR1-12 | m | Open | No PDF/EPS exports. The SEC traceability table says its architecture references are "to be confirmed" and has no test IDs. AC-01 to AC-10 exist and can serve as test IDs. |
| SR1-13 | M | Partly addressed | The new prototype fixes four of the six alignment issues: laptops instead of roadworks, no TXT, no C3 or "Analyst" labels. Remaining: [walkthrough.md](../ux/walkthrough.md) still lists all six issues as open; the prototype's 25 MB limit contradicts NFR-04 (proposed 20 MB); the privacy settings screen does not use the new policy vocabulary (C0–C3, LOCAL_ONLY, POLICY_BLOCKED); there are no walkthrough records from people outside the team; the prototype is not published (GitHub Pages returns 404). |
| SR1-14 | m | Open | Evaluation plan unchanged. |
| SR1-15 | M | Open | Project-management document unchanged, and it now links to the deleted checklist. |
| SR1-16 | B | Open | No tag, no `docs/predefence/pre-defense-1.md`, no setup/run/test section, no `.env.example`. New broken links: README → `docs/ux/prototype/index.html`, `docs/predefence/checklist.md`, `docs/predefence/presentation.md`; project-management → `../predefence/checklist.md`. |
| SR1-17 | M | Partly addressed | Clear improvement: the new deck has the architecture, requirement-flow, interview-matrix and B0/B1/B2 visuals and prototype screenshots. Remaining: see the presentation list below. |
| SR1-18 | M | Partly addressed | Localisation, cross-border transfer and provider terms are recorded as open decision D3, and the route registry (SEC-16) records retention and region. Law No. 106-VIII is still not named anywhere. |
| SR1-19 | M | Live check | To be done in section 3.5. |

**Presentation — what remains for SR1-17.**
- Slide 1 has neither the supervisor nor the titles in three languages.
- No slide covers supervisor feedback.
- Slide 14 is titled "Project management and risks" but repeats the evaluation content (RQ1–RQ4, B0–B2, targets, corpus). There is no Notion board, no milestones and no risks.
- Slide 8 says "9 non-functional" requirements, but the specification now has SEC-01 to SEC-19 and NFR-01 to NFR-09.
- Slide 6 claims BGE-M3 "supports Kazakh better" than E5-base. That is not measured; ADR-ML-01 itself leaves the choice to development data.
- Slide 6 also says "We chose BGE-M3 over E5-base", although the evaluation plan keeps E5-base as a required comparator (RQ1). Say "first candidate; E5-base is the comparator".
- Slide 8 says "Every requirement has an acceptance test". The specification has acceptance *criteria*; no tests exist yet. Say "acceptance criterion".
- Slide 7 describes unbuilt parts in the present tense ("Everything runs on one server… Only the gateway can reach an external model").
- 15 slides is still long for 8–10 minutes.
- The speaker notes were deleted with `presentation.md`, and the editable Canva source is not linked.

**Blockers.** One of the four R1 blockers is substantially addressed (SR1-10). Three remain open (SR1-01, SR1-06, SR1-16), and SR2-01 is a new one.

### 3.3 New comments (R2)

#### SR2-01 · This record and the links to changes · B · Owner: Ramazan (all respond)

**Finding.** Component 11 requires supervisor comments, the team's decisions and the PRs that implemented them. The team has made real changes in response to R1: SEC/NFR, the prototype and the deck. But this record is not in the repository, no response is filled in, and every change went in as a direct push. As it stands, the committee cannot see that R1 caused anything.

**Required change.**
- Commit this record through a PR, approved by another member.
- Fill in the *Team response* for every SR1 item: decision, reason, and the PR or commit that addressed it. For changes already pushed directly (`9e42ec6`, `5c0a609`, `1fe5592`, `3489f5e`), cite the commit and add a review comment on it from the named reviewer.
- From now on, one PR per comment.

**Done when.** The record is on `main` through a reviewed PR and every SR1 row has a response.

*Team response:* Decision ☐ Accept ☐ Accept with change ☐ Disagree — reason: … · PR: … · Date: …

#### SR2-02 · The new requirement tables do not render · M · Owner: Ramazan

**Finding.** None of the 18 tables added in `9e42ec6` has a Markdown delimiter row (`| --- | --- |`). They contain 494 tab characters, and the SEC/NFR tables merge two header cells ("Requirement⇥Acceptance"), so the header has fewer columns than the rows. On GitHub all of this shows as plain text, not tables; the most important new section of the package is hard to read. Row TH-07 is broken across two lines.

**Required change.**
- Rebuild the tables: one header cell per column, a delimiter row, pipes instead of tabs.
- Commit the two diagrams as editable sources (Mermaid, like the rest of the architecture package) instead of `user-attachments` images.
- Either create `docs/privacy/` or remove the reference to it.

**Done when.** All 18 tables render on GitHub, the diagrams have editable sources in the repository, and the `docs/privacy/` reference resolves.

*Team response:* … · PR: … · Date: …

#### SR2-03 · Deleted files left broken links · M · Owner: Rassul

**Finding.** `checklist.md`, `presentation.md` and the old prototype were deleted. The README (3 links) and the project-management document (1 link) now point to files that no longer exist. The checklist was the only map from each component to its evidence and remaining work.

**Required change.**
- Fix every link.
- Either restore a component-to-evidence map (the README table can serve if it links the new deck and prototype) or record why it was dropped.
- Keep the speaker notes somewhere in the repository.

**Done when.** A link check over the repository finds no broken relative links.

*Team response:* … · PR: … · Date: …

#### SR2-04 · Consistency between documents · M · Owner: Rassul (integration), each author for their part

**Finding.**
- The deck says 9 NFR while the specification has 19 SEC and 9 NFR.
- The prototype uses 25 MB; NFR-04 proposes 20 MB.
- The prototype has no C0–C3 classes or policy options.
- The database `data_class` column allows only `public`/`private`, while SEC-04 defines C0–C3. A future migration is needed; record it as a dependency.
- Role names must follow decision D-08 everywhere.
- The gateway is called "Privacy Gateway" 5 times and "Inference Gateway" 3 times in [requirements.md](../requirements/requirements.md). The architecture and decision D-03 use "Inference Gateway".

**Required change.**
- Align the numbers and the vocabulary across the requirements, deck and prototype.
- Add the `data_class` migration to the project plan as a dependency of SEC-04.

**Done when.** The requirements, deck and prototype use the same numbers and terms, and the migration is in the plan.

*Team response:* … · PR: … · Date: …

### 3.4 Supervisor decisions on the team's open decisions (D1–D5 in requirements.md)

| Ref | Team item | Decision |
| --- | --- | --- |
| D-06 | D1 — deletion versus historical reports | Option **B (tombstone)** is accepted: runs remain, citations show a deleted-source notice without a quote, derived quotes are redacted, and affected findings are marked `evidence_deleted`. |
| D-07 | D2 and D3 — default policy, legal basis, provider terms | New organizations start with **LOCAL_ONLY**. Until a lawyer confirms the personal-data localisation and cross-border transfer rules and the provider's terms (retention, region, training use), hosted routes may receive only **C0 public tender text and synthetic fixtures**. No real C1 or C2 data may go to a hosted provider. State this as a limitation in the submission note. |
| D-08 | D5 — role names | Use **owner / member / viewer** in every document and in the UI. "Analyst" stays a persona name only. |
| D-09 | D4 — numeric values | Defer the numbers until after the first end-to-end baseline, as proposed. A stated workload assumption is still required before pre-defense 2 (SR1-14 c). |

### 3.5 Live part (to be completed by the supervisor with the team)

| Member | Repository demo: task traced end to end (SR1-02) | Time | Cold question 1 (SR1-19) | Cold question 2 | Result |
| --- | --- | --- | --- | --- | --- |
| Daniyar Kairatov | | | Why composite foreign keys do not isolate reads | | |
| Rassul Akhmetov | | | Why B1 and B2 share a frozen evidence pack | | |
| Ramazan Talgatov | | | Why missing evidence is `unknown`, not `unmet` | | |

### 3.6 Re-check on 24 October 2026

**Repository state.** The re-check confirmed every finding in 3.1–3.3:
- `main` is still at `3489f5e` (23 October, 17:55).
- There are no new commits, branches or pull requests; the latest pull request is #15.
- There are no tags; `pre-defense-1` does not exist.
- This record is still not in the repository. `docs/supervisor-feedback/supervisor-feedback.md` on `main` is the old version from before R1.
- The broken links in SR2-03 are still broken.
- GitHub Pages still returns 404.

**Additional observations** (not in the 23 October text):
- **SR1-10 remainder.**
  - The cost requirement is missing. NFR-08 records calls, tokens and time, but no requirement enforces a cost ceiling within the project budget of $0–50. Add an NFR such as "the gateway stops paid calls at a configured cumulative limit" with a verification method.
  - No requirement covers the accessibility of the core screens.
- **SR1-17.** Slide 6 says BGE-M3 was "chosen over" E5-base, and slide 8 calls acceptance criteria "acceptance tests". Both are added to the presentation list in 3.2.
- **SR2-04.** The gateway has two names in the requirements; this is added to the SR2-04 list.
- **SR1-13.** `Overview page of ux prototype.pdf` is a single-page screenshot of the workspace screen. It shows the screen, but it is not evidence of a walkthrough by people outside the team.

### 3.7 Verdict

**Recommendation from the repository check (23 October, `3489f5e`; unchanged at the re-check on 24 October): not ready to tag yet.**

The design content is strong and the SEC/NFR work closes the largest gap. The package can be tagged on 24 October **with limitations** once these five conditions are done:

| # | Condition | Done on 24 October? |
| --- | --- | --- |
| 1 | **SR2-01:** this record is on `main` through a reviewed PR, and every SR1 row has a response with its commit or PR. | No |
| 2 | **SR1-01:** `main` is protected and the tag ruleset is set (screenshot). The submission note states honestly how the repository was assembled between 17 and 23 October. | No |
| 3 | **SR1-06:** each interview has its metadata block, or the submission note states plainly what is unverified and removes anything that did not happen. | No |
| 4 | **SR1-16 and SR2-03:** `.env.example` is restored, the setup/run/test section is added, the links are fixed and the submission note is written. | No |
| 5 | **SR2-02:** the requirement tables render. | No |

**Today's deadline.** Work in this order, each item as its own reviewed PR: 1 → 4 → 5 → 3 → 2. Then create the annotated `pre-defense-1` tag on the merge commit that contains all five, and send the supervisor the tag link. Whatever cannot be finished today goes into the submission note as a known limitation with a date, and into section 4.

Everything else may be carried over with a date in section 4.

**Final verdict** (supervisor, after the live part): ☐ Ready to tag ☐ Ready to tag with the limitations listed in the submission note ☐ Not ready — reason: …

**Accepted commit for `pre-defense-1`:** … Signature / confirmation: Almas Ospanov · Date: …

## 4. Items carried over to pre-defense 2

These carry-overs are proposed by the supervisor. They become final only when the verdict above is signed and the items are listed in the submission note.

| Item | Reason | Owner | New date |
| --- | --- | --- | --- |
| SR1-03 | Minor; does not affect the package | Rassul | 26 October 2026 |
| SR1-05 (objective targets) | Needs the evaluation pilot | Rassul with Daniyar | 13 November 2026 |
| SR1-07 | Reading new sources takes longer than one day | Daniyar (all contribute) | 13 November 2026 |
| SR1-08 | Comparator changes need a recheck and evidence | Rassul | 13 November 2026 |
| SR1-09 (ADRs) | Classification approach exists; ADR form and authentication ADR remain | Ramazan | 13 November 2026 |
| SR1-11 | Re-ranking and source columns need a joint review | Rassul | 13 November 2026 |
| SR1-12 | Exports and test IDs follow the SEC/NFR fix | Rassul | 13 November 2026 |
| SR1-13 (walkthroughs, Pages, vocabulary) | Needs participants | Ramazan | 13 November 2026 |
| SR1-14 | Depends on the 6-family pilot | Daniyar | 13 November 2026 |
| SR1-15 | Milestone dates depend on the department schedule | Ramazan | When the schedule is published |
| SR1-17 (remaining slide fixes) | Only if not fixed before the presentation | All | Before the presentation |
| SR1-18 | Law citation and legal review | Ramazan | 13 November 2026 |
| SR2-04 | Cross-document alignment | Rassul | 13 November 2026 |
