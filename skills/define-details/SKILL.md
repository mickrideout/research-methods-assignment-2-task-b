---
name: define-details
description: Populates the assignment's common details file (context/assignment.md) from the specification, rubric and staff clarifications, covering unit, due date, weighting, question IDs with marks and word limits, referencing, format, submission, spelling, code requirements, generative-AI policy, grade bands and project paths, and records every ambiguity as an open question instead of guessing. Use when starting a new assignment project, when the spec or a clarification changes, or when the user asks to set up, fill in or update the assignment details.
---

# define-details

## Purpose

Create the single source of truth that every other skill reads first: YAML frontmatter
(machine-readable facts and paths) plus a readable body. It also creates the answer file
skeleton once the question list is known.

## When to use

- First stage of every assignment, after the files are in `inputs/`.
- Again when the spec changes or a staff clarification arrives (re-run is safe; see Procedure step 8).

Do not use it to answer, plan or grade questions, or to enhance the rubric (`enhance-rubric` does that).

## Inputs

Path placeholders such as `<answers>` mean `paths.answers` in the details file. Run commands from the project root.

1. `context/assignment.md` (always first). If it is missing, run `python3 tools/init_project.py` to copy it from `templates/`.
2. `<extracted>/INDEX.md` and the extracted text of `<inputs>/spec/`, `<inputs>/rubric/`, `<inputs>/clarifications/` (and `<inputs>/outcomes/` for the unit code and name).
3. Field guide: [references/details-schema.md](references/details-schema.md).

## Procedure

1. Read `context/assignment.md`. Note any open-question `answer` values the user has filled in. They are authoritative.
2. Refresh the extracted text: `python3 <tools>/extract_inputs.py`. Report any ERROR rows (for example a scanned PDF) and read those files directly if your agent can.
3. Read the whole spec and rubric (extracted text), then every clarification, oldest first. A later clarification overrides earlier wording. Note that in `sources`.
4. Fill every frontmatter field following `references/details-schema.md`:
   - Record the evidence for each fact in `sources` as `{field, source: inputs/<path>#p.N}`.
   - If a fact is not stated, or the sources disagree, set it to `null` and add an `open_questions` entry. Give it a `field`, the question, `affects`, `source` and `blocking` (true only when an answer could change what gets written). Never guess.
   - If a fact clearly does not apply, use `"n/a"`, `false` or `[]`.
   - Keep `paths` at the template defaults unless the user asks otherwise.
   - Never change `grade_bands` unless the spec or the unit states different bands.
5. Regenerate the body sections (Overview, Questions, Key requirements, Open questions) from the frontmatter. Leave `## My notes` exactly as it is.
6. Validate: `python3 <tools>/details.py validate`. Fix every ERROR. Explain any WARN that remains.
7. Create or extend the answer file: `python3 <tools>/answer_section.py init`. It creates `<answers>` from `templates/answers.md`, or adds sections for new question IDs only. It never rewrites existing sections.
8. On a re-run, show the user a field-by-field diff of the frontmatter changes. Ask before overwriting any value that differs from what is there now. Never rename or renumber an existing question ID. If the spec renames a question, record the mapping in `## My notes` and ask.
9. Log the run: `python3 <tools>/log_ai_use.py --skill define-details --action "Extracted assignment facts from spec/rubric" --files context/assignment.md`.

## Output

- `context/assignment.md`: frontmatter (schema in `templates/assignment.md`) and the regenerated body.
- `<answers>`: created or extended (insert-only) by `answer_section.py init`.
- `<extracted>/`: refreshed by `extract_inputs.py`.
- Final message to the user:
  - a summary table of the questions
  - the list of open questions (blocking ones first)
  - the next step: "Answer the open questions in `context/assignment.md`, then run enhance-rubric."

## Quality checks

- `details.py validate` exits 0.
- Every non-null fact has a `sources` entry with a page or slide locator.
- Every `null` fact has an open question whose `field` names it.
- The question IDs match the spec's numbering. Question marks sum to `total_marks`, or the body explains the difference.
- The generative-AI policy is quoted, not paraphrased, in `permitted_uses`, `prohibited_uses` and `acknowledgement_format`.
- `answer_section.py check` exits 0.

## If inputs are missing

- No spec in `<inputs>/spec/`: stop and ask the user to add it. Do not fill anything from memory or from the unit name.
- No rubric: fill what the spec gives. Add a blocking open question ("No marking rubric provided") that affects all questions.
- Spec unreadable (no text layer, extraction ERROR): read it directly if your agent can. Otherwise stop and ask for a text version.
- The generative-AI policy is not stated: set `genai.policy: unclear` with an open question. Downstream skills treat `unclear` as needing the user's confirmation before drafting.
