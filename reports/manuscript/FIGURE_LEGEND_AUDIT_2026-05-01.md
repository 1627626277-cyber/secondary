# Figure Legend And File Audit

Date: 2026-05-01

Scope:

- Checked whether Fig. 1-6 are cited in the manuscript.
- Checked whether Fig. 1-6 have draft legends.
- Checked whether PNG, PDF, and SVG outputs exist for each planned main figure.

## Verdict

Status:

- Pass.

Interpretation:

- All six planned main figures are cited in the manuscript.
- All six planned main figures have draft legends.
- All six planned main figures have PNG, PDF, and SVG files in `analysis/manuscript_figures`.

## Figure-Level Audit

| Figure | Manuscript citation | Legend present | Output files present | Notes |
|---|---|---|---|---|
| Fig. 1 | Yes | Yes | PNG, PDF, SVG | Study design and evidence chain. |
| Fig. 2 | Yes | Yes | PNG, PDF, SVG | GSE269875 spatial discovery. |
| Fig. 3 | Yes | Yes | PNG, PDF, SVG | GSE271107 single-cell localization. |
| Fig. 4 | Yes | Yes | PNG, PDF, SVG | GSE24080/GSE2658 external bulk support. |
| Fig. 5 | Yes | Yes | PNG, PDF, SVG | CoMMpass/GDC and NG2024 validation. |
| Fig. 6 | Yes | Yes | PNG, PDF, SVG | GSE299193 Xenium program-level spatial validation. |

## Claim-Boundary Check

- Fig. 6 legend correctly states that GSE299193 validates the program-level spatial signal and does not directly validate TXNDC5, JCHAIN, or SDC1.
- Fig. 5 legend correctly states that adjusted models support association and do not prove clinical utility.
- Fig. 3 legend correctly states that TXNDC5 is not treated as a standalone prognostic biomarker.

## Remaining Before Upload

1. Confirm final figure upload format required by the journal portal.
2. Confirm final figure resolution if the portal flags any file.
3. Ensure figure legends are either included in the manuscript DOCX or uploaded as a separate figure-legend file according to the portal workflow.
