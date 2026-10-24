---
name: run-experiments
description: Writes and runs the code, experiments and tool runs needed for ONE named assignment question. Code goes in work/code, and every result (figure, table, number) is produced through a logged run recorded in the results manifest, so answers can cite only real, reproducible outputs. Use when a question's plan lists runs needed, or the user asks to implement, run, test or reproduce results for a specific question ID. Asks before long or GPU runs.
---

# run-experiments

## Purpose

Produce real results with provenance. The answer skill may cite only outputs that are
recorded in the manifest, so nothing is invented.

## When to use

- A `code` or `mixed` question whose plan lists runs, and the user names that question ID.
- Re-run after changing code. New runs are appended to the manifest; old entries remain.

Do not use it for written-only questions, to fabricate or hand-edit results, or for more than one question.

## Inputs

Path placeholders such as `<code_dir>` mean `paths.code_dir` in the details file.
Argument: **one question ID (required)**.

1. `context/assignment.md` (always first): the `code:` block, `max_run_minutes` and paths.
2. `<questions_dir>/<QID>/plan.md`: "Runs needed".
3. The latest `<reports_dir>/environment/*.md`. If none exists or it shows a FAIL, see the section below.
4. `<code_dir>/` (starter code already copied in), `<inputs>/data/`, `<results_manifest>`.
5. Guide: [references/experiment-hygiene.md](references/experiment-hygiene.md).

## Procedure

1. Confirm the ID and read the plan's runs table. For each run, state the command, its expected outputs and an estimated runtime.
2. Ask before any run that is estimated to exceed `code.max_run_minutes`, uses a GPU, downloads data or installs packages.
3. Write or modify code under `<code_dir>/`. Keep functions small and testable. Fix random seeds. Read paths from arguments, not hardcoded literals. Add or extend tests under `<code_dir>/tests/` for core logic.
4. Run the tests: `python3 <tools>/run_logged.py --name <QID>-tests --qid <QID> -- <test command>`.
5. Run each experiment through the logger, declaring every output it should produce:
   `python3 <tools>/run_logged.py --name <short-name> --qid <QID> --outputs <results_dir>/figures/<QID>-x.png,<results_dir>/tables/<QID>-y.md -- <command>`
   Name outputs `<QID>-<what>.<ext>`. Save tables as Markdown (or CSV plus Markdown) so answers can include them.
6. If a run fails, read the log, fix the cause and re-run. Never edit an output file by hand, and never drop failed runs from the manifest.
7. Summarise the results in `<questions_dir>/<QID>/results.md`. For each output give: what it shows, the manifest run id, the key numbers (copied from the output files, not retyped from memory) and any caveats (seeds, sample size, variance).
8. Log the run: `python3 <tools>/log_ai_use.py --skill run-experiments --qid <QID> --action "Wrote code and ran experiments" --files <changed code>,<outputs>`.

## Output

- `<code_dir>/**`: code and tests.
- `<results_dir>/figures/`, `<results_dir>/tables/`, `<results_dir>/logs/`: outputs and logs, written by `run_logged.py`.
- `<results_manifest>`: run entries (command, git commit, exit code, output sha256s).
- `<questions_dir>/<QID>/results.md`: interpretation notes for the answer.
- Final message: the runs and their status, the key results, failures, and the next suggested command `answer-question <QID>` (not run).

## Quality checks

- Every output referenced in results.md has a manifest entry with `status: ok`.
- Tests pass, or the failures are reported.
- No run exceeded the approved time or resources.
- `inputs/` is unchanged; no data was synthesised to replace missing data.

## If inputs are missing

- No environment report, or a failing one: run check-environment first, or ask the user to accept the risk.
- Dataset missing: stop and tell the user where the spec says to get it.
- Plan missing: ask whether to run plan-question first. If the user declines, derive the runs from the question text and confirm the list with the user before running.
- Results contradict the expected outcome: report them as they are. Do not tune until they match.
