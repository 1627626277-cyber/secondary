# Pre-Submission Hardening Report

Date: 2026-05-01

Scope:

- Editable Table 1 preparation.
- Methods expansion.
- Supplementary reproducibility appendix.
- Figure-legend audit.
- DOI/URL link audit.
- DOCX regeneration and render QA.

## Completed

1. Table 1 was converted into a separate editable DOCX file:
   - `submission\bmc_medical_genomics_2026-05-01\TABLE1_CROSS_COHORT_EVIDENCE_DRAFT.docx`

2. The main Methods section was expanded with:
   - score construction rules;
   - missing-data and complete-case rules;
   - FDR-family definitions;
   - adjusted Cox model boundary language;
   - supplementary reproducibility appendix reference.

3. A Supplementary Methods/reproducibility appendix was created:
   - `submission\bmc_medical_genomics_2026-05-01\SUPPLEMENTARY_METHODS_REPRODUCIBILITY_DRAFT.md`
   - `submission\bmc_medical_genomics_2026-05-01\SUPPLEMENTARY_METHODS_REPRODUCIBILITY_DRAFT.docx`

4. Figure-legend and output-file audit was completed:
   - `reports\manuscript\FIGURE_LEGEND_AUDIT_2026-05-01.md`

5. DOI/URL live-link audit was completed:
   - `reports\manuscript\REFERENCE_LINK_AUDIT_2026-05-01.md`
   - `reports\manuscript\REFERENCE_LINK_AUDIT_2026-05-01.tsv`

6. The main manuscript DOCX was regenerated after hardening:
   - `submission\bmc_medical_genomics_2026-05-01\MANUSCRIPT_BMC_MEDICAL_GENOMICS_SUBMISSION_DRAFT.docx`
   - backup: `submission\bmc_medical_genomics_2026-05-01\MANUSCRIPT_BMC_MEDICAL_GENOMICS_SUBMISSION_DRAFT_HARDENED_2026-05-01.docx`

7. The cover letter DOCX was regenerated:
   - `submission\bmc_medical_genomics_2026-05-01\COVER_LETTER_DRAFT.docx`
   - backup: `submission\bmc_medical_genomics_2026-05-01\COVER_LETTER_DRAFT_HARDENED_2026-05-01.docx`

## Render QA

Artifact-tool render checks:

- Table 1 DOCX: 1 page; pass.
- Supplementary Methods DOCX: 6 pages; pass.
- Hardened manuscript DOCX: 22 pages; pass.

The base manuscript DOCX was initially locked by Word/WPS. A suffixed hardened copy was generated first, then copied back to the base DOCX filename after the lock cleared.

## Integrity Checks

- Manuscript word count excluding references: 3,390.
- Abstract word count: 309.
- Expanded in-text citation coverage: references 1-26 used.
- Missing reference entries: none.
- Unused reference entries: none.
- Reference-link audit: no target remains marked failed.
- Six NCBI/GDC URLs required browser verification because local Python urllib produced TLS EOF errors.

## Remaining Before Upload

1. Public GitHub/code availability still needs resolution.
2. Corresponding-author details remain pending.
3. Final figure upload format must be confirmed in the journal portal.
4. Portal metadata, suggested reviewers, and opposed reviewers remain optional/final-entry items.
