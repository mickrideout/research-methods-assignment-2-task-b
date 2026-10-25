# AI-use log

Every skill appends one row via `python3 tools/log_ai_use.py`. Fill in **Your review**
(how you checked, changed or rejected the output); many units require this for the
acknowledgement. export-submission builds the AI acknowledgement from this log.

| When | Skill | Question | Agent / model | What the AI did | Files touched | Your review |
|---|---|---|---|---|---|---|
| 2026-10-25T10:32+11:00 | define-details | - | - | Extracted assignment facts from spec/rubric | context/assignment.md |  |
| 2026-10-25T10:34+11:00 | define-details | TB | - | Collapsed Q1-Q7 into a single question TB at user's request; rebuilt empty answer skeleton | context/assignment.md,  answers/answers.md |  |
| 2026-10-25T10:43+11:00 | enhance-rubric | TB | - | Built enhanced rubric and checklist | context/rubric.yaml,  context/checklist.yaml |  |
| 2026-10-25T10:53+11:00 | enhance-rubric | TB | - | Incremental update: added Week 9 lecture summary as a source | context/rubric.yaml,  context/checklist.yaml |  |
| 2026-10-25T10:59+11:00 | plan-question | TB | - | Planned structure and evidence | work/questions/TB/plan.md |  |
| 2026-10-25T11:03+11:00 | plan-question | TB | - | Recorded student's design decisions D1-D6 in plan | work/questions/TB/plan.md |  |
| 2026-10-25T11:06+11:00 | run-experiments | TB | - | Wrote code and ran experiments (power calculation) | work/code/src/power.py,  work/code/tests/test_power.py,  work/results/tables/TB-power.md,  work/results/tables/TB-power.json,  work/questions/TB/results.md |  |
| 2026-10-25T11:09+11:00 | answer-question | TB | - | Drafted answer (draft mode) | answers/answers.md,  work/questions/TB/sources.md |  |
| 2026-10-25T11:15+11:00 | grade-question | TB | - | Graded against rubric | reports/grading/TB/20261025-111336.md |  |
| 2026-10-25T11:20+11:00 | answer-question | TB | - | Revised answer (revise mode, from reports/grading/TB/20261025-111336.md) | answers/answers.md, work/questions/TB/sources.md |  |
| 2026-10-25T11:29+11:00 | grade-question | TB | - | Graded against rubric | reports/grading/TB/20261025-112832.md |  |
| 2026-10-25T11:32+11:00 | answer-question | TB | - | Revised answer (revise mode from reports/grading/TB/20261025-112832.md) | answers/answers.md, work/questions/TB/sources.md |  |
| 2026-10-25T11:42+11:00 | grade-question | TB | - | Graded against rubric | reports/grading/TB/20261025-114021.md |  |
| 2026-10-25T11:45+11:00 | check-compliance | - | - | Ran compliance checks | reports/compliance/20261025-114505.md |  |
| 2026-10-25T11:49+11:00 | export-submission | - | - | Built export and pre-submission check | export/36809268-Assignment-2-Task-B.pdf, reports/presubmission/20261025-114926.md |  |
