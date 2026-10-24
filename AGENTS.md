# AGENTS.md: assignment project instructions

These instructions are for any coding or AI agent working in this repository. This file is canonical.
`CLAUDE.md` is a symlink to it, and `.claude/skills` is a symlink to `skills/`.

This repository is one postgraduate assignment, copied from a template. The pipeline turns
the files in `inputs/` into a graded, compliant submission in `export/`. Each stage is a skill in
`skills/<name>/SKILL.md` (open Agent Skills format).

## Hard rules

1. **Read `context/assignment.md` first, every time.** Its frontmatter is the single source of truth
   for assignment facts and **all paths** (`paths.*`). It is the only path any skill may hardcode.
   Elsewhere, `<answers>`, `<tools>` and similar mean `paths.answers`, `paths.tools_dir` and so on.
2. **One answer file.** All answers live in `paths.answers`. Each question owns
   `<!-- BEGIN <ID> -->` … `<!-- END <ID> -->`. Write sections **only** with
   `python3 tools/answer_section.py put <ID> --from <file>`. Never edit that file by any other means.
3. **Answering is human-initiated.** Answer only the single question ID the user names. Never chain to
   another question, never pick the "next" one, and never run a suggested follow-up command yourself.
   The same rule applies to plan-question, research-question and run-experiments.
4. **Graders never edit answers.** grade-question, grade-assignment and check-compliance only write
   reports. They verify with `tools/fingerprint.py` that nothing changed.
5. **Never invent** references, page numbers, quotes, data, results or experiments. Cite only what is
   in `inputs/` or verified in the `.bib`. Report only results recorded in `paths.results_manifest`.
   If something is missing, stop and tell the user what is needed.
6. **`inputs/` is read-only.** Starter code is copied to `paths.code_dir` before you work on it.
7. **Ask before installing anything**, before runs longer than `code.max_run_minutes`, before GPU use,
   and before overwriting changed facts in the details file.
8. **Respect the unit's generative-AI policy** (`genai.*`). If it is `prohibited`, do not draft. If it is
   `unclear`, ask first. Every skill appends one row to the AI-use log via `tools/log_ai_use.py`.
9. **Australian English** (or whatever `spelling` says) in all generated text.
10. **Don't commit.** Skills never `git commit`. The user commits after each stage.
11. **Ignore `examples/`** unless the user asks about it. It is a fictional demo project.

## Pipeline

| # | Stage | Skill / command | Trigger | Writes |
|---|---|---|---|---|
| 0 | Set up from template | `python3 tools/init_project.py` | manual, once | `context/assignment.md`, `work/ai-use-log.md`, `work/references/references.bib`, symlinks |
| 0b | Extract inputs | `python3 tools/extract_inputs.py` | auto (skills run it) | `context/extracted/**`, `INDEX.md`, `index.json` |
| 1 | Define common details | `define-details` | manual | `context/assignment.md`, `answers/answers.md` (skeleton) |
| 1h | Resolve open questions | the user | manual | `open_questions[].answer` |
| 2 | Enhance rubric + checklist | `enhance-rubric` | manual | `context/rubric.{md,yaml}`, `context/checklist.{md,yaml}` |
| 3 | Validate environment | `check-environment` | conditional: `code.required` | `reports/environment/<ts>.md`, `work/code/` |
| 4 | Plan a question | `plan-question <QID>` | manual | `work/questions/<QID>/plan.md` |
| 5 | Research a question | `research-question <QID>` | manual, optional | `work/questions/<QID>/research.md`, `.bib` (append) |
| 6 | Code and experiments | `run-experiments <QID>` | conditional: runs needed | `work/code/**`, `work/results/**`, manifest |
| 7 | Answer / revise | `answer-question <QID> [--from <report>]` | manual | section `<QID>` only, `sources.md`, `history/` |
| 8 | Grade a question | `grade-question <QID>` | manual, fresh context | `reports/grading/<QID>/<ts>.md` |
| 9 | Compliance | `check-compliance` | manual (also run inside 10, 11) | `reports/compliance/<ts>.md` |
| 10 | Grade the assignment | `grade-assignment` | manual, fresh context | `reports/grading/assignment/<ts>.md` |
| 11 | Export + pre-submission | `export-submission` | manual | `export/*`, AI-ACK section, `reports/presubmission/<ts>.md` |

**Invoking a skill:** if your agent discovers skills natively, use it. Otherwise, when the user
names a skill, for example "answer-question Q2", "/answer-question Q2" or "answer Q2", open
`skills/<name>/SKILL.md` and follow it exactly. Its frontmatter `description` says when it applies.

## Conventions

- **Question IDs** come from the details file (`Q1`, `Q2a`, `T3`, …) and never change. `AI-ACK` is reserved.
- **Sources** are cited as `inputs/<folder>/<file>#p.N` (`#slide.N`, `#para.N`, `#table.N`, `#line.N`, `#cell.N`).
- **Citations in answers** use pandoc syntax `[@key, p. N]`, with keys from `paths.bibliography`. The reference list is generated at export.
- **Figures and tables** in answers are linked relative to `answers/`, e.g. `../work/results/figures/Q2-x.png`. Every one must come from a logged run (`tools/run_logged.py`).
- **Reports** are never overwritten. Get a path from `python3 tools/report_path.py <kind> [QID]`, which gives `YYYYMMDD-HHMMSS.md`.
- **Freshness:** grading reports record `answer_sha256` and `rubric_sha256` (`tools/fingerprint.py`). A changed hash means the report is stale.
- **Null vs n/a** in the details file: `null` = unknown (needs an open question), `"n/a"` = not applicable.

## Tools (Python 3.10+, standard library + PyYAML; run from the project root)

| Script | Purpose |
|---|---|
| `tools/init_project.py` | copy templates into place, create symlinks (never overwrites) |
| `tools/extract_inputs.py [--check\|--force]` | page/slide-tagged text of inputs, incremental |
| `tools/details.py validate\|get\|path\|qids\|question\|open` | read and validate the details file |
| `tools/answer_section.py init\|check\|list\|get\|hash\|put` | the only writer of the answer file |
| `tools/wordcount.py [IDs] [--text f] [--json]` | word counts using `word_count.exclude` rules |
| `tools/check_rubric.py` | validate rubric and checklist YAML |
| `tools/run_logged.py --name --qid --outputs -- cmd` | run with provenance, append to the results manifest |
| `tools/compliance.py [--out path]` | deterministic compliance checks |
| `tools/report_path.py <kind> [QID] [--latest]` | timestamped report paths |
| `tools/fingerprint.py [QID]` | hashes for report frontmatter and no-edit checks |
| `tools/log_ai_use.py` | append to the AI-use log |
| `tools/export.py [--to] [--dry-run]` | pandoc export + `export/MANIFEST.md` |
| `tools/validate_skills.py` | validate every SKILL.md |
| `tools/selftest.py` | end-to-end test of the tools on `examples/` |

External tools: pandoc (export), poppler `pdftotext` (PDF extraction), xelatex or LibreOffice (PDF output).

## Layout

```
inputs/      read-only originals (spec, rubric, outcomes, lectures, readings, clarifications,
             feedback, exemplars, starter, data)
context/     assignment.md (details), rubric.{md,yaml}, checklist.{md,yaml}, extracted/
work/        questions/<QID>/, references/, code/, results/, ai-use-log.md
answers/     answers.md: the single answer file
reports/     grading/<QID>/, grading/assignment/, compliance/, environment/, presubmission/
export/      submission files + MANIFEST.md
templates/   fill-in templates and report formats
skills/      Agent Skills (SKILL.md + references/ + scripts/)
tools/       shared deterministic scripts
examples/    fictional demo assignment (ignore unless asked)
```
