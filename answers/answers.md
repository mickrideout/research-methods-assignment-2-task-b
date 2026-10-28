<!--
COMMON ANSWER FILE. Do not edit sections by hand while an agent is working; write
sections only with:  python3 tools/answer_section.py put <ID> --from <draft.md>
Rules: each section sits between its own BEGIN/END markers on their own lines;
the meta line is written by the script; cite with [@key] (keys in the .bib file);
cite figures/tables from work/results/ by relative path, e.g.
![Caption](../work/results/figures/q2-fig1.png){#fig:q2-1}
The sample sections below are replaced by `answer_section.py init`, which
generates one section per question in context/assignment.md.
-->

<!-- BEGIN TB -->
## 0. Name & Student ID
<!-- meta: words=527/550 | criteria=C1,C2,C3,C4,C5 | updated=2026-10-28 | status=revised -->

Michael Rideout - 36809268

## 1. Proposed Hypothesis

Among Australians aged 18–30 who do not own a home, those who view a simulated social media feed of pessimistically framed housing posts will report a lower perceived likelihood of owning a home within ten years than those who view the same housing facts in neutral framing.

## 2. Null Hypothesis

Among Australians aged 18–30 who do not own a home, perceived likelihood of owning a home within ten years will not differ between those who view a simulated social media feed of pessimistically framed housing posts and those who view the same housing facts in neutral framing.

## 3. Independent, Dependent and Confounding Variables

- **Independent:** post framing (pessimistic or neutral), randomly assigned.
- **Dependent:** perceived likelihood (0–100%) of owning a home within ten years.
- **Confounding:** household income and savings, living arrangement (renting or with parents), capital city versus regional location, prior weekly exposure to housing posts. All are measured before exposure, randomisation balances them.

## 4. Data Collection

An online experiment will recruit 128 valid completers (64 per group). Online survey sampling is cheap and reaches young non-homeowners online. Instagram and TikTok advertisements, university notices and community groups link to a online survey platform screening age, residence and home ownership. Participants answer confounder questions, are randomly allocated, view eight mock posts with identical housing statistics across conditions, and rate ownership likelihood, tone and an attention item before a debrief. Costs (AUD): incentives $640 ($5 each), advertising $250, piloting and contingency $110. Hours: pilot 25, setup 15, recruitment 25, analysis 15 and reporting 20.

## 5. Statistical Tests

Welch's t-test will compare mean ownership likelihood between the groups. It suits this between-subjects design: two independent groups and a continuous 0–100 outcome. Unlike Student's t-test, it does not assume equal variances, which matters if pessimistic framing polarises people and widens one group's spread.

Each person responds once, the steps on the 0–100 scale must be treated as equal, and scores in each group should be approximately normal. If pre-specified Q–Q checks show floor or ceiling clustering, a Mann–Whitney U test will replace it.

Focusing on emotional barriers should make the same facts feel more daunting, lowering scores. Still, the test is two-sided (α = .05) so an unexpected boost is not missed. H0 is rejected if p < .05, and the hypothesis is only supported if the pessimistic group scores lower on average. Assuming a medium effect (d = 0.5), 64 per group gives 80% power.

## 6. Limitations

A brief, researcher made feed lacks the personalisation and repeated exposure of real platforms, so any effect may not transfer to everyday use. A multi day field study with a browser extension feed could test this. Self selected online volunteers probably over represent digitally engaged young people, which limits generalisation to all non-homeowners aged 18–30. Recruiting offline at TAFE campuses and workplaces may reach less digitally engaged people. A single, immediate survey question can skew results by capturing temporary feelings. A delayed, multi question follow up is needed to measure lasting impact.

## 7. Alternative Narrative

You could easily rig a study to 'prove' that housing pessimism comes from personal finances rather than social media. Just survey low-income city renters whose hopes are already near zero, wait a week so the media impact fades, and drop anyone affected by negative news. Everyone scores rock bottom, hiding the effect.
<!-- END TB -->
