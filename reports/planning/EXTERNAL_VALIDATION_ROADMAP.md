# External Validation Roadmap for SCI Q2 Submission

Project path: `D:\二区`
Date: 2026-04-28
Target: SCI Q2 bioinformatics / translational medicine / tumor data-analysis journal

## Executive Decision

The revised project can support an SCI Q2-oriented manuscript if the evidence chain is strengthened beyond the current GSE269875 spatial re-analysis.

Recommended structure:

1. Main discovery: GSE269875 human Visium bone marrow spatial transcriptomics.
2. Single-cell reference and validation: GSE223060 plus GSE271107 and selected immune/stromal single-cell cohorts.
3. Bulk / clinical validation: MMRF CoMMpass as the primary clinical-transcriptomic validation cohort; GSE24080/GSE2658 as supplementary microarray prognosis datasets if needed.
4. External spatial validation: GSE299193 human Xenium bone marrow trephine spatial dataset as a high-value, second-stage validation dataset.

Updated direction after first-pass GSE24080/GSE2658 validation:

- The manuscript should not be built around a single-gene `TXNDC5` prognostic claim.
- The stronger route is an MM bone marrow `plasma_secretory` clinical-subtype axis.
- `TXNDC5` should be used as a spatial/single-cell localization candidate within the axis.
- `POU2AF1`, `XBP1`, and `JCHAIN` should carry the clinical subtype / risk-association validation layer.

The first three directions should be treated as mandatory for Q2 competitiveness. The fourth direction is strong but heavier; use it after the plasma-secretory subtype axis and candidate marker set are stable.

## Direction 1: External Bulk / scRNA Transcriptome Validation

Priority: mandatory

Purpose:

- Verify whether spatially derived candidate genes and niche signatures are detectable in independent transcriptomic cohorts.
- Test whether candidate genes are plasma-cell specific, immune/stromal-associated, or mixed microenvironment signals.
- Reduce reviewer concern that findings are specific to one spatial dataset.

Primary datasets:

- MMRF CoMMpass / MMRF-COMMPASS via NCI GDC: open clinical and RNA-seq gene expression quantification are available; protected raw BAM requires dbGaP.
- GSE24080: 559 Affymetrix expression profiles from newly diagnosed MM bone marrow plasma cells with two-year OS/EFS milestone information.
- GSE2658: 559 pre-treatment MM bone marrow plasma-cell profiles linked to outcome after stem-cell transplantation.

Analyses:

- Candidate gene expression distribution in CoMMpass and GSE24080/GSE2658.
- Signature score construction from spatial candidate genes, prioritizing a `plasma_secretory` subtype axis rather than a single-gene marker.
- Separate marker roles:
  - `TXNDC5`: spatial and single-cell plasma localization marker.
  - `POU2AF1`, `XBP1`, `JCHAIN`: clinical subtype / risk-association markers.
- Association with risk groups, ISS/R-ISS if available, event-free survival, progression-free survival, and overall survival.
- ssGSEA/GSVA or rank-based module scores for immune exhaustion, inflammatory stroma, plasma-cell density, myeloid activation, angiogenesis, and ECM remodeling.

Expected figures:

- Candidate gene validation heatmap across independent cohorts.
- Kaplan-Meier curves for high vs low spatial-signature score.
- Forest plot showing effect consistency across CoMMpass and GEO microarray cohorts.
- Correlation matrix between spatial signatures and immune/stromal/bulk deconvolution signatures.

Risks:

- GSE24080/GSE2658 are purified CD138+ plasma-cell microarrays, so they validate malignant plasma-cell signals better than full microenvironment signals.
- CoMMpass processed expression is ideal for clinical association but may require registration or GDC/portal workflow.

## Direction 2: Additional Public MM Single-Cell Dataset

Priority: mandatory

Purpose:

- Strengthen cell-type annotation and candidate-marker attribution.
- Validate key cell states outside GSE223060.
- Support spatial deconvolution references and marker panels for plasma cells, exhausted T cells, myeloid cells, stromal fibroblasts/MSC, endothelial cells, and erythroid/megakaryocyte compartments.

Primary datasets:

- GSE223060: scRNA-seq of 53 BMMC samples from 41 MM patients, already suitable as a major reference.
- GSE271107: 19 bone marrow aspirate scRNA-seq samples including healthy donors, MGUS, SMM, and newly diagnosed MM; raw H5 package is about 389.9 MB.
- E-MTAB-9139: paired scRNA-seq of non-hematopoietic and immune microenvironment from newly diagnosed MM patients and non-cancer controls; useful for inflammatory stromal-cell validation.
- Published MMRF Immune Atlas / rapid-progressor immune scRNA cohorts can be used if processed data access is practical.

Analyses:

- Build a unified marker table from GSE223060 + GSE271107.
- Validate candidate gene cell-type specificity with dot plots and pseudo-bulk comparisons.
- Identify conserved cell-state signatures: exhausted T/NK, inflammatory monocyte/macrophage, stromal inflammatory MSC, angiogenic/endothelial, plasma-cell high-density state.
- Use single-cell-derived signatures as references for GSE269875 deconvolution / label transfer.

Expected figures:

- UMAP or reference atlas with major cell annotations.
- Dot plot of candidate genes across cell types and datasets.
- Cross-dataset marker consistency heatmap.
- Signature activity violin plots across HD/MGUS/SMM/MM if GSE271107 quality is adequate.

Risks:

- Cross-dataset single-cell integration may produce batch effects; the safer route is pseudo-bulk and marker-level validation rather than forcing a single combined atlas.
- Some Immune Atlas data may require MMRF Virtual Lab or controlled-access handling.

## Direction 3: Clinical Prognosis / Disease-Stage Association

Priority: mandatory

Purpose:

- Connect spatial molecular findings to clinical meaning.
- Provide the part reviewers often expect from bioinformatics/translational MM papers: prognosis, stage, risk, treatment-response, or progression association.

Primary route:

- Use CoMMpass as the first choice because it has RNA-seq, clinical variables, longitudinal information, and standard MM risk information.
- Validate the plasma-secretory clinical-subtype axis and the `POU2AF1/XBP1/JCHAIN` risk-linking module.
- Keep `TXNDC5` as a spatial/single-cell candidate unless an additional cohort supports a reproducible clinical association.

Secondary route:

- Use GSE24080 for OS/EFS milestone validation.
- Use GSE2658 for outcome-linked MM expression validation if processed matrix and annotations are usable.
- Use GSE271107 for stage trajectory from healthy donor -> MGUS -> SMM -> newly diagnosed MM, even though sample size is smaller.

Analyses:

- Define one or two spatially derived signatures, not too many:
  - MM plasma-secretory subtype score.
  - Optional immune-suppressed/inflammatory microenvironment score.
- Test association with:
  - ISS/R-ISS or high-risk genomic groups where available.
  - PFS/OS/EFS.
  - relapse/progression or treatment response variables if accessible.
- Explicitly report that `TXNDC5` is not yet a validated independent prognostic marker if the weak first-pass clinical result persists.
- Use univariate and multivariable Cox models where enough clinical covariates exist.
- Avoid overclaiming; frame as clinical association and risk stratification signal.

Expected figures:

- KM curves for signature-high vs signature-low patients.
- Cox forest plot.
- Boxplots of signature score across ISS/R-ISS or disease stages.
- Nomogram is optional; only add if the data quality is strong.

Risks:

- A clinical model built only from public retrospective data is not a clinical-grade predictor.
- If CoMMpass registration slows progress, use GSE24080 as a fast initial clinical validation.

## Direction 4: External Spatial Transcriptomics Dataset

Priority: high-value optional, staged after current pipeline stabilizes

Purpose:

- Provide direct external spatial validation, which is the strongest answer to reviewer concern that GSE269875-specific spatial patterns may not generalize.

Primary external candidate:

- GSE299193: human bone marrow trephine Xenium spatial transcriptomics; 22 samples, including controls, MGUS, SMM, active MM, and relapse myeloma. Raw package is about 76.6 GB.

How to use it:

- Do not mix Xenium raw analysis into the first discovery pass.
- First finish GSE269875 human Visium analysis and identify a small candidate signature.
- Then use GSE299193 to validate:
  - candidate gene spatial localization,
  - plasma-cell / stromal ecosystem organization,
  - immune-suppressed niche markers,
  - disease-stage gradient from control/MGUS/SMM/MM/relapse.

Expected figures:

- External Xenium spatial maps for top candidate genes.
- Cell-type neighborhood enrichment around plasma-cell-rich regions.
- Stage-wise signature score boxplots.
- Concordance table between Visium discovery and Xenium validation.

Risks:

- 76.6 GB download is manageable on the current D drive but should be staged because current free space is about 385.5 GiB.
- Xenium is targeted-panel, single-cell-resolution spatial data; it is not directly equivalent to Visium whole-transcriptome spots.
- The validation question must be narrow: confirm candidate localization and cell neighborhoods, not rerun the entire discovery workflow.

## Implementation Schedule

Phase A: Finish Current Foundation

- Complete sampled species QC for all nine GSE269875 human mainline samples.
- Build clean human-only manifest.
- Start processed Visium matrix acquisition / reconstruction for GSE269875 human samples.

Phase B: Discovery on GSE269875

- QC spots, normalize, and cluster each human spatial section.
- Annotate plasma-cell-rich, immune-rich, stromal/vascular, erythroid/megakaryocyte areas.
- Run differential expression by region and MM vs healthy control.
- Generate candidate genes and signatures.

Phase C: Single-Cell Validation

- Download processed GSE223060 and GSE271107 matrices first.
- Build marker reference and validate candidate-gene cell-type specificity.
- Use pseudo-bulk/dot-plot validation rather than forcing all datasets into one integrated atlas at the beginning.

Phase D: Bulk / Clinical Validation

- Start with GSE24080 for fast survival-linked validation.
- In parallel, set up CoMMpass access through GDC/MMRF route.
- Test candidate signatures against OS/EFS/PFS/risk groups.

Phase E: External Spatial Validation

- Only after a stable shortlist exists, download GSE299193.
- Validate a focused set of genes/signatures and spatial neighborhoods.

## Storage Plan

Current D drive free space checked on 2026-04-28:

- Free: about 385.5 GiB.
- Current largest folders:
  - `sra_cache`: about 10.41 GiB.
  - `qc_species_hHBM1`: about 1.81 GiB.
  - `qc_species_hHBM2`: about 1.79 GiB.
  - `qc_species_hMM1`: about 0.87 GiB.
  - `references` + `blastdb`: about 3.11 GiB.

Storage decision:

- 300 GiB was a safety threshold for full raw FASTQ workflows, not the amount we intend to consume immediately.
- The revised staged plan is compatible with current storage if we avoid bulk full FASTQ extraction and prefer processed matrices where available.
- GSE299193 alone is about 76.6 GB compressed; after extraction it may require substantially more. Download it only after the core analysis has narrowed candidate signatures.

## Go / No-Go Criteria

Go:

- At least 8/9 human GSE269875 samples pass human sequence-level QC.
- Spatial discovery yields reproducible MM-vs-control or plasma-cell-density-associated signatures.
- At least one single-cell cohort confirms cell-type attribution.
- At least one clinical/bulk cohort supports candidate score association with disease stage, risk, or outcome.

Conditional go:

- If GSE269875 spatial signal is weaker than expected, reposition manuscript toward "spatial atlas / microenvironment characterization with external transcriptomic support" rather than a prognostic-biomarker paper.

No-go for Q2:

- If species QC fails broadly or the human spatial matrices cannot be reconstructed/used.
- If candidate genes cannot be attributed to plausible cell types and show no support in bulk or scRNA external data.

## Source Notes

- GSE269875: current discovery spatial dataset; GEO reports human and mouse Visium bone marrow MM spatial transcriptomics.
- GSE223060: MM scRNA-seq reference with 53 BMMC samples from 41 patients.
- GSE271107: 19 bone marrow scRNA-seq samples across healthy donor, MGUS, SMM, and newly diagnosed MM.
- MMRF CoMMpass / MMRF-COMMPASS: large longitudinal MM genomic-clinical dataset with open RNA-seq gene expression quantification and clinical/biospecimen data via GDC; protected raw sequencing requires dbGaP.
- GSE24080/GSE2658: large MM plasma-cell microarray cohorts with outcome-linked annotations.
- GSE299193: human MM bone marrow trephine Xenium spatial transcriptomics external validation candidate.

## Source Links Checked

- GSE269875: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269875
- GSE223060: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE223060
- GSE271107: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE271107
- GSE24080: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE24080
- GSE2658: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE2658
- MMRF CoMMpass via NCI GDC: https://gdc.cancer.gov/about-gdc/contributed-genomic-data-cancer-research/foundation-medicine/multiple-myeloma-research-foundation-mmrf
- GSE299193 indexed GEO dataset page: https://www.omicsdi.org/dataset/geo/GSE299193
- GSE299193 associated article: https://pubmed.ncbi.nlm.nih.gov/40643106/
