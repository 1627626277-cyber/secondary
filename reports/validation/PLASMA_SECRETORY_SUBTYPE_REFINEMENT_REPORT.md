# Plasma-Secretory Clinical Subtype Refinement Report

Date: 2026-04-29

## Purpose

- Refine the manuscript direction from a single-gene TXNDC5 prognostic claim to a plasma-secretory clinical-subtype axis.
- Treat TXNDC5 as a spatial/single-cell localization candidate.
- Treat POU2AF1, XBP1, and JCHAIN as the clinical subtype / risk-linking module.

## Module Definition

- Clinical subtype module: mean within-cohort z-score of `POU2AF1`, `XBP1`, and `JCHAIN`.
- Module state: median split within each dataset into `module_high` and `module_low`.

## Main Results

| Dataset | Outcome | Variable | n | Events | Effect | Best FDR |
|---|---|---|---:|---:|---:|---:|
| GSE2658 | AMP_high_3plus | clinical_subtype_module_score_z | 248 | 114 | -4.67e-01 | 1.65e-05 |
| GSE2658 | AMP_high_3plus | POU2AF1_z | 248 | 114 | -6.23e-01 | 1.65e-05 |
| GSE2658 | AMP_high_3plus | XBP1_z | 248 | 114 | -6.01e-01 | 9.91e-05 |
| GSE2658 | AMP_high_3plus | JCHAIN_z | 248 | 114 | -3.00e-01 | 0.0122 |
| GSE24080 | os_24mo_event | XBP1_z | 559 | 78 | -3.91e-01 | 0.0362 |
| GSE24080 | efs_24mo_event | XBP1_z | 559 | 118 | -2.50e-01 | 0.1185 |
| GSE2658 | SURIND | JCHAIN_z | 559 | 100 | 0.2244 | 0.1402 |
| GSE2658 | SURIND | XBP1_z | 559 | 100 | 0.2640 | 0.1952 |
| GSE2658 | SURIND | TXNDC5_z | 559 | 100 | 0.2539 | 0.1952 |
| GSE2658 | SURTIM/SURIND | POU2AF1_z | 558 | 99 | 4.4079 | 0.2146 |

## Interpretation

- The strongest FDR-stable signal remains the GSE2658 1q21 amplification association for POU2AF1/XBP1/JCHAIN-related expression.
- The combined POU2AF1/XBP1/JCHAIN module is suitable as a clinical subtype axis, but its survival signal is exploratory and needs CoMMpass or another external clinical cohort.
- TXNDC5 should remain in the manuscript as a spatial and single-cell-supported plasma-localization marker, not as the current main clinical-risk marker.

## Outputs

- `analysis\plasma_secretory_subtype_refinement\plasma_secretory_subtype_sample_scores.tsv`
- `analysis\plasma_secretory_subtype_refinement\plasma_secretory_subtype_associations.tsv`
- `analysis\plasma_secretory_subtype_refinement\plasma_secretory_subtype_fdr_ranked.tsv`
- `analysis\plasma_secretory_subtype_refinement\plasma_secretory_subtype_effect_summary.tsv`
- `analysis\plasma_secretory_subtype_refinement\subtype_top_associations_barplot.png`
- `analysis\plasma_secretory_subtype_refinement\gse2658_module_by_1q21.png`
- `analysis\plasma_secretory_subtype_refinement\gse24080_xbp1_by_os.png`
- `analysis\plasma_secretory_subtype_refinement\gse2658_module_survival_km.png`
- `analysis\plasma_secretory_subtype_refinement\gse24080_axis_correlation_heatmap.png`
- `analysis\plasma_secretory_subtype_refinement\gse2658_axis_correlation_heatmap.png`
