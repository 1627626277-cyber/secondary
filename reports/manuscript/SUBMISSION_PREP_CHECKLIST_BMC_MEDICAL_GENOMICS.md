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

Submission hardening files:

- `submission\bmc_medical_genomics_2026-05-01\TABLE1_CROSS_COHORT_EVIDENCE_DRAFT.docx`
- `submission\bmc_medical_genomics_2026-05-01\SUPPLEMENTARY_METHODS_REPRODUCIBILITY_DRAFT.docx`
- `reports\manuscript\FIGURE_LEGEND_AUDIT_2026-05-01.md`
- `reports\manuscript\REFERENCE_LINK_AUDIT_2026-05-01.md`

## Remaining Required Before Upload

1. Convert manuscript to the journal-required upload format.
   - Status: complete; DOCX generated in `submission\bmc_medical_genomics_2026-05-01`.
2. Finalize title page:
   - author name: Zhuang Jiang
   - Chinese name source: confirmed by user as 蒋壮
   - affiliation/address: Guangdong University of Petrochemical Technology (GDUPT), 139 Guandu 2nd Road, Maoming 525000, Guangdong, China
   - corresponding author details: to be finalized before submission
   - ORCID: https://orcid.org/0009-0007-4388-5901
3. Finalize declarations:
   - ethics approval and consent to participate
   - consent for publication
   - availability of data and materials
   - competing interests
   - funding
   - author contributions
   - acknowledgements
   - Status: draft complete for the current single-author version. Revise if additional authors, funding, or institutional requirements are added before upload.
4. Final claim-placement citation check.
   - Coverage, Vancouver first-appearance ordering, formal reference-draft synchronization, and high-level claim-placement screen are complete.
5. Main versus supplementary figures/tables:
   - Keep Fig. 6 as a main figure.
   - Keep the cross-cohort evidence table as main Table 1.
   - Table 1 now has a separate editable DOCX file.
   - Supplementary Methods/reproducibility appendix now has Markdown and DOCX drafts.
6. Prepare cover letter.
   - Status: DOCX draft generated.
7. Perform final reproducibility audit from scripts to manuscript claims.
   - Status: Stage 2.5 integrity verification, figure-legend audit, and DOI/URL live-link audit completed.

## ORCID Profile Issue To Fix Outside The Manuscript

The ORCID screenshot shows an employment entry for "Fo Guang Shan: Kaohsiung City, TW" with "master (GDUPT)". This appears inconsistent with the manuscript affiliation and should be corrected in ORCID if it was entered by mistake.

The manuscript affiliation should remain:

- Guangdong University of Petrochemical Technology (GDUPT), Maoming, Guangdong, China

## Practical Submission Readiness

Current readiness estimate:

- Scientific evidence package: high for a public-data Q2 bioinformatics manuscript.
- Journal-upload package: close, but not complete only because corresponding-author and live portal metadata remain pending.
- GitHub/code availability, figure upload-format confirmation, DOI/URL link audit, line-number confirmation, and DOCX render checks are complete.

The project is in manuscript-finalization and submission-preparation. It is not yet ready for one-click journal upload because the corresponding-author metadata still needs to be finalized.
