# Q2 Review Revision Response

Date: 2026-05-01

Status: implemented in manuscript source, submission metadata, Table 1, supplementary methods, and figure legends.

## Summary Decision

The manuscript was revised according to a major-revision strategy. The central claim is now:

> A spatially reproducible plasma-secretory bone marrow program linked to PR/proliferation/1q21 molecular-risk context in multiple myeloma.

The manuscript no longer frames the program as an independent clinical biomarker or completed clinical validation result.

## Implemented Major Changes

1. Innovation framing was narrowed.

The title was changed to "A spatially reproducible plasma-secretory bone marrow program linked to molecular risk in multiple myeloma". The Background and Discussion now state that plasma-cell biology itself is not novel and that the contribution is cross-platform spatial reproducibility plus molecular-risk contextualization.

2. Spatial depth was strengthened.

Added `scripts/28_spatial_autocorrelation_niche_analysis.py`.

Outputs:

- `analysis/spatial_autocorrelation_niche/spatial_morans_i_results.tsv`
- `analysis/spatial_autocorrelation_niche/spatial_neighbor_enrichment_results.tsv`
- `reports/validation/SPATIAL_AUTOCORRELATION_NICHE_ANALYSIS.md`

Key result: plasma-secretory Moran's I was FDR-significant in 9 of 9 GSE269875 samples, with median Moran's I 0.477. Plasma-secretory-high spots had enriched neighboring plasma-cell marker, stromal ECM, endothelial, myeloid, and immune scores.

3. Confounding and sensitivity models were added.

Added `scripts/29_commppass_sensitivity_models.py`.

Outputs:

- `analysis/commppass_sensitivity_models/commppass_os_sensitivity_models.tsv`
- `analysis/commppass_sensitivity_models/commppass_1q21_sensitivity_models.tsv`
- `reports/validation/COMMPASS_SENSITIVITY_MODELS.md`

Key result: the basic OS model remained associated after age, sex, ISS, and 1q21 adjustment (HR 1.460, FDR=0.0485), but the association attenuated after PR probability and proliferation adjustment (HR 1.150, FDR=0.444). The manuscript now interprets this as molecular-risk-context association rather than an independent prognostic biomarker.

4. Module coverage and all-tested-association transparency were added.

Added and corrected `scripts/30_module_coverage_and_testing_inventory.py`.

Outputs:

- `analysis/module_coverage_and_testing_inventory/module_gene_coverage_by_dataset.tsv`
- `analysis/module_coverage_and_testing_inventory/all_tested_association_inventory.tsv`
- `reports/validation/MODULE_COVERAGE_AND_TESTING_INVENTORY.md`

Key coverage notes: GSE269875 and GSE271107 lack POU2AF1 for the defined module; GSE299193 lacks TXNDC5, JCHAIN, and SDC1. The manuscript explicitly frames GSE299193 as program-level reproducibility rather than gene-level validation.

5. Figure package was updated.

Added `scripts/31_build_review_hardening_figure.py` and generated:

- `analysis/manuscript_figures/fig7_spatial_and_sensitivity_hardening.png`
- `analysis/manuscript_figures/fig7_spatial_and_sensitivity_hardening.pdf`
- `analysis/manuscript_figures/fig7_spatial_and_sensitivity_hardening.svg`

Fig. 7 directly addresses the spatial-organization and Cox-confounding critiques.

6. Single-cell wording was tightened.

The Methods now report QC thresholds and cell counts: minimum 200 genes, minimum 500 counts, maximum 25% mitochondrial reads; 143,748 raw cells and 127,528 post-QC cells across 19 samples. The Results and Discussion now state that the data support plasma-cell compartment localization and do not establish malignant-plasma-cell-specific localization.

7. GSE2658 inconsistency was addressed.

The Results and Discussion now explicitly discuss possible reasons for direction inconsistency: platform differences, sample composition, FISH cutoff differences, therapy-era effects, expression-platform normalization, and incomplete module-gene coverage equivalence.

## Files Updated

- `reports/manuscript/MANUSCRIPT_BMC_MEDICAL_GENOMICS_TARGET_DRAFT.md`
- `reports/manuscript/FIGURE_LEGENDS_DRAFT.md`
- `submission/bmc_medical_genomics_2026-05-01/TITLE_PAGE_DRAFT.md`
- `submission/bmc_medical_genomics_2026-05-01/TABLE1_CROSS_COHORT_EVIDENCE_DRAFT.md`
- `submission/bmc_medical_genomics_2026-05-01/SUPPLEMENTARY_METHODS_REPRODUCIBILITY_DRAFT.md`
- `submission/bmc_medical_genomics_2026-05-01/PORTAL_METADATA_COPY_PASTE.md`
- `submission/bmc_medical_genomics_2026-05-01/DATA_AND_CODE_AVAILABILITY_DRAFT.md`
- `submission/bmc_medical_genomics_2026-05-01/DECLARATIONS_DRAFT.md`
- `submission/bmc_medical_genomics_2026-05-01/COVER_LETTER_DRAFT.md`

## Remaining Risks

- The project still does not include private fuller MMRF clinical tables, so R-ISS, PFS, and treatment-response validation remain incomplete.
- The spatial neighborhood analysis is exploratory and not histology-anchored niche segmentation.
- CoMMpass low-purity and CMMC are public proxies and do not replace direct flow cytometry or histology-based tumor-content measurement.
- The manuscript remains suitable for a cautious Q2 submission strategy after regenerated DOCX/QC, not for an overclaimed biomarker-discovery submission.
