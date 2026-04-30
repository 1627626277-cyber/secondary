# CoMMpass Cox PH Assumption Check

Date: 2026-05-01

Purpose:

- Screen Cox proportional hazards assumptions for CoMMpass/NG2024 adjusted OS models.
- Use Schoenfeld residual Spearman correlation with log(event time).
- Treat this as a presubmission diagnostic screen, not as a replacement for external statistical review.

## Primary Score Results

- Plasma-secretory score | OS adjusted for age, sex, ISS, 1q21: n=660, events=128, rho=-0.0637, p=0.4752, FDR=0.7777.
- POU2AF1/XBP1/JCHAIN module | OS adjusted for age, sex, ISS, 1q21: n=660, events=128, rho=-0.0585, p=0.5122, FDR=0.7889.

## Interpretation

- No FDR-significant PH-screen violation was detected for the two primary score terms.
- The 1q21 covariate reached FDR < 0.05 in the adjusted models.
- Report Cox results as adjusted association models rather than prospective prediction models.
- Mention the covariate-level PH signal as a modeling caution if space allows.

## Outputs

- `analysis/commppass_cox_ph_assumption/commppass_cox_ph_schoenfeld_tests.tsv`
- `analysis/commppass_cox_ph_assumption/commppass_cox_ph_schoenfeld_score_residuals.png`
- `analysis/commppass_cox_ph_assumption/commppass_cox_ph_schoenfeld_score_residuals.pdf`
- `analysis/commppass_cox_ph_assumption/commppass_cox_ph_schoenfeld_score_residuals.svg`

## Manuscript Language

A proportional hazards diagnostic screen based on Schoenfeld residual correlations with log(event time) did not detect an FDR-significant violation for the primary adjusted Cox score terms.
