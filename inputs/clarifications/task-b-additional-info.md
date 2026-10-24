## Task B

### Relevant Unit Content & Structure
- **Unit Coverage:** Based on **Week 9 — Inferential Statistics** and experimental/quantitative study design (*Welcome to Week 9 - 2026-09-28*; *Research Hypotheses - 2026-10-02*).
- **Headings:** Use the prescribed headings `0` to `7` (plus an optional `References` heading at the end) (*Assignment2 - 2026-10-02*).

### Permitted Statistical Tests
Clarified in *A2 Task B — clarification on permitted t-test variant - 2026-10-17* and *📢 Assignment 2 Specs Are Out - Comment 9 - 2026-09-22*:
- **Choice of Statistical Test:** You are **not restricted** strictly to the exact test variants shown on lecture slides (e.g., pooled-variance Student's t-test).
- **Variants Allowed (e.g., Welch's t-test):** You may use **any appropriate statistical test** (including a two-sided **Welch's independent-samples t-test** when equal population variances cannot be assumed), **provided that**:
  - It is appropriate to answer your research question and test (prove/disprove) your hypothesis.
  - You **justify your choice and its assumptions** in relation to your proposed hypothesis and variables.

### Formulating Research Hypotheses (Teaching Team Guide)
Detailed guidance provided in *Research Hypotheses - 2026-10-02*:
1. **Core Structure:** A hypothesis is a testable prediction structured around: **WHO + WHAT + COMPARED WITH WHAT + WHAT OUTCOME?**
2. **Use the PICO Framework to Define the Comparison:**
   - **P (Population):** Who are you studying? *(e.g., IT postgraduates)*
   - **I (Intervention):** What technology, feature, or condition are you evaluating? *(e.g., FLoRA with GPT support)*
   - **C (Comparison):** What are you comparing it against? *(e.g., FLoRA without GPT support)*
   - **O (Outcome):** What observable/measurable variable will you measure? *(e.g., task accuracy)*
3. **Directional vs. Non-Directional Hypotheses:**
   - **Directional Hypothesis:** Use when previous research or theory gives a reason to expect a specific direction (use words like *higher, lower, increase, decrease, faster, slower, greater, fewer*).
     - *Example:* "IT postgraduates using FLoRA with GPT support will achieve **higher** task accuracy than those using FLoRA without GPT support."
   - **Non-Directional Hypothesis:** Use when you expect a difference but do not have strong prior evidence/theory to predict the direction (use phrases like *"will differ from"* or *"is different to"*).
     - *Example:* "IT postgraduates using FLoRA with GPT support **will have different** task accuracy from those using FLoRA without GPT support."
4. **Avoid the "Significantly Different" Trap:**
   - **Do NOT write** `"statistically significant"` or `"significantly higher"` in your hypothesis statement.
   - `"Higher"` / `"different"` is your **research prediction** (hypothesis); `"statistically significant"` is a **statistical conclusion** reached only *after* collecting data and running a statistical test against the null hypothesis ($H_0$).
5. **Role of the Null Hypothesis ($H_0$):**
   - $H_0$ states there is **no difference or no association** between the variables being tested.
   - Sequence: `Hypothesis → Collect data → Statistical test (evaluates evidence against H₀) → Interpret result`.
6. **Controlling / Accounting for Other Variables:**
   - Real-world studies have potential confounding factors (e.g., prior domain knowledge, digital literacy, tool familiarity, cognitive fatigue, task difficulty, prior experience).
   - Recognise important extraneous variables in your study design and consider how they will be controlled, measured, or scoped (e.g., *"For IT postgraduates with comparable baseline domain knowledge..."*).

---
## 1.5 Referencing and word-count rules (A2)

Staff ruling for Tasks A and B (asked about the 0 to 5 headings for Task A and the 0 to 7 headings for Task B):

| Question | Staff answer |
|---|---|
| Are references required in Task A and Task B? | **No.** References are not required. |
| Can a "References" heading be added to the given headings? | **Yes.** |
| Do in-text citations count toward each section's word limit? | **Yes.** |
| Does the reference list count toward a word limit? | **No.** |
| Is APA 7th the correct style? | **Yes**, APA 7th is fine. |

## 1.6 General takeaways from Assignment 1 feedback that apply to Assignment 2

Staff posted the grade distribution and overall feedback on 2026-10-07. The A1 task content differs from A2, but the points below are transferable.

- **Justify, do not just describe.** Staff said they "observed a lot of students focusing on describing what they had done without adequately explaining why", and said "several students focused on describing what was done rather than justifying design decisions". (A1 results have been released - Comment 2 - 2026-10-07). This matches the A2 rule that every chart and every metric must be justified in the narrative. (Assignment 2 Task A: Can I use 4 metrics instead of 2? ... - Answer 1 - 2026-10-02)
- **Be specific, not generic.** Task A reasoning was marked down when "too generic or unconvincing", when issues were not connected to recognised frameworks, or when issues overlapped or were misplaced. (A1 results have been released - Comment 2 - 2026-10-07)
- **Wording and structure of response options:** In A1 Task B, common faults were uneven coverage of required constructs, constructs not properly measured, problematic question wording, and overlapping or incomplete response options. (A1 results have been released - Comment 2 - 2026-10-07)
- **Appearance does not earn marks.** A1 staff said layout and aesthetics are not graded. Quality of the answers is. (FIT5125 Part A - Answer 1 - 2026-09-11)
- **Grade distribution of A1 (/40):** 32–40: 43.3%; 28–<32: 32.2%; 24–<28: 13.2%; 20–<24: 7.4%; 0–<20: 3.9%. Staff described a "high grade skew". (A1 results have been released - Comment 2 - 2026-10-07)
- **Marking quality:** Staff said the teaching team "used the same rubric that was shared with students" and ran a consistency marking process. (Assignment 1 -- Grading - Comment 2 - 2026-10-06)
# 3. TASK B — Inferential Statistics

Headings: **0 to 7**. A "References" heading is allowed. Referencing rules are in §1.5. (Assignment2 - 2026-10-02)
Week 9 taught inferential statistics. (Welcome to Week 9 - 2026-09-28)

## 3.1 Permitted statistical tests

- **Staff position (final):** "You may use any appropriate statistical test, provided you justify your choice in relation to your proposed hypothesis and variables." (A2 Task B — clarification on permitted t-test variant - Answer 1 - 2026-10-17)
- **Welch's t-test:** The student proposed a two-sided Welch's independent-samples t-test for two independent groups, with justification that it does not assume equal variances. They asked whether it counted as a test taught in FIT5125, or whether the pooled-variance Student's t-test was required. The answer above permits it; staff did not require the pooled-variance test. (A2 Task B — clarification on permitted t-test variant - 2026-10-17)
- **Earlier statement (2026-09-22), same conclusion.** The question was whether "an independent-samples t-test (with Welch's t-test if equal variances are not reasonable)" counts as a test covered in the unit. Staff: "We only need you to identify statistical tests that you think will help answer your research question and prove/disprove your hypothesis." (📢 Assignment 2 Specs Are Out - Comment 9 - 2026-09-22)
- **Test choice must be justified** in relation to the hypothesis and variables, including its assumptions. (A2 Task B — clarification on permitted t-test variant - Answer 1 - 2026-10-17)

## 3.2 Hypothesis formulation guidelines (teaching team, Research Hypotheses post)

The post uses the studio FLoRA activity as an A/B test and sets out how to form a hypothesis. (Research Hypotheses - 2026-10-02)

1. **Start from the research question.** A hypothesis is a testable prediction. Think "WHO + WHAT + COMPARED WITH WHAT + WHAT OUTCOME?"
2. **Use PICO to organise your thinking:**

   | PICO | Ask yourself | Example |
   |---|---|---|
   | P – Population | Who are you studying? | IT postgraduates |
   | I – Intervention | What are you introducing or evaluating? | FLoRA with GPT support |
   | C – Comparison | What are you comparing it with? | FLoRA without GPT support |
   | O – Outcome | What will you measure? | Task accuracy |

   PICO in one sentence: "IT postgraduates using FLoRA with GPT support, compared with FLoRA without GPT support, will have different task accuracy."
3. **Turn PICO into a hypothesis:**
   - *Directional:* use when previous research or theory gives a reason to expect a direction. Useful words: higher, lower, increase, decrease, faster, slower, greater, fewer. Example: "IT postgraduates using FLoRA with GPT support will achieve higher task accuracy than those using FLoRA without GPT support."
   - *Non-directional:* use when you expect a difference but have no strong basis for a direction. Useful phrase: "will differ from". Example: "...will have different task accuracy from those using FLoRA without GPT support."
4. **The "significantly different" trap.**
   - Do **not** write "FLoRA with GPT support will produce **significantly higher** task accuracy".
   - Write "...will produce **higher** task accuracy" (directional, with evidence from previous research), or a non-directional version.
   - "Higher" is your prediction. "Statistically significant" is a conclusion from the statistical analysis.
5. **Null hypothesis (H₀):** it generally states no difference or no association. Example: "There is no difference in task accuracy between students using FLoRA with GPT support and students using FLoRA without GPT support." The test is run **after data collection** to evaluate evidence against H₀. Sequence: hypothesis → collect data → statistical test → interpret the result.
6. **Consider other factors that could affect the outcome** (prior domain knowledge, digital literacy, familiarity with FLoRA, familiarity with GPT-supported tools, cognitive fatigue, task difficulty, previous experience with similar tasks). You need not put every factor in the hypothesis, but recognise important variables and consider how to control, measure or account for them. A scoped example: "For IT postgraduates with comparable baseline domain knowledge, FLoRA with GPT support will result in higher task accuracy than FLoRA without GPT support."
7. **Quick check before submitting a hypothesis:**
   - P: have I identified the population?
   - I: what intervention, technology, feature or condition am I evaluating?
   - C: is the comparison clear?
   - O: is the outcome observable or measurable?
   - Direction: if I say higher, lower, increase or decrease, do I have a reason?
   - Significance: have I avoided putting "statistically significant" in the prediction?
   - Testable: could I collect data and test this?
8. **Final distinction:** PICO = what exactly am I studying. Hypothesis = what do I expect. Data collection = what happened. Statistical test = what the evidence says. Conclusion = what can I reasonably conclude.

## 3.3 Student design example (for context only)

A student proposed a randomised study comparing a numeric outcome between two independent groups, and referred to the Week 9 studio slides mentioning a t-test. This shows the kind of design staff had no objection to. (A2 Task B — clarification on permitted t-test variant - 2026-10-17)

## 3.4 Summary of Task B points

| Item | Rule | Source |
|---|---|---|
| Headings | 0 to 7 | (Assignment2 - 2026-10-02) |
| Tests | Any appropriate test, justified against hypothesis and variables (Welch's t-test acceptable) | (A2 Task B — clarification on permitted t-test variant - Answer 1 - 2026-10-17) |
| Hypothesis | Use PICO; directional only if supported; do not write "significantly" in the hypothesis; state H₀ | (Research Hypotheses - 2026-10-02) |
| Referencing | Not required; in-text citations count toward word limits; reference list does not; APA 7th | (Assignment2 - Answer 1 - 2026-10-02) |
| Word limits | The forum has no Task B word limit. Use the corrected spec (see §1.3). | (📢 Assignment 2 Specs Are Out - Comment 12 - 2026-09-26) |

---
