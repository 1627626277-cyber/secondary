# Supplementary Methods And Reproducibility Appendix

Manuscript title:

Spatial validation and clinical association of a plasma-secretory bone marrow program in multiple myeloma

Target journal:

BMC Medical Genomics

Date:

2026-05-01

## Scope

This appendix documents the public data inputs, analysis scripts, score construction rules, complete-case handling, and figure-output traceability used for the manuscript.

The appendix is designed to support reproducibility. It does not add new claims beyond the main manuscript.

## Data Resources

| Resource | Role | Data type | Main inclusion rule | Main output directory |
|---|---|---|---|---|
| GSE269875 | Spatial discovery | Human bone marrow spatial transcriptomics | Processed human spatial matrices passing sample-level QC | `analysis/spatial_candidate_signatures` |
| GSE299193 | Second spatial validation | Human bone marrow Xenium spatial transcriptomics | Cell-feature matrices from Ctrl, MGUS, SM, MM, and RM samples | `analysis/gse299193_xenium_validation` |
| GSE271107 | Single-cell localization | Single-cell RNA-seq | Public single-cell expression data summarized by marker-inferred categories | `analysis/scrna_gse271107_validation` |
| GSE2658 | External bulk support | Bulk expression microarray | Samples with expression and available FISH 1q21 annotation | `analysis/plasma_secretory_subtype_refinement` |
| GSE24080 | External bulk support | Bulk expression microarray | Samples with expression and available milestone OS annotation | `analysis/bulk_clinical_validation` |
| MMRF-COMMPASS/GDC | Clinical bulk validation | Baseline CD138+ RNA-seq | Baseline visit-1 bone marrow CD138+ samples | `analysis/commppass_gdc_validation` |
| Skerget NG2024 public CoMMpass supplements | Molecular annotation | Public CoMMpass molecular annotation | Patient identifiers matched to local CoMMpass/GDC sample scores | `analysis/skerget_ng2024_public_supplement` |

## Script Order

| Step | Script | Purpose |
|---:|---|---|
| 1 | `scripts/08_processed_spatial_matrix_qc.py` | Check processed spatial matrices and sample-level QC fields. |
| 2 | `scripts/09_preliminary_spatial_clustering.py` | Generate preliminary spatial clustering and marker summaries. |
| 3 | `scripts/10_sample_aware_spatial_signatures.py` | Build sample-aware spatial program scores and candidate rankings. |
| 4 | `scripts/11_gse271107_scrna_validation.py` | Validate candidate localization in single-cell data. |
| 5 | `scripts/12_bulk_clinical_validation.py` | Score external bulk expression cohorts and test available endpoints. |
| 6 | `scripts/13_plasma_secretory_subtype_refinement.py` | Refine the POU2AF1/XBP1/JCHAIN clinical subtype module. |
| 7 | `scripts/14_commppass_gdc_validation.py` | Build CoMMpass/GDC baseline CD138+ RNA-seq validation tables. |
| 8 | `scripts/18_gse299193_xenium_validation.py` | Validate the program-level spatial signal in GSE299193 Xenium data. |
| 9 | `scripts/19_skerget_ng2024_public_supplement_audit.py` | Audit and inventory NG2024 public CoMMpass supplementary files. |
| 10 | `scripts/20_skerget_ng2024_molecular_annotation_validation.py` | Join NG2024 annotations to local CoMMpass scores and test molecular-risk associations. |
| 11 | `scripts/21_commppass_ng2024_adjusted_models.py` | Fit adjusted OS, subtype, and molecular-risk models. |
| 12 | `scripts/22_commppass_cox_ph_assumption_check.py` | Screen Cox proportional hazards assumptions with Schoenfeld residuals. |
| 13 | `scripts/15_build_manuscript_figures.py` | Generate Fig. 1-6 and the cross-cohort evidence table. |
| 14 | `scripts/24_prepare_bmc_submission_package.py` | Generate the editable manuscript DOCX and cover-letter DOCX. |

## Score Construction

For each cohort, expression values were analyzed on the processed normalized scale available from the public resource, or after log transformation where count-like matrices were used.

For gene-level module scores:

1. Candidate genes were intersected with platform-available genes.
2. Available gene values were standardized within the cohort.
3. Module scores were calculated as the arithmetic mean of available standardized genes.
4. Missing genes were not imputed.
5. If no genes from a module were present, that module was not scored for that sample or platform.

Primary biological scores:

| Score | Genes or construct | Main use |
|---|---|---|
| Plasma-secretory score | Plasma-cell and secretory-pathway program genes available per platform | Main spatial, bulk, and CoMMpass axis |
| Clinical subtype module | POU2AF1, XBP1, JCHAIN where available | Clinical subtype and risk association support |
| Xenium panel-covered module | POU2AF1 and XBP1 | GSE299193 panel-compatible validation |
| TXNDC5 expression | TXNDC5 | Spatial/single-cell localization candidate |

## Dataset-Specific Notes

### GSE269875

Processed human bone marrow spatial matrices were used for discovery. Curated marrow and immune programs included plasma-secretory, myeloid-inflammatory, T/NK cytotoxic, stromal, endothelial, erythroid, and cycling states. Scores were summarized at sample level before MM-control comparison.

Main statistics reported:

- Median difference.
- Cohen's d.
- Mann-Whitney p value.

### GSE299193

The raw Xenium archive was not fully extracted. The validation script extracted only cell-feature matrices and lightweight metadata needed for gene-panel scoring. This avoided unnecessary expansion of imaging and transcript-position files.

Disease grouping:

- Active disease: MM and relapsed MM.
- Non-active comparison: Ctrl, MGUS, and SM.

Interpretation boundary:

- GSE299193 validates the program-level spatial signal.
- It does not directly validate TXNDC5, JCHAIN, or SDC1 because these genes were absent from the extracted Xenium matrices.

### GSE271107

Single-cell RNA-seq data were summarized by marker-inferred cell categories. The primary endpoint was whether candidate genes and module scores localized to plasma-cell compartments. Detection fraction was calculated as the fraction of observations with expression above zero.

Interpretation boundary:

- This supports localization.
- It does not establish TXNDC5 as a standalone prognostic biomarker.

### GSE2658 And GSE24080

External GEO bulk cohorts were used to test whether the spatially discovered axis related to available clinical or cytogenetic annotations outside the spatial datasets.

Endpoints:

- GSE2658: FISH 1q21 amplification.
- GSE24080: 24-month overall survival death.

Interpretation boundary:

- These data support external association.
- They do not establish uniform directional replication across all platforms.

### CoMMpass/GDC

MMRF-COMMPASS/GDC RNA-seq files were filtered to baseline visit-1 bone marrow CD138+ samples. The final validation table contained 762 baseline samples. Gene-level TPM values were log-transformed and z-scored before module scoring.

Endpoints:

- Overall survival event.
- ISS ordinal stage.
- Median-split overall survival.

Interpretation boundary:

- These analyses support retrospective clinical association.
- They do not complete R-ISS, PFS, or treatment-response validation.

### NG2024 Public CoMMpass Annotation

Public Skerget et al. NG2024 supplementary tables were joined to local CoMMpass/GDC scores by patient identifier. Supplementary Table 1 matched all 762 local baseline samples. RNA-subtype probability analyses used complete cases; the PR subtype analysis contained 707 complete samples.

Molecular annotations tested:

- PR RNA-subtype probability.
- 1q21 gain or amplification.
- 17p13 deletion.
- RNA-subtype categories.
- Cytogenetic high-risk annotations available in the public supplement.

## Complete-Case Rules

Complete-case analysis was performed separately for each endpoint.

Examples:

| Analysis | Required fields |
|---|---|
| OS event association | Score, OS event |
| ISS association | Score, ISS stage |
| Median-split OS | Score, OS time, OS event |
| Adjusted Cox model | Score, age, sex, ISS stage, 1q21 status, OS time, OS event |
| PR subtype probability | Score, PR probability, age, sex, ISS stage where adjusted |
| 1q21 logistic model | Score, 1q21 status, age, sex, ISS stage |

Sample numbers therefore differ between endpoint families. The manuscript reports denominators when they are central to interpretation.

## Multiple Testing

Benjamini-Hochberg FDR correction was applied within analysis families rather than across all analyses in the project.

Analysis families:

1. Spatial discovery program comparisons.
2. GSE299193 Xenium program and panel-covered gene comparisons.
3. Single-cell localization summaries.
4. External GEO bulk associations.
5. CoMMpass/GDC clinical associations.
6. NG2024 molecular annotation associations.
7. Adjusted CoMMpass/NG2024 model families.
8. Cox PH diagnostic screen.

## Cox Proportional Hazards Diagnostic

The primary adjusted Cox model included age, sex, ISS stage, and 1q21 status. Schoenfeld residual correlations with log event time were used as a diagnostic screen.

Primary score terms:

- Plasma-secretory score: rho=-0.0637, p=0.475, FDR=0.778.
- POU2AF1/XBP1/JCHAIN module: rho=-0.0585, p=0.512, FDR=0.789.

The 1q21 covariate showed time-related residual structure in adjusted models. Therefore, Cox results are reported as retrospective adjusted association models, not prospective risk-prediction models.

## Figure Traceability

| Figure | Primary script | Primary output files |
|---|---|---|
| Fig. 1 | `scripts/15_build_manuscript_figures.py` | `analysis/manuscript_figures/fig1_study_design_evidence_chain.*` |
| Fig. 2 | `scripts/10_sample_aware_spatial_signatures.py`; `scripts/15_build_manuscript_figures.py` | `analysis/manuscript_figures/fig2_spatial_plasma_secretory_discovery.*` |
| Fig. 3 | `scripts/11_gse271107_scrna_validation.py`; `scripts/15_build_manuscript_figures.py` | `analysis/manuscript_figures/fig3_scrna_plasma_secretory_localization.*` |
| Fig. 4 | `scripts/12_bulk_clinical_validation.py`; `scripts/13_plasma_secretory_subtype_refinement.py`; `scripts/15_build_manuscript_figures.py` | `analysis/manuscript_figures/fig4_geo_bulk_clinical_support.*` |
| Fig. 5 | `scripts/14_commppass_gdc_validation.py`; `scripts/20_skerget_ng2024_molecular_annotation_validation.py`; `scripts/21_commppass_ng2024_adjusted_models.py`; `scripts/15_build_manuscript_figures.py` | `analysis/manuscript_figures/fig5_commppass_os_iss_validation.*` |
| Fig. 6 | `scripts/18_gse299193_xenium_validation.py`; `scripts/15_build_manuscript_figures.py` | `analysis/manuscript_figures/fig6_gse299193_xenium_spatial_validation.*` |

Each figure is available as PNG, PDF, and SVG in `analysis/manuscript_figures`.

## Claim Boundaries

The current manuscript supports:

- Spatial discovery of a plasma-secretory bone marrow program.
- Independent program-level spatial validation in GSE299193.
- Plasma-cell localization in single-cell data.
- External bulk support for a clinical subtype/risk axis.
- Retrospective CoMMpass/GDC and NG2024 clinical/molecular associations.

The current manuscript does not claim:

- A standalone clinical biomarker.
- A prospective classifier.
- Treatment-selection utility.
- Completed R-ISS validation.
- Completed PFS validation.
- Completed treatment-response validation.
- Direct GSE299193 validation of TXNDC5, JCHAIN, or SDC1.
