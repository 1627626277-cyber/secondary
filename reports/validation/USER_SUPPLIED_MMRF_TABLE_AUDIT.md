# User-Supplied MMRF/CoMMpass Table Audit

Date: 2026-04-29

## Audit Question

The user supplied a set of 10 purported MMRF/CoMMpass-style clinical and molecular tables using patient identifiers such as `MMF-001` to `MMF-005`. The question was whether these data are correct and can be used for the project.

## Local Cross-Check

Checked local project files:

- `external_bulk/CoMMpass_GDC/gdc_mmrfcases_clinical.tsv`
- `external_bulk/CoMMpass_GDC/gdc_mmrfgene_expression_files.tsv`
- `analysis/commppass_gdc_validation/commppass_axis_clinical_scores.tsv`
- `external_bulk/CoMMpass_full_clinical`

Result:

- No matches were found for `MMF-001`, `MMF-002`, `MMF-003`, `MMF-004`, `MMF-005`, or the supplied `ALQ-*` aliquot identifiers.
- The local GDC/CoMMpass open data use identifiers such as `MMRF_1021`, `MMRF_1021_1_BM_CD138pos`, and `MMRF_1021_1_BM_CD138pos_T2_TSMRU_L01873`.
- `external_bulk/CoMMpass_full_clinical` remains empty, so no authorized fuller MMRF clinical files are locally available for confirming the supplied tables.

## Major Red Flags

1. Identifier mismatch:
   - Supplied IDs use `MMF-001` style identifiers.
   - Local CoMMpass/GDC data use `MMRF_####` style identifiers.

2. No provenance:
   - No official MMRF/Virtual Lab filename.
   - No data dictionary.
   - No download manifest.
   - No checksum.
   - No authorized export metadata.

3. Fictional/contextual wording:
   - The supplied text contains phrases such as role/persona continuity, encrypted-channel story language, and "continue the plot".
   - This is inconsistent with a genuine clinical table export.

4. Internal structure problems:
   - Some headers are concatenated or malformed.
   - Treatment-response columns are not consistently parseable.
   - The expression table claims a complete matrix but only gives a few illustrative values.

5. Scale mismatch:
   - Supplied data include only 5 synthetic-looking patients.
   - The current CoMMpass/GDC validation uses 762 baseline RNA-seq samples.

## Decision

These supplied tables should be treated as synthetic or fictional text, not as valid MMRF/CoMMpass clinical data.

They must not be used for:

- R-ISS validation;
- PFS validation;
- treatment-response validation;
- cytogenetic high-risk validation;
- manuscript figures;
- supplementary tables;
- any scientific claim.

## Acceptable Use

The supplied tables may only be used as a schema mock-up to design parsing code, not as data.

## Required Standard For Real Fuller MMRF/CoMMpass Files

Before use, real files should have:

- official source: MMRF Virtual Lab / Researcher Gateway / authorized export;
- original CSV/TSV/XLSX filenames;
- data dictionary or column descriptions;
- patient/sample identifiers compatible with CoMMpass IDs;
- enough rows to support analysis;
- no roleplay, narrative, or generated-text markers;
- clear permission to use controlled data.

## Current Valid Position

The project currently has valid data for:

- GSE269875 spatial discovery;
- GSE271107 single-cell validation;
- GSE24080/GSE2658 GEO bulk validation;
- MMRF-COMMPASS/GDC open OS/ISS validation;
- GSE299193 public Xenium download in progress.

Fuller MMRF R-ISS/PFS/treatment-response validation remains pending authorized clinical file access.

