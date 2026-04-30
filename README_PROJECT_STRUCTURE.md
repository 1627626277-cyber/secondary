# Project Structure

Date: 2026-04-29

This folder contains a pure public-data bioinformatics / translational data-analysis project for multiple myeloma bone marrow spatial transcriptomics.

No wet-lab experiment is planned or required for the current manuscript route.

## Current Manuscript Route

Target route:

1. Spatial discovery: `GSE269875` human Visium bone marrow spatial transcriptomics.
2. Single-cell validation: `GSE271107` and later optional `GSE223060`.
3. Bulk / clinical transcriptomic validation: completed first-pass `GSE24080`/`GSE2658` validation and CoMMpass/GDC OS/ISS validation.
4. Public CoMMpass molecular-risk annotation: Skerget et al. Nature Genetics 2024 supplementary-table download/audit, first-pass validation, and adjusted model validation completed.
5. External spatial validation: `GSE299193` completed as the main second-spatial-cohort validation.

Current manuscript direction:

- Spatial discovery + single-cell validation + bulk clinical validation support an MM bone marrow `plasma_secretory` clinical-subtype axis.
- `TXNDC5` is retained as a spatial/single-cell localization candidate within this axis.
- `POU2AF1`, `XBP1`, and `JCHAIN` are prioritized for clinical subtype / risk-association analysis.
- CoMMpass/GDC supports the axis with OS-event and ISS-stage associations.
- GSE299193 independently supports program-level spatial reproducibility, with `plasma_secretory_score_z` higher in MM/RM than Ctrl/MGUS/SM samples.

Current key risk:

- Plasma-cell biology alone is expected in MM. Direct clinical-outcome support for `TXNDC5` is weak, so the manuscript should not be framed as a single-gene `TXNDC5` prognostic paper.
- SCI Q2 competitiveness is now improved by CoMMpass/GDC validation.
- R-ISS, PFS, and treatment-response validation still require fuller MMRF/CoMMpass clinical files or another curated clinical cohort.
- Detailed cytogenetic and molecular-risk annotation may be partly replaced by the public Skerget et al. Nature Genetics 2024 CoMMpass supplementary tables if ID matching works.
- Current ID matching works: Table 1 matches 762/762 CoMMpass/GDC samples and Table 7 RNA subtype predictions match 707 samples.
- The original spatial discovery sample-size issue is now partly mitigated by GSE299193 Xenium validation.
- GSE299193 does not directly validate `TXNDC5`, `JCHAIN`, or `SDC1` because these genes are absent from the extracted Xenium feature matrices.

## Root Files

- `PROJECT_LOG.md`: chronological project log; keep this at root.
- `README_PROJECT_STRUCTURE.md`: this project map.
- `gse269875_manifest_enriched.tsv`: GSE269875 metadata manifest used by earlier workflow.
- `gse269875_human_species_qc_summary.tsv`: human species QC summary.
- `gse269875_processed_matrix_inventory.tsv`: processed Visium matrix inventory.
- `species_filter_log.md`: species QC notes.
- `species_qc_remaining_human_summary.tsv`: species QC summary for remaining human samples.
- `sample_manifest.tsv`: early sample manifest.
- `GSE269875_family.soft.gz`: GEO family metadata.
- `hg38.fa`, `mm10.fa`: local reference FASTA files used for species checks.

## Main Directories

- `reports/`: project reports and planning documents.
- `scripts/`: executable analysis scripts.
- `analysis/`: generated analysis outputs.
- `geo_processed/`: downloaded and extracted GSE269875 processed spatial files.
- `external_scRNA/`: downloaded external single-cell validation data.
- `external_bulk/`: downloaded external bulk expression and GPL570 annotation files.
- `sra_cache/`: downloaded SRA files used for sequence-level QC.
- `qc_species_*`: per-sample sampled species-QC working directories.
- `references/`, `blastdb/`: reference FASTA and BLAST/Magic-BLAST databases.
- `tools/`: Windows-native external command-line tools.
- `run_logs/`: command run logs.
- `downloads/`, `fastq/`, `tmp_fasterq/`: download and temporary processing locations.
- `数据治理与元数据锚定/`: earlier project context supplied by the user.

## Reports

Planning:

- `reports/planning/deep-research-report (2) (1) (1).md`
- `reports/planning/UPDATED_COMPLETE_PROJECT_REPORT.md`
- `reports/planning/REVISED_Q2_PROJECT_PLAN.md`
- `reports/planning/PROJECT_NOVELTY_AND_RISK_REVIEW.md`
- `reports/planning/EXTERNAL_VALIDATION_ROADMAP.md`
- `reports/planning/NEXT_STAGE_ACTION_PLAN.md`
- `reports/planning/COMMPASS_FULL_CLINICAL_ACQUISITION_PLAN.md`
- `reports/planning/REMAINING_GAPS_STATUS_AUDIT.md`
- `reports/planning/Q2_NO_MMRF_MAINLINE_PLAN.md`
- `reports/planning/PUBLIC_COMMPASS_NG2024_SUPPLEMENT_PLAN.md`
- `reports/planning/SPATIAL_SAMPLE_EXPANSION_SEARCH_2026-04-30.md`
- `reports/planning/NEXT_STEP_PILOT_RUNBOOK.md`

Setup:

- `reports/setup/ENVIRONMENT_SETUP_NOTES.md`

Spatial analysis:

- `reports/analysis/SPATIAL_MATRIX_QC_REPORT.md`
- `reports/analysis/PRELIMINARY_SPATIAL_CLUSTERING_REPORT.md`
- `reports/analysis/SPATIAL_SIGNATURE_DISCOVERY_REPORT.md`

Single-cell validation:

- `reports/validation/SCRNA_GSE271107_VALIDATION_REPORT.md`

Bulk / clinical validation:

- `reports/validation/BULK_CLINICAL_VALIDATION_REPORT.md`
- `reports/validation/PLASMA_SECRETORY_SUBTYPE_REFINEMENT_REPORT.md`
- `reports/validation/COMMPASS_GDC_VALIDATION_REPORT.md`
- `reports/validation/COMMPASS_FULL_CLINICAL_READINESS_REPORT.md`
- `reports/validation/SKERGET_NG2024_PUBLIC_SUPPLEMENT_AUDIT.md`
- `reports/validation/SKERGET_NG2024_MOLECULAR_ANNOTATION_VALIDATION_REPORT.md`
- `reports/validation/COMMPASS_NG2024_ADJUSTED_MODEL_REPORT.md`
- `reports/validation/GSE299193_XENIUM_DOWNLOAD_STATUS.md`
- `reports/validation/GSE299193_XENIUM_VALIDATION_REPORT.md`

Manuscript drafts:

- `reports/manuscript/MANUSCRIPT_MAIN_TEXT_DRAFT.md`
- `reports/manuscript/MANUSCRIPT_RESULTS_SKELETON.md`
- `reports/manuscript/FIGURE_LEGENDS_DRAFT.md`
- `reports/manuscript/FIGURE_DESIGN_REFERENCE_NOTE.md`
- `reports/manuscript/MANUSCRIPT_FORMAT_REFERENCE_NOTE.md`

## Scripts

- `scripts/07_batch_remaining_human_species_qc.py`: sampled species QC.
- `scripts/08_processed_spatial_matrix_qc.py`: processed Visium matrix QC.
- `scripts/09_preliminary_spatial_clustering.py`: first-pass spatial clustering and module scores.
- `scripts/10_sample_aware_spatial_signatures.py`: sample-aware spatial signature discovery and candidate ranking.
- `scripts/11_gse271107_scrna_validation.py`: GSE271107 single-cell validation.
- `scripts/12_bulk_clinical_validation.py`: GSE24080/GSE2658 bulk clinical validation.
- `scripts/13_plasma_secretory_subtype_refinement.py`: refined plasma-secretory clinical subtype-axis analysis.
- `scripts/14_commppass_gdc_validation.py`: CoMMpass/GDC open RNA-seq OS/ISS validation.
- `scripts/15_build_manuscript_figures.py`: manuscript-grade cross-cohort evidence table, Fig. 1-5, figure legends, and Results skeleton.
- `scripts/16_commppass_full_clinical_validation.py`: readiness scanner for fuller MMRF clinical R-ISS, PFS, cytogenetic high-risk, and treatment-response files.
- `scripts/17_gse299193_download_status.py`: GSE299193 SOFT metadata parser and download progress reporter.
- `scripts/start_gse299193_download.ps1`: resumable background curl download launcher for `GSE299193_RAW.tar`.
- `scripts/18_gse299193_xenium_validation.py`: post-download Xenium matrix extraction and plasma-secretory validation workflow.
- `scripts/19_skerget_ng2024_public_supplement_audit.py`: public CoMMpass NG2024 supplement download/audit and ID-matching workflow.
- `scripts/20_skerget_ng2024_molecular_annotation_validation.py`: molecular-risk annotation validation using public NG2024 CoMMpass features.
- `scripts/21_commppass_ng2024_adjusted_models.py`: adjusted CoMMpass/GDC + NG2024 Cox, logistic, and linear models.

## Analysis Outputs

- `analysis/spatial_qc/`: matrix QC outputs.
- `analysis/spatial_preliminary/`: first-pass spatial clustering outputs.
- `analysis/spatial_candidate_signatures/`: sample-aware signature and candidate gene outputs.
- `analysis/scrna_gse271107_validation/`: GSE271107 scRNA validation outputs.
- `analysis/bulk_clinical_validation/`: GSE24080/GSE2658 bulk clinical validation outputs.
- `analysis/plasma_secretory_subtype_refinement/`: subtype module analysis and publication-oriented exploratory figures.
- `analysis/commppass_gdc_validation/`: CoMMpass/GDC validation outputs.
- `analysis/manuscript_figures/`: manuscript-grade cross-cohort evidence table and Fig. 1-5 in PNG/SVG/PDF.
- `analysis/commppass_full_clinical_validation/`: fuller clinical file inventory and endpoint-column scan outputs.
- `analysis/gse299193_xenium_validation/`: GSE299193 sample manifest, download status, extracted Xenium matrix validation outputs, and program-level association results.
- `analysis/skerget_ng2024_public_supplement/`: public CoMMpass NG2024 molecular-annotation audit and validation outputs.
- `analysis/commppass_ng2024_adjusted_models/`: adjusted model outputs that test OS, ISS, cytogenetic/molecular-risk, 1q21/17p13, and PR subtype associations after covariate adjustment.

## What Not To Move Casually

Do not casually move these directories unless scripts are updated accordingly:

- `analysis/`
- `geo_processed/`
- `external_scRNA/`
- `scripts/`
- `sra_cache/`
- `qc_species_*`
- `references/`
- `blastdb/`

These paths are used by the current workflow and logs.

## Next Recommended Scientific Step

The current scientific step is manuscript polishing and final quality control, not wet-lab work.

Recommended next route:

1. Polish formal citations and manuscript claim-boundary wording.
2. Decide whether Fig. 6 remains a main figure or becomes supplementary after target-journal formatting is selected.
3. Run a focused reviewer-style critique of the updated manuscript package.
4. Keep fuller MMRF/CoMMpass clinical access as a future enhancement for R-ISS, PFS, and treatment-response validation.
5. Inspect GSE284727 only if final review requires another spatial dataset beyond GSE299193.

Reason:

- The current spatial, second-spatial, and scRNA evidence supports plasma-secretory biology.
- CoMMpass/GDC now supports the broader `plasma_secretory` axis with OS and ISS associations.
- Cytogenetic and molecular-risk validation is now partially solved through public CoMMpass NG2024 supplementary tables and adjusted CoMMpass/NG2024 models.
- GSE299193 materially reduces the second-spatial-validation weakness, but it is program-level rather than TXNDC5/JCHAIN-specific because of Xenium panel coverage.
- R-ISS, PFS, and treatment-response validation remain optional expansion items that require fuller MMRF/CoMMpass clinical files or another curated clinical cohort.
