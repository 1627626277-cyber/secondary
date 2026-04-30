# Project Review And Cleanup Plan

Date: 2026-04-30

## Review Scope

This review was performed after:

- repairing the NG2024 molecular-annotation figures;
- regenerating the manuscript evidence table and Fig. 1-5;
- integrating NG2024 and adjusted-model results into the manuscript draft;
- adding the requested Cox model: OS ~ plasma-secretory score + age + sex + ISS + 1q21.

## Editorial Status

Current judgment:

- The project is stronger than the previous review state.
- It is now a credible SCI Q2 public-data bioinformatics / translational oncology manuscript route.
- The previous second-spatial-cohort blocker has been materially reduced: GSE299193 Xenium validation is now complete and positive at the program level.
- It is not fully submission-ready yet because references, figure polish, and final claim-boundary checks still need to be completed.

Most important fixes completed:

- NG2024 no longer sits outside the manuscript package.
- The evidence table now includes public CoMMpass molecular-annotation support.
- Fig. 5 now includes CoMMpass/GDC, NG2024 molecular annotation and adjusted-model evidence.
- The NG2024 top plot now ranks by `-log10(FDR)` instead of mixing Kruskal H, Spearman rho and median differences on one effect-size axis.
- CoMMpass evidence now includes covariate-adjusted models.

## Current Claim That Can Be Defended

Defensible claim:

An MM bone marrow `plasma_secretory` spatial program is enriched in MM spatial transcriptomics, localizes to plasma-cell compartments in single-cell RNA-seq, is supported by external bulk cohorts, is associated with OS and ISS in CoMMpass/GDC, is linked to public NG2024 RNA-subtype and 1q21 annotations, and remains associated with OS after adjustment for age, sex, ISS and 1q21.

Do not claim:

- prospective clinical utility;
- complete PFS validation;
- treatment-response validation;
- direct R-ISS validation;
- wet-lab or mechanism validation;
- `TXNDC5` as a standalone independent prognostic biomarker.

## Updated Evidence State

Core evidence now complete:

- GSE269875 spatial discovery:
  - plasma-secretory signature enriched in MM vs control;
  - discovery-level because spatial n is small.
- GSE271107 single-cell localization:
  - plasma-secretory axis and TXNDC5 localize to marker-inferred plasma-cell compartment.
- GSE24080/GSE2658 bulk validation:
  - supports subtype/risk linkage, especially 1q21 and OS milestone signals.
- CoMMpass/GDC:
  - 762 baseline CD138+ RNA-seq samples;
  - OS and ISS association evidence.
- NG2024 public CoMMpass supplement:
  - Table 1 matched 762/762 local CoMMpass/GDC IDs;
  - Table 7 RNA subtype predictions matched 707 IDs;
  - plasma-secretory score associated with PR subtype probability and 1q21 call.
- Adjusted models:
  - OS adjusted for age, sex, ISS and 1q21:
    - plasma-secretory score HR `1.4596`, 95% CI `1.0690-1.9928`, FDR `0.0445`, n `660`, events `128`.

Completed after this review:

- GSE299193 Xenium second spatial cohort:
  - RAW tar reached the expected size `82,255,360,000` bytes.
  - 22 sample-level Xenium H5 matrices were analyzed.
  - `plasma_secretory_score_z` was higher in MM/RM than Ctrl/MGUS/SM samples: median delta `0.766`, FDR `0.000575`.
  - `POU2AF1/XBP1` panel-covered module was higher in MM/RM than Ctrl/MGUS/SM samples: median delta `1.068`, FDR `0.000575`.
  - Interpretation boundary: the Xenium panel lacks `TXNDC5`, `JCHAIN`, and `SDC1`; therefore GSE299193 supports program-level spatial validation, not direct TXNDC5/JCHAIN validation.

## Remaining Scientific Gaps

### Gap 1: Second Spatial Cohort

Status:

- Resolved as a major gap.
- GSE299193 is downloaded and first-pass Xenium validation is complete.

Why it matters:

- It directly addresses the small GSE269875 spatial discovery cohort.

Action:

- Completed:
  - `python scripts\17_gse299193_download_status.py`
  - `python scripts\18_gse299193_xenium_validation.py`
  - regenerated manuscript figures through `python scripts\15_build_manuscript_figures.py`.
- Fig. 6 and cross-cohort evidence-table rows were added.
- Panel limitation is now explicit in the validation report and manuscript.

### Gap 2: Formal Citations

Status:

- Manuscript still has reference anchors rather than a complete verified reference list.

Action:

- Replace reference anchors with verified primary literature and accession/source citations.
- Do not use textbooks, encyclopedias, blogs or low-quality papers as layout/scientific references.

### Gap 3: Single-Cell Malignancy Resolution

Status:

- GSE271107 validation uses marker-inferred cell categories.

Action:

- Keep the claim as plasma-cell compartment localization.
- Optional future enhancement: add author-annotated scRNA or infer malignant plasma cells if suitable data are available.

### Gap 4: Microarray Sensitivity

Status:

- GEO bulk validation uses probe-collapsed summaries.

Action:

- Optional before submission: add sensitivity using alternative probe handling for the few key genes.

### Gap 5: PFS / Treatment Response / R-ISS

Status:

- Not solved with current public/open tables.

Action:

- Preserve MMRF fuller clinical plan as future enhancement.
- Do not block Q2 route on this if GSE299193 validates or if the manuscript clearly states the limitation.

## File Classification

### Active Core Manuscript Assets

Keep in main working area:

- `reports\manuscript\MANUSCRIPT_MAIN_TEXT_DRAFT.md`
- `reports\manuscript\MANUSCRIPT_RESULTS_SKELETON.md`
- `reports\manuscript\FIGURE_LEGENDS_DRAFT.md`
- `analysis\manuscript_figures\cross_cohort_evidence_table.tsv`
- `analysis\manuscript_figures\fig1_study_design_evidence_chain.*`
- `analysis\manuscript_figures\fig2_spatial_plasma_secretory_discovery.*`
- `analysis\manuscript_figures\fig3_scrna_plasma_secretory_localization.*`
- `analysis\manuscript_figures\fig4_geo_bulk_clinical_support.*`
- `analysis\manuscript_figures\fig5_commppass_os_iss_validation.*`

### Active Analysis Scripts

Keep as current main pipeline:

- `scripts\08_processed_spatial_matrix_qc.py`
- `scripts\09_preliminary_spatial_clustering.py`
- `scripts\10_sample_aware_spatial_signatures.py`
- `scripts\11_gse271107_scrna_validation.py`
- `scripts\12_bulk_clinical_validation.py`
- `scripts\13_plasma_secretory_subtype_refinement.py`
- `scripts\14_commppass_gdc_validation.py`
- `scripts\15_build_manuscript_figures.py`
- `scripts\17_gse299193_download_status.py`
- `scripts\18_gse299193_xenium_validation.py`
- `scripts\19_skerget_ng2024_public_supplement_audit.py`
- `scripts\20_skerget_ng2024_molecular_annotation_validation.py`
- `scripts\21_commppass_ng2024_adjusted_models.py`
- `scripts\start_gse299193_download.ps1`

### Support / Provenance Assets

Keep, but do not treat as manuscript-active:

- `scripts\01_enrich_gse269875_manifest.py`
- `scripts\02_check_pilot_readiness.ps1`
- `scripts\03_pilot_hMM1_species_qc_template.ps1`
- `scripts\04_prepare_reference_genomes.py`
- `scripts\05_pilot_hMM1_magicblast_qc.ps1`
- `scripts\06_sample_fastq_pairs.py`
- `scripts\07_batch_remaining_human_species_qc.py`
- `qc_species_*`
- `sra_cache`
- `fastq`
- `tmp_fasterq`
- `references`
- `blastdb`
- `tools`
- `run_logs`

Reason:

- These establish species-QC and reproducibility provenance.
- They are no longer the manuscript main analysis focus.

### Future Optional Assets

Keep for possible MMRF access or fallback validation:

- `scripts\16_commppass_full_clinical_validation.py`
- `analysis\commppass_full_clinical_validation`
- `reports\planning\COMMPASS_FULL_CLINICAL_ACQUISITION_PLAN.md`
- `reports\validation\COMMPASS_FULL_CLINICAL_READINESS_REPORT.md`
- `reports\planning\SPATIAL_SAMPLE_EXPANSION_SEARCH_2026-04-30.md`

### Historical / Superseded Planning

Do not use as current project truth unless explicitly reviewing history:

- `reports\planning\UPDATED_COMPLETE_PROJECT_REPORT.md`
- `reports\planning\REVISED_Q2_PROJECT_PLAN.md`
- `reports\planning\EXTERNAL_VALIDATION_ROADMAP.md`
- `reports\planning\NEXT_STAGE_ACTION_PLAN.md`
- `reports\planning\NEXT_STEP_PILOT_RUNBOOK.md`
- original deep-research report copied into `reports\planning`

Recommendation:

- Later, move these into `reports\archive\planning_history\`.
- Do not move them while the project is actively downloading/analyzing unless scripts and logs are checked.

### Not For Manuscript Evidence

Keep only as audit/provenance:

- `reports\validation\USER_SUPPLIED_MMRF_TABLE_AUDIT.md`
- any pasted or roleplay-style MMRF tables not sourced from official MMRF/GDC/NG2024 files.

Reason:

- They are not valid controlled CoMMpass data.
- They must not enter analysis, tables, manuscript text or figures.

## Immediate Plan From Here

Priority 1:

- Formal citation cleanup and reference verification for all GEO/CoMMpass/NG2024 sources.

Priority 2:

- While downloading, polish manuscript wording and formal citations.

Priority 3:

- Review Fig. 6 layout and decide whether it remains a main figure or becomes a supplemental figure depending on final journal formatting limits.

Priority 4:

- Perform another focused manuscript review now that GSE299193 is integrated.

## Practical Judgment

The project should continue.

The Q2 route no longer depends on MMRF approval. MMRF would improve the paper, but the current public-data route has enough structure for a credible Q2 attempt if:

- GSE299193 provides program-level spatial reproducibility, with the explicit limitation that `TXNDC5`, `JCHAIN`, and `SDC1` are absent from the Xenium panel;
- citations are cleaned;
- claims stay bounded to association and public-data validation.
