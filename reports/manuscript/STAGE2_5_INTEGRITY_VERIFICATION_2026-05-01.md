# Stage 2.5 Integrity Verification

Date: 2026-05-01

Pipeline stage:

- Academic-pipeline Stage 2.5: integrity verification after Results-first rewrite.

Manuscript checked:

- `D:\二区\reports\manuscript\MANUSCRIPT_BMC_MEDICAL_GENOMICS_TARGET_DRAFT.md`

Submission DOCX checked:

- `D:\二区\submission\bmc_medical_genomics_2026-05-01\MANUSCRIPT_BMC_MEDICAL_GENOMICS_SUBMISSION_DRAFT.docx`

## Verdict

Status:

- Pass for Stage 2.5 with pre-submission action items.

Interpretation:

- The Results-first rewrite is internally consistent.
- Each Results subsection maps to Fig. 1-6 or Table 1.
- Numeric claims remain traceable to local output tables.
- Claim boundaries are preserved.
- The manuscript should now move into targeted revision, not additional data hunting.

## Results-To-Figure Mapping

| Results unit | Linked output | Stage 2.5 status |
|---|---|---|
| Cross-cohort design defined a bounded evidence chain | Fig. 1; Table 1 | Pass |
| Spatial transcriptomics identified the plasma-secretory program | Fig. 2 | Pass |
| Independent Xenium data reproduced the program-level spatial signal | Fig. 6 | Pass |
| Single-cell data localized the axis to plasma-cell compartments | Fig. 3 | Pass |
| External bulk cohorts supported a clinical subtype module | Fig. 4 | Pass |
| CoMMpass/GDC linked the axis to OS, ISS, and molecular risk | Fig. 5; Table 1 | Pass |
| Adjusted models supported covariate-adjusted OS association | Fig. 5D | Pass |

## Citation Integrity

Expanded Vancouver citation audit:

- References used after expanding ranges: 1-26.
- Reference entries present: 1-26.
- Missing referenced entries: none.
- Unused reference entries: none.

Status:

- Pass.

Remaining:

- DOI/URL live-link verification is still required before upload.

## Claim-Boundary Screen

Checked boundary statements:

- No standalone clinical biomarker claim.
- No prospective classifier claim.
- No treatment-selection claim.
- No completed R-ISS validation claim.
- No completed PFS validation claim.
- No completed treatment-response validation claim.
- No direct GSE299193 validation claim for TXNDC5, JCHAIN, or SDC1.

Status:

- Pass.

## Numeric Integrity

The key claims remain aligned with the Stage 2 numeric integrity report:

- GSE269875 spatial discovery: median difference 0.709, Cohen's d 3.129, Mann-Whitney p=0.0256.
- GSE299193 Xenium validation: active MM/RM vs Ctrl/MGUS/SM median difference 0.766, p=0.000182, FDR=0.000575.
- GSE299193 POU2AF1/XBP1 module: median difference 1.068, p=0.000287, FDR=0.000575.
- GSE271107 TXNDC5 plasma-cell localization: mean log-normalized expression 2.196, detection fraction 94.86%.
- CoMMpass/GDC: 762 baseline CD138+ RNA-seq samples.
- CoMMpass/GDC OS event association: FDR=9.31e-06.
- CoMMpass/GDC ISS ordinal association: Spearman rho=0.132, p=0.000316, FDR=0.0019.
- Adjusted Cox model: HR=1.460, 95% CI 1.069-1.993, p=0.0173, FDR=0.0445.
- Adjusted clinical module Cox model: HR=1.434, 95% CI 1.090-1.886, FDR=0.0299.

Status:

- Pass.

## Cox PH Assumption Check

Primary score-term diagnostic:

- Plasma-secretory score, OS adjusted for age, sex, ISS, and 1q21: rho=-0.0637, p=0.475, FDR=0.778.
- POU2AF1/XBP1/JCHAIN module, OS adjusted for age, sex, ISS, and 1q21: rho=-0.0585, p=0.512, FDR=0.789.

Covariate caution:

- The 1q21 covariate showed FDR-significant time-related Schoenfeld residual structure in adjusted models.
- ISS also showed a weaker time-related signal in some adjusted models.

Interpretation:

- The primary score terms did not show an FDR-significant PH-screen violation.
- The Cox models should remain framed as retrospective adjusted association models, not prediction models.

Status:

- Pass with cautious reporting.

## DOCX Rendering QA

Rendered with:

- `render_docx.py --renderer artifact-tool`

Outputs:

- Main manuscript: 21 rendered pages.
- Cover letter: 1 rendered page.

Visual QA:

- Title page inspected.
- Results opening inspected.
- Results continuation inspected.
- Cover letter inspected.
- Full contact sheet inspected after clearing stale render artifacts.

Status:

- Pass for current draft layout.

Table note:

- Embedding Table 1 in the main manuscript produced poor DOCX layout in an earlier render.
- Table 1 is therefore kept as a separate editable table draft for now:
  - `D:\二区\submission\bmc_medical_genomics_2026-05-01\TABLE1_CROSS_COHORT_EVIDENCE_DRAFT.md`

## Remaining Pre-Submission Integrity Items

1. Confirm whether the target journal portal accepts Table 1 as a separate editable table file or requires it inside the manuscript DOCX.
2. Confirm line numbers in Word/WPS because headless rendering does not reliably display Word line numbering.
3. Complete DOI/URL live-link verification.
4. Finalize corresponding-author details.
5. Finalize author contributions.
6. Complete GitHub push or provide a stable public code archive before formal upload.
