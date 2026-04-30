# GSE299193 Xenium Spatial Validation Report

Status: completed first-pass Xenium sample-level validation

Samples analyzed: 22

Panel coverage:

- `IRF4` present in 21/22 sample matrices.
- `JCHAIN` present in 0/22 sample matrices.
- `MZB1` present in 22/22 sample matrices.
- `PIM2` present in 21/22 sample matrices.
- `POU2AF1` present in 21/22 sample matrices.
- `PRDM1` present in 22/22 sample matrices.
- `SDC1` present in 0/22 sample matrices.
- `SLAMF7` present in 22/22 sample matrices.
- `TNFRSF17` present in 22/22 sample matrices.
- `TXNDC5` present in 0/22 sample matrices.
- `XBP1` present in 21/22 sample matrices.

Interpretation boundary:

- GSE299193 supports the plasma-secretory / POU2AF1-XBP1 program at the second spatial-cohort level.
- GSE299193 does not directly validate `TXNDC5`, `JCHAIN`, or `SDC1` because these genes are absent from the extracted Xenium feature matrices.

Primary outputs:

- `analysis/gse299193_xenium_validation/gse299193_sample_axis_scores.tsv`
- `analysis/gse299193_xenium_validation/gse299193_axis_group_associations.tsv`
- `analysis/gse299193_xenium_validation/gse299193_xenium_axis_validation.png`

Top association rows:

- MM_RM_vs_Ctrl_MGUS_SM / plasma_secretory_score_z: delta=0.766, p=0.000182, FDR=0.000575, n=11/11.
- MM_RM_vs_Ctrl_MGUS_SM / clinical_module_score_z: delta=1.068, p=0.000287, FDR=0.000575, n=10/11.
- MM_RM_vs_Ctrl_MGUS_SM / XBP1_mean_log1p: delta=0.257, p=0.000287, FDR=0.000575, n=10/11.
- Active_vs_non_active / plasma_secretory_score_z: delta=0.766, p=0.000182, FDR=0.000575, n=11/11.
- Active_vs_non_active / clinical_module_score_z: delta=1.068, p=0.000287, FDR=0.000575, n=10/11.
- Active_vs_non_active / XBP1_mean_log1p: delta=0.257, p=0.000287, FDR=0.000575, n=10/11.
- MM_RM_vs_Ctrl_MGUS_SM / POU2AF1_mean_log1p: delta=0.210, p=0.000823, FDR=0.00123, n=10/11.
- Active_vs_non_active / POU2AF1_mean_log1p: delta=0.210, p=0.000823, FDR=0.00123, n=10/11.
