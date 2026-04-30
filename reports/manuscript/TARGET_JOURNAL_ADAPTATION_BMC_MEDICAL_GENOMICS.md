# Target Journal Adaptation: BMC Medical Genomics

Date: 2026-05-01

Primary target:

- BMC Medical Genomics.

Backup targets:

- Frontiers in Oncology.
- Cancer Medicine.
- BMC Cancer only if the final framing avoids a biomarker-validation claim.

## Rationale

BMC Medical Genomics is a better first target than BMC Cancer for the current public-data route.

Reasons:

- The manuscript is a genomics and transcriptomics integration paper.
- The evidence chain uses spatial transcriptomics, Xenium, scRNA-seq, bulk expression, CoMMpass/GDC RNA-seq, and molecular annotation.
- The paper is not a wet-lab biomarker-validation study.
- The current claim is an adjusted association and cross-cohort reproducibility claim.

Risk with BMC Cancer:

- BMC Cancer has stricter language around computational-only biomarker work.
- It is safer to avoid submitting there before wet-lab or fully independent clinical validation is available.

## Required Format Changes

Use BMC-style biomedical headings:

- Title.
- Abstract.
- Keywords.
- Background.
- Results.
- Methods.
- Discussion.
- Conclusions.
- Availability of data and materials.
- Code availability.
- Declarations.
- References.

Current status:

- A BMC-target draft has been created:
  - `reports/manuscript/MANUSCRIPT_BMC_MEDICAL_GENOMICS_TARGET_DRAFT.md`
- The main heading `Introduction` has been converted to `Background`.
- A short `Conclusions` section has been added.
- References are now in Vancouver/numbered biomedical style.

## Claim Adaptation

Use:

- "spatially reproducible plasma-secretory program".
- "clinically associated axis".
- "adjusted association with OS".
- "program-level validation in Xenium".

Avoid:

- "validated prognostic biomarker".
- "clinical classifier".
- "treatment-selection marker".
- "PFS or treatment-response association".
- "direct TXNDC5 validation in GSE299193".

## Reference Style

Target style:

- Vancouver / numbered biomedical references.

Reference library:

- `references/REFERENCE_LIBRARY.tsv`
- `references/REFERENCES_VANCOUVER_NUMBERED_DRAFT.md`
- `references/downloaded_pdfs_manifest.tsv`

Downloaded full-text PDFs:

- Stored in `references/pdf`.
- Downloaded only from open public sources.

## Declarations To Complete Before Submission

Ethics approval and consent to participate:

- Draft language: not applicable because only public de-identified datasets were analyzed.

Consent for publication:

- Draft language: not applicable.

Availability of data and materials:

- Include GEO accessions GSE269875, GSE299193, GSE271107, GSE24080, and GSE2658.
- Include MMRF-COMMPASS/GDC open RNA-seq and clinical data.
- Include Skerget et al. NG2024 public supplementary tables.

Competing interests:

- Must be completed by the author before submission.

Funding:

- Must be completed by the author before submission.

Authors' contributions:

- Must be completed after the final author list is fixed.

## Next Target-Specific Work

1. Convert the Markdown draft into a BMC-ready DOCX.
2. Add declarations after author information is finalized.
3. Ensure every numbered citation is cited in-text.
4. Decide whether Fig. 6 is main or supplementary.
5. Run a final academic-paper-reviewer re-review after formatting.

## Official Sources Used

- BMC Medical Genomics aims and scope: https://bmcmedgenomics.biomedcentral.com/about
- BMC Medical Genomics manuscript preparation guidelines: https://bmcmedgenomics.biomedcentral.com/submission-guidelines/preparing-your-manuscript
- BMC Cancer manuscript preparation guidelines: https://bmccancer.biomedcentral.com/submission-guidelines/preparing-your-manuscript
