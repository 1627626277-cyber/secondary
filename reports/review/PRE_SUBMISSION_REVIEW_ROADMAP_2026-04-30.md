# Pre-Submission Review Roadmap

Date: 2026-04-30

Review target:

- `reports\manuscript\MANUSCRIPT_MAIN_TEXT_Q2_POLISHED_PASS1.md`
- `analysis\manuscript_figures\fig1-fig6`
- `analysis\manuscript_figures\cross_cohort_evidence_table.tsv`

## Reviewer Configuration

Editor-in-Chief:

- Translational hematology / computational oncology editor.
- Main concern: whether the manuscript is more than expected plasma-cell biology.

Reviewer 1, Methods and Statistics:

- Focus: cohort joins, FDR handling, survival modeling, covariate adjustment, panel-gene limitations.

Reviewer 2, Multiple Myeloma Biology:

- Focus: biological novelty, MM subtype/risk interpretation, TXNDC5/POU2AF1/XBP1/JCHAIN framing.

Reviewer 3, Spatial and Single-Cell Genomics:

- Focus: spatial reproducibility, Xenium panel coverage, cell-type annotation robustness.

Devil's Advocate:

- Focus: strongest rejection arguments, overclaiming, expected biology, public-data circularity.

## Editorial Decision Simulation

Current simulated decision:

- Major revision before submission.

Reason:

- The evidence chain is now strong enough for a Q2 attempt, especially after GSE299193.
- The manuscript still requires citation integrity, figure polish, and tighter methods detail before it should be sent to a journal.

## Major Issues To Fix Before Submission

### 1. Citation Integrity Is Not Yet Submission-Ready

Severity: Critical before submission.

The manuscript currently has reference anchors, not verified formal citations. This must be converted to a complete reference list with DOI/PMID/GEO accession verification. Do not submit until all dataset and method references are resolved.

Action:

- Build `REFERENCES_VERIFIED.md` or BibTeX.
- Verify GSE269875, GSE299193, GSE271107, GSE24080, GSE2658, GDC MMRF-COMMPASS, MMRF CoMMpass, and Skerget NG2024 from primary sources only.

### 2. Methods Need More Reproducibility Detail

Severity: Major.

The current Methods section is readable but still too compressed for reproducible bioinformatics. It should specify exact score formulas, FDR family definitions, survival-model package/function, sample inclusion rules, and how missing genes were handled in each platform.

Action:

- Add a subsection: `Signature scoring and missing-gene handling`.
- Add a subsection: `Statistical analysis`.
- Add explicit statement that GSE299193 scores used panel-covered genes only.

### 3. GSE299193 Should Be Framed Precisely

Severity: Major.

GSE299193 is a strong addition, but it cannot validate TXNDC5, JCHAIN, or SDC1. The manuscript currently states this correctly. This boundary must also appear in Fig.6 legend, Results, Discussion, and evidence table.

Action:

- Keep Fig.6 as main if the target journal allows six figures.
- If figure count is limited, move Fig.6 to Supplementary Fig.1 but mention it in the main Results.

### 4. TXNDC5 Claim Needs Conservative Language

Severity: Major.

The strongest clinical construct is the plasma-secretory axis, not TXNDC5 alone. TXNDC5 should not appear in the title and should not be presented as the central prognostic biomarker.

Action:

- Keep title centered on plasma-secretory program.
- Use TXNDC5 as a localization candidate and supporting marker.

### 5. Need One Clean Summary Table For Reviewers

Severity: Moderate.

The cross-cohort evidence table is useful but should be converted into a manuscript-ready Table 1 or Supplementary Table 1 with columns that reviewers can scan quickly.

Action:

- Convert `cross_cohort_evidence_table.tsv` into a formatted table.
- Add claim level: discovery, spatial validation, localization, external validation, clinical validation, adjusted model.

## Minor Issues

- Abstract is strong but long; target-journal word limit may require cutting.
- Figure legends need panel-by-panel descriptions, not only general descriptions.
- Methods should state whether tests were two-sided.
- Use consistent names: `RM` should be defined as relapsed multiple myeloma.
- Use consistent terminology: `plasma-secretory program`, `plasma-secretory axis`, and `clinical subtype module` should not be used interchangeably without definitions.

## Current Strengths

- Multi-layer public-data design is now coherent.
- GSE299193 removes the most obvious second-spatial-cohort weakness.
- CoMMpass/GDC sample size is strong.
- NG2024 public annotations add molecular-risk credibility.
- Adjusted Cox model directly addresses a likely reviewer objection.

## Current Weaknesses

- No PFS/treatment-response validation.
- No wet-lab validation.
- Single-cell malignant/normal plasma distinction is marker-inferred rather than author-curated malignant annotation.
- Some cohorts are microarray-based and platform heterogeneous.
- Formal citations are incomplete.

## Recommended Next Stage

Proceed to Stage 2.5 Integrity Verification before another full rewrite.

Immediate tasks:

1. Verify and format references.
2. Add reproducibility details to Methods.
3. Convert evidence table into manuscript-ready Table 1.
4. Add panel-specific figure legends.
5. Run a second reviewer pass after those fixes.
