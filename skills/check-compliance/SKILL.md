---
name: check-compliance
description: Runs deterministic compliance checks on the common answer file. It checks section markers, word counts against limits under the spec's counting rules, leftover placeholders, citation keys against the bibliography, unverifiable references, broken links and images, figures not traceable to logged runs, spelling convention, required sections and the AI acknowledgement, then writes a timestamped pass/fail report. Use before grading the whole assignment, before export, or whenever the user asks to check word counts, references or formatting compliance.
---

# check-compliance

## Purpose

Catch the mechanical problems that cost marks or invalidate a submission, quickly and
reproducibly. A script does the checking. The agent interprets the result and proposes fixes.

## When to use

- Any time. It is cheap and safe, and each run writes a new report. It is also run by grade-assignment and export-submission.

Do not use it to judge quality (that is grading), or to fix anything automatically: it never edits answers.

## Inputs

Path placeholders such as `<answers>` mean `paths.answers` in the details file.

1. `context/assignment.md` (always first): `word_count`, `format.required_sections`, `spelling`, `genai`, `open_questions`.
2. `<answers>`, `<bibliography>`, `<results_manifest>`.
3. Scripts: `<tools>/compliance.py` (all checks; exit 1 on any FAIL) and `<tools>/wordcount.py` (per-section detail).

## Procedure

1. Get a report path and run the checks:
   `python3 <tools>/compliance.py --out "$(python3 <tools>/report_path.py compliance)"`
   If your shell does not support `$( )`, run `report_path.py` first and pass the printed path to `--out`.
2. For a word-limit FAIL, run `python3 <tools>/wordcount.py` to show the per-section counts and the counting rules applied.
3. For each FAIL and WARN, add a "Proposed fixes" section to the end of the report. Each fix names the section ID, what to change, and which skill or command does it. For example: "Q2 over by 64 words: answer-question Q2 --from <this report>", or "add a bib entry for smith2021 via research-question Q1". Treat spelling WARNs as suggestions, since technical terms and quotations may legitimately use US spelling.
4. Log the run: `python3 <tools>/log_ai_use.py --skill check-compliance --action "Ran compliance checks" --files <report>`.

## Output

- `<reports_dir>/compliance/<YYYYMMDD-HHMMSS>.md`: frontmatter (`kind`, `generated`, `result`, `fails`, `warnings`, `answers_sha256`), a check table, and the "Proposed fixes" section you append.
- Final message: PASS/FAIL, the list of FAILs, and the single most important fix.

## Quality checks

- The report file exists, and its `answers_sha256` matches the current file.
- Every FAIL has a proposed fix naming a skill or command.
- `<answers>` was not modified.

## If inputs are missing

- No answers file: tell the user to run define-details (which creates it) and stop.
- No `.bib`: citations will fail. Recommend research-question or adding entries.
- No manifest: figure traceability WARNs are expected for written-only assignments. Say so.
