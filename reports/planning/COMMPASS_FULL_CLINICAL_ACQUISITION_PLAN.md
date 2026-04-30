# CoMMpass Fuller Clinical Acquisition Plan

Date: 2026-04-29

## Purpose

The current manuscript has completed OS and ISS validation using the open GDC MMRF-COMMPASS clinical slice. The following endpoints are not complete:

- R-ISS.
- PFS.
- detailed cytogenetic high-risk.
- treatment response.

These require fuller MMRF/CoMMpass clinical files from MMRF Virtual Lab / Researcher Gateway or equivalent authorized CoMMpass releases.

## Evidence From Official / Primary Sources

MMRF Virtual Lab documentation states that Virtual Lab integrates clinical, genomic, and multi-omic data and allows data access/download for harmonized datasets. It lists CoMMpass as longitudinal genomic and clinical data from newly diagnosed MM patients.

MMRF CoMMpass Clinical Data Overview states that the clinical dataset includes diagnostic and disease characteristics, Cytogenetics/FISH, initial therapy regimens, response and relapse documentation, subsequent therapy lines, response assessments, progression/relapse dates, PFS, OS, and time-to-event variables.

MMRF Interim Analysis documentation states that IA24 is the final comprehensive release and that Repository filters can identify Summary Data Files and Clinical Data Tables. Filtered results may include harmonized clinical data tables such as labs, treatments, and outcomes.

MMRFBiolinks documentation states that GDC clinical information is only a subset of clinical information downloaded directly from MMRF-CoMMpass Researcher Gateway, and gives `MMRF_CoMMpass_IA14_STAND_ALONE_TRTRESP.csv` as an example treatment-response file.

Primary CoMMpass high-risk work in Blood Cancer Journal used CoMMpass data layers including canonical Ig translocations, CNA segmentation, treatment response, ISS, and disease progression/survival data to define genomic and functional high-risk groups. This supports the feasibility of the proposed enhanced analyses if fuller files are obtained.

## Files To Obtain

Place all downloaded files under:

- `external_bulk/CoMMpass_full_clinical`

Priority files:

1. Patient-level aggregate clinical table
   - needed for ISS/R-ISS components, baseline labs, demographics, diagnosis date, follow-up.
2. Survival / progression table
   - needed for PFS, progression date, relapse date, treatment-change date, OS cross-check.
3. Treatment-response table
   - needed for best overall response, first-line response, refractory status.
   - expected legacy example: `MMRF_CoMMpass_IA14_STAND_ALONE_TRTRESP.csv`.
4. Treatment regimen / therapy line table
   - needed for first-line regimen, treatment class, transplant, line assignment.
5. Cytogenetics / FISH table
   - needed for del17p, t(4;14), t(14;16), 1q gain/amplification.
6. Canonical variants / copy-number / seqFISH summary table
   - needed if clinical FISH is incomplete.
7. Sample manifest / molecular metadata
   - needed to link patient IDs to baseline RNA-seq samples already used in the project.

## Endpoint Construction Plan

R-ISS:

- Required components:
  - ISS stage;
  - LDH status or LDH value with institutional upper limit if available;
  - high-risk cytogenetics: del17p, t(4;14), t(14;16).
- Analysis:
  - compare `plasma_secretory_score_z` across R-ISS I/II/III;
  - test R-ISS III vs I/II;
  - optionally fit ordinal or multinomial models if sample size is adequate.

PFS:

- Required components:
  - baseline date;
  - progression / relapse / death date;
  - last follow-up date;
  - event indicator.
- Analysis:
  - median-split Kaplan-Meier;
  - log-rank test;
  - Cox proportional hazards model;
  - optional adjustment for age, sex, ISS/R-ISS, and high-risk cytogenetics.

Cytogenetic high-risk:

- Required components:
  - del17p;
  - t(4;14);
  - t(14;16);
  - 1q gain/amplification;
  - optional TP53 biallelic inactivation if mutation/CNA data are available.
- Analysis:
  - high-risk vs standard-risk association;
  - feature-specific association;
  - compare plasma-secretory and POU2AF1/XBP1/JCHAIN module scores.

Treatment response:

- Required components:
  - first-line regimen or therapy class;
  - best overall response;
  - CR/VGPR/PR/SD/PD or derived response grouping;
  - refractory status if available.
- Analysis:
  - responder vs non-responder association;
  - deep response CR/VGPR vs lower response;
  - treatment-class stratified analysis if sample size permits.

## How To Run After Files Are Added

1. Put downloaded CSV/TSV/XLSX files into:
   - `external_bulk/CoMMpass_full_clinical`
2. Run:
   - `python scripts/16_commppass_full_clinical_validation.py`
3. Inspect:
   - `analysis/commppass_full_clinical_validation/full_clinical_inventory.tsv`
   - `analysis/commppass_full_clinical_validation/endpoint_candidate_columns.tsv`
   - `reports/validation/COMMPASS_FULL_CLINICAL_READINESS_REPORT.md`
4. If candidate fields are found, implement harmonization with:
   - `analysis/commppass_gdc_validation/commppass_axis_clinical_scores.tsv`

## Current Status

Current local scan:

- `external_bulk/CoMMpass_full_clinical` contains no fuller clinical files.
- Therefore R-ISS, PFS, detailed cytogenetic high-risk, and treatment-response analyses are not yet executable.

Current project decision:

- Continue manuscript writing using the completed spatial + scRNA + GEO bulk + CoMMpass OS/ISS evidence chain.
- Treat fuller clinical validation as an enhancement, not a blocker.

## Source Links

- MMRF Virtual Lab documentation: https://themmrf.github.io/docs-vlab/
- CoMMpass Clinical Data Overview: https://themmrf.github.io/docs-vlab/mmrf-resources/mmrf-commpass/clinical-overview/
- CoMMpass Interim Analysis access: https://themmrf.github.io/docs-vlab/mmrf-resources/mmrf-commpass/historic-ia/
- MMRFBiolinks clinical vignette: https://rdrr.io/github/marziasettino/MMRFBiolinks/f/vignettes/Clinical.Rmd
- Blood Cancer Journal CoMMpass high-risk example: https://www.nature.com/articles/s41408-021-00576-3

