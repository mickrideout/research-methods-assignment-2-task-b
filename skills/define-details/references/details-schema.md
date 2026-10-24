# Details file: field guide

The frontmatter of `context/assignment.md` is parsed by `tools/details.py` and the other
scripts. Keep field names exactly as in `templates/assignment.md`.

## Value conventions

| Situation | Value | Also required |
|---|---|---|
| Stated in a source | the value | `sources: [{field, source: inputs/<path>#p.N}]` |
| Not stated / ambiguous / conflicting | `null` | open question with `field: <dotted.path>` |
| Clearly not applicable | `"n/a"`, `false` or `[]` | nothing |

For question-level fields, the open question's `field` is `questions.<QID>.<field>`,
e.g. `questions.Q2.word_limit`.

## Where facts usually hide

| Field | Look in | Watch for |
|---|---|---|
| `assignment.due` | spec cover page, LMS text, clarifications | time zone (AEST +10:00 vs AEDT +11:00); extensions announced later |
| `assignment.weighting_pct` vs `total_marks` | spec header vs rubric total | "worth 40%" but "marked out of 100" are both facts; record both |
| `questions[].id` | spec numbering | keep the spec's own IDs (Q1, Q2a, Task 3 → `T3`); IDs never change once answers exist |
| `questions[].marks` | rubric or spec | marks given only per criterion, not per question → null + open question |
| `questions[].word_limit` | spec | "approximately 1000 words" → limit 1000 plus open question about tolerance |
| `questions[].type` | task wording | `code` if the deliverable is mostly code/results; `mixed` if a written discussion of results |
| `word_count.exclude` | spec, unit guide, FAQ | default assumption (headings, references, code, tables, captions excluded) must be confirmed; in-text citations are the usual ambiguity |
| `word_count.tolerance_pct` | spec, unit policy | "±10%" is common but must be stated |
| `referencing.style` | spec, unit guide | "Harvard" has variants (AGPS, Cite Them Right); ask which, and get the CSL file |
| `format.*` | spec "presentation" section | cover page contents, font, spacing, page limits |
| `submission.filename_pattern` | spec/LMS | placeholders: `{unit_code} {assignment_number} {assignment_title} {student_id} {student_name}` |
| `code.*` | spec "technical requirements", starter README, notebook headers | versions pinned in starter code, `requirements.txt`, GPU mentions |
| `genai.*` | spec "academic integrity" / "use of AI" section, unit outline | quote verbatim; note whether an acknowledgement or prompt log is required |
| `grade_bands` | unit outline | keep the template HD/D/C/P/N defaults unless the unit states otherwise |

## Open-question quality

A good open question is specific, cites where the ambiguity is, and says what changes
depending on the answer:

```yaml
- id: OQ3
  question: "Spec p.2 says 'about 1500 words'. Is there a tolerance, and are in-text citations counted?"
  field: word_count.tolerance_pct
  affects: [Q1, Q2]
  blocking: false
  source: inputs/spec/brief.pdf#p.2
  answer: null
```

Mark `blocking: true` only when drafting would differ materially depending on the answer
(for example, which case study to analyse). The user fills in `answer`. If the answer
came from staff, the user should also save the post to `inputs/clarifications/`.

## Body regeneration

Regenerate everything except `## My notes`. The body is a summary; if it ever disagrees with the
frontmatter, the frontmatter wins.
