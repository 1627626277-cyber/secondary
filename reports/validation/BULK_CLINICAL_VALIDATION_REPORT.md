# Bulk / Clinical Transcriptomic Validation Report

Date: 2026-04-29

## Purpose

- Validate the spatially discovered plasma-secretory / TXNDC5 axis in independent MM bulk transcriptomic cohorts.
- Test whether candidate genes or signature scores associate with clinical outcome variables available in GEO metadata.
- Strengthen the pure public-data translational route without requiring wet-lab experiments.

## Datasets

- GSE24080: 559 samples scored from GPL570 processed series matrix.
- GSE2658: 559 samples scored from GPL570 processed series matrix.

## Method Summary

- Parsed GPL570 annotation and mapped target genes to available Affymetrix probes.
- Collapsed each target gene to the highest-variance mapped probe within each dataset.
- Calculated z-scored plasma-secretory, myeloid-inflammatory, and stromal/ECM signatures within each cohort.
- Tested GSE24080 24-month EFS and OS milestone outcomes with Mann-Whitney and median-split Fisher tests.
- Tested GSE2658 disease-related death and follow-up time using binary association and a simple median-split log-rank test.

## Data Coverage

| Dataset | Samples | Plasma signature scored | TXNDC5 scored |
|---|---:|---:|---:|
| GSE24080 | 559 | 559 | 559 |
| GSE2658 | 559 | 559 | 559 |

## Key Association Results

### GSE24080: 24-month EFS event

| Variable | n | Events | Delta/effect | MW p/FDR | Fisher p/FDR | Log-rank p/FDR | AUC/event |
|---|---:|---:|---:|---:|---:|---:|---:|
| XBP1 | 559 | 118 | -2.37e-01 | 0.0198/0.1383 | 0.0972/0.6806 | NA/NA | 0.4302 |
| JCHAIN | 559 | 118 | 0.0787 | 0.2041/0.4884 | 0.6045/0.8463 | NA/NA | 0.5380 |
| PIM2 | 559 | 118 | 0.1360 | 0.2093/0.4884 | 0.2543/0.7037 | NA/NA | 0.5376 |
| plasma_secretory_score_z | 559 | 118 | -8.87e-02 | 0.5799/0.8403 | 0.3016/0.7037 | NA/NA | 0.4834 |
| POU2AF1 | 559 | 118 | 0.0837 | 0.8403/0.8403 | 0.6045/0.8463 | NA/NA | 0.5060 |

### GSE24080: 24-month OS death

| Variable | n | Events | Delta/effect | MW p/FDR | Fisher p/FDR | Log-rank p/FDR | AUC/event |
|---|---:|---:|---:|---:|---:|---:|---:|
| XBP1 | 559 | 78 | -3.71e-01 | 0.0060/0.0422 | 0.0509/0.3562 | NA/NA | 0.4031 |
| PIM2 | 559 | 78 | 0.2578 | 0.0858/0.3002 | 0.2720/0.6346 | NA/NA | 0.5606 |
| plasma_secretory_score_z | 559 | 78 | -1.18e-01 | 0.1696/0.3957 | 0.2246/0.6346 | NA/NA | 0.4515 |
| POU2AF1 | 559 | 78 | 0.1070 | 0.6655/0.7418 | 0.3930/0.6532 | NA/NA | 0.5153 |
| MZB1 | 559 | 78 | -7.62e-02 | 0.4189/0.6694 | 0.6275/0.7320 | NA/NA | 0.4715 |

### GSE2658: Disease-related death indicator

| Variable | n | Events | Delta/effect | MW p/FDR | Fisher p/FDR | Log-rank p/FDR | AUC/event |
|---|---:|---:|---:|---:|---:|---:|---:|
| JCHAIN | 559 | 100 | 3205.2010 | 0.0234/0.1636 | 0.0976/0.2277 | NA/NA | 0.5723 |
| TXNDC5 | 559 | 100 | 3120.0000 | 0.2256/0.5264 | 0.0976/0.2277 | NA/NA | 0.5386 |
| XBP1 | 559 | 100 | 1928.0505 | 0.1272/0.4451 | 0.0976/0.2277 | NA/NA | 0.5486 |
| POU2AF1 | 559 | 100 | -6.39e+02 | 0.5209/0.7293 | 0.3793/0.6638 | NA/NA | 0.4795 |
| plasma_secretory_score_z | 559 | 100 | 0.0262 | 0.4366/0.7293 | 0.5813/0.6782 | NA/NA | 0.5248 |

### GSE2658: Disease-related survival

| Variable | n | Events | Delta/effect | MW p/FDR | Fisher p/FDR | Log-rank p/FDR | AUC/event |
|---|---:|---:|---:|---:|---:|---:|---:|
| POU2AF1 | 558 | 99 | 4.4079 | NA/NA | NA/NA | 0.0358/0.2504 | NA |
| PIM2 | 558 | 99 | 2.5540 | NA/NA | NA/NA | 0.1100/0.3851 | NA |
| MZB1 | 558 | 99 | 0.6633 | NA/NA | NA/NA | 0.4154/0.8743 | NA |
| XBP1 | 558 | 99 | 0.4558 | NA/NA | NA/NA | 0.4996/0.8743 | NA |
| TXNDC5 | 558 | 99 | 0.1302 | NA/NA | NA/NA | 0.7183/0.9269 | NA |

### GSE2658: FISH 1q21 amplification >=3 copies

| Variable | n | Events | Delta/effect | MW p/FDR | Fisher p/FDR | Log-rank p/FDR | AUC/event |
|---|---:|---:|---:|---:|---:|---:|---:|
| POU2AF1 | 248 | 114 | -4.26e+03 | 4.46e-06/3.12e-05 | 2.34e-05/1.64e-04 | NA/NA | 0.3308 |
| XBP1 | 248 | 114 | -4.39e+03 | 4.96e-05/1.73e-04 | 0.0153/0.0536 | NA/NA | 0.3504 |
| JCHAIN | 248 | 114 | -4.28e+03 | 0.0081/0.0189 | 0.0974/0.2274 | NA/NA | 0.4024 |
| MZB1 | 248 | 114 | 2506.4005 | 0.0337/0.0590 | 0.1609/0.2816 | NA/NA | 0.5783 |
| PIM2 | 248 | 114 | 27.7500 | 0.4714/0.6599 | 1.0000/1.0000 | NA/NA | 0.5266 |

## Interpretation

- This step converts the project from spatial plus scRNA validation into a translational validation workflow.
- Direct clinical-outcome support for TXNDC5 is weak in this first-pass analysis, so TXNDC5 should not yet be framed as an independent prognostic marker.
- The most FDR-stable signals are XBP1 for GSE24080 24-month OS death and POU2AF1/XBP1/JCHAIN for GSE2658 1q21 amplification status.
- The manuscript route should therefore broaden from a single-gene TXNDC5 claim to a plasma-secretory clinical-subtype axis, then seek CoMMpass or another clinically annotated MM cohort for stronger validation.

## Outputs

- `analysis\bulk_clinical_validation\bulk_clinical_sample_scores.tsv`
- `analysis\bulk_clinical_validation\bulk_target_gene_expression.tsv`
- `analysis\bulk_clinical_validation\bulk_signature_scores.tsv`
- `analysis\bulk_clinical_validation\bulk_target_probe_mapping.tsv`
- `analysis\bulk_clinical_validation\bulk_outcome_association_results.tsv`
- `analysis\bulk_clinical_validation\bulk_validation_dataset_summary.tsv`
- `analysis\bulk_clinical_validation\GSE24080_efs_24mo_event_boxplots.png`
- `analysis\bulk_clinical_validation\GSE24080_os_24mo_event_boxplots.png`
- `analysis\bulk_clinical_validation\GSE2658_SURIND_boxplots.png`
- `analysis\bulk_clinical_validation\GSE2658_AMP_high_3plus_boxplots.png`

## Probe Mapping Note

- Target genes with at least one GPL570 probe selected: 35.
- Multi-probe genes were represented by the highest-variance probe within each dataset; this is appropriate for exploratory validation and should be described in Methods.
- FDR values were calculated within each dataset/outcome family for each statistical test type.
