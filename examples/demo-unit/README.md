# Demo: DSCI9001 Assignment 2 (fictional)

A fictional assignment taken through every pipeline stage, to show the file handoffs. It has two questions: Q1
is written (300 words) and Q2 is code plus a write-up (200 words). The answers are deliberately **placeholder
quality**. The demo shows the mechanics, not model answers. The unit, the reading, the forum posts
and the student are all invented.

The walkthrough ran in a fresh copy of the template (`skills/`, `tools/` and `templates/` are not duplicated
here). An agent following each SKILL.md wrote the documents, and the deterministic steps used the scripts.
To re-run the deterministic parts automatically, use `python3 tools/selftest.py` from the repository root.

## Inputs (what the "university" supplied)

| File | Format | Tests |
|---|---|---|
| `inputs/spec/dsci9001-a2-brief.pdf` | PDF | `pdftotext` page markers |
| `inputs/rubric/dsci9001-a2-rubric.docx` | DOCX table | DOCX table extraction (`#table.1`) |
| `inputs/lectures/week03-reproducible-workflows.pptx` | PPTX with speaker notes | slide markers + notes |
| `inputs/readings/nguyen2024-practical-reproducibility.pdf` | PDF | citations with `file` field |
| `inputs/outcomes/`, `inputs/feedback/` | Markdown | rubric enrichment sources |
| `inputs/clarifications/2026-10-20-…`, `2026-10-21-…` | Markdown | word-count rules; resolving open questions |
| `inputs/starter/` (stubbed `smoother.py` + tests), `inputs/data/sensor.csv` | code, CSV | environment check, experiments |

## Walkthrough

| # | Stage | What happened | Artefacts |
|---|---|---|---|
| 0 | init | `tools/init_project.py` copied the templates and made the symlinks | `context/assignment.md` (blank) |
| 0b | extract | 10 inputs, all extracted or indexed; a second run reprocessed 0 | `context/extracted/INDEX.md` |
| 1 | define-details | Facts filled with sources. **2 open questions**: word tolerance ("approximate") and the Harvard variant. `answer_section.py init` built Q1, Q2 and AI-ACK sections (AI-ACK because acknowledgement is required) | `context/assignment.md`, `answers/answers.md` |
| 1h | you | Forum reply saved; OQ1 = ±10%, OQ2 = Cite Them Right; CSL file downloaded | `inputs/clarifications/2026-10-21-…`, `work/references/style.csl` |
| 2 | enhance-rubric | 3 criteria (verbatim wording, weights 40/40/20, observable levels, sourced evidence and pitfalls); 11 checklist items. `check_rubric.py`: 0 errors, 0 warnings (verbatim wording verified) | `context/rubric.{md,yaml}`, `context/checklist.{md,yaml}` |
| 3 | check-environment | All requirements PASS. The smoke test FAILs as expected (starter stubs raise `NotImplementedError`). `requirements.txt` created after approval | `reports/environment/…`, `work/code/` |
| 4 | plan-question Q1, Q2 | Criteria → sections → word budget; evidence and runs needed | `work/questions/Q*/plan.md` |
| 5 | research-question Q1 | Verbatim quotes with `file#p.1`; 2 bib entries with `file` fields | `work/questions/Q1/research.md`, `references.bib` |
| 6 | run-experiments Q2 | Smoother implemented; tests and RMSE/figure run through `run_logged.py` | `work/results/**`, `manifest.yaml`, `work/questions/Q2/results.md` |
| 7 | answer-question Q1, Q2 | Sections written by `answer_section.py put`; the bytes outside each section were verified identical | `answers/answers.md`, `work/questions/Q*/sources.md` |
| 8 | grade-question Q1, Q2 | Reports with per-criterion levels, quotes and fixes. Fingerprint unchanged before and after | `reports/grading/Q1/…095330.md`, `reports/grading/Q2/…` |
| 7r | answer-question Q1 --from report | Fixes 1–2 applied. The old version went to `history/`; `report_status.py` then showed Q1 **STALE** | `work/questions/Q1/history/…` |
| 8 | grade-question Q1 (again) | Fresh report, 41/50 | `reports/grading/Q1/…095436.md` |
| 9 | check-compliance | **FAIL**, correctly: the AI use statement was missing. Proposed fixes appended | `reports/compliance/…095415.md` |
| 10 | grade-assignment | 80.5/100 (D, range 76–84); C3 counted once; fix list ranked by marks per effort | `reports/grading/assignment/…` |
| 11 | export-submission | AI use statement written from the log; compliance PASS; PDF + code zip; only the AI-ACK hash changed; GO | `export/`, `reports/presubmission/…` |

The full AI-use trail is in `work/ai-use-log.md`. The "Your review" column is blank because that column is the student's to fill in.

## Issues the walkthrough found and fixed in the template

- A section-marker regex matched across the preceding newline. This was fixed in `tools/_sections.py`.
- DOCX rubric tables were extracted one cell per paragraph. They are now Markdown tables (`#table.N`).
- Pre-submission freshness compared whole-file hashes, so writing AI-ACK always made the grade look stale.
  It is now per question section (`section_sha256`).
- PDF figures floated to the end. They are now kept in place.
- Run IDs and log filenames used different timestamps. They now share one.
