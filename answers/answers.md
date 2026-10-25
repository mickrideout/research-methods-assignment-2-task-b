---
title: "FIT5125 : Task B: Working with Hypotheses"
author: "Michael Rideout (36809268)"
lang: en-AU
---

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
## 0. Your Name & Student ID
<!-- meta: words=538/550 | criteria=C1,C2,C3,C4,C5 | updated=2026-10-25 | status=revised -->

**Name:** Michael Rideout  
**Student ID:** 36809268

## 1. Proposed Hypothesis (< 50 words)

Among Australians aged 18–30 who do not own a home, those who view a simulated social media feed of pessimistically framed housing posts will report a lower perceived likelihood of owning a home within ten years than those who view the same housing facts in neutral framing.

## 2. Null Hypothesis (<50 words)

Among Australians aged 18–30 who do not own a home, perceived likelihood of owning a home within ten years will not differ between those who view a simulated social media feed of pessimistically framed housing posts and those who view the same housing facts in neutral framing.

## 3. Independent, Dependent and Confounding Variables (< 50 words)

- **Independent:** post framing (pessimistic or neutral), randomly assigned.
- **Dependent:** perceived likelihood (0–100%) of owning a home within ten years.
- **Confounding:** household income and savings; living arrangement (renting or with parents); capital-city versus regional location; prior weekly exposure to housing posts. All are measured before exposure; randomisation balances them.

## 4. Data Collection (< 100 words)

An online between-subjects experiment will recruit 128 valid completers (64 per group). Voluntary-response convenience sampling is cheap and reaches young non-homeowners online. Instagram and TikTok advertisements, university notices and community groups link to a Qualtrics survey screening age, residence and home ownership. Participants answer confounder questions, are randomly allocated, view eight mock posts with identical housing statistics across conditions, and rate ownership likelihood, tone (manipulation check) and an attention item before a debrief. Costs (AUD): incentives 640 (5 each), advertising 250, piloting and contingency 110. Hours: stimuli/pilot 25, ethics/setup 15, recruitment 25, analysis 15, reporting 20.

## 5. Statistical Tests (< 150 words)

Welch's independent-samples t-test will compare mean ownership likelihood between groups. It suits a between-subjects design with two independent groups and a continuous 0–100 outcome. Unlike Student's t-test, it does not assume equal variances, which pessimistic framing may widen by polarising responses. The test assumes independent observations (one response per person, random allocation), interval-level measurement and approximately normal scores within each group; if Q–Q plots show floor or ceiling clustering, a Mann–Whitney U test, which compares rank distributions, will replace it. The hypothesis is directional because emotive, barrier-focused framing should make identical facts seem less surmountable, but the test is two-sided (α = .05) so an opposite effect is not missed. H0 is rejected if p < .05; H1 is supported only if the pessimistic mean is lower. The mean difference, 95% CI and Cohen's d will be reported. Assuming a medium effect (d = 0.5), 64 per group gives 80% power.

## 6. Limitations (< 200 words)

A brief, researcher-made feed lacks the personalisation and repeated exposure of real platforms, so any effect may not transfer to everyday use; a multi-day field study with a browser-extension feed could test this. Self-selected online volunteers probably over-represent digitally engaged young people, which limits generalisation to all non-homeowners aged 18–30; recruiting offline at TAFE campuses and workplaces would reach less digitally engaged peers. An immediate single-item rating may capture passing mood rather than a stable perception and invite demand effects that overstate lasting change; a delayed follow-up with a multi-item measure would show whether the effect persists.

## 7. Alternative Narrative (< 50 words)

"Housing pessimism reflects finances, not feeds" could be manufactured by recruiting only low-income capital-city renters, whose near-floor ratings leave framing no room; measuring likelihood a week later, so effects fade; and excluding pessimistic-condition participants who passed the manipulation check. Equal near-floor group means would then 'show' framing is irrelevant.
<!-- END TB -->
