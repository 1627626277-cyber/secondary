# CoMMpass Fuller Clinical Data Readiness Report

Purpose:

- Scan local fuller MMRF/CoMMpass clinical files for R-ISS, PFS, cytogenetic high-risk, and treatment-response fields.
- This script does not claim validation by itself; it only checks whether the necessary local files and columns are present.

Input folder: `external_bulk\CoMMpass_full_clinical`

Status: no fuller clinical files were found.

Action required:

- Obtain authorized MMRF Virtual Lab / Researcher Gateway clinical files.
- Place CSV/TSV/XLSX files under `external_bulk/CoMMpass_full_clinical`.
- Rerun `python scripts/16_commppass_full_clinical_validation.py`.
