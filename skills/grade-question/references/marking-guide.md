# Marking guide: strict, calibrated marking

Used by grade-question and grade-assignment.

## Stance

You are an experienced marker for a postgraduate unit, marking blind against the rubric.
You are neither the author's coach nor their critic: you award what the page earns.
When in doubt between two levels, award the lower one and say what would secure the higher.

## Evaluate substance and style separately

Follow Implementation Rule 3 and the shared Academic Writing Style Guidelines (`skills/answer-question/references/writing-guide.md`):

1. **Rubric-compliance (substance) check:** Establish whether the answer is factually accurate, complete, grounded in verifiable evidence, and responsive to the command words and marking criteria.
2. **Academic style and natural expression check:** Establish whether the prose is clear, direct, concise, and written in an authentic postgraduate voice rather than generic, formulaic language-model output.
3. **No cross-compensation:** Neither check compensates for failure in the other. Fluent, natural prose does not earn marks for missing analysis or evidence; equally, an answer that touches rubric points through repetitive AI filler, broad claims with generic elaboration, or bloated phrasing must be flagged for editorial tightening and specific analysis.

## Procedure per criterion

1. Re-read the criterion's `original_wording` and every level's `observable` list.
2. Collect the evidence: verbatim quotes from the answer that bear on this criterion.
3. Start at the lowest level and climb. A level is met when **most** of its observable
   descriptors are evidenced and **none** of its "must" features are missing.
4. Place the mark within the level's range:
   - bottom third: just meets the level
   - middle: meets it securely
   - top third: meets it and shows some features of the next level
5. Write the next-level gap as specific, observable additions, not "be more critical".

## Calibration traps

| Trap | Correction |
|---|---|
| Length or polish read as quality | Fluent prose without evaluation is a description-level answer |
| AI-stylistic / formulaic filler | Habitual filler ("It is important to note that…", "This underscores the significance of…", "At its core…"), repetitive "This suggests/indicates/highlights" openings, or broad assertions ("provides valuable insights") do not count as specific analysis |
| Sources counted, not used | Ten citations summarised one after another is not synthesis |
| Rewarding intent | Mark only what is on the page, not what the plan or notes say |
| Halo effect | Mark each criterion independently; a strong criterion does not lift a weak one |
| Generosity with own work | Assume a sceptical second marker will moderate your marks |
| Inflation at the top | HD requires the HD descriptors (concrete mechanisms, explicit evaluation criteria, justified trade-offs and limitations), not just the absence of errors |
| Unverifiable claims | Numbers without a source or result file count against accuracy criteria |

## Evidence quoting

- Quote exact sentences (≤ 40 words each) with their position (paragraph number or heading).
- For absence, write: "No evidence found: searched for <what> in <section>."

## Style and natural expression review

Alongside criterion marking, assess the answer against `skills/answer-question/references/writing-guide.md` (§3–15):

- **Directness and concision:** Flag throat-clearing introductions, restatements of the question, or unnecessary summary paragraphs.
- **Specificity over generic claims:** Flag broad claims ("has many advantages and disadvantages") that should be replaced with concrete mechanisms, named variables/stakeholders, or explicit evaluation criteria.
- **Formulaic phrasing and rhythm:** Flag habitual AI filler phrases, repetitive sentence openings, or rigid mechanical paragraph templates.
- **Calibrated uncertainty:** Flag overclaiming ("clearly", "obviously", "proves") or vague disclaimers that should be replaced with specific methodological or data qualifications.

## Fixes

Every fix states where, what, and the expected effect (covering both substantive gaps and style/concision improvements):
- Substantive fix: "§2, paragraph 3: add a limitation of the CRISP-DM framing (cite [@lee2020, p. 7]) and weigh it against the alternative; ~60 words; targets C1 D→HD."
- Style/concision fix: "§1, opening sentence: cut the generic topic announcement ('In today's rapidly evolving landscape…') and state the main design trade-off directly; saves ~25 words for C2 analysis."

## Marks recoverable and effort

- Marks recoverable ≈ (midpoint of the next level − current mark) × the probability the fix achieves it.
- Effort: S (under 30 min, local edit), M (a new paragraph or re-analysis), L (new research or experiment runs).
- Ratio = recoverable / effort weight (S=1, M=2, L=4). Sort descending.

## Confidence

- **high:** the descriptors are concrete and the evidence is clear-cut.
- **medium:** one or two criteria sit on a boundary.
- **low:** the rubric is vague, levels are missing, or interpretation is ambiguous. Say which criteria.
