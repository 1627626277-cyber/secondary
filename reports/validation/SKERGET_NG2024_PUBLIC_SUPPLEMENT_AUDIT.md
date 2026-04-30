# Skerget NG2024 Public CoMMpass Supplement Audit

Date: 2026-04-30

## Download Status

- Files present/downloaded in this run: 7.
- Download directory: `D:\二区\external_bulk\Skerget_NG2024_CoMMpass_public_supplement`.
- Manifest: `D:\二区\analysis\skerget_ng2024_public_supplement\download_manifest.tsv`.

## Workbook Inventory

- Workbook inventory: `D:\二区\analysis\skerget_ng2024_public_supplement\workbook_inventory.tsv`.
- Large workbooks above 150 MB are recorded but not loaded unless `--audit-large` is used.

## ID Matching

- ID match summary: `D:\二区\analysis\skerget_ng2024_public_supplement\id_match_summary.tsv`.
- Best overlap: Supplementary Table 1 / 1A_Patient_features / `Patient_ID` = 762 local CoMMpass/GDC IDs.
- This means patient-level molecular annotation can likely be joined to the current CoMMpass axis score table.

## Claim Boundary

- These public files can support molecular-risk and subtype annotation after verified ID matching.
- They should not be used to claim PFS, treatment-response, or therapy-line validation unless those fields are explicitly found and validated.

## Source

- Skerget et al., Nature Genetics 2024: https://www.nature.com/articles/s41588-024-01853-0
