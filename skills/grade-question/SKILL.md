---
name: grade-question
description: Marks ONE named question's answer as a strict, calibrated university marker against the enhanced rubric and evaluates academic writing style separately from substance. For each criterion it awards a level and mark with quoted evidence, says what is missing for the next level, checks the question's checklist items, word limit and natural academic expression, and gives specific fixes. Writes a timestamped report and never edits answers. Use when the user asks to grade, mark, assess or review a specific question ID, ideally in a fresh context.
---

# grade-question

## Purpose

Give an honest, evidence-based mark for one question, evaluating rubric substance and natural academic style separately, with fixes ordered by marks recoverable.
This skill is read-only on answers: it writes reports only.

## When to use

- The user names exactly one question ID, e.g. "grade Q1".
- After `answer-question` or a manual edit. Re-run as often as you like; each run writes a new report.

Do not use it to edit or rewrite answers (that is `answer-question --from <this report>`), to grade the whole
assignment (`grade-assignment`), or for more than one ID.

## Fresh context (do this first)

The grader must not mark its own draft from memory.
- If your agent can start a sub-agent or a new session with a clean context, delegate steps 2–9 to it. Pass only this skill's path, the question ID and the project root. The sub-agent returns the report path.
- If it cannot, tell the user that the best practice is to run this skill in a new session. Then proceed, reading only the inputs listed below, and record `fresh context: no` in the report.

## Inputs

Path placeholders such as `<rubric_yaml>` mean `paths.rubric_yaml` in the details file.
Argument: **one question ID (required)**.

1. `context/assignment.md` (always first): marks, `word_limit`, `word_count` rules, `grade_bands`, `genai`.
2. `<rubric_yaml>` criteria for the ID and `ALL`; `<checklist_yaml>` items for the ID and `ALL`.
3. **Only** the answer section: `python3 <tools>/answer_section.py get <QID>`, plus the figures and tables it links to and the code files it references.
4. `<bibliography>`, to check the citations.
5. Do **not** read `<questions_dir>/<QID>/plan.md`, `research.md` or drafts. Mark what is on the page, not what was intended.
6. Guides: [references/marking-guide.md](references/marking-guide.md) and [../answer-question/references/writing-guide.md](../answer-question/references/writing-guide.md). Format: `templates/grading-report-question.md`.

## Procedure

1. Confirm the ID. Record the hashes before marking: `python3 <tools>/fingerprint.py <QID>`. It prints `answer_sha256`, `answers_sha256`, `rubric_sha256`, `checklist_sha256` and `generated` as YAML for the report frontmatter.
2. Word count: `python3 <tools>/wordcount.py <QID>`. Apply over-limit consequences only if the spec states them; otherwise flag the overrun.
3. **Evaluate substance (rubric criteria):** Mark each applicable criterion separately, following [references/marking-guide.md](references/marking-guide.md):
   - Start at the lowest level and move up only while the answer meets that level's observable descriptors. Do not let fluent or formulaic prose compensate for missing analysis or evidence.
   - Award the level, then a mark within its range.
   - Quote the evidence verbatim. Name what is missing for the next level up, and give concrete fixes (where, what to add or cut, roughly how many words).
   - For cross-cutting (`ALL`) criteria, assess this question's contribution only, and note that the final mark is set by grade-assignment.
4. **Evaluate style and natural expression separately ([../answer-question/references/writing-guide.md](../answer-question/references/writing-guide.md) §15):**
   - Check whether the answer reads as direct, natural postgraduate reasoning rather than formulaic language-model prose.
   - Flag any habitual AI filler phrases ("It is important to note that…", "This underscores the significance of…", "At its core…"), repetitive sentence openings ("This suggests/indicates/demonstrates/highlights…"), generic topic introductions, broad claims lacking concrete mechanisms, or mechanical paragraph templates, and write specific editorial fixes.
5. Check each checklist item: PASS, FAIL or UNCLEAR, with evidence.
6. Check integrity:
   - Every citation key must exist in the `.bib`.
   - Every claim with a number must trace to a source or a results file.
   - A suspected invented reference or result is an automatic flag in the verdict.
7. Compute `marks_awarded` and `percent`, and map the percentage to `grade_bands`. Set `confidence` based on how unambiguous the descriptors were.
8. Write the report to the path from `python3 <tools>/report_path.py grading <QID>`, following `templates/grading-report-question.md`. The frontmatter must include `answer_sha256`, `rubric_sha256`, `checklist_sha256` and the `criteria` list.
9. Run `python3 <tools>/fingerprint.py <QID>` again. Every hash must match step 1. If any differs, the answers changed during grading: discard the report and tell the user.
10. Log the run: `python3 <tools>/log_ai_use.py --skill grade-question --qid <QID> --action "Graded against rubric" --files <report>`.

## Output

- `<reports_dir>/grading/<QID>/<YYYYMMDD-HHMMSS>.md`: frontmatter as in `templates/grading-report-question.md`; the body has the verdict, per-criterion sections, style and natural expression review, checklist table, word limit and priority fixes.
- Final message: mark and band, summary of substance vs style findings, the top 3 fixes, the report path, and the suggested command `answer-question <QID> --from <report path>` (not run).

## Quality checks

- Substance and style are evaluated distinctly; neither compensates for failure in the other.
- Every applicable criterion has a level, a mark within that level's range, at least one verbatim quote (or "no evidence found"), and a next-level gap.
- The marks sum correctly. The band matches `grade_bands`.
- The answer file is byte-identical before and after.
- No plan or notes were read.

## If inputs are missing

- No `<rubric_yaml>`: grade against the spec's criteria and the original rubric text, mark `confidence: low`, and recommend running enhance-rubric.
- Section empty or placeholder: write a short report ("not answered", 0 marks) and stop.
- A linked figure or code file is missing: FAIL the related evidence and note it in the fixes.
