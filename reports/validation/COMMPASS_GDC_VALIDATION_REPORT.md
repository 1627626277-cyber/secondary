# CoMMpass / GDC Clinical Validation Report

Date: 2026-04-29

## Purpose

- Validate the plasma-secretory clinical-subtype axis in CoMMpass using open GDC STAR-count RNA-seq and GDC clinical fields.
- Prioritize OS and ISS because these are available in the open GDC clinical slice.
- Keep R-ISS, cytogenetic high-risk, PFS, and treatment response as pending until a fuller CoMMpass/MMRF clinical table is obtained.

## Data

- Open STAR-count gene-expression files indexed by GDC: 859.
- Baseline visit-1 bone marrow CD138+ samples selected: 762.
- Samples with merged RNA-seq and clinical data: 762.
- OS events in merged data: 153.
- ISS available in merged data: 742.

## Main Results

| Outcome | Variable | n | Events | Effect | Best FDR |
|---|---|---:|---:|---:|---:|
| os_event | plasma_secretory_score_z | 762 | 153 | 0.3460 | 9.31e-06 |
| os_event | clinical_subtype_module_score_z | 762 | 153 | 0.2813 | 5.46e-05 |
| os_event | JCHAIN_z | 762 | 153 | 0.2205 | 8.08e-04 |
| os_event | XBP1_z | 762 | 153 | 0.2358 | 0.0011 |
| iss_stage_num | plasma_secretory_score_z | 742 |  | 0.1319 | 0.0019 |
| os_event | TXNDC5_z | 762 | 153 | 0.1749 | 0.0163 |
| os_event | POU2AF1_z | 762 | 153 | 0.2796 | 0.0224 |
| iss_stage_III | XBP1_z | 742 | 211 | 0.2186 | 0.0326 |
| iss_stage_III | plasma_secretory_score_z | 742 | 211 | 0.1211 | 0.0326 |
| iss_stage_num | XBP1_z | 742 |  | 0.0926 | 0.0349 |
| iss_stage_num | clinical_subtype_module_score_z | 742 |  | 0.0818 | 0.0387 |
| iss_stage_num | POU2AF1_z | 742 |  | 0.0846 | 0.0387 |

## Interpretation

- This analysis provides CoMMpass-scale support for the revised subtype-axis route.
- The plasma-secretory score and POU2AF1/XBP1/JCHAIN module show FDR-supported OS-event associations.
- The plasma-secretory score also shows FDR-supported ISS-stage association and a median-split OS log-rank signal.
- The open GDC clinical slice does not provide sufficient R-ISS, detailed cytogenetic high-risk, PFS, or treatment-response fields, so those endpoints require a fuller MMRF/CoMMpass clinical table or another curated cohort.

## Outputs

- `analysis\commppass_gdc_validation\commppass_baseline_manifest.tsv`
- `analysis\commppass_gdc_validation\commppass_target_tpm.tsv`
- `analysis\commppass_gdc_validation\commppass_axis_clinical_scores.tsv`
- `analysis\commppass_gdc_validation\commppass_axis_associations.tsv`
- `analysis\commppass_gdc_validation\commppass_axis_fdr_ranked.tsv`
- `analysis\commppass_gdc_validation\commppass_module_by_iss.png`
- `analysis\commppass_gdc_validation\commppass_module_os_km.png`
- `analysis\commppass_gdc_validation\commppass_top_associations_barplot.png`
- `analysis\commppass_gdc_validation\commppass_axis_correlation_heatmap.png`
