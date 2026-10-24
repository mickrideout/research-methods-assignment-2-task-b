---
name: check-environment
description: Validates the local computing environment for assignments that need code, experiments or tools. It detects required languages, versions, packages, GPU/CUDA, datasets and starter code from the spec, checks what is installed, smoke-tests the starter code, and writes a timestamped pass/fail environment report with proposed fixes. It never installs anything without asking. Use after define-details when code.required is true, or before running experiments on a new machine.
---

# check-environment

## Purpose

Find environment problems before you depend on them: wrong versions, missing packages,
no GPU, missing datasets, or starter code that does not run.

## When to use

- Only when `code.required: true` in the details file (conditional stage), after `define-details`.
- Again after installing anything, or on a different machine. Each run writes a new report.

Do not use it for written-only assignments, or to write solution code (`run-experiments` does that).

## Inputs

Path placeholders such as `<code_dir>` mean `paths.code_dir` in the details file.

1. `context/assignment.md` (always first): the `code:` block and paths.
2. Extracted spec text and `<inputs>/starter/` (README, requirements files, imports, notebook headers) and `<inputs>/data/`.
3. Script: `scripts/env_check.py`. It is read-only, prints JSON or a Markdown table, and exits 1 on any FAIL.
4. Format: `templates/environment-report.md`.

## Procedure

1. Read `context/assignment.md`. If `code.required` is not `true`, say so and stop. Write no report.
2. Detect requirements the details file may have missed. Scan the spec, the starter README, `requirements*.txt`, `pyproject.toml`, `environment.yml`, `package.json`, notebook imports and any mentions of GPU, CUDA or dataset downloads.
   - List anything missing from the `code:` block under "Requirements detected … not yet in the details file" in the report.
   - Do not edit the details file. Suggest re-running define-details or ask the user before editing.
3. If `<code_dir>` has no code yet and starter code exists, copy `<inputs>/starter/` into `<code_dir>/`. `inputs/` stays pristine.
4. Run `python3 skills/check-environment/scripts/env_check.py --md --smoke`. Add `--python <path>` if the unit uses a specific interpreter or virtual environment.
5. For each FAIL, propose one concrete fix: a command, its scope (virtual environment or system), and its risk. Prefer project-local virtual environments, e.g. `python3 -m venv <code_dir>/.venv`. **Ask before running any install command**, and run only the approved ones.
6. If no lock or requirements file exists in `<code_dir>`, propose one built from `code.packages`, e.g. `requirements.txt` with the pinned versions that pass. Write it only after the user approves.
7. Get a path with `python3 <tools>/report_path.py environment`. Write the report there, following the template. Paste the `--md` table verbatim and add the smoke-test output tail.
8. Log the run: `python3 <tools>/log_ai_use.py --skill check-environment --action "Checked environment" --files <report path>`.

## Output

- `<reports_dir>/environment/<YYYYMMDD-HHMMSS>.md`: frontmatter fields `kind`, `generated`, `result`, `interpreter`, `fails` and `warnings`, then the template sections.
- `<code_dir>/`: starter copied in (if it was empty). A lock or requirements file only with approval.
- Final message: PASS/FAIL counts, the blocking failures, the fixes awaiting approval, and the next step: "plan-question <QID>".

## Quality checks

- Every item in the `code:` block appears in the report table.
- The smoke test was run, or there is a stated reason it could not be.
- Nothing was installed without explicit approval in this conversation.
- `inputs/starter/` is unchanged.

## If inputs are missing

- `code:` block empty but the spec mentions code: report this, list the detected requirements, and recommend re-running define-details.
- No starter code: skip the smoke test and say so.
- A dataset is missing: FAIL it with the download source from the spec. Never fabricate or substitute data.
- No GPU when one is required: FAIL. Suggest the options (lab machine, cloud, CPU fallback) and ask the user whether CPU runs are acceptable under the spec.
