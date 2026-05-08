# MMRF/CoMMpass Data Request Screen Guide

Date: 2026-05-02

## Purpose

This guide summarizes the fuller MMRF/CoMMpass data needed for the current multiple-myeloma manuscript extension and how the user can work with Codex while navigating the MMRF interface.

Current manuscript already has:

- GDC open MMRF-COMMPASS RNA-seq and clinical slice.
- OS and ISS association.
- Public NG2024/Skerget molecular annotations.

Current manuscript does not yet have complete:

- R-ISS.
- PFS.
- detailed treatment-response validation.
- complete therapy-line/regimen validation.
- complete authorized clinical/FISH cytogenetics tables beyond public/open slices.

## Must-Request Data Categories

### 1. Patient Clinical Data

Purpose:

- Complete demographics, diagnosis, baseline disease status, ISS/R-ISS components, baseline labs, follow-up.

Needed fields:

- Patient ID / subject ID.
- Age, sex, race/ethnicity.
- Diagnosis date.
- Myeloma subtype if available.
- ISS stage.
- R-ISS stage if directly provided.
- Hemoglobin, creatinine, calcium.
- LDH or LDH status.
- Beta-2 microglobulin.
- Albumin.
- Last follow-up date.
- Vital status.
- Death date if available.
- OS time and OS event if available.

Priority: highest.

### 2. Outcome / Survival / PFS Data

Purpose:

- Add PFS/progression/relapse analyses that are not available in the current open GDC slice.

Needed fields:

- PFS time.
- PFS event.
- Progression date.
- Relapse date.
- Death date.
- Last follow-up date.
- Event indicator.
- Time-to-event variables if already harmonized.

Priority: highest.

### 3. Treatment Response Data

Purpose:

- Test whether the plasma-secretory / POU2AF1-XBP1-JCHAIN axis relates to response depth or refractory state.

Needed fields:

- Best overall response.
- CR / sCR / VGPR / PR / MR / SD / PD.
- Responder vs non-responder grouping if provided.
- Refractory status.
- Relapse/progression after treatment.
- Response by therapy line if available.

Expected legacy-style file example recorded in project log:

- `MMRF_CoMMpass_IA14_STAND_ALONE_TRTRESP.csv`

Priority: high.

### 4. Treatment / Regimen / Therapy-Line Data

Purpose:

- Stratify clinical associations by initial therapy class and treatment line.

Needed fields:

- First-line regimen.
- Therapy line number.
- Drug class.
- Specific drugs.
- Transplant / ASCT status.
- Treatment start date.
- Treatment end date.
- Response to each line.

Priority: high.

### 5. Cytogenetics / FISH Data

Purpose:

- Build R-ISS and high-risk cytogenetic analyses.

Needed fields:

- del17p.
- t(4;14).
- t(14;16).
- t(11;14), useful but not part of R-ISS high-risk definition.
- 1q gain / 1q amplification.
- del13q.
- MYC rearrangement if available.
- FISH risk annotation.
- High-risk cytogenetics group.

Priority: highest.

### 6. Copy Number / Canonical Variant / Molecular Annotation Data

Purpose:

- Fill gaps if clinical FISH fields are incomplete and support molecular-risk sensitivity analyses.

Needed fields:

- 1q gain/amplification.
- 17p deletion.
- 13q deletion.
- Other CNA features.
- TP53 mutation.
- KRAS / NRAS / BRAF.
- DIS3.
- FAM46C.
- Canonical IGH translocations if provided.

Priority: medium-high.

### 7. Sample / Patient Mapping

Purpose:

- Link downloaded clinical and molecular tables to the already analyzed CoMMpass/GDC baseline RNA-seq score table.

Needed fields:

- Patient ID.
- Sample ID.
- Aliquot ID.
- Baseline sample flag.
- Visit / timepoint.
- Tissue type.
- CD138+ / tumor sample marker.
- RNA-seq availability.

Priority: highest.

### 8. Bulk Tumor Gene Expression

Purpose:

- Optional backup. Current project already has GDC bulk RNA-seq expression, so this is not the first priority unless MMRF provides cleaner processed expression linked to full clinical metadata.

Needed fields:

- Processed tumor bulk expression matrix.
- Sample IDs matching clinical table.
- Baseline sample flag.

Priority: optional / backup.

## Which Portal Options To Choose If Shown

If the MMRF form asks intended platform use:

- Choose: `Browse + Request Data Access`.

If it asks CoMMpass Summary Data:

- Choose the Interim Analysis / Summary CoMMpass datasets if available, especially clinical, copy-number, expression, fusion, somatic-variant, structural-variant, and LOH summary files.

If it asks CoMMpass Patient Sample Data:

- Choose `Patient Clinical Data (Treatment, Demographics, Outcome/PFS)`.
- Choose processed patient sample genomic data if available and allowed, especially tumor bulk expression, copy-number, variants, fusions.

If it asks manuscript-related supplementary data:

- Skerget et al. Nature Genetics 2024 supplementary data are useful and already partly used publicly.
- Pilcher et al. Nature Cancer 2025/2026 supplementary data are useful for single-cell/bone-marrow immune context but are not a replacement for fuller clinical PFS/treatment-response tables.

## Local Destination After Download

Put authorized downloaded files here:

```text
D:\二区\external_bulk\CoMMpass_full_clinical
```

Accepted file types:

- `.csv`
- `.tsv`
- `.txt`
- `.xlsx`
- `.xls`

Then run:

```text
python scripts\16_commppass_full_clinical_validation.py
```

The script will generate:

```text
D:\二区\analysis\commppass_full_clinical_validation\full_clinical_inventory.tsv
D:\二区\analysis\commppass_full_clinical_validation\endpoint_candidate_columns.tsv
D:\二区\reports\validation\COMMPASS_FULL_CLINICAL_READINESS_REPORT.md
```

## How Codex Can Help During Screen Navigation

Codex cannot directly see or control the user's full Windows desktop screen unless the user provides the screen content through the chat.

Workable workflow:

1. User opens the MMRF/Virtual Lab/Researcher Gateway page locally.
2. User sends a screenshot of the current page or pastes the visible options/text.
3. Codex tells the user exactly which option to select and what to avoid.
4. If files are downloaded, user places them in:
   - `D:\二区\external_bulk\CoMMpass_full_clinical`
5. Codex scans the folder and reports whether the needed endpoints are present.

Do not send passwords, verification codes, private tokens, or account credentials in chat.

## Current Scientific Role Of These Data

If obtained, fuller MMRF data can upgrade the manuscript by adding:

- R-ISS validation.
- PFS validation.
- treatment-response analysis.
- therapy-line stratification.
- stronger cytogenetic high-risk adjustment.

These are strengthening analyses, not current blockers. The current manuscript remains built around:

- spatial discovery;
- second spatial cohort reproducibility;
- single-cell localization;
- external bulk support;
- CoMMpass/GDC OS and ISS association;
- NG2024 molecular-risk context.

## 2026-05-02 Open GDC Audit Result

The open GDC route was retested locally using the GDC API current data release.

Open GDC can provide:

- RNA-seq gene expression quantification files.
- Masked somatic mutation MAF files.
- Copy-number segment files.
- limited OS/ISS clinical fields from the GDC cases endpoint.
- treatment-exposure / therapeutic-agent metadata.

Open GDC still does not provide the missing fuller clinical endpoints needed for the optional enhancement:

- usable PFS;
- R-ISS;
- treatment-response outcomes;
- baseline laboratory fields such as LDH, albumin, beta-2 microglobulin;
- complete FISH/cytogenetic fields such as del17p, t(4;14), t(14;16), and 1q gain/amplification.

Therefore the user still needs authorized MMRF Researcher Gateway / Virtual Lab files if the manuscript is to add R-ISS, PFS, treatment-response, and detailed cytogenetic validation.

Local audit outputs:

```text
D:\二区\scripts\32_gdc_mmrf_open_data_audit.py
D:\二区\reports\validation\GDC_OPEN_MMRF_COMMPASS_DATA_AUDIT.md
D:\二区\analysis\mmrf_open_data_audit\gdc_open_file_inventory.tsv
D:\二区\analysis\mmrf_open_data_audit\gdc_open_file_type_counts.tsv
D:\二区\analysis\mmrf_open_data_audit\gdc_open_clinical_endpoint_candidate_columns.tsv
```
