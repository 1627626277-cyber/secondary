# Next Stage Action Plan

Date: 2026-04-29

## Current Confirmed Finding

The current defensible manuscript claim is:

- An MM bone marrow `plasma_secretory` spatial program was discovered in spatial transcriptomics.
- The program was localized and supported by single-cell validation.
- The same axis was clinically supported in CoMMpass/GDC bulk RNA-seq by OS and ISS associations.

Current marker roles:

- `TXNDC5`: spatial and single-cell localization candidate within the axis.
- `POU2AF1`, `XBP1`, `JCHAIN`: clinical subtype / risk-linking module.
- `plasma_secretory_score_z`: strongest cross-layer axis score.

## Evidence Completed

Spatial discovery:

- GSE269875 human Visium processed matrices.
- Strongest spatial program: `plasma_secretory`.

Single-cell validation:

- GSE271107.
- `TXNDC5` is plasma-cell associated and highly detected in marker-inferred plasma cells.

GEO bulk clinical validation:

- GSE24080 and GSE2658.
- Supported subtype/risk association, especially `XBP1`, `POU2AF1`, and `JCHAIN`.

CoMMpass/GDC validation:

- 762 baseline visit-1 bone marrow CD138+ RNA-seq samples.
- 153 OS events.
- 742 samples with ISS stage.
- `plasma_secretory_score_z` vs OS event: FDR `9.31e-06`.
- `POU2AF1/XBP1/JCHAIN` clinical subtype module vs OS event: FDR `5.46e-05`.
- `plasma_secretory_score_z` vs ISS ordinal stage: FDR `0.0019`.
- `plasma_secretory_score_z` median-split OS log-rank: FDR `0.0401`.

## Confirmed Limitation

The current GDC open clinical slice does not provide enough usable fields for:

- R-ISS.
- PFS.
- detailed cytogenetic high-risk.
- treatment response.

Local data check:

- `analysis/commppass_gdc_validation/commppass_axis_clinical_scores.tsv` includes OS and ISS fields.
- The only progression-like merged field currently present is `diagnoses.0.progression_or_recurrence`, which is not usable because it is uniformly unknown in the inspected GDC clinical slice.

External data-access check:

- CoMMpass is a longitudinal MMRF genomic-clinical study and GDC is the source of truth for the open dataset.
- MMRF indicates CoMMpass and related datasets are shared through MMRF Virtual Lab.
- MMRFBiolinks documentation indicates fuller MMRF-RG workflows use local Researcher Gateway files including patient-clinical, treatment-response, and canonical-variants datasets; this requires authorized MMRF-RG access.

## Next Target

Primary next target:

- Consolidate the current analysis into manuscript-grade figures and tables.

Reason:

- The current result is already substantially stronger after CoMMpass/GDC validation.
- Waiting for fuller MMRF access may delay progress.
- The paper can be drafted around OS/ISS now, while R-ISS/PFS/treatment response are framed as pending optional expansion.

Secondary next target:

- Attempt to obtain fuller MMRF/CoMMpass clinical files for R-ISS, PFS, cytogenetics, and treatment-response validation.

Reason:

- These endpoints would further improve SCI Q2 competitiveness.
- They are not required to continue writing the current OS/ISS-supported manuscript route.

## Immediate Action Plan

Step 1: Build manuscript-grade result framework.

- Add a manuscript-consolidation script:
  - `scripts/15_build_manuscript_figures.py`.
- Create a cross-cohort evidence table:
  - spatial discovery;
  - scRNA cell-type localization;
  - GSE24080/GSE2658 clinical/subtype validation;
  - CoMMpass/GDC OS/ISS validation.
- Output:
  - `analysis/manuscript_figures/cross_cohort_evidence_table.tsv`.

Step 2: Generate final publication figure panels.

- Figure 1: study design and data flow.
- Figure 2: spatial discovery of `plasma_secretory` program.
- Figure 3: GSE271107 single-cell localization and `TXNDC5` plasma-cell specificity.
- Figure 4: GEO bulk subtype/risk support.
- Figure 5: CoMMpass/GDC OS and ISS validation.
- Output directory:
  - `analysis/manuscript_figures`.

Step 3: Write manuscript result skeleton.

- Draft Results section headings and claim boundaries.
- Explicitly state:
  - `TXNDC5` is not a standalone validated prognostic biomarker.
  - the validated clinical claim is for the broader `plasma_secretory` axis.
- Output:
  - `reports/manuscript/MANUSCRIPT_RESULTS_SKELETON.md`.

Step 4: Prepare fuller clinical-data acquisition checklist.

- Required data source:
  - MMRF Virtual Lab / Researcher Gateway.
- Required files:
  - patient-clinical table;
  - treatment-response table;
  - canonical variants / cytogenetic annotation table;
  - optional longitudinal follow-up table.
- Required endpoints:
  - R-ISS;
  - PFS;
  - high-risk cytogenetics;
  - treatment class and best overall response.
- Local target folder:
  - `external_bulk/CoMMpass_full_clinical`.

Step 5: If fuller clinical files are obtained, add a new script.

- Proposed script:
  - `scripts/16_commppass_full_clinical_validation.py`.
- Proposed outputs:
  - R-ISS association table;
  - PFS log-rank/Cox table;
  - cytogenetic high-risk association table;
  - treatment-response association table.

## Go / Pause Decision

Go now:

- Start manuscript-grade figure/table consolidation.

Parallel optional task:

- User can apply for or log into MMRF Virtual Lab / Researcher Gateway to obtain fuller clinical files.

Do not wait:

- Do not block the current manuscript route on R-ISS/PFS/treatment-response fields, because OS and ISS validation are already available and significant in CoMMpass/GDC.

## Source Links Checked

- AWS Open Data Registry for CoMMpass: https://registry.opendata.aws/mmrf-commpass/
- MMRF CoMMpass / Virtual Lab page: https://themmrf.org/finding-a-cure/personalized-treatment-approaches/
- GDC MMRF data portal update: https://gdc.cancer.gov/news-and-announcements/explore-mmrf-mutations-data-portal
- MMRFBiolinks paper: https://academic.oup.com/bib/article/22/5/bbab050/6209690
