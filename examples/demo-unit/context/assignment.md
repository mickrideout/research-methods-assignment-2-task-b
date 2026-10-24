---
# COMMON DETAILS FILE: single source of truth for assignment facts and project paths.
# Every skill reads this first. Validate with: python3 tools/details.py validate
# Convention: null = UNKNOWN (must have an open question whose `field` names it);
#             "n/a" / false / [] = NOT APPLICABLE. Cite where each fact came from in `sources`.
schema_version: 1
status: confirmed                   # draft | confirmed (set to confirmed once you have checked it)

unit:
  code: DSCI9001                  # e.g. COMP9001
  name: Foundations of Data Practice
assignment:
  title: Reproducible Analysis
  number: 2                       # e.g. 2 (used in export filename)
  due: 2026-11-13T23:59:00+11:00  # ISO 8601 with offset, e.g. 2026-11-07T23:59:00+11:00
  weighting_pct: 30               # % of the unit grade
  total_marks: 100                # marks the assignment is scored out of
  individual_or_group: individual
student:                          # used only for the export filename and title page
  name: Alex Example
  id: "12345678"

questions:                        # one entry per separately answered part; IDs are stable forever
  - id: Q1
    title: Reproducibility practices
    marks: 50
    word_limit: 300               # integer, or "n/a" if none
    type: written                 # written | code | mixed
    source: inputs/spec/dsci9001-a2-brief.pdf#p.1
  - id: Q2
    title: Smoothing a sensor series
    marks: 50
    word_limit: 200
    type: mixed
    source: inputs/spec/dsci9001-a2-brief.pdf#p.1

word_count:
  scope: per_question             # per_question | total | both
  total_limit: null               # or "n/a"
  tolerance_pct: 10               # OQ1 / clarification 2026-10-21
  exclude: [headings, references, code_blocks, tables, captions]   # clarification 2026-10-20: citations ARE counted

referencing:
  style: Harvard (Cite Them Right) # e.g. APA 7th, Harvard (AGPS), IEEE; CSL file goes at paths.csl
  notes: "Variant confirmed in clarification 2026-10-21 (OQ2)"                     # e.g. "minimum 10 peer-reviewed sources"

format:
  file_type: pdf                  # docx | pdf | md | html  (list allowed, e.g. [pdf, docx])
  reference_docx: null            # optional styled .docx for pandoc (e.g. a university template)
  font: "n/a"
  font_size: "n/a"
  line_spacing: "n/a"
  margins: "n/a"
  page_limit: "n/a"
  cover_page: "n/a"               # required? what must it contain?
  required_sections: [AI use statement]   # headings that must appear, e.g. [Executive summary, References]
  other: []

submission:
  method: Moodle assignment box (Turnitin)
  filename_pattern: "{unit_code}_A{assignment_number}_{student_id}"
  files: [{name: report, type: pdf}, {name: code, type: zip}]
  code_bundle: true               # true -> export zips paths.code_dir

spelling: en-AU                   # en-AU | en-GB | en-US | en-NZ | en-CA

code:
  required: true
  languages: [{name: python, version: ">=3.10"}]
  packages:                       # numpy/matplotlib permitted (spec p.1); pytest needed for the supplied tests
    - {name: numpy, version: null, ecosystem: pip}
    - {name: matplotlib, version: null, ecosystem: pip}
    - {name: pytest, version: null, ecosystem: pip}
  tools: []                       # e.g. [{name: docker, check: "docker --version"}]
  hardware: {gpu: false, cuda: null, min_ram_gb: null, min_disk_gb: null}
  datasets: [{name: sensor series, path: inputs/data/sensor.csv, url: null}]
  starter: {path: inputs/starter, smoke_test: "python3 -m pytest -q"}   # smoke_test runs in paths.code_dir
  interpreter: null               # e.g. work/code/.venv/bin/python
  max_run_minutes: 30             # runs longer than this need your approval

genai:
  policy: restricted              # prohibited | restricted | permitted | unclear
  permitted_uses: ["brainstorming", "feedback on your drafts", "code assistance"]
  prohibited_uses: ["submit AI-generated text as your own without acknowledgement"]
  acknowledgement_required: true  # true | false
  acknowledgement_format: "You must acknowledge any use in an \"AI use statement\" describing the tools used and how you used them."
  source: inputs/spec/dsci9001-a2-brief.pdf#p.1

research:
  web_search: false               # research-question may search the web only when true

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

sources:                          # facts -> evidence, e.g. [{field: assignment.due, source: inputs/spec/brief.pdf#p.1}]
  - {field: unit, source: inputs/spec/dsci9001-a2-brief.pdf#p.1}
  - {field: assignment, source: inputs/spec/dsci9001-a2-brief.pdf#p.1}
  - {field: questions, source: inputs/spec/dsci9001-a2-brief.pdf#p.1}
  - {field: word_count.exclude, source: inputs/clarifications/2026-10-20-forum-word-counts-and-edges.md#line.1}
  - {field: referencing.style, source: inputs/spec/dsci9001-a2-brief.pdf#p.1}
  - {field: submission, source: inputs/spec/dsci9001-a2-brief.pdf#p.1}
  - {field: code, source: inputs/spec/dsci9001-a2-brief.pdf#p.1}
  - {field: genai, source: inputs/spec/dsci9001-a2-brief.pdf#p.1}
  - {field: word_count.tolerance_pct, source: inputs/clarifications/2026-10-21-forum-tolerance-referencing.md#line.1}
  - {field: student, source: "user (fictional demo values)"}

open_questions:                   # anything ambiguous; YOU fill in `answer`
  - id: OQ1
    question: "Spec says 'Word limits are approximate'. What tolerance applies (e.g. +/-10%)?"
    field: word_count.tolerance_pct
    affects: [Q1, Q2]
    blocking: false
    source: inputs/spec/dsci9001-a2-brief.pdf#p.1
    answer: "+/-10% (unit coordinator, forum 2026-10-21; saved to inputs/clarifications/)"
  - id: OQ2
    question: "Spec says 'Harvard referencing'. Which variant (AGPS/Style Manual, Cite Them Right)? Needed to choose the CSL file."
    field: referencing.style
    affects: [Q1, Q2]
    blocking: false
    source: inputs/spec/dsci9001-a2-brief.pdf#p.1
    answer: "Cite Them Right Harvard (forum 2026-10-21)"
#  - id: OQ1
#    question: "Does the 1500-word limit include in-text citations?"
#    field: word_count.exclude    # the field this would settle (needed when that field is null)
#    affects: [Q1, Q2]
#    blocking: false              # true -> answer-question refuses affected questions until answered
#    source: inputs/spec/brief.pdf#p.2
#    answer: null                 # your answer, or "asked on forum <date>"
---

# DSCI9001 Reproducible Analysis: assignment details

> Human-readable summary of the frontmatter above. The frontmatter is authoritative;
> define-details regenerates this body. Keep your own notes under "My notes".

## Overview

- **Unit:** DSCI9001 Foundations of Data Practice (fictional)
- **Assignment:** 2, Reproducible Analysis (weighting 30%, marked out of 100), individual
- **Due:** Friday 13 November 2026, 11:59 pm AEDT (+11:00)
- **Submission:** Moodle (Turnitin): one PDF `DSCI9001_A2_<studentID>.pdf` plus a code zip

## Questions

| ID | Title | Marks | Word limit | Type | Source |
|---|---|---|---|---|---|
| Q1 | Reproducibility practices | 50 | ~300 | written | spec p.1 |
| Q2 | Smoothing a sensor series | 50 | ~200 + code | mixed | spec p.1 |

## Key requirements

- Referencing: Harvard (Cite Them Right); word limits ±10%
- Word count excludes headings, reference list, code, tables and captions; in-text citations count (forum, 20 Oct 2026)
- Spelling: Australian English
- Code: Python ≥ 3.10; numpy and matplotlib permitted; must pass the supplied tests with `python3 -m pytest`
- Q2 must state its edge-handling approach (forum, 20 Oct 2026)
- Generative AI: restricted (brainstorming, draft feedback, code assistance). An "AI use statement" section is required

## Open questions

| ID | Question | Affects | Blocking | Answer |
|---|---|---|---|---|
| OQ1 | Tolerance on "approximate" word limits? | Q1, Q2 | no | ±10% (forum 21 Oct) |
| OQ2 | Which Harvard variant? | Q1, Q2 | no | Cite Them Right (forum 21 Oct) |

## My notes

(Yours. define-details never changes this section.)
