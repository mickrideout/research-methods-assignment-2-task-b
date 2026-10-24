<!-- extracted from inputs/lectures/week-9-summary.md sha256=cad7adf90075b506e13064ff70f74af54ad96a5115d1a7a97d3e0594d4fbc35c on 2026-10-25T10:52:12+11:00 via text -->


## [line 1]

# Week 9 – Introduction to Inferential Statistics: Summary

**Unit:** FIT5125 / FIT4005 – IT Research and Innovation Methods (Monash FIT, Semester 2 2026)

**Sources covered**

| Source | File |
|---|---|
| Lecture notes (Introduction to Inferential Statistics) | `lecture/lecture-summary.md` |
| Reading transcript (9.1 Introduction to Inferential Stats) | `readings/introduction-to-inferential-stats.md` |
| Studio ("tutorial") activity sheet and notes | `studio/Week 9 S2 2026 - Studio Activity Sheet.pdf`, `studio/studio.md` |
| Supplementary study flashcards (covering test selection & design topics missing from the truncated lecture file) | `week-9-anki.md`, `anki.md` |

---

## 1. Main Theme

**Inferential statistics enables researchers to go beyond merely describing collected data (descriptive statistics) to draw rigorous, generalisable conclusions about a wider *population* from a smaller *sample*, and to quantify the probability that observed differences or relationships in a sample reflect genuine population effects rather than random chance.**

- **Important:** The validity of any statistical inference depends fundamentally on **how well the sample represents the target population**, whether the **hypothesis is testable**, whether **confounding variables and biases** (selection, reporting, visualisation, cherry-picking, p-hacking, HARKing) are controlled, and whether the **chosen statistical test** (parametric vs. non-parametric) matches the experimental design and data distribution.

---

## 2. Logical Sections

1. Descriptive vs. Inferential Statistics
2. Population, Sample, and Census
3. Sampling Methods: Probability vs. Non-Probability Sampling
4. Choosing and Reporting a Sampling Strategy
5. Hypothesis Testing: Testability, Null ($H_0$) and Alternative ($H_1$) Hypotheses, and Workflow
6. Experimental Design, Variables, and Statistical Tests (Parametric vs. Non-Parametric)
7. Research Biases, Ethical Pitfalls, and Studio Activities

---

## 3. Section Summaries

### 3.1 Descriptive vs. Inferential Statistics

#### Descriptive Statistics
- **Definition:** Methods that summarise, organise, and describe the patterns and trends within the dataset that has actually been collected, without generalising beyond it.
- **Numerical measures:** mean, median, mode, variance, and standard deviation.
- **Visual representations:** graphs, charts, and plots (e.g., pie charts, bar graphs, scatterplots).

#### Inferential Statistics
- **Definition:** Methods that use observations from a smaller **sample** to:
  1. Make informed conclusions, predictions, or generalisations about a larger **population**.
  2. **Quantify the likelihood** that observed differences between groups or relationships between variables in a sample occurred by **chance** versus reflecting true differences in the population.
- **Important:** Descriptive statistics asks *"What patterns exist in the data we collected?"*; inferential statistics asks *"Do these patterns generalise to the wider population, or could they have arisen by chance?"*


## [line 51]

#### Worked Example: Coles vs. Woolworths Shopper Survey
- **Scenario (lecture):** 100 shoppers are surveyed on supermarket preference; 60% prefer Coles and 40% prefer Woolworths.
  - *Descriptive analysis:* Reports that 60% of the 100 surveyed shoppers prefer Coles and 40% prefer Woolworths (e.g., via percentages or a bar chart).
  - *Inferential analysis:* Evaluates whether the responses from these 100 shoppers allow us to infer supermarket preferences across the wider population of shoppers (e.g., as illustrated in the reading, reasoning from a sample of 100 mall shoppers that roughly 70%–80% of all shoppers in the mall prefer one supermarket over the other).

---

### 3.2 Population, Sample, and Census

- **Population:** The entire group of individuals, items, or objects about which the researcher wants to draw conclusions.
  - *Examples:* all Monash students; all first-year Monash students; all users of a software application; all shoppers in Australia (or in a specific mall); all adult males in the world.
- **Sample:** The specific subset of the population from whom data is actually collected and analysed.
  - *Worked Example (Lecture):*
    ```text
    Population:          10,000 first-year Monash students
    Survey offered to:    1,000 students
    Responses received:      50 students
    ------------------------------------------------------
    Final sample size =      50 students
    ```
  - **Important:** The sample size is the number of participants from whom data is *actually obtained* ($n = 50$), not the number invited ($1,000$) or the population ($10,000$).
  - *Worked Example (Reading):* To estimate the average height of all adult males in the world (the population), a researcher selects adult males from various countries as a sample.
- **Why Sampling Is Necessary:** Collecting data from an entire population is rarely feasible because research operates under practical constraints:
  1. Time
  2. Money / budget
  3. Personnel
  4. Software / technical resources
  5. Access to participants
  6. General practical feasibility
- **Census:** An unusual data-collection approach that attempts to gather information from essentially the entire population rather than a sample.
- **Important (Representativeness):** For inferential statistics to be meaningful, the sample must be **reasonably representative of the population**. Poor representativeness invalidates generalisation regardless of the statistical test used.

---

### 3.3 Sampling Methods: Probability vs. Non-Probability Sampling

The reading divides sampling strategies into two overarching categories—**probability sampling** and **non-probability sampling**—spanning eight specific methods across the lecture and reading notes:

#### A. Probability Sampling
**Definition (Reading):** Sampling methods in which **every member of the population has a known, non-zero chance of being selected** using randomisation criteria.

| Method | Definition & Mechanism | Examples, Advantages & Pitfalls |
|---|---|---|
| **1. Simple Random Sampling** *(Random Sampling)* | Every member of the population has an independent and equal (or approximately equal) chance of selection. | **Advantages (Important):**<br>• Reduces systematic selection bias<br>• Increases sample representativeness<br>• Makes sampling error more predictable<br>• Satisfies independence/randomness assumptions required by parametric statistical tests<br>**Counter-example (Bias):** A lecturer seeking teaching feedback who surveys *only* High Distinction (HD) students introduces severe systematic selection bias. |
| **2. Systematic Sampling** | Participants are selected from an ordered list or flow according to a fixed, regular interval ($k$). | • Selecting every 3rd student entering a classroom.<br>• Selecting every 10th person from an enrolment list. |
| **3. Stratified Sampling** | The population is divided into meaningful, mutually exclusive subgroups (**strata**) based on shared characteristics, and participants are sampled from *each* stratum. | **Purpose (Important):** Ensures key subgroups are adequately represented in the sample.<br>**Examples of university strata:**<br>• Domestic vs. international students<br>• Full-time vs. part-time enrolment<br>• Year level (1st, 2nd, 3rd year)<br>• Different faculties |
| **4. Cluster Sampling** *(in reading only)* | The population is divided into subgroups (**clusters**), where each cluster is miniature-representative (has similar characteristics to the whole population), and entire clusters or individuals within selected clusters are sampled. | **Important distinction:** In *stratified* sampling, each stratum is internally homogeneous (e.g., grouped by year level) and all strata are sampled; in *cluster* sampling, each cluster should mirror the diversity of the whole population. |

#### B. Non-Probability Sampling
**Definition (Reading):** Sampling methods in which individuals are selected based on **non-random criteria**, meaning **not every member of the population has a chance of being included**.

## [line 101]


| Method | Definition & Mechanism | Examples & Limitations |
|---|---|---|
| **1. Convenience Sampling** | Participants are selected because they are the most readily accessible to the researcher. | **Example:** A Monash researcher studying university lecturers recruits only Monash lecturers.<br>**Important limitation:** Not inherently invalid, but has **limited generalisability** (Monash lecturers may differ from lecturers elsewhere). Researchers *must* explicitly acknowledge these limitations. |
| **2. Purposive Sampling** | The researcher uses their domain expertise to deliberately select participants who belong to a specific group directly relevant to the research question. | **Examples:**<br>• Fortune 500 CEOs<br>• High-performing students<br>• Users with a rare or specialised experience |
| **3. Snowball Sampling** | Existing study participants help recruit future participants from their social or professional networks (`Participant A → recruits friends → they join and recruit others`). | **Use case:** Particularly valuable when the target population is hidden, niche, or difficult to identify/access directly. |
| **4. Voluntary Response Sampling** *(in reading only)* | Participants self-select (**opt in**) to participate in response to an open invitation or survey. | Prone to self-selection bias (individuals with strong opinions are more likely to opt in). |

---

### 3.4 Choosing and Reporting a Sampling Strategy

- **Important:** There is no single universally "correct" sampling strategy. Choosing an appropriate sampling method depends on five factors:
  1. **The research question**
  2. **The target population**
  3. **Participant accessibility**
  4. **Available resources** (time, funding, personnel)
  5. **The statistical analysis to be performed** (e.g., whether random sampling assumptions must be met)
- **Important (Reporting Requirement):** In any academic or industry research report, researchers must clearly state:
  1. **Which** sampling strategy was used.
  2. **Why** it was selected given the research context and constraints.
  3. **How** the sampling choice may affect or limit the generalisability of the findings.

---

### 3.5 Hypothesis Testing: Testability, $H_0$ vs. $H_1$, and Workflow

#### What is a Hypothesis?
- **Definition:** An informed belief, assumption, or prediction about a phenomenon, grounded in prior observations, theory, or existing domain knowledge.
  - *Example:* *"Users make fewer errors when website buttons are larger."*
- **Goal of Hypothesis Testing:** To collect empirical data and apply statistical tests to evaluate whether an observed relationship or group difference is genuine in the population or could plausibly have occurred by random chance.

#### Testability Requirement
- **Important:** A useful scientific hypothesis **must be testable** (and falsifiable) using **observable or measurable empirical evidence**.
- *Counter-example (Untestable Claim):* *"A ball falls because invisible mischievous unicorns cause it to fall."* Because invisible unicorns cannot be observed or measured, this explanation cannot be empirically tested and is not a valid scientific hypothesis.

#### Null and Alternative Hypotheses
Hypothesis testing sets up two competing, mutually exclusive statements:

1. **Null Hypothesis ($H_0$):**
   - **Definition:** States that there is **no relationship, no effect, or no meaningful difference** between the variables or groups in the population (any observed sample difference is attributed to chance).
   - *Example:* *"There is no relationship between children's sugar consumption and hyperactivity."*
2. **Alternative Hypothesis ($H_1$ or $H_A$):**
   - **Definition:** Proposes that a **genuine relationship, effect, or difference exists** between the variables or groups in the population.
   - *Example:* *"There is a relationship between children's sugar consumption and hyperactivity."*

#### General Hypothesis-Testing Process (Workflow)
```text
1. Research question / initial belief (from theory or observation)
        ↓

## [line 151]

2. Formulate a testable research hypothesis
        ↓
3. Define the Null Hypothesis (H₀: no effect / no difference)
        ↓
4. Define the Alternative Hypothesis (H₁ / H_A: effect / difference exists)
        ↓
5. Collect sample data (using an appropriate sampling strategy & experimental design)
        ↓
6. Choose an appropriate statistical test (based on design, variables, and distribution)
        ↓
7. Calculate the test statistic and p-value / confidence interval
        ↓
8. Evaluate statistical significance (reject or fail to reject H₀) and interpret limitations
```

---

### 3.6 Experimental Design, Variables, and Statistical Tests

*(Note: These topics are listed in the Lecture Overview, Reading 9.1 introduction, Studio Activity 3, and the Week 9 quiz flashcards in `week-9-anki.md`, though the end of `lecture/lecture-summary.md` was cut off at Section 9.)*

#### Variables in Experimental Design
- **Independent Variable (IV):** The variable or condition that the researcher manipulates, controls, or uses to group participants (the presumed cause).
- **Dependent Variable (DV):** The outcome variable measured by the researcher to assess the effect of the independent variable.
- **Confounding Variable:** An extraneous variable that correlates with both the IV and DV and can distort or mask the true relationship between them.
- **Important:** Good experimental design **minimises the effect of confounding variables** while isolating and observing the effect of one or more **independent variables** on one or more **dependent variables**.

#### Between-Subjects vs. Within-Subjects Designs
- **Between-Subjects Design:** Each participant is exposed to only **one** experimental condition (different groups of participants experience different conditions).
- **Within-Subjects (Repeated-Measures) Design:** The **same** participants are exposed to **multiple** conditions over time.
  - **Important advantages & requirements:**
    - Within-subjects studies are generally **more statistically powerful** (controlling for individual baseline variation).
    - Every participant must have a valid measurement for each condition/measure.
    - **Counter-balancing** the order of conditions is essential in within-subjects studies to prevent **order effects** (e.g., practice or fatigue effects).

#### Confidence Intervals & Statistical Significance
- **Confidence Interval (CI):** Estimates the range/probability within which a sample statistic represents the true population parameter.
- **Statistical Significance:** Quantifies whether the test statistic (and resulting $p$-value) makes the observed sample result sufficiently unlikely under $H_0$ to reject $H_0$.

#### Choosing Statistical Tests: Parametric vs. Non-Parametric
- **Important:** You do **not** simply force/normalise all data into a normal distribution or pick any test arbitrarily; test selection depends on (1) **number of groups/conditions**, (2) **between- vs. within-subjects design**, and (3) **whether parametric assumptions (such as normality and level of measurement) hold**.

| Scenario | Parametric Test (Normally distributed continuous data) | Non-Parametric Alternative (Non-normal or ordinal/ranked data) |
|---|---|---|
| **2 groups, Between-Subjects** | **Student's $t$-test** (equal variances) or **Welch's $t$-test** (unequal variances; e.g., MATLAB `ttest2` handles unequal group sizes).<br>**Important properties of the $t$-statistic:**<br>A higher $t$-value is produced by:<br>1. A **larger difference in means** between groups ($\Delta \bar{x} \uparrow \implies t \uparrow$)<br>2. A **lower pooled standard deviation** ($SD_{\text{pooled}} \downarrow \implies t \uparrow$)<br>3. A **larger sample size / number of participants** ($n \uparrow \implies t \uparrow$)<br>*(Note: Welch's $t$-test does NOT produce a lower $t$-value in all cases, nor is skew calculated to choose between Student's and Welch's $t$-test—variance equality is what matters.)* | **Mann-Whitney $U$ test**<br>*(Applicable to non-normal continuous data or ordinal questionnaire items, e.g., letter grades `A, B, C, D, F, X`.)* |
| **2 conditions, Within-Subjects** | **Paired / Within-Subjects $t$-test** *(requires every subject to have a value for each measure).* | **Wilcoxon Signed-Rank test** *(used when within-subjects data are not normally distributed).* |
| **> 2 groups (3+ groups)** | **One-Way ANOVA** (Analysis of Variance; or **ANCOVA** when controlling for covariates).<br>**Important limitation of ANOVA:** A one-way ANOVA only tells you *whether* at least one group differs significantly; it **cannot identify which specific group(s) differ**.<br>**Post-hoc test:** A **Tukey post-hoc test** calculates a $p$-value for every possible pair of groups to identify specifically which group means differ significantly. *(Note: a between-subjects one-way ANOVA cannot be used for within-subjects studies.)* | *(Kruskal-Wallis / Friedman tests in general statistics, though not explicitly named in the local notes.)* |

---


## [line 201]

### 3.7 Research Biases, Ethical Pitfalls, and Studio Activities

#### Ethical Problems & Biases in Inferential Statistics
The lecture overview and studio activities highlight critical validity and ethical failures when analysing and reporting statistical data:
1. **Selection / Sampling Bias:** Recruiting a sample that systematically differs from the target population (e.g., surveying only current/satisfied customers, early adopters, highly productive users, HD students, or companies already prone to cyberattacks; ignoring uneven regional or language response rates).
2. **Cherry-Picking & Reporting Bias:** Running multiple analyses or collecting multiple metrics across groups, then reporting *only* the favourable/statistically significant results while omitting non-significant or negative findings.
3. **$p$-Hacking:** Manipulating data collection, outlier removal, or statistical tests until a statistically significant $p$-value ($p < 0.05$) is achieved.
4. **HARKing (Hypothesising After the Results are Known):** Presenting a post-hoc pattern discovered in the data as if it were an a priori hypothesis defined before data collection.
5. **Misleading Visualisations & Unsubstantiated Claims:** Using charts that exaggerate minor, statistically non-significant trends; omitting context for satisfaction ratings; making nonsensical comparisons (e.g., comparing AI chatbot response time directly against human response time); or acknowledging sample bias in a footnote while still presenting unsubstantiated performance claims to management.

#### Studio Activities Summary (Topic 9 Workshop)
- **Important Assessment Rule:** The weekly studio includes a **graded quiz completed during the studio session, worth 20% of the total unit marks**.
- **Activity 1 (45 min, individual task on Flora platform):** Critique four IT research scenarios for research, statistical, and reporting biases:
  - *Scenario 1 – Global Cloud:* Selection bias (only current customers), language bias, sampling bias (differing regional response rates), and visualisation bias overstating results.
  - *Scenario 2 – Productivity Software:* Selection/user bias (studying early adopters and already highly productive users rather than the broader customer population), visualisation bias (plotting increasing rates without establishing statistical significance), and reporting bias (cherry-picking results and ignoring non-significant statistical tests to justify a product).
  - *Scenario 3 – Security Software:* Selection bias (testing only companies prone to attacks rather than also testing companies with strong baseline security), reporting/visualisation bias (cherry-picking tests), and communication failure (overstating effectiveness to management).
  - *Scenario 4 – AI Customer Service:* Selection bias (surveying previous/happy users), reporting failures (reporting only positive statistical tests, ignoring negative ones, and arguing unsubstantiated improvements despite acknowledging selection bias), and visualisation/comparison bias (lacking context for satisfaction scores; invalid comparison of chatbot vs. human response speed).
- **Activity 2 & Activity 3 (Group tasks):**
  - Reflect on using the Flora learning platform (where different group members may have access to different tools/functionalities, such as LLM chatbots, timers, search, or planners).
  - Formulate a unique, testable **null hypothesis ($H_0$)** and **alternative hypothesis ($H_1$)** using platform data (e.g., $H_0$: LLM access has no impact on response quality; $H_1$: LLM access has an impact on response quality).
  - Identify the **independent variable** (e.g., access to LLM/feature), **dependent variable** (e.g., response quality/score), and **confounding variables**, specify the **data collection and sampling methods**, and justify an appropriate **statistical test** (e.g., $t$-test, ANCOVA) alongside its required assumptions.

---

## 4. Final Condensed Summary

**Descriptive statistics** summarises and visualises the data actually collected (mean, median, mode, variance, SD, charts), whereas **inferential statistics** uses a **sample** to draw conclusions about a wider **population** and quantifies the probability that observed differences or relationships are due to **chance** rather than real population effects. Because studying an entire population (a **census**) is rarely feasible due to time, cost, personnel, and access constraints, researchers rely on sampling. **Important:** The quality of any statistical inference depends on how representative the sample is of the population.

Sampling methods fall into two categories:
1. **Probability sampling** (every population member has a chance of selection): **simple random** (equal chance; reduces bias and supports test assumptions), **systematic** (every $k$-th individual), **stratified** (dividing into homogeneous subgroups/strata and sampling from each), and **cluster** (dividing into mini-population clusters).
2. **Non-probability sampling** (non-random selection): **convenience** (most accessible), **purposive** (deliberately chosen for specific expertise/traits), **snowball** (participants recruit others, ideal for hard-to-reach groups), and **voluntary response** (opt-in). Researchers must choose a strategy based on their research question, population, accessibility, resources, and planned analysis, and **must report the method, rationale, and resulting limitations**.

**Hypothesis testing** evaluates a **testable, measurable prediction** by contrasting a **null hypothesis ($H_0$: no effect/relationship/difference)** against an **alternative hypothesis ($H_1/H_A$: an effect/relationship/difference exists)**. Good experimental design isolates the effect of **independent variables** on **dependent variables** while minimising **confounding variables**, using either **between-subjects** or **within-subjects** designs (the latter having higher statistical power but requiring **counter-balancing** to avoid order effects). Statistical test selection depends on group count, study design, and data distribution: **parametric tests** include **Student's/Welch's $t$-test** (2 groups, between-subjects; higher $t$ comes from larger mean differences, lower pooled SD, and larger $n$), **paired $t$-test** (2 conditions, within-subjects), and **one-way ANOVA** (>2 groups, requiring a **Tukey post-hoc test** to pinpoint which specific group pair differs), while **non-parametric tests** for non-normal or ordinal data include the **Mann-Whitney $U$ test** (between-subjects) and **Wilcoxon Signed-Rank test** (within-subjects). Finally, researchers must guard against **selection bias, cherry-picking, $p$-hacking, HARKing, and misleading visualisations**.

---

## 5. Unclear, Incomplete, or Missing Information

1. **Truncation of `lecture/lecture-summary.md` at Line 372:**
   - The lecture notes file in `lecture/lecture-summary.md` cuts off mid-sentence at the end of Section 9 (`Evaluate statistical`), omitting five core topics promised in its own Overview (lines 15–24):
     - Independent, dependent, and confounding variables
     - Statistical significance ($p$-values, $\alpha$ thresholds, Type I / Type II errors)
     - Choosing appropriate statistical tests
     - Parametric versus non-parametric tests
     - Definitions and examples of **cherry-picking, $p$-hacking, HARKing, and misleading visualisations**
   - *How this summary handled it:* Details on IV/DV/confounding variables, between- vs. within-subjects designs, parametric vs. non-parametric tests ($t$-tests, ANOVA, Tukey, Mann-Whitney $U$, Wilcoxon Signed-Rank), and research biases were reconstructed from `week-9-anki.md` and `studio/` so that your summary remains complete, but the original lecture text for those sections is missing from `lecture/lecture-summary.md`.
2. **Incomplete Reading Transcripts (`readings/`):**
   - `readings/introduction-to-inferential-stats.md` contains only video transcript **9.1** (stopping right after voluntary response sampling). Transcripts for subsequent videos (e.g., 9.2 on experimental design/hypothesis testing and 9.3 on parametric/non-parametric tests, which are referenced in `week-9-anki.md` as "in the video") are not present in `readings/`.
3. **Directory Naming (`tutorial/` vs. `studio/`):**
   - There is no `tutorial/` directory in the workspace; tutorial materials are stored in `studio/` (`Week 9 S2 2026 - Studio Activity Sheet.pdf` and `studio/studio.md`).

## [line 251]

4. **Missing Mathematical Formulas and Thresholds:**
   - Neither the lecture file nor the reading transcript includes the explicit mathematical formulas for Student's/Welch's $t$-statistic, pooled standard deviation, ANOVA $F$-ratio, or standard $\alpha$ significance thresholds (e.g., $\alpha = 0.05$), even though conceptual relationships (how mean difference, pooled SD, and $n$ affect $t$) are tested in `week-9-anki.md`.
5. **External Flora Platform Scenarios:**
   - The full text of the four IT research scenarios in Studio Activity 1 is hosted inside the external Flora Moodle environment (`https://www.floraengine.org/moodle/`) and is not included in the PDF; only the user's bias-identification notes in `studio/studio.md` are available locally.
