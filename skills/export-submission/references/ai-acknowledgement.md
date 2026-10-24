# Writing the generative-AI acknowledgement

The unit's wording wins. If `genai.acknowledgement_format` quotes a required template,
fill in that template exactly. Otherwise, use the default structure below.

## Default structure (when the unit gives no template)

1. **Tools:** name and version or model, and the interface used
   (e.g. "an AI coding agent using <model>, via a command-line tool").
2. **Uses:** what the AI did, grouped by the stages in the log (planning, research
   support, drafting, code, grading feedback, editing). Say which questions are affected.
3. **Human contribution:** what the student did: decisions, verification, rewriting.
   Take this from the log's "Your review" column. Never invent it; leave a
   placeholder that the user must complete if the column is empty.
4. **Verification:** how outputs were checked: sources read, results reproduced,
   references verified.
5. **Compliance statement:** "This use is consistent with the unit's policy on generative AI
   ([cite the spec page])."

## Rules

- Derive everything from `work/ai-use-log.md`. Never understate the use.
- Keep it factual and concise (usually 100–250 words). It is normally excluded from the
  word count. Confirm this with `word_count.exclude` or an open question.
- If the unit requires prompt logs or chat transcripts as an appendix, tell the user. Those
  come from the agent's own history, not from this template.
- The user must confirm the text before export proceeds.
