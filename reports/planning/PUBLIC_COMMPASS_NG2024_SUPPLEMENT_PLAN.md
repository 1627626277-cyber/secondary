# Public CoMMpass NG2024 Supplement Plan

Date: 2026-04-29

## Route Decision

Add a low-cost public CoMMpass molecular-annotation validation line to the Q2 manuscript route.

This line is based on Skerget et al., Nature Genetics 2024, "Comprehensive molecular profiling of multiple myeloma identifies refined copy number and expression subtypes."

This does not replace fuller MMRF clinical access for PFS or treatment response, but it can replace part of the missing molecular annotation layer.

## Why This Matters

The current project already has:

- spatial discovery in GSE269875;
- single-cell localization in GSE271107;
- GEO bulk validation in GSE24080 and GSE2658;
- CoMMpass/GDC open RNA-seq OS and ISS validation in 762 baseline CD138+ samples;
- GSE299193 identified as a second public MM bone marrow spatial validation dataset.

The public Skerget et al. supplement is valuable because it can add:

- larger CoMMpass patient-level context;
- ISS and baseline laboratory context;
- copy-number and cytogenetic annotation;
- 1q21, 17p13, 13q14, hyperdiploid and translocation calls;
- RNA expression subtype labels;
- somatic mutation and structural-event annotation if the larger tables are parsed.

This directly improves the Q2 route by strengthening the "clinical molecular risk" layer without waiting for MMRF approval.

## What It Can Support

Primary use:

- test whether the existing `plasma_secretory_score_z` and `POU2AF1/XBP1/JCHAIN` module align with public CoMMpass molecular risk annotations after ID matching;
- test association with cytogenetic high-risk labels, 1q21 gain/amplification, 17p13 deletion, 13q14 deletion, hyperdiploidy and RNA subtypes;
- add a public molecular-annotation validation table or supplementary figure;
- improve Discussion and limitation handling by comparing our axis with a Nature Genetics-defined CoMMpass molecular subtype framework.

Secondary use:

- parse mutation tables for TP53, KRAS, NRAS, BRAF, DIS3 and TENT5C/FAM46C;
- parse structural-event tables for IGH-related translocation support;
- use expression subtype classifier output to position the plasma-secretory axis relative to established MM expression subtypes.

## What It Cannot Support

Do not use this public supplement to claim the following unless the actual downloaded tables contain verified fields:

- completed PFS validation;
- treatment-response validation;
- best overall response validation;
- line-of-therapy analysis;
- therapy-specific predictive value.

Those endpoints remain assigned to the fuller MMRF / CoMMpass clinical access plan.

## Priority Files To Acquire

Priority 1:

- Supplementary Table 1 / individual patient features.
- Purpose: ISS, baseline labs, copy-number calls, cytogenetic high-risk labels, RNA subtype labels.

Priority 2:

- Supplementary Table 7 / gene-expression subtype classifier results and model coefficients.
- Purpose: subtype comparison and expression-subtype positioning.

Priority 3:

- Supplementary Table 5 / somatic SNV/INDEL events.
- Purpose: TP53, KRAS, NRAS, BRAF, DIS3, TENT5C/FAM46C mutation annotation.

Priority 4:

- Supplementary Table 6 / structural events.
- Purpose: IGH translocations and fusion/structural-event context.

Priority 5:

- Larger expression, copy-number and LOF/GOF matrices.
- Purpose: optional deeper molecular integration if storage and parsing are acceptable.

## Planned Local Workflow

Create:

- `external_bulk/Skerget_NG2024_CoMMpass_public_supplement/`
- `analysis/skerget_ng2024_public_supplement/`
- `reports/validation/SKERGET_NG2024_PUBLIC_SUPPLEMENT_AUDIT.md`
- `scripts/19_skerget_ng2024_public_supplement_audit.py`

Script responsibilities:

1. Download or register local paths for the public supplementary files.
2. Inventory file names, sizes, sheet names and column names.
3. Detect patient/sample ID format.
4. Attempt ID matching to `analysis/commppass_gdc_validation/commppass_axis_clinical_scores.tsv`.
5. Run first-pass association tests if IDs match.
6. Write a report listing usable fields and unusable fields.

## Figure And Manuscript Integration

If ID matching works:

- add a molecular-risk validation panel to Fig. 5 or create a supplemental figure;
- update the cross-cohort evidence table;
- state that the plasma-secretory axis is additionally evaluated against public CoMMpass molecular-risk annotations.

If ID matching fails:

- still use the public supplement as contextual evidence;
- do not run patient-level score association claims;
- report it as a source of established MM molecular-risk definitions rather than a direct validation cohort.

## Updated Q2 Route

The revised Q2 route is:

1. GSE269875 spatial discovery.
2. GSE271107 single-cell localization.
3. GSE24080/GSE2658 bulk validation.
4. CoMMpass/GDC open OS and ISS validation.
5. Skerget et al. Nature Genetics 2024 public CoMMpass molecular-annotation validation.
6. GSE299193 second public spatial validation.
7. Fuller MMRF clinical access only as future enhancement for PFS, R-ISS and treatment-response endpoints.

## Source Basis

The Nature Genetics article states that CoMMpass is a longitudinal observational study of 1,143 newly diagnosed patients with multiple myeloma with WGS, WES and RNA-seq profiling, and that Supplementary Tables 1-7 are freely available on Zenodo.

The Nature Genetics data-availability section also documents that IA22 includes the full planned observation period for most patients and that nonidentifiable clinical and processed datasets are accessible through MMRF channels.
