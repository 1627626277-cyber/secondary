# CoMMpass Sensitivity Models

Purpose: address reviewer concerns that OS and 1q21 associations may be driven by PR subtype probability, proliferation, cytogenetic risk, or public purity/tumor-burden annotations.

Cox OS models:

| model_name                          |   n |   events |      hr |   ci_lower |   ci_upper |   p_value |       fdr |   c_index | covariates                                                                                |
|:------------------------------------|----:|---------:|--------:|-----------:|-----------:|----------:|----------:|----------:|:------------------------------------------------------------------------------------------|
| M1 age+sex+ISS+1q21                 | 660 |      128 | 1.45957 |   1.06903  |    1.99277 | 0.0173057 | 0.0484559 |  0.723855 | age_z,male,iss_stage_num,oneq21                                                           |
| M2 M1+PR probability                | 613 |      119 | 1.31723 |   0.9357   |    1.85432 | 0.114312  | 0.200046  |  0.718892 | age_z,male,iss_stage_num,oneq21,pr_probability_z                                          |
| M3 M1+PR+proliferation              | 613 |      119 | 1.14951 |   0.804757 |    1.64195 | 0.443713  | 0.443713  |  0.745539 | age_z,male,iss_stage_num,oneq21,pr_probability_z,proliferation_z                          |
| M4 M1+del17p+high-risk cytogenetics | 630 |      124 | 1.44901 |   1.05719  |    1.98604 | 0.021124  | 0.0492894 |  0.716402 | age_z,male,iss_stage_num,oneq21,del17p,high_risk_cyto                                     |
| M5 M1+low-purity probability        | 613 |      119 | 1.55294 |   1.10981  |    2.17302 | 0.010234  | 0.035819  |  0.71804  | age_z,male,iss_stage_num,oneq21,low_purity_probability_z                                  |
| M6 M1+PR+proliferation+low-purity   | 613 |      119 | 1.16672 |   0.814235 |    1.67181 | 0.400785  | 0.431615  |  0.745255 | age_z,male,iss_stage_num,oneq21,pr_probability_z,proliferation_z,low_purity_probability_z |
| M7 M1+clinical tumor burden CMMC    | 262 |       45 | 1.48132 |   0.820478 |    2.67442 | 0.192382  | 0.269335  |  0.734109 | age_z,male,iss_stage_num,oneq21,log1p_cmmc_z                                              |

1q21 logistic sensitivity models:

| score                           | score_label                |   n |   cases |   odds_ratio |   ci_lower |   ci_upper |      coef |       se |    p_value | covariates                                                                         | status   | note                                                                                    |        fdr |
|:--------------------------------|:---------------------------|----:|--------:|-------------:|-----------:|-----------:|----------:|---------:|-----------:|:-----------------------------------------------------------------------------------|:---------|:----------------------------------------------------------------------------------------|-----------:|
| plasma_secretory_score_z        | Plasma-secretory score     | 613 |     212 |      1.3955  |   1.00494  |   1.93783  |  0.333249 | 0.167509 | 0.0466522  | age_z,male,iss_stage_num,pr_probability_z,proliferation_z,low_purity_probability_z | ok       | 1q21 association adjusted for PR probability, proliferation, and low-purity probability | 0.0466522  |
| clinical_subtype_module_score_z | POU2AF1/XBP1/JCHAIN module | 613 |     212 |      0.65513 |   0.498978 |   0.860148 | -0.422921 | 0.138914 | 0.00233077 | age_z,male,iss_stage_num,pr_probability_z,proliferation_z,low_purity_probability_z | ok       | 1q21 association adjusted for PR probability, proliferation, and low-purity probability | 0.00466154 |

Interpretation boundary:

- Models are retrospective association models, not prospective prediction models.
- If PR/proliferation adjustment attenuates the score, this supports reframing the axis as a PR/proliferation/1q21 molecular-risk context rather than an independent clinical biomarker.
- Low-purity probability and CMMC are public annotation proxies; they do not replace direct tumor purity or matched flow cytometry.