# Submission Remaining Items Before Final Upload

Date: 2026-05-01

Scope: BMC Medical Genomics submission package in `D:\二区\submission\bmc_medical_genomics_2026-05-01`.

## Blocking Items Before Clicking Final Submit

| Item | Current status | Where it appears | Required action |
|---|---|---|---|
| Corresponding author name | Not finalized in title page and cover letter | `TITLE_PAGE_DRAFT.md`; `COVER_LETTER_DRAFT.md`; `PORTAL_METADATA_COPY_PASTE.md`; `AUTHOR_AND_ORCID_STATUS.md` | Decide whether Zhuang Jiang is also the corresponding author. If yes, replace placeholders with `Zhuang Jiang`. |
| Corresponding author email | Placeholder remains | `TITLE_PAGE_DRAFT.md`; `COVER_LETTER_DRAFT.md`; `PORTAL_METADATA_COPY_PASTE.md` | Add the exact submission email. Do not submit while this field remains `[to be finalized before submission]`. |
| Corresponding author postal address | Placeholder remains in title page; portal draft has GDUPT address as candidate | `TITLE_PAGE_DRAFT.md`; `PORTAL_METADATA_COPY_PASTE.md` | Confirm final postal address. Candidate: Guangdong University of Petrochemical Technology (GDUPT), 139 Guandu 2nd Road, Maoming 525000, Guangdong, China. |
| GitHub release / commit hash / Zenodo DOI | Not created or confirmed | `DATA_AND_CODE_AVAILABILITY_DRAFT.md`; `PORTAL_METADATA_COPY_PASTE.md` | Optional but recommended: create a GitHub release or Zenodo archive. If created, replace the generic repository URL or add the DOI/release URL. |
| APC/payment source | Unknown | `PORTAL_METADATA_COPY_PASTE.md` | Decide APC payment route. Current portal guidance: APC payment source is unknown/to be confirmed by author. |
| Institutional agreement, waiver, or discount | Not checked in live portal | `PORTAL_METADATA_COPY_PASTE.md` | Check whether GDUPT, another institution, or a waiver/discount applies. |
| License choice | Not finalized | `PORTAL_METADATA_COPY_PASTE.md` | Select the live portal license option according to journal/institution requirement. Default journal open-access license can be used only after user confirmation. |
| Word/WPS line-number display | Metadata inserted, but headless render cannot prove line numbers display in Word/WPS | `PORTAL_METADATA_COPY_PASTE.md`; `SUBMISSION_PACKAGE_INDEX.md`; `EDITORIAL_QC_CHECKLIST.md` | Open `MANUSCRIPT_BMC_MEDICAL_GENOMICS_SUBMISSION_DRAFT.docx` in Word/WPS and visually confirm line numbers and page numbers. |
| Figure upload mapping | Files are prepared, but live portal upload must still be checked | `PORTAL_METADATA_COPY_PASTE.md`; `SUBMISSION_PACKAGE_INDEX.md` | Upload Fig. 1-8 using the correct file names and confirm the portal labels match the figure numbers. |

## Conditional Or Portal-Dependent Items

| Item | Current status | Where it appears | Required action if triggered |
|---|---|---|---|
| Suggested reviewers | Optional/not finalized | `PORTAL_METADATA_COPY_PASTE.md`; `PORTAL_REQUIREMENTS_CONFIRMATION_2026-05-01.md` | If the portal requires this, prepare 3-5 independent researchers in spatial transcriptomics, multiple myeloma genomics, or translational bioinformatics. Avoid same-institution researchers, collaborators, or obvious conflicts. |
| Opposed reviewers | None identified | `PORTAL_METADATA_COPY_PASTE.md`; `EDITORIAL_QC_CHECKLIST.md` | Enter `None` or leave blank if the portal allows. |
| Author contributions if additional authors are added | Current statement assumes single author | `MANUSCRIPT_BMC_MEDICAL_GENOMICS_TARGET_DRAFT.md`; `DECLARATIONS_DRAFT.md`; generated manuscript body | If any coauthor is added, revise author contributions and competing-interest/funding responsibility statements. |
| Combined reading-layout manuscript upload | Prepared for author review, not primary upload | `PORTAL_METADATA_COPY_PASTE.md`; `SUBMISSION_PACKAGE_INDEX.md` | Upload only if the live portal requests a combined manuscript with embedded figures. Otherwise use the editable main DOCX plus separate figures/tables. |

## Recommended Cleanup Before Upload

| Item | Current status | Where it appears | Recommended action |
|---|---|---|---|
| ORCID profile affiliation cleanup | ORCID screenshot appeared to contain a suspicious `Fo Guang Shan` employment entry | `AUTHOR_AND_ORCID_STATUS.md` | Correct ORCID employment/education entries so they match GDUPT, or at least avoid using the incorrect ORCID employment entry as manuscript affiliation. |
| Code package completeness | Current local package is organized and GitHub synchronization is being completed | `SUBMISSION_PACKAGE_INDEX.md`; `DATA_AND_CODE_AVAILABILITY_DRAFT.md` | Verify the repository contains current `scripts`, `analysis/manuscript_figures`, compact result TSVs, validation reports, and submission metadata. Do not upload large raw data unless intentionally archived elsewhere. |
| Old internal reports with historical status | Some older internal planning reports may contain outdated claims, such as “pushed to GitHub” | `reports/manuscript/*` | Use `SUBMISSION_PACKAGE_INDEX.md`, `DATA_AND_CODE_AVAILABILITY_DRAFT.md`, and this remaining-items file as the current source of truth. |

## Items Already Corrected In This Pass

- Chinese name source is now stored as `蒋壮` in current metadata files.
- Local path text in current submission Markdown files is now stored as `D:\二区` rather than mojibake text.
- Approximate word count on the title page was updated to 4,156 words excluding references.

## Current Decision

The manuscript is scientifically assembled and formatted for pre-submission review, but it is not ready for final portal submission until the blocking items above are resolved.
