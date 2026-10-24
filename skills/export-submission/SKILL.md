---
name: export-submission
description: Assembles the final submission from answers/answers.md with pandoc into the required format (docx, pdf and so on), with citations rendered in the required style, the required filename and an optional code zip. It writes the generative-AI acknowledgement section from the AI-use log and the unit's policy, then runs a pre-submission checklist that ends in a GO/NO-GO decision. Use when the user asks to export, build, assemble, finalise or check readiness to submit the assignment.
---

# export-submission

## Purpose

Produce exactly the files that will be uploaded, then verify them against everything the
spec requires. The final step is a GO/NO-GO report. Submitting is always the user's action.

## When to use

- When the answers are final or near-final. Re-run freely: it overwrites `<export_dir>/*` and the AI-ACK section.

Do not use it to improve answer content (it changes no question section), or to submit anything.

## Inputs

Path placeholders such as `<export_dir>` mean `paths.export_dir` in the details file.

1. `context/assignment.md` (always first): `format`, `submission`, `student`, `genai`, `spelling`, `open_questions`.
2. `<answers>`, `<bibliography>`, `<csl>` (if present), `<ai_log>`, `<code_dir>` (if `submission.code_bundle`).
3. `<checklist_yaml>`, the latest `<reports_dir>/grading/assignment/` report, the latest compliance report.
4. Scripts: `<tools>/export.py`, `<tools>/compliance.py`, `<tools>/answer_section.py`.
5. Guides: [references/ai-acknowledgement.md](references/ai-acknowledgement.md), `templates/presubmission-report.md`.

## Procedure

1. **AI acknowledgement:**
   - If `genai.acknowledgement_required` is true, draft the acknowledgement from `<ai_log>` following `genai.acknowledgement_format` and the guide.
   - Start the draft with the heading the spec requires (a heading in `format.required_sections` such as "AI use statement"), or "Acknowledgement of generative AI use" if none is named.
   - Write it with `python3 <tools>/answer_section.py put AI-ACK --from <draft> --status final` (add `--create` if the section does not exist).
   - **Show the user the text and ask them to confirm it is accurate before continuing.** Only the user knows their full AI use.
   - If the log's "Your review" column is empty, warn that most units expect it to be filled in.
2. **Compliance:** run `python3 <tools>/compliance.py --out "$(python3 <tools>/report_path.py compliance)"`. If it reports any FAIL, stop with NO-GO, unless the user explicitly accepts a listed FAIL.
3. **Build:** run `python3 <tools>/export.py`. Use `--dry-run` first if the formats or filename look wrong. If the CSL file is missing and `referencing.style` is set, stop and ask the user to download the CSL (see the export.py note). Use the default style only if the user agrees.
4. **Inspect the output:**
   - Convert the main export to text, e.g. `pandoc <export_dir>/<name>.docx -t plain`, or `pdftotext <export_dir>/<name>.pdf -`.
   - Check that the reference list rendered, and that there are no `???`, unresolved `@key` citations, or leftover `<!--` markers.
   - Check that each figure appears.
   - Check that the headings match the required sections.
5. **Pre-submission checklist:** fill in every row of `templates/presubmission-report.md`:
   - every `must` item in `<checklist_yaml>`, with evidence
   - the latest assignment grade is current: its `section_sha256` matches the `sections` from `python3 <tools>/fingerprint.py` for every question (AI-ACK excluded, since this skill writes it)
   - no unresolved open questions
   - the export is newer than `<answers>`, and the filenames match
   - formatting rules that need eyes (font, cover page) are marked "check manually" when they cannot be verified from text
6. **Decide.** GO only if every row passes or the user has explicitly waived it. Write the report to `python3 <tools>/report_path.py presubmission`.
7. **Log the run:** `python3 <tools>/log_ai_use.py --skill export-submission --action "Built export and pre-submission check" --files <export files>,<report>`.

## Output

- `<export_dir>/<filename>.<ext>` for each format in `format.file_type`, `<export_dir>/<filename>_code.zip` (if required), `<export_dir>/MANIFEST.md`, and `<export_dir>/build/` (intermediate files).
- `<answers>`: the AI-ACK section only (if required).
- `<reports_dir>/presubmission/<YYYYMMDD-HHMMSS>.md` with `decision: GO|NO-GO`.
- Final message:
  - the decision
  - the files to upload, with their sizes
  - any blocking items
  - the user's manual steps: read the export end to end, fill in the AI-log review, then submit via `submission.method` before `assignment.due`

## Quality checks

- `export.py` exited 0 and every output passed its validity check (docx zip or `%PDF` header).
- The compliance report is from this run and shows PASS (or the user waived the listed FAILs).
- No question section changed. Check this with `fingerprint.py` before and after; only the AI-ACK hash may differ.
- The AI acknowledgement was confirmed by the user.

## If inputs are missing

- Policy `prohibited`: produce NO-GO and explain that AI-assisted content conflicts with the unit policy.
- `format.file_type` null: ask the user. Do not guess the format.
- `student.id` or `student.name` missing for the filename pattern: ask.
- pandoc or LaTeX missing: report it. For PDF, offer to export DOCX and convert it with LibreOffice.
