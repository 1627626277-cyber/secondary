# Submission-Preparation Checklist: BMC Medical Genomics

Date: 2026-05-01

Target status: submission preparation started; formal journal submission not yet performed.

## Target Journal

Primary target:

- BMC Medical Genomics

Working manuscript:

- `reports\manuscript\MANUSCRIPT_BMC_MEDICAL_GENOMICS_TARGET_DRAFT.md`

Target-journal adaptation file:

- `reports\manuscript\TARGET_JOURNAL_ADAPTATION_BMC_MEDICAL_GENOMICS.md`

## Core Manuscript Claim

The manuscript should claim that a plasma-secretory program in multiple myeloma is spatially reproducible, single-cell localized to malignant/plasma-cell states, and associated with clinical and molecular-risk features across public bulk cohorts.

Recommended wording:

- "spatially reproducible and clinically associated program"
- "public-data integrative analysis"
- "hypothesis-generating translational genomics evidence"

Avoid:

- "validated clinical biomarker"
- "prospective classifier"
- "treatment-response predictor"
- "R-ISS/PFS validation completed"

## Completed Evidence Blocks

| Block | Status | Manuscript Use |
|---|---:|---|
| GSE269875 spatial discovery | Complete | Primary spatial discovery |
| GSE299193 Xenium second spatial validation | Complete | Program-level external spatial validation |
| GSE271107 single-cell validation | Complete | Cell-state localization, TXNDC5 support |
| GSE24080/GSE2658 bulk validation | Complete | Independent expression/clinical support |
| CoMMpass/GDC bulk validation | Complete | OS and ISS association |
| NG2024 public CoMMpass annotation | Complete | 1q21, 17p13, RNA subtype, PR subtype probability |
| Adjusted CoMMpass models | Complete | OS/1q21/risk adjusted association |
| Cox PH assumption screen | Complete | Model assumption support with caution for 1q21 |

## Known Boundaries

| Item | Status | Handling |
|---|---:|---|
| R-ISS validation | Not complete | Mention as unavailable in public clinical slice |
| PFS validation | Not complete | Do not report as result |
| Treatment-response validation | Not complete | Keep as future MMRF-enabled analysis |
| Direct GSE299193 TXNDC5 validation | Not possible from analyzed panel | Report GSE299193 as program-level validation only |
| Wet-lab validation | Not available | State as limitation |

## Files Ready For Submission Package

Manuscript:

- `reports\manuscript\MANUSCRIPT_BMC_MEDICAL_GENOMICS_TARGET_DRAFT.md`

Figures and legends:

- `analysis\manuscript_figures`
- `analysis\manuscript_figures_png_rerun_20260430_1850`
- `reports\manuscript\FIGURE_LEGENDS_DRAFT.md`
- `reports\manuscript\FIGURE_REPRODUCIBILITY_TABLE_STAGE2.md`

Statistics and validation:

- `reports\validation\COMMPASS_NG2024_ADJUSTED_MODEL_REPORT.md`
- `reports\validation\COMMPASS_COX_PH_ASSUMPTION_CHECK.md`
- `reports\review\STAGE2_NUMERIC_INTEGRITY_CHECK_2026-04-30.md`

References:

- `references\REFERENCE_LIBRARY.tsv`
- `references\REFERENCES_VANCOUVER_NUMBERED_DRAFT.md`
- `references\downloaded_pdfs_manifest.tsv`

## Remaining Required Before Upload

1. Convert manuscript to the journal-required upload format, likely DOCX.
2. Finalize title page:
   - author names
   - affiliations
   - corresponding author
   - ORCID identifiers if available
3. Finalize declarations:
   - ethics approval and consent to participate
   - consent for publication
   - availability of data and materials
   - competing interests
   - funding
   - author contributions
   - acknowledgements
4. Cross-check all in-text citation numbers against the final reference list.
5. Decide main versus supplementary figures/tables.
6. Prepare cover letter.
7. Perform final reproducibility audit from scripts to manuscript claims.

## Practical Submission Readiness

Current readiness estimate:

- Scientific evidence package: high for a public-data Q2 bioinformatics manuscript.
- Journal-upload package: not complete.
- Main remaining risk: wording discipline, citation consistency, and final submission formatting.

The project is ready to move from analysis-building into manuscript-finalization and submission-preparation. It is not yet ready for one-click journal upload.
