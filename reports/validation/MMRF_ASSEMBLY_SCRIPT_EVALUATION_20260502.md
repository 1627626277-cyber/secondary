# MMRF Assembly Scripts Evaluation

Date: 2026-05-02

## Purpose

Evaluate two newly added helper scripts and determine whether their outputs can strengthen the current multiple-myeloma manuscript.

Scripts evaluated:

- `assemble_mmrf_data.py`
- `parse_mmrf_flatfiles.py`

## Execution Summary

### `assemble_mmrf_data.py`

Command:

```text
python D:\二区\assemble_mmrf_data.py --output D:\二区\analysis\mmrf_assembly_20260502 --synthetic-patients 500
```

Result:

- Python `requests` calls to the GDC API failed on this Windows environment with SSL EOF errors.
- Published summary tables were generated successfully.
- Synthetic prototype patient/sample tables were generated successfully.

Follow-up fix:

- Added a `curl.exe --ssl-no-revoke` fallback to `assemble_mmrf_data.py`.
- Replaced broad GDC clinical field requests with explicit case, demographic, diagnosis, ISS, follow-up, and treatment-exposure fields.
- Re-ran the fixed script with synthetic output skipped:

```text
python D:\二区\assemble_mmrf_data.py --output D:\二区\analysis\mmrf_assembly_20260502_curl_fixed_v2 --skip-synthetic
```

Fixed-run outputs:

```text
D:\二区\analysis\mmrf_assembly_20260502_curl_fixed_v2\mmrf_clinical_gdc.tsv
D:\二区\analysis\mmrf_assembly_20260502_curl_fixed_v2\mmrf_biospecimen_gdc.tsv
D:\二区\analysis\mmrf_assembly_20260502_curl_fixed_v2\mmrf_rnaseq_files_gdc.tsv
D:\二区\analysis\mmrf_assembly_20260502_curl_fixed_v2\mmrf_mutations_gdc.tsv
D:\二区\analysis\mmrf_assembly_20260502_curl_fixed_v2\mmrf_copynumber_gdc.tsv
D:\二区\analysis\mmrf_assembly_20260502_curl_fixed_v2\published_baseline_demographics.csv
D:\二区\analysis\mmrf_assembly_20260502_curl_fixed_v2\published_fish_cytogenetics.csv
D:\二区\analysis\mmrf_assembly_20260502_curl_fixed_v2\published_mutation_frequencies.csv
D:\二区\analysis\mmrf_assembly_20260502_curl_fixed_v2\published_treatment_response.csv
D:\二区\analysis\mmrf_assembly_20260502_curl_fixed_v2\published_treatment_regimens.csv
```

Fixed-run dimensions:

- `mmrf_clinical_gdc.tsv`: 995 rows x 401 columns.
- `mmrf_biospecimen_gdc.tsv`: 995 rows x 8 columns.
- `mmrf_rnaseq_files_gdc.tsv`: 859 rows x 8 columns.
- `mmrf_mutations_gdc.tsv`: 1,091 rows x 5 columns.
- `mmrf_copynumber_gdc.tsv`: 2,020 rows x 5 columns.

Fixed-run endpoint check:

- ISS was present: I=348, II=353, III=266, Unknown=28.
- `diagnoses.0.progression_or_recurrence` was still uniformly `unknown` across 995 cases.
- 64 `treatment_outcome` columns were present but had 0 non-empty cells.
- Therefore PFS and treatment-response validation remain unavailable from open GDC.

Generated files:

```text
D:\二区\analysis\mmrf_assembly_20260502\published_baseline_demographics.csv
D:\二区\analysis\mmrf_assembly_20260502\published_fish_cytogenetics.csv
D:\二区\analysis\mmrf_assembly_20260502\published_mutation_frequencies.csv
D:\二区\analysis\mmrf_assembly_20260502\published_treatment_response.csv
D:\二区\analysis\mmrf_assembly_20260502\published_treatment_regimens.csv
D:\二区\analysis\mmrf_assembly_20260502\synthetic_patient_data_prototype.csv
D:\二区\analysis\mmrf_assembly_20260502\synthetic_sample_mapping_prototype.csv
```

Output dimensions:

- published baseline demographics: 14 rows x 3 columns.
- published FISH/cytogenetics: 8 rows x 5 columns.
- published mutation frequencies: 6 rows x 3 columns.
- published treatment response: 7 rows x 3 columns.
- published treatment regimens: 7 rows x 3 columns.
- synthetic patient prototype: 500 rows x 30 columns.
- synthetic sample prototype: 500 rows x 6 columns.

### `parse_mmrf_flatfiles.py`

Command:

```text
python D:\二区\parse_mmrf_flatfiles.py --input D:\二区\external_bulk\CoMMpass_full_clinical --output D:\二区\analysis\mmrf_flatfile_parse_20260502 --ia-version IA19
```

Result:

- Loaded 0/5 expected MMRF FlatFiles.
- No patient-level fuller MMRF clinical data were parsed because the authorized files are not present locally.

Expected files include:

```text
CoMMpass_IA19_FlatFiles\MMRF_CoMMpass_IA19_PER_PATIENT.csv
CoMMpass_IA19_FlatFiles\MMRF_CoMMpass_IA19_PER_PATIENT_VISIT.csv
CoMMpass_IA19_FlatFiles\MMRF_CoMMpass_IA19_STAND_ALONE_TRTRESP.csv
MMRF_OS_PFS_ASCT.csv
MMRF_OS_PFS_non-ASCT.csv
```

## Data Usefulness Assessment

### Useful Now

The published summary tables are useful only as contextual support:

- cohort demographics and ISS/OS context;
- aggregate FISH/cytogenetic frequencies;
- aggregate mutation-frequency context;
- broad therapy/regimen context if cited and verified.

These tables can support the Introduction, Discussion, or a supplementary background/context table. They do not provide patient-level endpoints and cannot be used for Cox models, PFS analysis, treatment-response association, or R-ISS validation.

### Not Suitable For Manuscript Results

The synthetic patient and sample tables must not be used as real results.

They can be used only for:

- pipeline testing;
- schema prototyping;
- verifying that future plotting/analysis scripts can run once real MMRF FlatFiles are obtained.

They must not be used for:

- manuscript figures;
- statistical tests;
- reported patient counts;
- clinical validation;
- claims about PFS, R-ISS, treatment response, FISH, or molecular risk.

### Not Solved Yet

These endpoints remain unavailable without authorized MMRF Gateway / Virtual Lab flatfiles:

- R-ISS.
- usable PFS.
- treatment-response outcome.
- therapy-line response.
- baseline laboratory fields such as LDH, albumin, beta-2 microglobulin.
- full FISH/cytogenetic fields such as del17p, t(4;14), t(14;16), and 1q gain/amplification.

## Relation To Existing Project Data

The separate GDC open-data audit already succeeded using `curl.exe --ssl-no-revoke`:

```text
D:\二区\scripts\32_gdc_mmrf_open_data_audit.py
D:\二区\reports\validation\GDC_OPEN_MMRF_COMMPASS_DATA_AUDIT.md
```

That audit showed:

- Open GDC has RNA-seq expression, MAF mutation files, CNV segment files, limited OS/ISS clinical fields, and treatment-exposure metadata.
- Open GDC does not solve PFS, R-ISS, treatment-response, or full FISH/cytogenetic validation.

Therefore the fixed `assemble_mmrf_data.py` is useful for reproducible GDC metadata assembly, but it does not add a new usable patient-level endpoint beyond what is already known from the safer curl-based audit.

## Decision For Manuscript Progression

No main manuscript result should be changed based on the synthetic data or approximate published response/regimen tables.

Potentially useful manuscript action:

- Add a conservative supplementary/context statement that public CoMMpass summary literature reports broad cohort demographics and cytogenetic frequencies, while the present analysis uses patient-level public NG2024/Skerget annotations for the actual molecular-risk association tests.

Do not claim:

- completed R-ISS validation;
- completed PFS validation;
- completed treatment-response validation;
- completed FISH validation from open GDC or synthetic data.

## Next Action If Real MMRF Data Are Downloaded

Place authorized FlatFiles under:

```text
D:\二区\external_bulk\CoMMpass_full_clinical
```

Expected folder layout:

```text
D:\二区\external_bulk\CoMMpass_full_clinical\CoMMpass_IA19_FlatFiles\MMRF_CoMMpass_IA19_PER_PATIENT.csv
D:\二区\external_bulk\CoMMpass_full_clinical\CoMMpass_IA19_FlatFiles\MMRF_CoMMpass_IA19_PER_PATIENT_VISIT.csv
D:\二区\external_bulk\CoMMpass_full_clinical\CoMMpass_IA19_FlatFiles\MMRF_CoMMpass_IA19_STAND_ALONE_TRTRESP.csv
D:\二区\external_bulk\CoMMpass_full_clinical\MMRF_OS_PFS_ASCT.csv
D:\二区\external_bulk\CoMMpass_full_clinical\MMRF_OS_PFS_non-ASCT.csv
```

Then run:

```text
python D:\二区\parse_mmrf_flatfiles.py --input D:\二区\external_bulk\CoMMpass_full_clinical --output D:\二区\analysis\mmrf_flatfile_parse_20260502 --ia-version IA19
python D:\二区\scripts\16_commppass_full_clinical_validation.py
```
