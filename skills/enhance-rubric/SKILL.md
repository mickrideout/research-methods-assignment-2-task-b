---
name: enhance-rubric
description: Builds an enhanced marking rubric and a requirements checklist for the assignment. It keeps each official criterion verbatim and adds weights, observable differences between performance levels, marker evidence, pitfalls and question mapping, all cited to the spec, learning outcomes, lectures, readings, staff clarifications, exemplars and prior feedback. Writes Markdown for reading and YAML for the grading skills. Use after define-details, or when new clarifications, exemplars or feedback arrive.
---

# enhance-rubric

## Purpose

Turn a terse official rubric into a precise, sourced marking guide that the answer and
grading skills can aim at and mark against. Extract every explicit requirement in the
spec into a checklist.

## When to use

- After `define-details`, once its blocking open questions are answered.
- Re-run when a new clarification, exemplar or feedback file is added. When `<rubric_yaml>` and `<checklist_yaml>` already exist, the skill runs incrementally (comparing `sources_sha256` against `<extracted>/index.json` and patching only affected items; see Procedure step 10). Review the change with `git diff`.

Do not use it to grade or answer, or to change the official wording or weights.

## Inputs

Path placeholders such as `<rubric_yaml>` mean `paths.rubric_yaml` in the details file.

1. `context/assignment.md` (always first): question IDs, total marks, levels and paths.
2. Extracted text (`<extracted>/`) of all of these:
   - `<inputs>/rubric/`: authority 1
   - `<inputs>/spec/`: authority 2
   - `<inputs>/clarifications/`: authority 3
   - `<inputs>/outcomes/`, `<inputs>/lectures/`, `<inputs>/readings/`: authority 4
   - `<inputs>/exemplars/`, `<inputs>/feedback/`: authority 5
3. Guide: [references/rubric-writing-guide.md](references/rubric-writing-guide.md).
4. Formats: `templates/rubric.yaml`, `templates/rubric.md`, `templates/checklist.yaml`, `templates/checklist.md`.

## Procedure

1. Read `context/assignment.md`. If it has unresolved `blocking: true` open questions about marks or criteria, list them and ask whether to continue.
2. Refresh the extracted text: `python3 <tools>/extract_inputs.py`.
3. Copy each official criterion's name, wording and level descriptors verbatim into `original_wording` and `levels[].original`, with `original_source` (file#p.N). Use the rubric's own level names in `levels`.
4. Set each criterion's `weight` from the rubric, in marks or percent (`weight_unit`). Set each level's `marks: [min, max]`. If the rubric gives only band percentages, convert them using `grade_bands` and show the arithmetic in rubric.md.
5. Map criteria to questions (`applies_to`). Use `[ALL]` with `cross_cutting: true` for criteria such as structure, referencing and presentation. Every question must be covered.
6. Enrich each level with `observable` descriptors: concrete, checkable features of the work, worded the same way across levels, each with `sources`. Then add `evidence` (what a marker looks for) and `pitfalls`, each with a source. Follow the guide's source-mining order and descriptor rules.
7. Where sources conflict, the higher authority wins. Record every conflict in `conflicts` with a `resolution`.
8. Build the checklist. Include every sentence in the spec or clarifications that uses must, should, required, need to, ensure, include or do not. Each item gets `verbatim`, a checkable `text`, a `strength` (must or should), `applies_to`, `source`, and a `check` type.
9. Record `sources_sha256` from `<extracted>/index.json` for every file consulted, and `generated`.
10. On a re-run (when `<rubric_yaml>` and `<checklist_yaml>` already exist), diff `sources_sha256` against `<extracted>/index.json` to find new or modified sources. Preserve existing criterion IDs, weights, mark ranges, and unchanged descriptors or checklist items; patch only the criteria, `conflicts`, `sources_sha256`, and checklist items affected by the changed sources. Write `<rubric_yaml>` and `<checklist_yaml>`, then render `<rubric_md>` and `<checklist_md>` from them using the Markdown templates, and summarise the incremental changes for the user.
11. Validate: `python3 <tools>/check_rubric.py`. Fix every ERROR. For each "not found verbatim" WARN, re-check the source; PDF line-wrapping is usually the cause.
12. Log the run: `python3 <tools>/log_ai_use.py --skill enhance-rubric --action "Built enhanced rubric and checklist" --files <rubric_yaml>,<checklist_yaml>`.

## Output

- `<rubric_yaml>` and `<rubric_md>`: schema in `templates/rubric.yaml`; the readable version follows `templates/rubric.md`.
- `<checklist_yaml>` and `<checklist_md>`: schema in `templates/checklist.yaml`.
- Final message:
  - criteria count and weights
  - checklist counts (must and should)
  - conflicts found
  - inferred additions with only weak sources (exemplars or feedback alone)
  - next step: "Run check-environment (if code is required) or plan-question <QID>."

## Quality checks

- `check_rubric.py` exits 0.
- No addition lacks a source. No original wording is paraphrased.
- Adjacent levels differ in something a marker can point at, not just an adverb.
- Every question ID appears in at least one criterion, and in at least one checklist item where the spec has requirements for it.
- Existing grading reports are now stale if the rubric changed. Say so.

## If inputs are missing

- No official rubric: build the criteria from the spec's stated marking guidance only. Flag every criterion as `original_wording: null` in rubric.md and tell the user that grading confidence will be low. Ask whether to proceed.
- No exemplars, feedback or lectures: proceed with fewer sources and say which source types were absent.
- A source cannot be extracted: list it and continue; never cite what was not read.
