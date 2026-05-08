# Module Coverage And Testing Inventory

Purpose: address reviewer concerns about cross-platform module equivalence and flexible FDR families.

Module coverage summary:

| dataset           | module                  |   n_present |   n_total | genes_present                                                        | genes_absent             | scoring_formula                                                              |
|:------------------|:------------------------|------------:|----------:|:---------------------------------------------------------------------|:-------------------------|:-----------------------------------------------------------------------------|
| GSE269875_spatial | plasma_secretory        |           5 |         6 | TXNDC5,XBP1,JCHAIN,MZB1,SDC1                                         | POU2AF1                  | mean of available within-cohort standardized genes; absent genes not imputed |
| GSE269875_spatial | clinical_subtype_module |           2 |         3 | XBP1,JCHAIN                                                          | POU2AF1                  | mean of available within-cohort standardized genes; absent genes not imputed |
| GSE269875_spatial | extended_plasma_axis    |          10 |        11 | IRF4,JCHAIN,MZB1,PIM2,PRDM1,SDC1,SLAMF7,TNFRSF17,TXNDC5,XBP1         | POU2AF1                  | mean of available within-cohort standardized genes; absent genes not imputed |
| GSE299193_Xenium  | plasma_secretory        |           3 |         6 | POU2AF1,XBP1,MZB1                                                    | TXNDC5,JCHAIN,SDC1       | mean of available within-cohort standardized genes; absent genes not imputed |
| GSE299193_Xenium  | clinical_subtype_module |           2 |         3 | POU2AF1,XBP1                                                         | JCHAIN                   | mean of available within-cohort standardized genes; absent genes not imputed |
| GSE299193_Xenium  | extended_plasma_axis    |           7 |        11 | IRF4,MZB1,PIM2,POU2AF1,SLAMF7,TNFRSF17,XBP1                          | JCHAIN,PRDM1,SDC1,TXNDC5 | mean of available within-cohort standardized genes; absent genes not imputed |
| GSE271107_scRNA   | plasma_secretory        |           5 |         6 | TXNDC5,XBP1,JCHAIN,MZB1,SDC1                                         | POU2AF1                  | mean of available within-cohort standardized genes; absent genes not imputed |
| GSE271107_scRNA   | clinical_subtype_module |           2 |         3 | XBP1,JCHAIN                                                          | POU2AF1                  | mean of available within-cohort standardized genes; absent genes not imputed |
| GSE271107_scRNA   | extended_plasma_axis    |          10 |        11 | IRF4,JCHAIN,MZB1,PIM2,PRDM1,SDC1,SLAMF7,TNFRSF17,TXNDC5,XBP1         | POU2AF1                  | mean of available within-cohort standardized genes; absent genes not imputed |
| GSE24080_bulk     | plasma_secretory        |           6 |         6 | TXNDC5,POU2AF1,XBP1,JCHAIN,MZB1,SDC1                                 |                          | mean of available within-cohort standardized genes; absent genes not imputed |
| GSE24080_bulk     | clinical_subtype_module |           3 |         3 | POU2AF1,XBP1,JCHAIN                                                  |                          | mean of available within-cohort standardized genes; absent genes not imputed |
| GSE24080_bulk     | extended_plasma_axis    |          11 |        11 | IRF4,JCHAIN,MZB1,PIM2,POU2AF1,PRDM1,SDC1,SLAMF7,TNFRSF17,TXNDC5,XBP1 |                          | mean of available within-cohort standardized genes; absent genes not imputed |
| GSE2658_bulk      | plasma_secretory        |           6 |         6 | TXNDC5,POU2AF1,XBP1,JCHAIN,MZB1,SDC1                                 |                          | mean of available within-cohort standardized genes; absent genes not imputed |
| GSE2658_bulk      | clinical_subtype_module |           3 |         3 | POU2AF1,XBP1,JCHAIN                                                  |                          | mean of available within-cohort standardized genes; absent genes not imputed |
| GSE2658_bulk      | extended_plasma_axis    |          11 |        11 | IRF4,JCHAIN,MZB1,PIM2,POU2AF1,PRDM1,SDC1,SLAMF7,TNFRSF17,TXNDC5,XBP1 |                          | mean of available within-cohort standardized genes; absent genes not imputed |
| CoMMpass_GDC_bulk | plasma_secretory        |           6 |         6 | TXNDC5,POU2AF1,XBP1,JCHAIN,MZB1,SDC1                                 |                          | mean of available within-cohort standardized genes; absent genes not imputed |
| CoMMpass_GDC_bulk | clinical_subtype_module |           3 |         3 | POU2AF1,XBP1,JCHAIN                                                  |                          | mean of available within-cohort standardized genes; absent genes not imputed |
| CoMMpass_GDC_bulk | extended_plasma_axis    |          11 |        11 | IRF4,JCHAIN,MZB1,PIM2,POU2AF1,PRDM1,SDC1,SLAMF7,TNFRSF17,TXNDC5,XBP1 |                          | mean of available within-cohort standardized genes; absent genes not imputed |

Important incomplete-coverage cases:

| dataset           | module                  | genes_absent             |
|:------------------|:------------------------|:-------------------------|
| GSE269875_spatial | plasma_secretory        | POU2AF1                  |
| GSE269875_spatial | clinical_subtype_module | POU2AF1                  |
| GSE269875_spatial | extended_plasma_axis    | POU2AF1                  |
| GSE299193_Xenium  | plasma_secretory        | TXNDC5,JCHAIN,SDC1       |
| GSE299193_Xenium  | clinical_subtype_module | JCHAIN                   |
| GSE299193_Xenium  | extended_plasma_axis    | JCHAIN,PRDM1,SDC1,TXNDC5 |
| GSE271107_scRNA   | plasma_secretory        | POU2AF1                  |
| GSE271107_scRNA   | clinical_subtype_module | POU2AF1                  |
| GSE271107_scRNA   | extended_plasma_axis    | POU2AF1                  |

Testing inventory summary:

| analysis_family             | prespecified_or_exploratory   |   n_rows |
|:----------------------------|:------------------------------|---------:|
| adjusted_models             | prespecified                  |       54 |
| commppass_gdc               | prespecified                  |       24 |
| commppass_sensitivity_os    | exploratory_or_sensitivity    |       14 |
| external_bulk               | exploratory_or_sensitivity    |       30 |
| ng2024_annotations          | exploratory_or_sensitivity    |      192 |
| spatial_discovery           | prespecified                  |       28 |
| spatial_morans_i            | exploratory_or_sensitivity    |       54 |
| spatial_neighbor_enrichment | exploratory_or_sensitivity    |       63 |
| xenium_validation           | prespecified                  |       18 |

Interpretation boundary:

- Modules are not assumed to be identical across platforms when genes are absent.
- Absent genes are not imputed.
- The inventory records all available tested rows from current result tables and marks exploratory/sensitivity analyses separately from prespecified primary analyses.