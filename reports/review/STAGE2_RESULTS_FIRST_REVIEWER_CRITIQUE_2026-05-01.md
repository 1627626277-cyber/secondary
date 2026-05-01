# Stage 2 Reviewer-Style Critique After Results-First Rewrite

Date: 2026-05-01

Manuscript:

- `D:\二区\reports\manuscript\MANUSCRIPT_BMC_MEDICAL_GENOMICS_TARGET_DRAFT.md`

Review mode:

- Internal pre-submission reviewer-style critique.

## Editorial Verdict

Recommendation:

- Major revision before submission.

Rationale:

- The manuscript now has a coherent Q2-level structure: spatial discovery, second spatial validation, single-cell localization, external bulk support, and CoMMpass clinical/molecular association.
- The Results-first rewrite improves readability and makes the evidence chain reviewable.
- The manuscript is not yet upload-ready because formatting, table placement, author metadata, code availability, and final methods granularity still need tightening.

## Major Strengths

1. The evidence chain is now explicit.

The Results section no longer reads as disconnected analyses. Each paragraph is anchored to Fig. 1-6 or Table 1.

2. The manuscript avoids overclaiming.

The current draft does not claim that TXNDC5 is a standalone prognostic biomarker, and it does not claim completed R-ISS, PFS, or treatment-response validation.

3. The second spatial dataset reduces the largest earlier weakness.

GSE299193 adds an independent spatial validation layer. Because the Xenium panel lacks TXNDC5, JCHAIN, and SDC1, this should stay framed as program-level validation.

4. Adjusted CoMMpass/NG2024 models are a meaningful upgrade.

The OS association persists after adjustment for age, sex, ISS, and 1q21 status. This is important for Q2 credibility, provided it remains association language.

## Major Concerns

1. Table 1 placement is unresolved.

Table 1 is central to the manuscript logic. The current separate editable Markdown table avoids DOCX overflow, but the final submission needs a journal-compatible table format. This must be resolved before upload.

2. Methods are still compressed relative to the number of datasets.

The current Methods are usable for an internal draft, but a reviewer may ask for clearer filtering rules, complete-case definitions, score formulas, FDR families, software versions, and exact script-output links.

3. Clinical interpretation remains bounded by missing fuller clinical endpoints.

The manuscript does not have complete R-ISS, PFS, cytogenetic high-risk clinical outcome stratification, or treatment-response validation. This is acceptable for a Q2 bioinformatics/translational analysis only if the language stays precise.

4. Single-cell labels are marker-inferred.

This is disclosed, but a reviewer may still question the strength of cell-type localization. The manuscript should keep "marker-inferred plasma-cell compartments" rather than implying atlas-grade annotation.

5. The Cox PH check supports the score terms but flags model covariates.

The primary score terms do not show an FDR-significant Schoenfeld residual signal. However, 1q21 and some ISS covariate terms show time-related residual structure. The manuscript should not present the Cox models as definitive prediction models.

6. Code availability is not fully resolved.

The GitHub URL is drafted, but local push remains blocked by network/authentication. A journal upload should not proceed until the repository or archive URL is public and testable.

## Minor Concerns

1. The abstract is currently 309 words. This is probably acceptable for BMC Medical Genomics, but it should be checked against the portal during upload.
2. The cover letter still contains corresponding-author placeholders by design.
3. The manuscript contains page and line-numbering metadata, but Word/WPS visual confirmation is still required.
4. DOI and URL checks remain incomplete.
5. Figure legends should be reviewed once the final figure/table upload decision is made.

## Reviewer-Style Questions To Pre-Answer

1. Why is this not only a plasma-cell abundance signature?

The Discussion already states this limitation. The Methods and Results should make clear that the manuscript studies a plasma-secretory program, not a fully independent tumor-intrinsic biomarker.

2. Why is TXNDC5 highlighted if the strongest clinical module is POU2AF1/XBP1/JCHAIN?

The answer should remain: TXNDC5 is the spatial/single-cell localization candidate, whereas POU2AF1/XBP1/JCHAIN better supports the clinical subtype/risk axis.

3. What exactly does GSE299193 validate?

It validates the program-level spatial disease signal. It does not directly validate TXNDC5, JCHAIN, or SDC1 because those genes were absent from the extracted panel.

4. Why no R-ISS, PFS, or treatment response?

The available public clinical slices do not support complete validation of those endpoints. The manuscript must state this as a limitation, not hide it.

## Required Next Revisions

1. Convert Table 1 into a journal-compatible editable table file, likely DOCX or XLSX.
2. Expand Methods details for complete-case handling and score definitions.
3. Add a short Supplementary Methods or reproducibility appendix if main-text Methods become too dense.
4. Verify all figure panels against final legends.
5. Complete DOI/URL live-link verification.
6. Resolve public code availability.
7. Finalize corresponding author, contributions, and line-number check before upload.

## Current Submission Readiness

Scientific route:

- Feasible for Q2-style bioinformatics/translational oncology submission after revision.

Current package:

- Not yet ready for formal upload.

Most important blocker:

- Public code availability and final table/formatting package.
