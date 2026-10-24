---
name: answer-question
description: Drafts or revises the answer to ONE assignment question that the user names by ID, applying the shared Academic Writing Style Guidelines for natural, human-like postgraduate prose. It aims at the top rubric band within the word limit and referencing style, writes only that question's section of answers/answers.md via the section-replacement script, and records sources used. Never invents references, results or data; it stops and reports when a run or source is missing. Use when the user says "answer Q2", "draft Q1" or "revise Q3 from this feedback". Never chains to another question.
---

# answer-question

## Purpose

Write (or revise) one question's answer in natural, human-like postgraduate academic prose, aimed at the top performance band, grounded only in provided sources and logged results, and saved through a script that cannot touch other sections.

Before finalising an answer, apply the shared Academic Writing Style Guidelines ([references/writing-guide.md](references/writing-guide.md)).

First, develop an answer that satisfies the question, marking rubric, evidence requirements and technical constraints. Then perform a separate editorial revision to improve clarity, naturalness, concision and variation in expression.

Do not rely on superficial synonym replacement or random sentence restructuring. Improve the writing by removing redundant content, replacing generic claims with specific analysis, making logical relationships explicit, and varying structure according to the ideas being expressed.

Preserve all substantive findings, necessary reasoning, citations, calculations, technical details and rubric coverage. Do not invent evidence, personal experience or sources.

Return only the requested assignment answer and its required supporting material. Do not include internal outlines, style-review commentary or self-evaluations unless explicitly requested.

## When to use

- The user explicitly names exactly one question ID. This is the only way answering starts.
- **Draft mode:** `answer-question Q2`.
- **Revise mode:** `answer-question Q2 --from <path>`, where `<path>` is a grading report (`reports/grading/Q2/...`), an assignment report, or a feedback file in `inputs/feedback/`. Apply its fixes for Q2 only.

Do not use it without an ID, for several questions in one run, to answer the "next" question, or to grade.
After finishing, suggest the next command but never run it.

## Inputs

Path placeholders such as `<answers>` mean `paths.answers` in the details file.
Argument: **one question ID (required)**; optional `--from <report-or-feedback>`.

1. `context/assignment.md` (always first): the question's marks, `word_limit`, `type`, `word_count`, `referencing`, `spelling`, `genai` and `open_questions`.
2. `<rubric_yaml>` criteria for the ID (and `ALL`), and `<checklist_yaml>` items for the ID (and `ALL`).
3. `<questions_dir>/<QID>/plan.md`, `research.md` and `results.md` (if present), plus `<results_manifest>`.
4. `<bibliography>`, and the relevant `<extracted>/` inputs.
5. The current section (`python3 <tools>/answer_section.py get <QID>`) and any already-completed sections in `<answers>` (read-only, to maintain consistent terminology, notation, assumptions and register across questions).
6. Revise mode only: the `--from` file.
7. Shared Academic Writing Style Guidelines: [references/writing-guide.md](references/writing-guide.md).

## Procedure

1. **Gate on the question ID.** If none was given, ask. Check it exists: `python3 <tools>/details.py question <QID>`.
2. **Gate on generative-AI policy.**
   - `prohibited`, or drafting is listed in `prohibited_uses`: refuse to draft. Offer only what `permitted_uses` allows, e.g. feedback on the user's own draft.
   - `unclear`: ask the user to confirm that drafting is allowed before continuing.
3. **Gate on open questions.** If an unresolved open question has `blocking: true` and its `affects` includes this ID, stop and list it.
4. **Gate on evidence.** Every claim that needs a source must map to `research.md`, the extracted inputs, or a `.bib` entry. Every result must map to a manifest output with `status: ok`. If anything is missing, **stop** and tell the user exactly what is needed: a run (`run-experiments <QID>`) or a source (put it in `inputs/readings/`). Do not draft around the gap with invented content.
5. **Draft from a reasoning outline (Implementation Rule 1).**
   - Before generating prose, establish the logical line of reasoning from `<questions_dir>/<QID>/plan.md` (or formulate an internal reasoning outline if no plan exists): identify the precise command words, the central finding/position/recommendation, the key supporting claims, the specific evidence/calculations, the causal mechanisms or trade-offs, and the conclusion.
   - Match the structure and tone to the question type (Explain, Analyse, Evaluate, Compare, Discuss, Justify, Design/propose, Calculate/solve, Reflect; see Section 11 of [references/writing-guide.md](references/writing-guide.md)) rather than forcing a universal introduction–body–conclusion template.
   - The reasoning outline is an internal scaffold and must **never** appear in the final answer.
6. **Compose the substantive draft (`<questions_dir>/<QID>/draft.md`).**
   - **Draft mode:** write to `<questions_dir>/<QID>/draft.md`, following the plan's structure and word budget, and targeting the top-level `observable` descriptors of each applicable criterion.
     - Start with the required section heading (e.g. `## <QID>. <title>`, or the exact heading mandated by `format` in `context/assignment.md`).
     - Cite using pandoc syntax (`[@key]` or `[@key, p. N]`) or the assignment's internal citation scheme specified in `referencing`.
     - Include figures and tables from `<results_dir>` by relative path from `<answers>`'s folder, e.g. `![Caption](../work/results/figures/Q2-x.png)`. Do not paste code wholesale; reference files in `<code_dir>`, or include short excerpts (≤15 lines) only when the rubric rewards discussing them.
     - Use the `spelling` convention (e.g. `en-AU`) throughout.
   - **Revise mode:** start from the current section in `<answers>`. Apply each substantive and stylistic fix from the `--from` file that concerns this ID while keeping what already earns marks. Record which fixes were applied and which were skipped, and why.
7. **Perform a distinct editorial pass (Implementation Rule 2 & Section 15 of the Style Guidelines).**
   Once `<questions_dir>/<QID>/draft.md` satisfies all rubric and evidence requirements, review and revise the prose through four dedicated passes without weakening technical accuracy, citations or rubric coverage:
   - **Pass 1 — Question alignment:** Verify every part of the question, command word and marking criterion is directly answered, with the main finding or position stated early when appropriate. Cut generic topic introductions, restatements of the question, and textbook explanations of concepts an academic reader already knows.
   - **Pass 2 — Substantive quality:** Ensure broad assertions ("provides valuable insights", "has many advantages and disadvantages") are replaced with concrete mechanisms, named variables/stakeholders/theories, specific evidence, and explicit evaluation criteria. Express uncertainty and material limitations precisely without vague disclaimers or overclaiming ("clearly", "obviously", "proves").
   - **Pass 3 — Natural expression:** Remove habitual AI filler phrases ("It is important to note that…", "It is worth noting that…", "Furthermore, it is important to consider…", "This highlights the importance of…", "This underscores the significance of…", "A key takeaway is that…", "Delving deeper into…", "At its core…", "It is crucial to understand that…", "Ultimately, this demonstrates that…") and repetitive sentence openings ("This suggests/indicates/demonstrates/highlights…"). Vary sentence and paragraph lengths according to idea complexity rather than forcing every paragraph into a mechanical four-sentence pattern.
   - **Pass 4 — Assignment-wide consistency:** Check against other answered sections in `<answers>` so terminology, notation and assumptions are reused consistently, earlier explanations are not unnecessarily repeated, and no contradictions exist across answers. Ensure no internal outlines, style-review commentary or self-evaluations remain in `<draft>`.
8. **Verify technical and word-count constraints on `<draft>`:**
   - `python3 <tools>/wordcount.py --text <draft>` must be within `word_limit` (plus `tolerance_pct`), as well as any per-item sub-limits noted in `context/assignment.md`. Cut verbosity if over.
   - Every `[@key]` must exist in `<bibliography>` (when BibTeX referencing is used).
   - Every figure path must exist and appear in the manifest.
9. **Write the section only through the script:**
   `python3 <tools>/answer_section.py put <QID> --from <draft> --criteria C1,C3 --status draft|revised`
   The script writes the meta line, saves the previous version to `<questions_dir>/<QID>/history/`, and confirms the rest of the file is byte-identical. Never edit `<answers>` any other way. Delete the temporary draft afterwards, or keep it as `draft.md`.
10. **Record sources.** Write `<questions_dir>/<QID>/sources.md` (template `templates/question-sources.md`): each citation key or file, its location, and what it supports. Include the section hash from `answer_section.py hash <QID>`.
11. **Log the run:** `python3 <tools>/log_ai_use.py --skill answer-question --qid <QID> --action "Drafted|Revised answer (<mode>)" --files <answers>,<questions_dir>/<QID>/sources.md`.

## Output

- `<answers>`: only section `<QID>` changed, containing only the requested assignment answer and its required supporting material (no internal outlines, style-review notes or self-evaluations). The meta line reads `words=N/limit | criteria=… | updated=YYYY-MM-DD | status=…`.
- `<questions_dir>/<QID>/sources.md`. `<questions_dir>/<QID>/history/<timestamp>.md` holds the previous version (written by the script).
- Final message to the user:
  - word count against the limit
  - criteria targeted
  - summary of substantive points and key editorial refinements made during the style pass
  - assumptions made
  - in revise mode, the fixes applied and skipped
  - anything the user must check
  - suggested next command, not run: `grade-question <QID>`, ideally in a fresh session

## Quality checks

Evaluate substance and style separately (Implementation Rule 3). Neither check compensates for failure in the other:

- **Substance and compliance check:**
  - `python3 <tools>/answer_section.py check` exits 0. The script reported "rest of file byte-identical".
  - Within the word limit (and any sub-limits) by the spec's counting rules.
  - No citation key is missing from the `.bib`. No result is absent from the manifest. No invented data, quotes, personal experiences or page numbers.
  - Every `must` item in the checklist for this ID and every targeted rubric descriptor is addressed, or its omission is explained to the user.
  - No other question's section, plan or notes were modified.
- **Style and natural expression check ([references/writing-guide.md](references/writing-guide.md) §15–16):**
  - Directly answers the question using structure suited to the command words rather than a generic overview or rigid template.
  - Free of habitual AI filler phrases, throat-clearing introductions, repetitive sentence openings ("This suggests/indicates/highlights…"), and redundant summary paragraphs.
  - Claims are specific and analytical (naming mechanisms, trade-offs, criteria and limitations) rather than broad assertions with generic elaboration.
  - Consistent in terminology, notation, assumptions and academic register with the rest of `<answers>`.
  - Contains no internal outlines, meta-commentary or self-evaluations inside the answer section.

## If inputs are missing

- No plan: ask whether to run plan-question first. If the user declines, build the internal reasoning outline inline (command words → central argument → criteria → sections → words) before drafting and state that you did.
- No rubric YAML: draft against the spec only and warn that the criteria targeting is provisional.
- Missing source or run: stop (step 4). List exactly what is missing and the command or action that would supply it.
- `--from` file does not mention this ID: say so and ask whether to apply its general (cross-cutting) fixes.
