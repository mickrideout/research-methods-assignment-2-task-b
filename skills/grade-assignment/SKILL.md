---
name: grade-assignment
description: Grades the whole assignment as a strict marker. It summarises each question from fresh per-question grading reports, assesses cross-cutting criteria and assignment-wide writing style consistency (structure, coherence, natural academic expression, terminology consistency, referencing, presentation, word limits, checklist completeness), estimates the total mark and grade band with confidence, and ends with a fix list prioritised by marks recoverable per unit of effort. Writes a timestamped report and never edits answers. Use when the user asks to grade, mark or review the entire assignment or to estimate the overall mark.
---

# grade-assignment

## Purpose

Estimate the overall mark honestly, evaluating rubric substance and assignment-wide academic style separately, and tell the user where the next hour of work earns the most marks.
This skill is read-only on answers.

## When to use

- After the questions have been answered and (ideally) graded individually, and before export.
- Re-run after revisions. Each run writes a new report.

Do not use it to edit answers, to grade a single question in depth (use `grade-question`), or to fix compliance issues.

## Fresh context

As in grade-question: if your agent can run a sub-agent or a new session with a clean context, delegate steps 2–8 to it.
Otherwise suggest a new session, proceed, and record `fresh context: no`.

## Inputs

Path placeholders such as `<reports_dir>` mean `paths.reports_dir` in the details file.

1. `context/assignment.md` (always first): questions, marks, `total_marks`, `grade_bands`, `word_count`, `format`, `genai`.
2. `<rubric_yaml>` (especially `cross_cutting` criteria) and `<checklist_yaml>`.
3. `<answers>` (the whole file) and `<bibliography>`.
4. The latest per-question reports and their freshness: `python3 skills/grade-assignment/scripts/report_status.py`.
5. A fresh compliance report: `python3 <tools>/compliance.py --out "$(python3 <tools>/report_path.py compliance)"`.
6. Guides: [../grade-question/references/marking-guide.md](../grade-question/references/marking-guide.md) and [../answer-question/references/writing-guide.md](../answer-question/references/writing-guide.md) (especially §14–16). Format: `templates/grading-report-assignment.md`.
7. Do not read plans, research notes or drafts.

## Procedure

1. Run `python3 <tools>/fingerprint.py` and keep its output, to compare at the end.
2. Run `report_status.py`. For each question:
   - **FRESH:** use the report's marks.
   - **STALE or NOT GRADED:** grade that question inline, following the grade-question procedure and marking guide. Mark it "inline" in the per-question table. Alternatively, tell the user which questions to grade first with grade-question for a fuller report.
3. Run the compliance script (input 5) and read its FAIL and WARN rows.
4. Assess the cross-cutting and style-consistency aspects across the whole file, with quoted evidence (evaluating substance and style separately per [../answer-question/references/writing-guide.md](../answer-question/references/writing-guide.md) §14–15):
   - **Structure and coherence:** does each answer use a structure suited to its question type while the whole submission reads coherently without every answer sounding structurally identical?
   - **Consistency across answers:** the same terms, definitions, assumptions, notation and numbers across answers; no unnecessary repetition of explanations already supplied in earlier answers; no contradictions. Quote any inconsistencies.
   - **Natural academic expression:** check for cross-question formulaic AI patterns (habitual filler phrases, repetitive paragraph templates, generic introductions or conclusions, or broad claims lacking specific mechanisms).
   - **Referencing:** style consistency, accuracy against the `.bib` (or internal quote scheme), appropriate integration into reasoning rather than decoration, and over-reliance on any one source.
   - **Presentation:** headings, figure and table referencing, formatting requirements from `format`.
   - **Word limits** (from compliance) and **checklist completeness** (every `must` item met, with evidence).
5. Mark each `cross_cutting: true` criterion with a level, a mark, evidence, and the next-level gap.
6. Total = per-question criterion marks + cross-cutting criterion marks. Make sure no criterion is counted twice: a criterion's weight is awarded once. Map the total to `grade_bands`. Give a plausible `range` and a `confidence`, with reasons.
7. Build the prioritised fix list from all per-question reports, the cross-cutting/style findings and compliance FAILs:
   - estimate marks recoverable and effort for each fix (marking guide), and sort by ratio
   - each row gets the exact command to act on it, e.g. `answer-question Q2 --from <this report>`
8. Write the report to `python3 <tools>/report_path.py grading-assignment`, following the template. Copy `answers_sha256` and the `sections` map (as `section_sha256`) from step 1's fingerprint output.
9. Run `fingerprint.py` again. `answers_sha256` must be unchanged.
10. Log the run: `python3 <tools>/log_ai_use.py --skill grade-assignment --action "Graded whole assignment" --files <report>`.

## Output

- `<reports_dir>/grading/assignment/<YYYYMMDD-HHMMSS>.md`: frontmatter as in `templates/grading-report-assignment.md`.
- `<reports_dir>/compliance/<YYYYMMDD-HHMMSS>.md`: from the compliance script.
- Final message: the estimate, band and range, summary of substance vs style consistency across the submission, the top 5 fixes with their commands, and any stale or inline-graded questions. Do not start any fix.

## Quality checks

- Substance and style are evaluated distinctly; neither compensates for failure in the other.
- The per-question marks plus the cross-cutting marks add up to the estimate. No criterion was double-counted.
- Every cross-cutting and style claim quotes evidence or cites a compliance row.
- The fix list is sorted by ratio, and every fix names a question ID or "ALL" and a command.
- The answers file is unchanged (fingerprint matches).

## If inputs are missing

- No per-question reports: grade inline (step 2) and lower the confidence by one level.
- No rubric YAML: estimate from the spec and the original rubric. Set confidence low and recommend enhance-rubric.
- Sections still contain placeholders: count them as 0 and put "answer <QID>" at the top of the fix list.
