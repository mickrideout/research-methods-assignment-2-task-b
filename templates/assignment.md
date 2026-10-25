---
# COMMON DETAILS FILE: single source of truth for assignment facts and project paths.
# Every skill reads this first. Validate with: python3 tools/details.py validate
# Convention: null = UNKNOWN (must have an open question whose `field` names it);
#             "n/a" / false / [] = NOT APPLICABLE. Cite where each fact came from in `sources`.
schema_version: 1
status: draft                     # draft | confirmed (set to confirmed once you have checked it)

unit:
  code: null                      # e.g. COMP9001
  name: null
assignment:
  title: null
  number: null                    # e.g. 2 (used in export filename)
  due: null                       # ISO 8601 with offset, e.g. 2026-11-07T23:59:00+11:00
  weighting_pct: null             # % of the unit grade
  total_marks: null               # marks the assignment is scored out of
  individual_or_group: individual
student:                          # used only for the export filename and title page
  name: null
  id: null

questions:                        # one entry per separately answered part; IDs are stable forever
  - id: Q1
    title: null
    marks: null
    word_limit: null              # integer, or "n/a" if none
    type: written                 # written | code | mixed
    source: null                  # e.g. inputs/spec/brief.pdf#p.3

word_count:
  scope: per_question             # per_question | total | both
  total_limit: null               # or "n/a"
  tolerance_pct: 0                # e.g. 10 for "+/-10%"
  exclude: [headings, references, code_blocks, tables, captions]   # see tools/wordcount.py for options

referencing:
  style: null                     # e.g. APA 7th, Harvard (AGPS), IEEE; CSL file goes at paths.csl
  notes: null                     # e.g. "minimum 10 peer-reviewed sources"

format:
  file_type: null                 # docx | pdf | tex | md | html  (list allowed, e.g. [pdf, docx]); pdf is compiled from LaTeX
  reference_docx: null            # optional styled .docx for pandoc docx output (e.g. a university template)
  font: null
  font_size: null
  line_spacing: null
  margins: null
  page_limit: "n/a"
  cover_page: null                # required? what must it contain?
  required_sections: []           # headings that must appear, e.g. [Executive summary, References]
  other: []

submission:
  method: null                    # e.g. LMS assignment box with Turnitin
  filename_pattern: "{unit_code}_A{assignment_number}_{student_id}"
  files: []                       # e.g. [{name: report, type: pdf}, {name: code, type: zip}]
  code_bundle: false              # true -> export zips paths.code_dir

spelling: en-AU                   # en-AU | en-GB | en-US | en-NZ | en-CA

code:
  required: false
  languages: []                   # e.g. [{name: python, version: ">=3.10"}]
  packages: []                    # e.g. [{name: numpy, version: ">=1.26", ecosystem: pip}]
  tools: []                       # e.g. [{name: docker, check: "docker --version"}]
  hardware: {gpu: false, cuda: null, min_ram_gb: null, min_disk_gb: null}
  datasets: []                    # e.g. [{name: train, path: inputs/data/train.csv, url: null}]
  starter: {path: inputs/starter, smoke_test: null}   # smoke_test runs in paths.code_dir
  interpreter: null               # e.g. work/code/.venv/bin/python
  max_run_minutes: 30             # runs longer than this need your approval

genai:
  acknowledgement_required: null  # true | false
  acknowledgement_format: null    # quote the required wording/format verbatim
  source: null

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

sources: []                       # facts -> evidence, e.g. [{field: assignment.due, source: inputs/spec/brief.pdf#p.1}]

open_questions: []                # anything ambiguous; YOU fill in `answer`
#  - id: OQ1
#    question: "Does the 1500-word limit include in-text citations?"
#    field: word_count.exclude    # the field this would settle (needed when that field is null)
#    affects: [Q1, Q2]
#    blocking: false              # true -> answer-question refuses affected questions until answered
#    source: inputs/spec/brief.pdf#p.2
#    answer: null                 # your answer, or "asked on forum <date>"
---

# {{unit.code}} {{assignment.title}}: assignment details

> Human-readable summary of the frontmatter above. The frontmatter is authoritative;
> define-details regenerates this body. Keep your own notes under "My notes".

## Overview

- **Unit:** …
- **Assignment:** … (weighting …%, total … marks)
- **Due:** … (time zone …)
- **Submission:** … as … named …

## Questions

| ID | Title | Marks | Word limit | Type | Source |
|---|---|---|---|---|---|

## Key requirements

- Referencing: …
- Formatting: …
- Spelling: …
- Code and tools: …
- Generative AI acknowledgement: …

## Open questions

| ID | Question | Affects | Blocking | Answer |
|---|---|---|---|---|

## My notes

(Yours. define-details never changes this section.)
