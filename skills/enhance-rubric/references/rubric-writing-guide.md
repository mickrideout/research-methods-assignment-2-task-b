# Rubric enhancement guide

## Source authority (highest first)

1. Official rubric (`inputs/rubric/`): wording, weights and levels are never changed.
2. Assignment spec (`inputs/spec/`).
3. Staff clarifications (`inputs/clarifications/`): later posts override earlier ones.
4. Learning outcomes, lectures and readings (`inputs/outcomes/`, `inputs/lectures/`, `inputs/readings/`).
5. Exemplars and prior feedback (`inputs/exemplars/`, `inputs/feedback/`).

A lower source may add detail but never contradict a higher one. If it does, record a
conflict: `{description, sources, resolution: "official rubric wins: <what applies>"}`.

## Where to mine each kind of addition

| Addition | Best sources | Example |
|---|---|---|
| Observable level differences | rubric level text, spec task verbs, ULO verbs (analyse, evaluate, justify) | "HD: evaluates at least two alternatives against stated criteria; D: compares alternatives without explicit criteria" |
| Evidence a marker looks for | spec deliverables, lecture "what I expect" slides, exemplar features | "Explicit link from each recommendation to a cited finding" |
| Pitfalls | prior feedback, FAQ posts, lecture warnings | "Describing the framework instead of applying it (feedback A1 p.1)" |
| Question mapping | spec structure, rubric headings | criterion "Implementation" → Q2 only |

## Descriptor rules

1. **Observable, not adverbial.** Name what is present, absent or different. Avoid adverb
   ladders such as "very thorough" vs "thorough" vs "somewhat thorough".
2. **About the work, not the student.** "Argument lacks counter-evidence", not "student
   does not understand".
3. **Parallel structure.** Each level addresses the same aspects in the same order, so the
   difference between adjacent levels is findable in seconds.
4. **The top level is achievable.** It describes strong real work, not perfection.
5. **Spell out the boundaries.** The HD/D and P/N boundaries cause most marking drift.
   Give them the most concrete descriptors.
6. **Master's level.** Top bands normally require synthesis across sources, critical
   evaluation (limitations, assumptions, alternatives), justified positions and
   professional or research-grade presentation. State only what the sources support.
   If you infer this from general Master's expectations or a ULO verb, cite the ULO.
7. **Split double-barrelled criteria** in the *observable* list (for example clarity vs
   accuracy). Keep the original criterion and weight intact.

## Source citation format

`inputs/<sub>/<file>#p.N` for PDFs, `#slide.N` for slides, `#para.N` or `#table.N` for docx, `#line.N` for
text, `#cell.N` for notebooks. Paths are relative to the project root and must exist.
Cite the original input file, not the extracted copy.

## Checklist extraction

- Trigger words: must, should, required, need to, needs to, ensure, include, do not,
  must not, at least, no more than, maximum, minimum.
- One requirement per item. Split compound sentences.
- `text` is a checkable restatement; `verbatim` is the exact sentence.
- `strength: must` for must, required, need to, do not and limits. `should` for should and recommended.
- `check`: `wordcount` (limits), `compliance` (format, referencing, sections), `export`
  (file type, naming), otherwise `manual`.

## Mark ranges

When the rubric gives per-level marks, use them. When it gives only a criterion weight and
named levels, derive the ranges from `grade_bands`, e.g. weight 20 with HD ≥85%: HD [17, 20],
D [15, 16.9], C [13, 14.9], P [10, 12.9], N [0, 9.9]. Show the derivation in rubric.md.
