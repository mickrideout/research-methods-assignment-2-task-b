---
name: plan-question
description: Decomposes ONE named assignment question into what it really asks, its central argument and reasoning outline, which rubric criteria and checklist items it must satisfy, a task-matched section structure with a word budget, the evidence and experiment runs it needs, and the gaps the student must fill. Writes work/questions/<QID>/plan.md. Use when the user asks to plan, outline, break down or scope a specific question ID, before research or drafting. Never plans more than the one question named.
---

# plan-question

## Purpose

Produce a reasoning-driven plan that makes the answer's central argument and route to the top band explicit before any drafting: command words → central position/conclusion → claims & reasoning → criteria → sections → words → evidence.

## When to use

- The user names exactly one question ID, e.g. "plan Q2".
- Re-run after a rubric change or major feedback. The previous plan is moved to `history/` first.

Do not use it without a question ID, for more than one question, or to draft answer text.

## Inputs

Path placeholders such as `<questions_dir>` mean `paths.questions_dir` in the details file.
Argument: **one question ID (required)**.

1. `context/assignment.md` (always first): the question's marks, word limit, type, `word_count` rules and open questions.
2. `<rubric_yaml>`: criteria whose `applies_to` includes the ID or `ALL`. `<checklist_yaml>`: items for the ID or `ALL`.
3. Extracted spec text for the question, plus relevant lectures and readings in `<extracted>/`.
4. Existing `<questions_dir>/<QID>/` notes, plus other questions' plans or completed sections in `<answers>` (read-only, to avoid duplicating definitions or explanations across questions). `<results_manifest>` for code questions.
5. Shared Academic Writing Style Guidelines: [../answer-question/references/writing-guide.md](../answer-question/references/writing-guide.md) (especially §2, §3, §6, §11, §12 and §14).
6. Format: `templates/question-plan.md`.

## Procedure

1. Confirm the ID exists: `python3 <tools>/details.py question <QID>`. If none was given, ask. Never pick one.
2. Check open questions affecting the ID (`python3 <tools>/details.py open`). Flag blocking ones at the top of the plan.
3. Quote the task verbs (command words such as *analyse*, *evaluate*, *compare*, *justify*, *discuss*, *design*) and constraints verbatim, with the source. Determine what the question requires the reader to understand or conclude, and note any interpretation risks.
4. Build the **reasoning outline** (following [../answer-question/references/writing-guide.md](../answer-question/references/writing-guide.md) §2–3):
   - State the main finding, position, thesis or design recommendation that the answer will advance.
   - Sequence the supporting claims, the specific evidence/calculations required for each, the analytical reasoning (mechanisms, trade-offs, evaluation criteria, limitations), and the conclusion.
   - Prefer specific analytical claims over broad topic overviews.
5. Build the criteria map. For each applicable criterion, summarise what its *top* level needs (from `observable`) and assign it to a section or claim. Do the same for each checklist item.
6. Propose a **task-matched structure** (following [../answer-question/references/writing-guide.md](../answer-question/references/writing-guide.md) §6, §11–12):
   - Adapt the structure to the question type rather than applying a mechanical introduction–body–conclusion template to every question.
   - Omit generic topic introductions, restatements of the question, and redundant summary paragraphs when the answer is already clear and the question does not require one.
   - Avoid excessive headings that fragment a short answer, and check other questions' plans/answers so shared concepts are not defined repeatedly.
   - Assign each section/component a purpose, the criteria served, and a word budget summing to at most 95% of the limit (and respecting any per-item sub-limits) to leave room for revision.
7. List the evidence needed per claim and mark whether it already exists in `inputs/` (with file#p.N) or is missing.
8. For `code`/`mixed` questions, list the runs needed (result, script, expected output path) and check them against the manifest.
9. Write the gaps for the user: sources to obtain, decisions to make, runs to approve.
10. If `<questions_dir>/<QID>/plan.md` exists, move it to `<questions_dir>/<QID>/history/<YYYYMMDD-HHMMSS>-plan.md`. Then write the new plan.
11. Log the run: `python3 <tools>/log_ai_use.py --skill plan-question --qid <QID> --action "Planned structure and evidence" --files <questions_dir>/<QID>/plan.md`.

## Output

- `<questions_dir>/<QID>/plan.md`, following `templates/question-plan.md`.
- Final message: the central argument/reasoning outline, the structure table, the count of missing evidence and runs, and the suggested next command:
  - `research-question <QID>` if evidence is missing
  - `run-experiments <QID>` if runs are needed
  - otherwise `answer-question <QID>`

  Do not run that command.

## Quality checks

- Every applicable criterion and checklist item appears in the map.
- The plan establishes a logical line of reasoning (central position, claims, evidence, reasoning, conclusion) tailored to the question's command words, without generic filler sections.
- The word budget sums to at most the limit (or "no limit" is stated) and respects any sub-limits.
- Every "have it" evidence row has a real file#locator that you opened.
- Only this question's folder was written.

## If inputs are missing

- No `<rubric_yaml>`: say that enhance-rubric has not run. Plan from the spec only, marked "provisional".
- Question ID not in the details file: stop and ask. Suggest re-running define-details if the spec has new questions.
- Blocking open question unresolved: produce the plan with the affected parts marked "depends on OQn".
