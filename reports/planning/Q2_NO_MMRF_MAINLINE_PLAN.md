# Q2 Mainline Plan Without Required Fuller MMRF Clinical Data

Date: 2026-04-29

## Route Decision

The project will no longer depend on fuller MMRF/CoMMpass clinical data as a required condition for manuscript submission.

New mainline:

- spatial discovery;
- single-cell localization;
- multi-bulk clinical validation;
- public CoMMpass molecular-annotation validation;
- second spatial cohort validation.

Fuller MMRF/CoMMpass clinical data remain useful but are now a future enhancement rather than a blocker for PFS, R-ISS, treatment-response and therapy-line endpoints.

## Rationale

The current project already has:

- spatial discovery in GSE269875;
- single-cell localization validation in GSE271107;
- GEO bulk validation in GSE24080 and GSE2658;
- CoMMpass/GDC open OS and ISS validation in 762 baseline CD138+ RNA-seq samples;
- adjusted CoMMpass/GDC + NG2024 models for OS, ISS, molecular-risk and RNA-subtype probability;
- manuscript-grade Fig. 1-5 and first-pass manuscript text.

Newly added public-data enhancement:

- Skerget et al., Nature Genetics 2024 public CoMMpass supplementary tables can provide patient-level molecular annotations, including ISS/baseline laboratory context, copy-number calls, cytogenetic high-risk labels, RNA subtype labels, mutation records and structural-event records.
- These public supplementary files are lower-friction than fuller MMRF clinical access and should be tested before waiting for controlled MMRF approval.

The missing fuller MMRF endpoints are:

- R-ISS;
- complete PFS;
- treatment response;
- detailed therapy/regimen validation.

The public Nature Genetics 2024 supplement may reduce the cytogenetic/molecular-risk gap. It does not by itself close the PFS or treatment-response gap unless verified endpoint columns are actually present after download.

These fuller clinical endpoints would improve clinical depth, but they are not essential for a Q2-style public-data integrative bioinformatics manuscript if the public molecular-annotation line and the second spatial validation are completed.

## Revised Manuscript Claim

Use this bounded claim:

An MM bone marrow `plasma_secretory` spatial program is discovered in spatial transcriptomics, localized to plasma-cell compartments by single-cell RNA-seq, supported by external bulk cohorts, associated with OS and ISS in CoMMpass/GDC, evaluated against public CoMMpass molecular-risk annotations where ID matching is possible, and externally tested in a second human MM bone marrow spatial dataset.

If Skerget et al. public CoMMpass supplementary tables can be matched to the local CoMMpass/GDC score table, extend the claim to:

The `plasma_secretory` axis is additionally evaluated against public CoMMpass molecular-risk annotations, including cytogenetic/copy-number and expression-subtype features.

Do not claim:

- R-ISS validation;
- complete PFS validation;
- treatment-response validation;
- definitive clinical classifier performance;
- prospective clinical utility.

## Mainline Data Components

Completed:

1. GSE269875 spatial discovery.
2. GSE271107 single-cell validation.
3. GSE24080/GSE2658 external bulk validation.
4. CoMMpass/GDC open RNA-seq OS/ISS validation.
5. Fig. 1-5 first-pass manuscript figures.
6. Main manuscript text first draft.
7. Skerget et al. Nature Genetics 2024 public CoMMpass supplement download, audit and first-pass molecular annotation validation.
8. Adjusted CoMMpass/GDC + NG2024 models for OS, ISS, molecular-risk, 1q21/17p13 and PR subtype probability.
9. GSE299193 human Xenium second spatial validation.
   - Download completed at expected size `82,255,360,000` bytes.
   - 22 sample matrices analyzed.
   - `plasma_secretory_score_z` higher in MM/RM than Ctrl/MGUS/SM: median delta `0.766`, FDR `0.000575`.
   - `POU2AF1/XBP1` module higher in MM/RM than Ctrl/MGUS/SM: median delta `1.068`, FDR `0.000575`.
   - Limitation: the Xenium panel lacks `TXNDC5`, `JCHAIN`, and `SDC1`; use this as program-level spatial validation, not direct TXNDC5/JCHAIN validation.
10. Fig. 6 and GSE299193 rows added to the manuscript figure package and cross-cohort evidence table.

In progress:

11. Formal citation cleanup, figure polish, and focused reviewer-style manuscript quality control.

Future optional enhancement:

10. Fuller MMRF/CoMMpass clinical validation if approved.

## Revised Figure Plan

Figure 1:

- Study design and evidence chain.

Figure 2:

- GSE269875 spatial discovery of the `plasma_secretory` program.

Figure 3:

- GSE271107 single-cell localization and TXNDC5 plasma-cell support.

Figure 4:

- GSE24080/GSE2658 bulk validation and subtype/risk support.

Figure 5:

- CoMMpass/GDC OS and ISS validation.
- Extension: public CoMMpass molecular-risk annotations from Skerget et al. NG2024.
- Current first-pass evidence:
  - Table 1 patient features match 762/762 local CoMMpass/GDC samples.
  - Table 7 RNA subtype predictions match 707 local CoMMpass/GDC samples.
  - `plasma_secretory_score_z` associates with NG2024 RNA subtype and `Cp_1q21_Call`.

Figure 6:

- GSE299193 Xenium second spatial cohort validation.
- Current panels:
  - sample-level `plasma_secretory` score by group;
  - sample-level `POU2AF1/XBP1` module score by group;
  - available axis-gene expression heatmap by group.
- Required figure note:
  - `TXNDC5`, `JCHAIN`, and `SDC1` are absent from the Xenium panel.
  - Fig. 6 supports program-level spatial reproducibility, not direct TXNDC5/JCHAIN validation.

Supplementary:

- cross-cohort evidence table;
- public CoMMpass molecular-annotation audit table;
- gene-set definitions;
- data inventory;
- claim-boundary table.

## Immediate Next Steps

Priority 1:

- Completed on 2026-04-30:
  - integrated Skerget et al. NG2024 public molecular annotation into the manuscript package;
  - added NG2024 and adjusted-model evidence to the cross-cohort evidence table;
  - updated Fig. 1 and Fig. 5;
  - updated manuscript Abstract, Methods, Results, Discussion and Data Availability;
  - kept PFS/treatment response out of completed claims.

Priority 2:

- Completed on 2026-04-30:
  - `GSE299193_RAW.tar` download reached expected size.
  - `python scripts\17_gse299193_download_status.py` confirmed 100%.
  - `python scripts\18_gse299193_xenium_validation.py` completed first-pass validation.

Priority 3:

- Completed on 2026-04-30:
  - regenerated manuscript figure package through `python scripts\15_build_manuscript_figures.py`;
  - added Fig. 6;
  - updated Results;
  - updated Discussion;
  - updated Abstract;
  - updated evidence table.

Priority 4:

- Decide whether Fig. 6 remains a main figure or becomes supplementary after target-journal formatting is selected.

Priority 4 fallback:

- GSE284727 is no longer urgent. Inspect only if final review requires another spatial dataset.
- Do not describe `GSE284727` as a completed spatial validation dataset until its public matrices/objects are downloaded and inventoried.

Priority 5:

- Add formal references and figure callouts to `MANUSCRIPT_MAIN_TEXT_DRAFT.md`.

## MMRF Plan Preserved As Future Enhancement

If MMRF Virtual Lab / Researcher Gateway access is approved later:

- download fuller clinical files to:
  - `external_bulk/CoMMpass_full_clinical`
- run:
  - `python scripts/16_commppass_full_clinical_validation.py`
- evaluate whether fields are available for:
  - R-ISS;
  - PFS;
  - cytogenetic high-risk;
  - treatment response;
  - therapy/regimen stratification.

If usable:

- add enhanced clinical validation as either:
  - an additional main figure;
  - an extended Fig. 5;
  - or supplementary clinical validation tables.

If not approved or not usable:

- proceed with the no-MMRF Q2 mainline and use public CoMMpass molecular-annotation supplement as the main molecular-risk enhancement source.

## Current Strategic Judgment

The project remains viable for a Q2 bioinformatics / translational oncology / tumor data-analysis journal without fuller MMRF clinical files.

The strongest near-term route is to combine two additions:

1. public CoMMpass molecular-annotation validation from Skerget et al. Nature Genetics 2024;
2. GSE299193 independent Xenium spatial validation.

Together these compensate for the absence of controlled PFS/treatment-response data by strengthening molecular-risk annotation and spatial reproducibility.
