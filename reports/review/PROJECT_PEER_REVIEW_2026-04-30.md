# Project Peer Review

Date: 2026-04-30

Mode: full academic-paper-reviewer style project review.

Target: SCI Q2 bioinformatics / translational oncology / tumor data-analysis manuscript.

## Reviewer Configuration

- Editor-in-Chief: translational oncology / multi-omics public-data journal fit.
- Reviewer 1, methodology: biostatistics, survival analysis, reproducibility.
- Reviewer 2, domain: multiple myeloma biology, CoMMpass, plasma-cell programs.
- Reviewer 3, translational perspective: clinical interpretability and figure/storyline quality.
- Devil's Advocate: tests whether the core novelty survives skeptical review.

## Editorial Decision

Current decision: Major Revision before submission.

Not reject. The project has a viable Q2 route because it now has spatial discovery, single-cell localization, GEO bulk support, CoMMpass/GDC OS/ISS support, and public NG2024 molecular annotation support.

Not submission-ready yet. The current manuscript package is behind the analysis state, the strongest new NG2024 result has not been integrated into the manuscript figures/text, and the clinical analysis still needs clearer boundaries or multivariable testing before the claim can be defended as translational rather than purely descriptive.

## Major Findings

### 1. Manuscript package is stale relative to the completed NG2024 result

Severity: major.

Evidence:

- `reports/manuscript/MANUSCRIPT_MAIN_TEXT_DRAFT.md` still describes a four-stage design ending at CoMMpass/GDC.
- `analysis/manuscript_figures/cross_cohort_evidence_table.tsv` contains no NG2024 molecular annotation evidence.
- `reports/planning/Q2_NO_MMRF_MAINLINE_PLAN.md` already records NG2024 as completed first-pass validation.

Impact:

The strongest newly added public molecular-risk layer is absent from the manuscript draft and evidence table. A reviewer reading the current manuscript would think the project still lacks cytogenetic / molecular-risk annotation depth.

Required fix:

- Add NG2024 as a fifth analysis layer in Abstract, Methods, Results, Discussion, figure legends, and cross-cohort evidence table.
- Update Fig. 1 and Fig. 5 or add a supplementary NG2024 molecular annotation figure.

### 2. CoMMpass clinical evidence is association-level, not independent prognostic validation

Severity: major.

Evidence:

- `scripts/14_commppass_gdc_validation.py` tests OS event with Mann-Whitney, ISS with Spearman, and OS with median-split log-rank.
- No Cox proportional hazards model is currently implemented.
- No adjustment for age, sex, ISS, 1q21, cytogenetic high-risk, or RNA subtype is currently implemented.

Impact:

The manuscript can claim "associated with OS and ISS", but cannot claim independent prognostic value or clinical classifier performance. If the manuscript wording drifts toward biomarker/classifier language, reviewers will challenge it.

Required fix:

- Either keep all language strictly at "association" level, or add multivariable Cox/logistic models after integrating NG2024 annotations.
- Minimum useful models:
  - OS Cox: plasma-secretory score + age + sex + ISS.
  - OS Cox with NG2024 covariates where available: + Cp_1q21_Call or Cytogenetic_High_Risk.
  - ISS/IMWG ordinal or binary models for risk association.

### 3. Spatial discovery remains underpowered and exploratory

Severity: major.

Evidence:

- GSE269875 spatial discovery has 3 controls and 6 MM samples.
- The main spatial p value is Mann-Whitney p=0.0256 for the plasma-secretory signature.
- The manuscript reports this as enrichment, but the statistical strength comes mostly from effect size and downstream validation, not from the small spatial cohort alone.

Impact:

A skeptical reviewer can argue that the spatial discovery is expected plasma-cell enrichment in MM, not a novel spatial discovery by itself.

Required fix:

- Explicitly frame GSE269875 as discovery-level.
- Avoid making the p=0.0256 result carry too much weight.
- Emphasize the cross-layer evidence chain and NG2024/CoMMpass support.
- Add GSE299193 second spatial validation if possible before submission.

### 4. GSE299193 is not yet a result, and one validation report is stale

Severity: major.

Evidence:

- `reports/validation/GSE299193_XENIUM_DOWNLOAD_STATUS.md` reports 8.42 GiB / 76.61 GiB downloaded.
- `reports/validation/GSE299193_XENIUM_VALIDATION_REPORT.md` still says 270,598,144 / 82,255,360,000 bytes.
- No GSE299193 expression validation result has been generated yet.

Impact:

The second spatial cohort cannot be claimed. The stale validation report creates internal inconsistency in the project record.

Required fix:

- Regenerate the GSE299193 status report before continuing.
- Do not mention second spatial validation as completed until the RAW tar is complete and `scripts/18_gse299193_xenium_validation.py` produces usable results.

### 5. NG2024 association figure mixes incompatible effect metrics

Severity: major for figure quality, moderate for science.

Evidence:

- `scripts/20_skerget_ng2024_molecular_annotation_validation.py` combines Kruskal H statistics, Spearman rho, and median differences into one `effect` field.
- `ng2024_top_molecular_annotation_associations.png` plots these heterogeneous effect values on the same y-axis.

Impact:

The figure visually overstates categorical Kruskal tests because H statistics around 90-144 are plotted next to correlations around 0.3. This is misleading even if the underlying p values are correct.

Required fix:

- Plot `-log10(FDR)` for ranking instead of raw effect.
- Use separate panels for:
  - RNA subtype categorical associations;
  - subtype probability correlations;
  - cytogenetic/copy-number binary comparisons.
- For effect panels, use comparable effect definitions only.

### 6. NG2024 key boxplot panels include weak or nonsignificant pairings

Severity: moderate.

Evidence:

- The NG2024 report highlights `Cytogenetic_High_Risk` vs `JCHAIN_z`, not vs `plasma_secretory_score_z`.
- The current boxplot script plots `Cytogenetic_High_Risk` vs `plasma_secretory_score_z`, where the audited result is weak.
- The WHSC1/t(4;14) panel is borderline rather than a strong molecular-risk result.

Impact:

The boxplot figure does not currently show the strongest evidence and may confuse the molecular-risk story.

Required fix:

- Replace weak panels with the strongest clinically relevant tested pairs:
  - Cp_1q21_Call vs plasma_secretory_score_z.
  - ISS_Stage vs plasma_secretory_score_z.
  - IMWG_Risk_Class vs plasma_secretory_score_z.
  - Cp_17p13_Call vs POU2AF1_z or clinical_subtype_module_score_z.

### 7. Single-cell validation is marker-inferred and does not distinguish malignant from normal plasma cells

Severity: moderate.

Evidence:

- The GSE271107 report states no author-provided fine cell-type labels were used.
- Annotation is marker-inferred coarse labeling.

Impact:

The scRNA result supports compartment localization, but not malignant plasma-cell specificity. Reviewers may ask whether the signal simply marks normal antibody-secreting plasma cells.

Required fix:

- Keep the claim as "plasma-cell compartment localization".
- If time permits, add a second scRNA dataset with author annotations or infer malignant plasma cells using CNV/clone signals.

### 8. External GEO microarray validation is useful but exploratory

Severity: moderate.

Evidence:

- GPL570 multi-probe genes are collapsed to the highest-variance probe.
- GSE24080 uses 24-month milestone endpoints, while GSE2658 uses available disease-related death and 1q21 annotations.

Impact:

These are supportive datasets, not definitive clinical validation. They should be described as external support and not over-weighted relative to CoMMpass/GDC and NG2024.

Required fix:

- Add probe-selection sensitivity or average-probe validation for key genes.
- Keep the main clinical weight on CoMMpass/GDC and NG2024.

## Reviewer Reports

### Editor-in-Chief

The paper has a plausible Q2 fit if framed as a public-data integrative translational analysis, not as a new clinical biomarker paper. The strongest editorial angle is now "spatial discovery plus cross-platform public validation of a plasma-secretory MM axis." The weakness is novelty: plasma-secretory biology is expected in MM. The manuscript must demonstrate that the value is the cross-cohort anchoring to OS, ISS, RNA subtype and copy-number/cytogenetic annotations.

### Methodology Reviewer

The pipeline is reproducible and most outputs are traceable to scripts. The largest methodological gap is survival modeling. Mann-Whitney OS-event tests and median-split log-rank curves are acceptable exploratory analyses, but insufficient for strong prognostic claims. The NG2024 validation adds valuable covariates and should be used to build adjusted models or at least stratified sensitivity analyses.

### Domain Reviewer

The TXNDC5 repositioning is appropriate. TXNDC5 should remain a localization candidate, while POU2AF1/XBP1/JCHAIN and the broader plasma-secretory score carry the clinical subtype story. The current biology is coherent, but the paper needs a sharper explanation of how this axis relates to known MM expression subtypes, 1q gain, PR subtype, and high-risk cytogenetic states.

### Translational Perspective Reviewer

The project can be publishable without wet lab validation if the claims stay bounded. The current draft needs stronger tables and cleaner figures. The cross-cohort evidence table should become a central asset, but it must include NG2024 and later GSE299193 if completed.

### Devil's Advocate

Strongest counter-argument: "This study rediscovers that MM samples contain more plasma-cell transcriptional signal, then finds that plasma-cell/secretory genes correlate with known MM risk features in bulk tumor data. The spatial and single-cell parts mainly localize expected plasma-cell biology rather than reveal a new mechanism."

Response strategy:

- Do not argue novelty as "plasma genes are high in MM."
- Argue novelty as a rigorously bounded public-data evidence chain:
  - spatial tissue-level discovery;
  - single-cell localization;
  - bulk cohort support;
  - CoMMpass OS/ISS association;
  - NG2024 RNA subtype/copy-number molecular annotation;
  - second spatial validation if GSE299193 completes.

## Revision Roadmap

Priority 1:

- Update manuscript draft and Fig. 1/Fig. 5/cross-cohort evidence table to include NG2024.
- Correct NG2024 plotting to avoid mixed effect-size axes.
- Add a concise claim-boundary table.

Priority 2:

- Add adjusted CoMMpass/NG2024 models if feasible.
- At minimum, test whether plasma_secretory_score_z remains associated with OS event after age, sex, ISS and 1q21/cytogenetic annotations.

Priority 3:

- Resume GSE299193 and complete second spatial validation.
- If it validates, promote it to Fig. 6; if weak, keep it as supplementary or state negative/partial validation.

Priority 4:

- Replace placeholder references with verified primary citations.
- Update Data Availability to include NG2024 public supplements.
- Clean stale GSE299193 validation status.

## Final Recommendation

Proceed. Do not abandon the project.

Current submission readiness: not ready.

Estimated state after Priority 1 fixes: credible Q2 manuscript draft.

Estimated state after Priority 1 plus adjusted models: stronger Q2 / possible lower-Q1 attempt depending on GSE299193 outcome.

