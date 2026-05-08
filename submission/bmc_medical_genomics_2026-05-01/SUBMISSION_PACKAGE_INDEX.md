# Submission Package Index

Target journal: BMC Medical Genomics

Date started: 2026-05-01

Current status: pre-submission preparation in progress.

Latest internal gates:

- Stage 2.5 integrity verification passed with pre-submission action items on 2026-05-01.
- External Q2-style review hardening pass completed on 2026-05-01: spatial autocorrelation/neighborhood analysis, CoMMpass sensitivity models, module-coverage table, all-tested-association inventory, and Fig. 3/Fig. 8 were added.

## Primary Files

Main manuscript draft:

- `D:\二区\reports\manuscript\MANUSCRIPT_BMC_MEDICAL_GENOMICS_TARGET_DRAFT.md`

Editable submission DOCX:

- `D:\二区\submission\bmc_medical_genomics_2026-05-01\MANUSCRIPT_BMC_MEDICAL_GENOMICS_SUBMISSION_DRAFT.docx`

Cover letter DOCX:

- `D:\二区\submission\bmc_medical_genomics_2026-05-01\COVER_LETTER_DRAFT.docx`

Main Table 1:

- `D:\二区\submission\bmc_medical_genomics_2026-05-01\TABLE1_CROSS_COHORT_EVIDENCE_DRAFT.md`
- `D:\二区\submission\bmc_medical_genomics_2026-05-01\TABLE1_CROSS_COHORT_EVIDENCE_DRAFT.docx`

Supplementary methods and reproducibility appendix:

- `D:\二区\submission\bmc_medical_genomics_2026-05-01\SUPPLEMENTARY_METHODS_REPRODUCIBILITY_DRAFT.md`
- `D:\二区\submission\bmc_medical_genomics_2026-05-01\SUPPLEMENTARY_METHODS_REPRODUCIBILITY_DRAFT.docx`

Integrated reading-layout manuscript for author review:

- `D:\二区\submission\bmc_medical_genomics_2026-05-01\MM_spatial_plasma.docx`
- `D:\二区\submission\bmc_medical_genomics_2026-05-01\MM_spatial_plasma.pdf`

Note:

- The reading-layout manuscript embeds figures, Table 1, figure legends, declarations, and references in one continuous file for author review. It is not intended to replace the editable BMC submission DOCX unless the target journal specifically allows or requests a combined manuscript file.

## Figures

Main figure directory:

- `D:\二区\analysis\manuscript_figures`

Current planned main figures:

- Fig. 1: study design and evidence chain
- Fig. 2: GSE269875 spatial discovery
- Fig. 3: GSE269875 spatial organization
- Fig. 4: GSE299193 Xenium spatial reproducibility
- Fig. 5: GSE271107 single-cell localization
- Fig. 6: GSE24080/GSE2658 bulk support
- Fig. 7: CoMMpass/GDC retrospective clinical association and NG2024 molecular annotation
- Fig. 8: CoMMpass sensitivity analyses

Current figure/table decision:

- Fig. 3 remains a main figure because it directly addresses whether the spatial result has spatial organization beyond sample-level scoring.
- Fig. 4 remains a main figure because it directly addresses the second-spatial-cohort weakness.
- Fig. 8 remains a main figure because it directly addresses confounding-control critiques.
- The cross-cohort evidence table remains main Table 1 because it summarizes the evidence chain and claim boundaries.

## Submission Draft Components In This Folder

- `TITLE_PAGE_DRAFT.md`
- `DECLARATIONS_DRAFT.md`
- `COVER_LETTER_DRAFT.md`
- `DATA_AND_CODE_AVAILABILITY_DRAFT.md`
- `AUTHOR_AND_ORCID_STATUS.md`
- `EDITORIAL_QC_CHECKLIST.md`
- `PORTAL_METADATA_COPY_PASTE.md`
- `SUBMISSION_REMAINING_ITEMS_2026-05-01.md`
- `CITATION_AUDIT_STAGE1.md`
- `CITATION_AUDIT_STAGE2_FINAL.md`
- `TABLE1_CROSS_COHORT_EVIDENCE_DRAFT.md`
- `TABLE1_CROSS_COHORT_EVIDENCE_DRAFT.docx`
- `SUPPLEMENTARY_METHODS_REPRODUCIBILITY_DRAFT.md`
- `SUPPLEMENTARY_METHODS_REPRODUCIBILITY_DRAFT.docx`
- `MM_spatial_plasma.docx`
- `MM_spatial_plasma.pdf`
- `MANUSCRIPT_CELLS_STYLE_READING_VERSION_SOURCE.md`
- `MANUSCRIPT_BMC_MEDICAL_GENOMICS_SUBMISSION_DRAFT.docx`
- `COVER_LETTER_DRAFT.docx`

## New Review-Hardening Outputs

- `D:\二区\reports\validation\SPATIAL_AUTOCORRELATION_NICHE_ANALYSIS.md`
- `D:\二区\reports\validation\COMMPASS_SENSITIVITY_MODELS.md`
- `D:\二区\reports\validation\MODULE_COVERAGE_AND_TESTING_INVENTORY.md`
- `D:\二区\analysis\spatial_autocorrelation_niche\spatial_morans_i_results.tsv`
- `D:\二区\analysis\spatial_autocorrelation_niche\spatial_neighbor_enrichment_results.tsv`
- `D:\二区\analysis\commppass_sensitivity_models\commppass_os_sensitivity_models.tsv`
- `D:\二区\analysis\module_coverage_and_testing_inventory\module_gene_coverage_by_dataset.tsv`
- `D:\二区\analysis\module_coverage_and_testing_inventory\all_tested_association_inventory.tsv`
- `D:\二区\submission\bmc_medical_genomics_2026-05-01\SUPPLEMENTARY_TABLE_S1_MODULE_GENE_COVERAGE.tsv`
- `D:\二区\submission\bmc_medical_genomics_2026-05-01\SUPPLEMENTARY_TABLE_S2_ALL_TESTED_ASSOCIATIONS.tsv`
- `D:\二区\submission\bmc_medical_genomics_2026-05-01\SUPPLEMENTARY_TABLE_S3_COX_SENSITIVITY_MODELS.tsv`

## Reproducible Formatting Scripts

- `D:\二区\scripts\24_prepare_bmc_submission_package.py`
- `D:\二区\scripts\25_prepare_submission_table_and_supplement.py`
- `D:\二区\scripts\27_build_cells_style_reading_version.py`
- `D:\二区\scripts\31_build_review_hardening_figure.py`

These scripts regenerate the manuscript DOCX, cover-letter DOCX, Table 1 DOCX, supplementary methods DOCX, and integrated author-review DOCX from the current Markdown sources.

## GitHub Status

Local project folder:

- `D:\二区`

Remote:

- `https://github.com/1627626277-cyber/secondary`

Important note:

- Formal journal submission has not yet been performed.
- Git/GitHub synchronization is being completed for the current local submission package before final journal upload.

## Remaining Before Upload

1. Finalize the corresponding author name, email, and postal correspondence address.
2. Confirm the Word/WPS line numbers and page numbers display correctly in the regenerated main DOCX.
3. Confirm every uploaded figure maps to the correct figure number, including the new Fig. 3 and Fig. 8.
4. Confirm the GitHub repository URL opens publicly in a browser before final portal submission.
5. Confirm no claim says R-ISS, PFS, treatment-response validation, prospective classifier, independent prognostic biomarker, or clinical biomarker assay is completed.
