# Claude Code MMRF Download Fix Notes

Date: 2026-05-02

These notes are for debugging the separate Claude Code downloader attempt. They are not part of the manuscript project log.

## Main Problems Found

1. The generated script overstates what open GDC can provide.
   - Open GDC is useful for RNA-seq expression, masked somatic mutation MAF, copy-number segment files, limited OS/ISS clinical fields, and treatment-exposure/therapeutic-agent metadata.
   - It should not mark PFS, treatment response outcomes, complete therapy-line response, complete R-ISS, or FISH/cytogenetics as covered unless those exact fields are verified in downloaded tables.

2. The script writes biospecimen data by calling the clinical endpoint again.
   - `clinical/MMRF-COMMPASS` returned 404 during local testing and should not be used as the clinical source.
   - Use the GDC `cases` endpoint for open clinical/case fields.
   - Sample mapping should be derived from the GDC files/cases metadata or a valid GDC biospecimen endpoint if available.

3. File-search for `Clinical Supplement` returned no open clinical-supplement files in the GDC files endpoint during the 2026-05-02 audit.
   - The script should not claim treatment records were downloaded from clinical supplements unless actual files are returned and downloaded.

4. PowerShell/Python HTTPS access may fail with SSL EOF on this machine.
   - `curl.exe -L --ssl-no-revoke https://api.gdc.cancer.gov/status` worked.
   - Prefer a curl-based downloader or allow a curl fallback on Windows.

5. Avoid downloading all expression/MAF/CNV files by default.
   - The project already has the needed baseline RNA-seq expression layer.
   - For fuller clinical validation, the bottleneck is authorized MMRF clinical data, not more open GDC expression files.

## Recommended Next Script Behavior

1. Audit first, download later.
   - Query GDC status.
   - Query open file inventory for MMRF-COMMPASS.
   - Save file type counts.
   - Download only current clinical TSV.
   - Scan columns for R-ISS, PFS, treatment response, therapy/regimen, FISH/cytogenetics, and baseline labs.

2. Report endpoint coverage conservatively.
   - `covered` only if exact columns or downloaded files exist.
   - `not covered` if the field is absent from the open clinical TSV and no corresponding open file exists.
   - `requires MMRF authorization` for fuller PFS, response, treatment-line, R-ISS, and FISH/cytogenetics.

3. Put authorized MMRF files here for the main project:
   - `D:\二区\external_bulk\CoMMpass_full_clinical`

4. Then run:
   - `python D:\二区\scripts\16_commppass_full_clinical_validation.py`

## Existing Corrected Audit Script

Use this project script as the safer reference:

```text
D:\二区\scripts\32_gdc_mmrf_open_data_audit.py
```

It uses `curl.exe --ssl-no-revoke`, does not download large expression/MAF/CNV files, and produces a conservative coverage report.
