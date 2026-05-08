# GDC Open MMRF-COMMPASS Data Audit

Date: 2026-05-02 12:09:26

Purpose:

- Verify what the open GDC MMRF-COMMPASS API can provide for the current manuscript.
- Distinguish already available open GDC data from fuller MMRF Researcher Gateway clinical files.

GDC status:

- API status: OK
- Data release: Data Release 45.0 - December 04, 2025

Open file inventory:

- Total open files found: 2960
- 1091 file(s): Simple Nucleotide Variation / Masked Somatic Mutation / WXS / MAF
- 1010 file(s): Copy Number Variation / Copy Number Segment / WGS / TXT
- 859 file(s): Transcriptome Profiling / Gene Expression Quantification / RNA-Seq / TSV

Clinical-like files in the GDC files endpoint:

- None found in the open GDC files endpoint.

Clinical endpoint:

- Current clinical TSV saved to `external_bulk\CoMMpass_GDC\gdc_mmrfcases_clinical_current_20260502.tsv`.
- Current cases returned: 995.
- Number of columns in current GDC cases/clinical TSV: 401.

Endpoint candidate columns detected by keyword scan:

- R-ISS: none detected
- PFS: diagnoses.0.progression_or_recurrence
- treatment_response: diagnoses.0.treatments.0.days_to_treatment_end, diagnoses.0.treatments.0.days_to_treatment_start, diagnoses.0.treatments.0.therapeutic_agents, diagnoses.0.treatments.0.treatment_or_therapy, diagnoses.0.treatments.0.treatment_outcome, diagnoses.0.treatments.0.treatment_type, diagnoses.0.treatments.1.days_to_treatment_end, diagnoses.0.treatments.1.days_to_treatment_start, diagnoses.0.treatments.1.therapeutic_agents, diagnoses.0.treatments.1.treatment_or_therapy, diagnoses.0.treatments.1.treatment_outcome, diagnoses.0.treatments.1.treatment_type ... (384 columns total)
- cytogenetic_fish: none detected
- baseline_labs: none detected

Usability checks for key open clinical fields:

- `diagnoses.progression_or_recurrence` values: [('unknown', 995)]
- treatment outcome non-empty cells: 0
- treatment type values: [('Stem Cell Transplantation, Autologous', 544), ('Stem Cell Transplantation, Allogeneic', 14)]
- therapeutic agent values: [('Dexamethasone', 1760), ('Lenalidomide', 1393), ('Bortezomib', 1076), ('Cyclophosphamide', 694), ('Carfilzomib', 567), ('Melphalan', 491), ('Other', 210), ('Pomalidomide', 127), ('Prednisone', 92), ('Daratumumab', 59), ('Ixazomib', 42), ('Thalidomide', 39)]
- treatment-or-therapy values: [('yes', 7184)]
- treatment start-date non-empty cells: 6163
- treatment end-date non-empty cells: 5214

Interpretation for the manuscript:

- Open GDC remains useful for RNA-seq expression, masked somatic mutation MAF, copy-number segment files, limited OS/ISS clinical fields, and treatment-exposure/therapeutic-agent metadata.
- The current open GDC cases/clinical TSV still does not provide usable PFS, R-ISS, treatment-response outcome, baseline laboratory, or FISH/cytogenetic fields needed for the optional fuller-clinical extension.
- Therefore open GDC cannot replace authorized MMRF Researcher Gateway / Virtual Lab fuller clinical tables for R-ISS, PFS, treatment response, and detailed cytogenetic validation.

Outputs:

- `analysis\mmrf_open_data_audit\gdc_open_file_inventory.tsv`
- `analysis\mmrf_open_data_audit\gdc_open_file_type_counts.tsv`
- `analysis\mmrf_open_data_audit\gdc_open_clinical_endpoint_candidate_columns.tsv`
- `analysis\mmrf_open_data_audit\gdc_open_clinical_columns.txt`
