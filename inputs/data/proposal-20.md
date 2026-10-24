# Task B Proposal 20: Predicting Belief That Homeownership Is Achievable Within Ten Years

## 0. Your Name & Student ID

**Name:** [Your name]  
**Student ID:** [Your student ID]

## 1. Proposed Hypothesis

Among non-home-owning Australians aged 18–30, higher housing-content social media exposure and higher perceived misinformation exposure will predict lower odds of believing that homeownership is achievable within ten years, while higher income will predict higher odds.

## 2. Null Hypothesis

Housing-content exposure, perceived misinformation exposure, and income do not predict the odds of believing homeownership is achievable within ten years among non-home-owning Australians aged 18–30.

## 3. Independent, Dependent and Confounding Variables

**IVs:** weekly housing-content exposure, perceived misinformation exposure, and household income (all continuous). **DV:** belief homeownership is achievable within ten years (yes/no). **Confounders:** age, education, and employment status.

## 4. Data Collection

Cross-sectional online survey of 150 non-home-owning Australians aged 18–30, recruited via university networks, housing and finance community groups, and AUD $180 of advertising. A 10-minute survey measures weekly exposure minutes, a misinformation-exposure scale, income, the binary achievability belief, age, education, and employment. Participants enter a draw for six AUD $75 vouchers (AUD $450), keeping total cost near AUD $630. Informed online consent, voluntary participation, and anonymised storage meet standard ethics requirements.

## 5. Statistical Tests

Multiple binary logistic regression predicts the odds of believing homeownership is achievable within ten years from exposure, misinformation exposure, and income, appropriate for a binary outcome with multiple continuous predictors. Age, education, and employment are entered as covariates. Assumptions include independence of observations, linearity between predictors and the log-odds (Box-Tidwell test), absence of multicollinearity (VIF < 5), and adequately sized outcome groups (at least 10 events per predictor). If linearity in the logit is violated, continuous predictors are categorised into tertiles as a fallback. Significance is set at α = .05, with adjusted odds ratios, 95% confidence intervals, and Nagelkerke R² as effect-size measures. The cross-sectional design supports association, not causal, conclusions about exposure and belief.

## 6. Limitations

Self-selected sampling from finance-interested groups may skew belief distributions and limit generalisability (Australian Bureau of Statistics, 2021). Perceived misinformation exposure cannot verify actual content falsity (Vosoughi et al., 2018). Cross-sectional data cannot establish temporal precedence among predictors and belief. Multicollinearity between exposure and misinformation-exposure items is possible. A future longitudinal design would help disentangle these overlapping predictors.

## 7. Alternative Narrative

A significant odds ratio could be overstated as proof social media 'destroys' optimism by omitting income as a predictor or reporting only the misinformation-exposure coefficient. Restricting the sample to low-income respondents would inflate the apparent effect—a risk of selective analysis.

## References

Australian Bureau of Statistics. (2021). *Housing occupancy and costs, 2019–20 financial year*. https://www.abs.gov.au/statistics/people/housing/housing-occupancy-and-costs/latest-release

Parkinson, S., Rowley, S., Stone, W., James, A., Spinney, A., & Reynolds, M. (2019). *Young Australians and the housing aspirations gap* (AHURI Final Report No. 318). Australian Housing and Urban Research Institute. https://www.ahuri.edu.au/research/final-reports/318

Vosoughi, S., Roy, D., & Aral, S. (2018). The spread of true and false news online. *Science, 359*(6380), 1146–1151. https://doi.org/10.1126/science.aap9559
