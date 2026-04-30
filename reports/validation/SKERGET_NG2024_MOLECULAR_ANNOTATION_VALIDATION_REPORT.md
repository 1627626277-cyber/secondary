# Skerget NG2024 Molecular Annotation Validation

Date: 2026-04-30

## Data Join

- Current CoMMpass/GDC score table samples: 762.
- Samples with NG2024 patient-feature annotations: 762.
- Samples with NG2024 RNA subtype predictions: 707.

## Analysis Scope

- Tested plasma-secretory, clinical subtype module and marker z-scores against public CoMMpass molecular-risk annotations.
- Tested binary calls, ordinal/lab variables, categorical molecular subtypes and RNA subtype probability scores.
- PFS, treatment response and therapy-line claims remain out of scope.

## Top Associations

- categorical_kruskal: `RNA_Subtype_Name` vs `JCHAIN_z`, n=707, effect=144, p=2.53e-25, FDR=2.43e-23.
- categorical_kruskal: `RNA_Subtype_Name_ng2024` vs `JCHAIN_z`, n=707, effect=144, p=2.53e-25, FDR=2.43e-23.
- categorical_kruskal: `RNA_Subtype_Name` vs `clinical_subtype_module_score_z`, n=707, effect=129.9, p=1.86e-22, FDR=8.93e-21.
- categorical_kruskal: `RNA_Subtype_Name_ng2024` vs `clinical_subtype_module_score_z`, n=707, effect=129.9, p=1.86e-22, FDR=8.93e-21.
- subtype_probability_spearman: `PR` vs `plasma_secretory_score_z`, n=707, effect=0.3399, p=1.41e-20, FDR=5.43e-19.
- subtype_probability_spearman: `Low purity` vs `TXNDC5_z`, n=707, effect=-0.3295, p=2.31e-19, FDR=7.39e-18.
- subtype_probability_spearman: `1q gain` vs `JCHAIN_z`, n=707, effect=-0.3246, p=8.34e-19, FDR=2.29e-17.
- categorical_kruskal: `RNA_Subtype_Name` vs `POU2AF1_z`, n=707, effect=107.1, p=6.8e-18, FDR=1.45e-16.
- categorical_kruskal: `RNA_Subtype_Name_ng2024` vs `POU2AF1_z`, n=707, effect=107.1, p=6.8e-18, FDR=1.45e-16.
- categorical_kruskal: `RNA_Subtype_Name` vs `plasma_secretory_score_z`, n=707, effect=92.18, p=6.22e-15, FDR=1.09e-13.
- categorical_kruskal: `RNA_Subtype_Name_ng2024` vs `plasma_secretory_score_z`, n=707, effect=92.18, p=6.22e-15, FDR=1.09e-13.
- categorical_kruskal: `RNA_Subtype_Name_ng2024` vs `XBP1_z`, n=707, effect=91.57, p=8.2e-15, FDR=1.21e-13.

## Clinically Relevant Annotation Results

- binary_mannwhitney: `Cp_1q21_Call` vs `plasma_secretory_score_z`, n=680, effect=0.2676, p=2.13e-06, FDR=1.24e-05.
- binary_mannwhitney: `Cp_13q14_Call` vs `JCHAIN_z`, n=680, effect=-0.3018, p=4e-05, FDR=0.000197.
- ordinal_spearman: `ISS_Stage` vs `plasma_secretory_score_z`, n=742, effect=0.1319, p=0.000316, FDR=0.00138.
- binary_mannwhitney: `Cp_13q14_Call` vs `plasma_secretory_score_z`, n=680, effect=0.1631, p=0.000374, FDR=0.00153.
- ordinal_spearman: `IMWG_Risk_Class` vs `plasma_secretory_score_z`, n=630, effect=0.1342, p=0.000733, FDR=0.00287.
- binary_mannwhitney: `Cp_17p13_Call` vs `POU2AF1_z`, n=680, effect=0.3367, p=0.00147, FDR=0.00532.
- binary_mannwhitney: `Cp_1q21_Call` vs `TXNDC5_z`, n=680, effect=0.231, p=0.00259, FDR=0.00843.
- binary_mannwhitney: `Hyperdiploid_Call` vs `TXNDC5_z`, n=680, effect=-0.2955, p=0.00513, FDR=0.0154.
- binary_mannwhitney: `Cytogenetic_High_Risk` vs `JCHAIN_z`, n=648, effect=-0.2215, p=0.00656, FDR=0.0194.
- binary_mannwhitney: `Cp_17p13_Call` vs `clinical_subtype_module_score_z`, n=680, effect=0.2295, p=0.0093, FDR=0.0263.
- ordinal_spearman: `ISS_Stage` vs `XBP1_z`, n=742, effect=0.0926, p=0.0116, FDR=0.0319.
- binary_mannwhitney: `Cp_1q21_Call` vs `JCHAIN_z`, n=680, effect=-0.226, p=0.0153, FDR=0.0409.

## Outputs

- Merged annotation table: `analysis/skerget_ng2024_public_supplement/commppass_scores_with_ng2024_annotations.tsv`.
- Association table: `analysis/skerget_ng2024_public_supplement/ng2024_molecular_annotation_associations.tsv`.
- Ranked association table: `analysis/skerget_ng2024_public_supplement/ng2024_molecular_annotation_fdr_ranked.tsv`.
- Top-association plot: `analysis/skerget_ng2024_public_supplement/ng2024_top_molecular_annotation_associations.png`.
- Key boxplots: `analysis/skerget_ng2024_public_supplement/ng2024_key_molecular_annotation_boxplots.png`.

## Interpretation

- This public supplement can now be used as a molecular-risk annotation layer for the Q2 mainline.
- The result should be framed as molecular annotation / subtype support, not as PFS or treatment-response validation.
