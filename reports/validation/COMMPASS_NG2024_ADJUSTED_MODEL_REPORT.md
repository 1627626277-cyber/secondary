# CoMMpass / NG2024 Adjusted Model Report

Date: 2026-04-30

## Purpose

- Strengthen the project beyond univariate associations by testing whether the plasma-secretory axis remains associated with OS, ISS and public molecular-risk annotations after basic covariate adjustment.
- This analysis uses public GDC CoMMpass OS/ISS fields plus public Skerget et al. Nature Genetics 2024 CoMMpass molecular annotations.
- It does not add PFS, R-ISS or treatment-response endpoints because those fields are not available in the current public/open tables.

## Input

- Input table: `analysis\skerget_ng2024_public_supplement\commppass_scores_with_ng2024_annotations.tsv`.
- Samples in merged table: 762.
- OS events: 153.
- ISS available: 742.
- Cytogenetic high-risk available: 648.
- 1q21 call available: 680.

## Models

- Cox proportional hazards: OS ~ score + age + sex + ISS.
- Cox proportional hazards: OS ~ score + age + sex + ISS + 1q21.
- Cox proportional hazards: OS ~ score + age + sex + ISS + cytogenetic high-risk.
- Logistic regression: ISS III ~ score + age + sex.
- Logistic regression: IMWG non-standard risk / cytogenetic high-risk / 1q21 / 17p13 ~ score + age + sex + ISS.
- Linear model: PR RNA-subtype probability ~ score + age + sex + ISS.

## Top Adjusted Results

| Model | Endpoint | Score | n | Events/cases | Effect | 95% CI | FDR |
|---|---|---|---:|---:|---:|---:|---:|
| PR RNA-subtype probability adjusted for age, sex, ISS | PR | Plasma-secretory score | 690 |  | 0.0941 | 0.0656-0.1225 | 9.51e-09 |
| PR RNA-subtype probability adjusted for age, sex, ISS | PR | POU2AF1/XBP1/JCHAIN module | 690 |  | 0.0648 | 0.0402-0.0893 | 8.16e-06 |
| PR RNA-subtype probability adjusted for age, sex, ISS | PR | JCHAIN | 690 |  | 0.0386 | 0.0217-0.0555 | 1.58e-04 |
| 1q21 gain/amplification adjusted for age, sex, ISS | Cp_1q21_Call | Plasma-secretory score | 660 | 233 | 1.8725 | 1.4085-2.4894 | 2.13e-04 |
| OS adjusted for age, sex, ISS, cytogenetic high risk | overall_survival | JCHAIN | 630 | 124 | 1.5257 | 1.2303-1.8920 | 0.0013 |
| OS adjusted for age, sex, ISS, 1q21 | overall_survival | JCHAIN | 660 | 128 | 1.4279 | 1.1598-1.7580 | 0.0071 |
| OS adjusted for age, sex, ISS | overall_survival | JCHAIN | 742 | 147 | 1.3828 | 1.1409-1.6758 | 0.0073 |
| PR RNA-subtype probability adjusted for age, sex, ISS | PR | XBP1 | 690 |  | 0.0289 | 0.0115-0.0462 | 0.0078 |
| 17p13 deletion adjusted for age, sex, ISS | Cp_17p13_Call | POU2AF1 | 660 | 86 | 1.4917 | 1.1672-1.9065 | 0.0084 |
| 1q21 gain/amplification adjusted for age, sex, ISS | Cp_1q21_Call | TXNDC5 | 660 | 233 | 1.3126 | 1.1076-1.5556 | 0.0091 |
| OS adjusted for age, sex, ISS | overall_survival | Plasma-secretory score | 742 | 147 | 1.5571 | 1.1772-2.0596 | 0.0094 |
| PR RNA-subtype probability adjusted for age, sex, ISS | PR | POU2AF1 | 690 |  | 0.0263 | 0.0088-0.0438 | 0.0152 |
| OS adjusted for age, sex, ISS, cytogenetic high risk | overall_survival | Plasma-secretory score | 630 | 124 | 1.5466 | 1.1373-2.1034 | 0.0226 |
| Cytogenetic high risk adjusted for age, sex, ISS | Cytogenetic_High_Risk | JCHAIN | 630 | 191 | 0.7947 | 0.6739-0.9372 | 0.0244 |
| OS adjusted for age, sex, ISS | overall_survival | POU2AF1/XBP1/JCHAIN module | 742 | 147 | 1.4112 | 1.0956-1.8178 | 0.0268 |
| OS adjusted for age, sex, ISS, cytogenetic high risk | overall_survival | POU2AF1/XBP1/JCHAIN module | 630 | 124 | 1.4521 | 1.1025-1.9125 | 0.0268 |

## Interpretation

- Completed adjusted models: 54.
- FDR < 0.05 adjusted findings: 21.
- These results can support the manuscript as covariate-adjusted association evidence, but they should not be written as causal mechanism or wet-lab validation.
- Because public/open CoMMpass still lacks PFS, R-ISS and treatment-response fields, those endpoints remain future MMRF-dependent enhancements.

## Outputs

- `analysis\commppass_ng2024_adjusted_models\commppass_ng2024_adjusted_model_results.tsv`
- `analysis\commppass_ng2024_adjusted_models\commppass_ng2024_adjusted_model_fdr_ranked.tsv`
- `analysis\commppass_ng2024_adjusted_models\commppass_ng2024_adjusted_model_forestplot.png`
- `analysis\commppass_ng2024_adjusted_models\commppass_ng2024_adjusted_model_forestplot.pdf`
