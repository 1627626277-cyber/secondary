# Stage 2 Full Internal Review After Methods Expansion

Date: 2026-04-30

Reviewed file:

- `reports/manuscript/MANUSCRIPT_STAGE2_POLISHED_Q2_DRAFT.md`

Review mode:

- Academic-paper-reviewer full internal review.
- Perspectives: editor, methodology reviewer, myeloma domain reviewer, translational bioinformatics reviewer, and devil's advocate.

## Editorial Decision

Decision:

- Major revision before submission.

Q2 potential:

- Yes, the project remains viable for an SCI Q2 bioinformatics or translational oncology journal.

Reason:

- The evidence chain is now coherent.
- The second spatial validation cohort materially reduces the original spatial sample-size weakness.
- The adjusted CoMMpass/NG2024 model strengthens the clinical association.
- Remaining problems are mainly manuscript polish, citation finalization, and claim calibration.

## Reviewer 1: Editor

Assessment:

- The manuscript has a clear and bounded story.
- It is stronger than a simple single-cohort bioinformatics analysis.
- The current narrative is suitable for a Q2 target if formatted tightly.

Major concerns:

- The title should avoid implying clinical deployment.
- The Abstract is clear but still dense.
- References remain preliminary.
- The manuscript needs target-journal formatting before external submission.

Required revisions:

- Convert reference anchors into a formal bibliography.
- Add a limitations paragraph in the Abstract or final Discussion sentence.
- Decide whether Fig. 6 is main or supplementary based on journal limits.

## Reviewer 2: Methodology

Assessment:

- The revised Methods are materially improved.
- Script paths and software versions are now present.
- Numeric traceability is documented.

Major concerns:

- FDR families need exact definitions in one paragraph.
- Module score construction should be formalized with an equation or explicit sentence.
- Complete-case handling should be stated for each validation layer.
- Survival modeling needs proportional hazards assumptions reported or acknowledged.

Required revisions:

- Add a short "Statistical analysis" subsection.
- Define z-score module scoring precisely.
- Add complete-case rules for NG2024 Table 7 and adjusted models.
- Add a note that PH assumptions were not yet fully stress-tested.

## Reviewer 3: Myeloma Domain

Assessment:

- The biological framing is plausible.
- POU2AF1, XBP1, and JCHAIN are appropriate for secretory plasma-cell biology.
- The manuscript correctly avoids overclaiming TXNDC5.

Major concerns:

- Plasma-cell secretory biology is not novel by itself.
- The novelty depends on cross-platform spatial-to-clinical linkage.
- R-ISS, PFS, and treatment-response validation remain absent.

Required revisions:

- Emphasize the spatial-to-clinical integration as the contribution.
- Keep TXNDC5 as a localization candidate.
- State that fuller MMRF clinical files would be needed for PFS and treatment-response endpoints.

## Reviewer 4: Translational Bioinformatics

Assessment:

- The project has adequate computational breadth for Q2.
- It now includes spatial, Xenium, scRNA, GEO bulk, CoMMpass/GDC, and NG2024 molecular annotation.

Major concerns:

- External bulk directionality is not uniform.
- The manuscript should avoid implying that every cohort supports the same direction.
- Figure legends need panel-level detail.

Required revisions:

- Use "associated with" for GSE2658 1q21 results.
- Add panel-level legends for Fig. 1-6.
- Add a supplementary table with script and result-file mapping.

## Reviewer 5: Devil's Advocate

Assessment:

- The strongest attack is that the axis may reflect plasma-cell abundance.
- A second attack is that clinical associations may mirror known high-risk biology.
- A third attack is that public-data integration can look post hoc.

Countermeasures:

- Present the study as a reproducible integrative analysis, not a new biomarker product.
- Use adjusted models as association support, not causal proof.
- Keep claim boundaries explicit throughout Abstract, Results, and Discussion.
- Add a sensitivity paragraph discussing plasma-cell abundance as a possible confounder.

## Current Readiness

Scientific evidence:

- 85%.

Manuscript structure:

- 78%.

Methods reproducibility:

- 75%.

Citation readiness:

- 50%.

Figure readiness:

- 75%.

Submission readiness:

- 68%.

## Blocking Items Before Submission

1. Finalize citations and reference style.
2. Add a formal Statistical Analysis subsection.
3. Expand figure legends panel by panel.
4. Add proportional hazards assumption status.
5. Add plasma-cell abundance confounding as a limitation.
6. Choose a target journal and adapt formatting.

## Bottom Line

The project should continue into manuscript revision.

The current public-data route is enough for a Q2 attempt after revision.

Full MMRF clinical access would strengthen the paper, but it is no longer required for the main Q2 route.
