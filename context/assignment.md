---
# COMMON DETAILS FILE: single source of truth for assignment facts and project paths.
# Every skill reads this first. Validate with: python3 tools/details.py validate
# Convention: null = UNKNOWN (must have an open question whose `field` names it);
#             "n/a" / false / [] = NOT APPLICABLE. Cite where each fact came from in `sources`.
schema_version: 1
status: draft                     # draft | confirmed (set to confirmed once you have checked it)

unit:
  code: FIT5125
  name: IT Research and Innovation Methods
assignment:
  title: "Task B: Working with Hypotheses"
  number: 2
  due: "2026-11-02"               # date from OQ6; time of day not given
  weighting_pct: 10
  total_marks: 10
  individual_or_group: individual
student:
  name: Michael Rideout
  id: "36809268"

questions:
  - id: TB
    title: Working with Hypotheses
    marks: 10
    word_limit: 550               # sum of per-heading limits as resolved in OQ1-OQ3: 50+50+50+100+150+100+50
    type: written
    source: inputs/spec/task-b-spec.md#line.9

word_count:
  scope: per_question
  total_limit: "n/a"
  tolerance_pct: 0                # strict: words beyond the limit are not marked
  exclude: [headings, references, code_blocks, captions]   # in-text citations COUNT; tables are counted (conservative)

referencing:
  style: APA 7th
  notes: "References are not required. If used, cite in APA 7; in-text citations count toward each section's word limit; the reference list does not. An optional 'References' heading may follow heading 7."

format:
  file_type: pdf
  reference_docx: "n/a"
  font: "n/a"                     # no requirement stated
  font_size: "n/a"
  line_spacing: "n/a"
  margins: "n/a"
  page_limit: "n/a"
  cover_page: "n/a"               # no cover page; heading 0 carries name and student ID
  required_sections:
    - "Your Name & Student ID"
    - "Proposed Hypothesis"
    - "Null Hypothesis"
    - "Independent, Dependent and Confounding Variables"
    - "Data Collection"
    - "Statistical Tests"
    - "Limitations"
    - "Alternative Narrative"
  other:
    - "Use the prescribed headings numbered 0 to 7 in order (heading 0 = 'Your Name & Student ID'); an optional 'References' heading may be added at the end."
    - "Strict word limits: for answers that exceed a limit, only the part within the limit is marked."
    - "Per-heading word limits inside TB (the marker applies these per heading): 1 Proposed Hypothesis 50; 2 Null Hypothesis 50; 3 Variables 50; 4 Data Collection 100 (OQ1); 5 Statistical Tests 150; 6 Limitations 100 (OQ2); 7 Alternative Narrative 50 (OQ3). Total 550. Each is the lower of the spec's two conflicting figures."
    - "Rubric criteria map to headings: Hypothesis and null hypothesis (2) -> headings 1-2; Variables (2) -> 3; Data Collection (2) -> 4; Statistical Analysis (2) -> 5; Study Limitations and Alternative Narrative (2) -> 6-7."
    - "Layout and aesthetics are not graded (A1 staff comment, stated as transferable to A2)."

submission:
  method: Moodle
  filename_pattern: "{student_id}-Assignment-2-Task-B"
  files: [{name: report, type: pdf}]
  code_bundle: false

spelling: en-AU

code:
  required: false
  languages: []
  packages: []
  tools: []
  hardware: {gpu: false, cuda: null, min_ram_gb: null, min_disk_gb: null}
  datasets: []
  starter: {path: inputs/starter, smoke_test: null}
  interpreter: null
  max_run_minutes: 30

genai:
  policy: permitted
  permitted_uses: []
  prohibited_uses: []
  acknowledgement_required: false     # OQ5: the student adds any acknowledgement manually; export does not generate one
  acknowledgement_format: "n/a"
  source: "context/assignment.md open_questions OQ4 (student's answer: 'gen ai is allowed'); no policy text in inputs/"

research:
  web_search: false

grade_bands:                      # highest first; min_pct is the band's lower bound
  - {code: HD, label: High Distinction, min_pct: 85}
  - {code: D,  label: Distinction,      min_pct: 75}
  - {code: C,  label: Credit,           min_pct: 65}
  - {code: P,  label: Pass,             min_pct: 50}
  - {code: N,  label: Fail,             min_pct: 0}

paths:                            # every key project file; skills never hardcode these
  details: context/assignment.md
  inputs: inputs
  extracted: context/extracted
  rubric_md: context/rubric.md
  rubric_yaml: context/rubric.yaml
  checklist_md: context/checklist.md
  checklist_yaml: context/checklist.yaml
  answers: answers/answers.md
  questions_dir: work/questions
  bibliography: work/references/references.bib
  csl: work/references/style.csl
  code_dir: work/code
  results_dir: work/results
  results_manifest: work/results/manifest.yaml
  ai_log: work/ai-use-log.md
  reports_dir: reports
  export_dir: export
  templates_dir: templates
  tools_dir: tools

sources:
  - {field: unit.code, source: "inputs/clarifications/Assignment-2-faq.md#line.1"}
  - {field: assignment.title, source: "inputs/rubric/task-b-rubric.md#line.1"}
  - {field: assignment.number, source: "inputs/spec/task-b-spec.md#line.19"}
  - {field: assignment.total_marks, source: "inputs/rubric/task-b-rubric.md#line.1"}
  - {field: assignment.individual_or_group, source: "inputs/spec/task-b-spec.md#line.37"}
  - {field: questions, source: "inputs/spec/task-b-spec.md#line.9", note: "one answered part (TB); the spec's tasks 1-7 are heading sections within it (lines 21-28), at the user's direction"}
  - {field: questions.TB.marks, source: "inputs/rubric/task-b-rubric.md#line.1", note: "five criteria x 2 marks (lines 6-10)"}
  - {field: questions.TB.word_limit, source: "inputs/spec/task-b-spec.md#line.9", note: "per-heading limits from lines 9-15 and 22-28; conflicts at headings 4, 6 and 7 resolved by the student in OQ1-OQ3 (100, 100, 50); total 550"}
  - {field: word_count.scope, source: "inputs/spec/task-b-spec.md#line.32"}
  - {field: word_count.tolerance_pct, source: "inputs/spec/task-b-spec.md#line.32", note: "strict limit; excess words not marked"}
  - {field: word_count.exclude, source: "inputs/clarifications/task-b-additional-info.md#line.46", note: "in-text citations count (line 46); reference list does not (line 47); headings excluded is the template default"}
  - {field: referencing.style, source: "inputs/clarifications/task-b-additional-info.md#line.48", note: "FAQ (2026-10-19) agrees: inputs/clarifications/Assignment-2-faq.md#line.85"}
  - {field: referencing.notes, source: "inputs/clarifications/Assignment-2-faq.md#line.85"}
  - {field: format.file_type, source: "inputs/spec/task-b-spec.md#line.19"}
  - {field: format.required_sections, source: "inputs/spec/task-b-spec.md#line.21", note: "headings 0-7 at lines 21-28; optional References heading per inputs/clarifications/task-b-additional-info.md#line.5"}
  - {field: format.cover_page, source: "inputs/spec/task-b-spec.md#line.21"}
  - {field: format.other, source: "inputs/spec/task-b-spec.md#line.22", note: "per-heading limits lines 9-15 and 22-28; layout not graded per inputs/clarifications/task-b-additional-info.md#line.57; criteria per inputs/rubric/task-b-rubric.md#line.6"}
  - {field: submission.filename_pattern, source: "inputs/spec/task-b-spec.md#line.19", note: "STUDENT-ID-Assignment-2-Task-B.pdf"}
  - {field: submission.files, source: "inputs/spec/task-b-spec.md#line.19"}
  - {field: spelling, source: "inputs/spec/task-b-spec.md#line.37", note: "Monash University (Australia); en-AU is the project default"}
  - {field: code.required, source: "inputs/spec/task-b-spec.md#line.3", note: "a study plan only; no data are collected or analysed"}

open_questions:
  - id: OQ1
    question: "Heading 4 (Data Collection) word limit conflicts within the spec: the task list says 'max. 150 words' (line 12) but the prescribed heading says '4. Data Collection (< 100 words)' (line 25). The forum notes refer to a 'corrected spec (see §1.3)' that is not in inputs/. Which limit applies? (Safe default: 100, which satisfies both readings.)"
    field: format.other
    affects: [TB]
    blocking: true
    source: inputs/spec/task-b-spec.md#line.12
    answer: 100
  - id: OQ2
    question: "Heading 6 (Limitations) word limit conflicts within the spec: the task list says 'max. 100 words' (line 14) but the heading says '6. Limitations (< 200 words)' (line 27). Which limit applies? (Safe default: 100.)"
    field: format.other
    affects: [TB]
    blocking: true
    source: inputs/spec/task-b-spec.md#line.14
    answer: 100
  - id: OQ3
    question: "Heading 7 (Alternative Narrative) word limit conflicts within the spec: the task list says 'max. 100words' (line 15) but the heading says '7. Alternative Narrative (< 50 words)' (line 28). Which limit applies? (Safe default: 50.) Also: is inputs/spec/task-b-spec.md the 'corrected spec' the forum refers to (inputs/clarifications/task-b-additional-info.md#line.118), and should the word limits be printed in the headings as the spec shows them?"
    field: format.other
    affects: [TB]
    blocking: true
    source: inputs/spec/task-b-spec.md#line.15
    answer: 50
  - id: OQ4
    question: "What is the unit's generative-AI policy for Assignment 2? None of the inputs state it. Please add the policy text (unit guide, Moodle or spec section) to inputs/clarifications/ or quote it here, including permitted and prohibited uses."
    field: genai.policy
    affects: [TB]
    blocking: true
    source: inputs/spec/task-b-spec.md#line.37
    answer: gen ai is allowed
  - id: OQ5
    question: "Is an acknowledgement of generative-AI use required in the submission, and if so in what wording or format?"
    field: genai.acknowledgement_required
    affects: [TB]
    blocking: false
    source: inputs/spec/task-b-spec.md#line.19
    answer: i will manually add
  - id: OQ6
    question: "When is Task B due (date, time and time zone)? Not stated in the inputs."
    field: assignment.due
    affects: []
    blocking: false
    source: inputs/spec/task-b-spec.md#line.17
    answer: 2nd November
  - id: OQ7
    question: "What percentage of the unit grade is Assignment 2 Task B worth? The rubric gives 10 marks but no weighting."
    field: assignment.weighting_pct
    affects: []
    blocking: false
    source: inputs/rubric/task-b-rubric.md#line.1
    answer: 10
  - id: OQ8
    question: "What is the full name of unit FIT5125?"
    field: unit.name
    affects: []
    blocking: false
    source: inputs/clarifications/Assignment-2-faq.md#line.1
    answer: IT Research and Innovation Methods
  - id: OQ9
    question: "How is the PDF submitted (e.g. Moodle assignment box with Turnitin)?"
    field: submission.method
    affects: []
    blocking: false
    source: inputs/spec/task-b-spec.md#line.17
    answer: moodle
  - id: OQ10
    question: "Your student ID (needed for heading 0 and the filename STUDENT-ID-Assignment-2-Task-B.pdf)."
    field: student.id
    affects: []
    blocking: false
    source: inputs/spec/task-b-spec.md#line.19
    answer: 36809268
  - id: OQ11
    question: "Your name as it should appear under heading 0."
    field: student.name
    affects: []
    blocking: false
    source: inputs/spec/task-b-spec.md#line.21
    answer: Michael Rideout
---

# FIT5125 Task B: Working with Hypotheses: assignment details

> Human-readable summary of the frontmatter above. The frontmatter is authoritative;
> define-details regenerates this body. Keep your own notes under "My notes".

## Overview

- **Unit:** FIT5125 IT Research and Innovation Methods
- **Assignment:** Assignment 2, Task B: Working with Hypotheses, individual (10% of the unit; total 10 marks)
- **Topic:** "How does social media influence the perceptions of young Australians regarding the housing crisis?" Here "young Australian" means anyone aged 18–30 who does not yet own a home. The task is to propose and justify a study plan, including statistical testing, on a budget of up to AUD 1,000 plus up to 100 hours of your time.
- **Due:** 2 November 2026 (time of day not given; AEDT applies)
- **Submission:** one PDF named `STUDENT-ID-Assignment-2-Task-B.pdf`; submitted via Moodle
- **Learning outcomes:** ULO1 (frame and design all aspects of the research and innovation pipeline) and ULO4 (evaluate, select and justify research and innovation methods, including data collection and analysis).

## Questions

| ID | Title | Marks | Word limit | Type | Source |
|---|---|---|---|---|---|
| TB | Working with Hypotheses | 10 | 550 total | written | inputs/spec/task-b-spec.md#line.9 |

The task is answered as one question. The spec's seven tasks are the prescribed heading sections inside it, each with its own strict word limit:

| Heading | Spec task | Word limit | Rubric criterion (marks) |
|---|---|---|---|
| 0. Your Name & Student ID | – | – | – |
| 1. Proposed Hypothesis | 1 (line 9) | 50 | Hypothesis and null hypothesis (2, shared with 2) |
| 2. Null Hypothesis | 2 (line 10) | 50 | shared with 1 |
| 3. Independent, Dependent and Confounding Variables | 3 (line 11) | 50 | Variables (2) |
| 4. Data Collection | 4 (line 12) | 100 (OQ1) | Data Collection (2) |
| 5. Statistical Tests | 5 (line 13) | 150 | Statistical Analysis (2) |
| 6. Limitations | 6 (line 14) | 100 (OQ2) | Study Limitations and Alternative Narrative (2, shared with 7) |
| 7. Alternative Narrative | 7 (line 15) | 50 (OQ3) | shared with 6 |

`tools/wordcount.py` checks only the 550-word total for TB. The per-heading limits have to be checked by hand, or by the planning and grading skills. Heading 0 (name and student ID) sits inside TB, so its few words count toward the total.

**Rubric level marks:** each criterion is scored at fixed levels: N 0, P 1, C 1.25, D 1.5, HD 2 (whole task: 0 / 5 / 6.25 / 7.5 / 10). These percentages (50 / 62.5 / 75 / 100) do not line up with the template grade bands, which have been left unchanged. enhance-rubric should use the rubric's own level marks.

## Key requirements

- Referencing: not required. If used, APA 7th. In-text citations count toward each heading's word limit; the reference list does not. An optional "References" heading may follow heading 7.
- Word count: strict, 0% tolerance. Words beyond a limit are not marked. Excluded: headings, reference list, code blocks, captions. In-text citations and tables are counted. Note that the headings say "< 50" where the task list says "max. 50", so staying a word or two under each limit is safest.
- Formatting: a PDF with the prescribed headings 0–7 in order. No font, spacing, margin or page requirements are stated, and layout is not graded.
- Spelling: en-AU.
- Code and tools: none. This is a study plan, so nothing is run.
- Statistical tests: any appropriate test is allowed, including Welch's t-test. The choice must be justified against the hypothesis and variables, with its assumptions stated (FAQ 2026-10-19; forum 2026-10-17).
- Hypothesis guidance (teaching team): use PICO (population, intervention, comparison, outcome). Make the hypothesis directional only if there is a reason to. Never write "significantly" in the hypothesis. H0 states no difference or no association.
- Alternative narrative (FAQ): describe a specific hypothetical result that supports a different conclusion, and explain what changes to data selection, methods or processes would produce it. Do not just restate a null-test outcome or a limitation. Future investigations under heading 6 should address the limitations.
- Generative AI: **permitted**, per the student's answer to OQ4 (no policy text is in `inputs/`). The student will add any acknowledgement manually (OQ5), so export does not generate one.

## Open questions

| ID | Question | Affects | Blocking | Answer |
|---|---|---|---|---|
| OQ1 | Heading 4 word limit: 150 (task list) or < 100 (heading)? | TB | yes | 100 |
| OQ2 | Heading 6 word limit: 100 (task list) or < 200 (heading)? | TB | yes | 100 |
| OQ3 | Heading 7 word limit: 100 (task list) or < 50 (heading)? Is this the "corrected spec"? Print limits in headings? | TB | yes | 50 |
| OQ4 | Generative-AI policy for A2 | TB | yes | gen ai is allowed |
| OQ5 | Is an AI-use acknowledgement required, and in what format? | TB | no | i will manually add |
| OQ6 | Due date and time | – | no | 2nd November |
| OQ7 | Weighting (% of unit) | – | no | 10 |
| OQ8 | Unit name | – | no | IT Research and Innovation Methods |
| OQ9 | Submission method | – | no | moodle |
| OQ10 | Student ID | – | no | 36809268 |
| OQ11 | Student name | – | no | Michael Rideout |

## My notes

(Yours. define-details never changes this section.)
