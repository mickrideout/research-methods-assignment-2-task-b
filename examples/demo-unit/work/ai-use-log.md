# AI-use log

Every skill appends one row via `python3 tools/log_ai_use.py`. Fill in **Your review**
(how you checked, changed or rejected the output); many units require this for the
acknowledgement. export-submission builds the AI acknowledgement from this log.

| When | Skill | Question | Agent / model | What the AI did | Files touched | Your review |
|---|---|---|---|---|---|---|
| 2026-10-19T09:51+11:00 | define-details | - | demo walkthrough | Extracted assignment facts from spec/rubric/clarifications | context/assignment.md |  |
| 2026-10-19T09:51+11:00 | enhance-rubric | - | demo walkthrough | Built enhanced rubric and checklist | context/rubric.yaml, context/checklist.yaml |  |
| 2026-10-19T09:52+11:00 | check-environment | - | demo walkthrough | Checked environment; created requirements.txt (approved) | reports/environment/20261019-095207.md, work/code/requirements.txt |  |
| 2026-10-19T09:52+11:00 | plan-question | Q1 | demo walkthrough | Planned structure and evidence | work/questions/Q1/plan.md |  |
| 2026-10-19T09:52+11:00 | plan-question | Q2 | demo walkthrough | Planned structure and evidence | work/questions/Q2/plan.md |  |
| 2026-10-19T09:52+11:00 | research-question | Q1 | demo walkthrough | Collected evidence (web: off) | work/questions/Q1/research.md, work/references/references.bib |  |
| 2026-10-19T09:53+11:00 | run-experiments | Q2 | demo walkthrough | Implemented smoother; ran tests and RMSE/figure | work/code/smoother.py, work/code/run_q2.py, work/results/tables/Q2-rmse.md, work/results/figures/Q2-smoothing.png |  |
| 2026-10-19T09:53+11:00 | answer-question | Q1 | demo walkthrough | Drafted answer (draft mode) | answers/answers.md, work/questions/Q1/sources.md |  |
| 2026-10-19T09:53+11:00 | answer-question | Q2 | demo walkthrough | Drafted answer (draft mode) | answers/answers.md, work/questions/Q2/sources.md |  |
| 2026-10-19T09:54+11:00 | grade-question | Q1 | demo walkthrough | Graded against rubric | reports/grading/Q1/20261019-095330.md |  |
| 2026-10-19T09:54+11:00 | grade-question | Q2 | demo walkthrough | Graded against rubric | reports/grading/Q2/20261019-095400.md |  |
| 2026-10-19T09:54+11:00 | answer-question | Q1 | demo walkthrough | Revised answer (--from reports/grading/Q1/20261019-095330.md; fixes 1-2 applied) | answers/answers.md |  |
| 2026-10-19T09:54+11:00 | check-compliance | - | demo walkthrough | Ran compliance checks | reports/compliance/20261019-095415.md |  |
| 2026-10-19T09:54+11:00 | grade-question | Q1 | demo walkthrough | Re-graded after revision | reports/grading/Q1/20261019-095436.md |  |
| 2026-10-19T09:54+11:00 | grade-assignment | - | demo walkthrough | Graded whole assignment | reports/grading/assignment/20261019-095451.md |  |
| 2026-10-19T09:56+11:00 | export-submission | - | demo walkthrough | Wrote AI use statement; built PDF + code zip; pre-submission check (NO-GO) | export/DSCI9001_A2_12345678.pdf, export/DSCI9001_A2_12345678_code.zip, reports/presubmission/20261019-095559.md |  |
