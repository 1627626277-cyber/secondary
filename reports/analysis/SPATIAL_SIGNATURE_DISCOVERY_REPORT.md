# Spatial Signature Discovery Report

Date: 2026-04-29

Script:

- `scripts/10_sample_aware_spatial_signatures.py`

Output directory:

- `analysis/spatial_candidate_signatures`

## 1. Purpose

This step converts the previous spot-level exploratory spatial clustering into a sample-aware candidate signature analysis.

The goal is to reduce the risk of spot-level pseudoreplication before moving into external single-cell and clinical transcriptomic validation.

## 2. Inputs

Main inputs:

- 9 human `GSE269875` processed Visium matrices.
- Previous spot-level cluster assignments from `analysis/spatial_preliminary/combined_spot_embedding_clusters.tsv.gz`.
- Previous spot-level QC fields, including UMI count, gene count, mitochondrial percentage, and spatial coordinates.

Human sample structure:

- Controls: `hHBM1`, `hHBM2`, `hHBM3`
- MM: `hMM1`, `hMM2`, `hMM3`, `hMM4`, `hMM5`, `hMM6`

## 3. Method summary

The script performed:

1. Per-spot 10,000-count normalization and `log1p` transformation.
2. Signature scoring for seven biological programs:
   - `plasma_secretory`
   - `myeloid_inflammatory`
   - `t_nk_cytotoxic_exhaustion`
   - `stromal_ecm`
   - `endothelial_angiogenic`
   - `erythroid_megak`
   - `cycling_proliferation`
3. Sample-level median signature scoring.
4. Sample-level gene mean expression and detection-rate calculation.
5. Within-sample high-vs-low spatial-region contrasts based on signature score quartiles.
6. Candidate gene ranking using:
   - MM-vs-control sample-level expression difference,
   - number of MM samples above the control median,
   - spatial-region enrichment,
   - region-level cross-sample consistency,
   - broad biological category.
7. Sensitivity checks:
   - all samples,
   - excluding low-spot `hMM1`,
   - strong-depth MM samples `hMM2` and `hMM3` plus controls.

## 4. Main outputs

Important output files:

- `analysis/spatial_candidate_signatures/sample_signature_scores.tsv`
- `analysis/spatial_candidate_signatures/signature_sensitivity_results.tsv`
- `analysis/spatial_candidate_signatures/candidate_spatial_signature_table.tsv`
- `analysis/spatial_candidate_signatures/candidate_spatial_signature_top100.tsv`
- `analysis/spatial_candidate_signatures/candidate_validation_shortlist.tsv`
- `analysis/spatial_candidate_signatures/gene_spatial_region_contrasts.tsv.gz`
- `analysis/spatial_candidate_signatures/sample_gene_mean_log_norm.tsv.gz`
- `analysis/spatial_candidate_signatures/sample_gene_pct_detected.tsv.gz`
- `analysis/spatial_candidate_signatures/sample_signature_score_heatmap.png`
- `analysis/spatial_candidate_signatures/signature_effects_all_samples.png`
- `analysis/spatial_candidate_signatures/top_candidate_genes_barplot.png`

## 5. Signature-level results

### 5.1 Plasma secretory signature

This is currently the strongest and most stable signal.

All-sample sensitivity:

- MM median score: `0.709`
- Control median score: `0.000`
- MM minus control: `0.709`
- Sample-level Cohen's d: `3.129`
- Mann-Whitney p value: `0.0256`

After excluding low-spot `hMM1`:

- MM minus control: `0.561`
- Cohen's d: `2.875`
- Mann-Whitney p value: `0.0325`

Interpretation:

- This is a robust MM-associated spatial program.
- It is biologically expected but useful as the anchor program for downstream validation.
- Novelty should not be claimed from canonical plasma markers alone; novelty must come from spatial organization, cross-dataset validation, and clinical association.

### 5.2 Stromal / ECM signature

This is the strongest secondary candidate program.

All-sample sensitivity:

- MM median score: `0.361`
- Control median score: `0.000`
- MM minus control: `0.361`
- Sample-level Cohen's d: `1.483`
- Mann-Whitney p value: `0.0878`

Interpretation:

- The effect is weaker than plasma-secretory but biologically plausible.
- Stromal/ECM genes may become a stronger translational angle if they validate in scRNA or bulk clinical cohorts.

### 5.3 Myeloid inflammatory signature

All-sample sensitivity:

- MM median score: `0.292`
- Control median score: `0.000`
- MM minus control: `0.292`
- Sample-level Cohen's d: `0.642`
- Mann-Whitney p value: `0.500`

Strong-depth subset:

- MM minus control: `0.817`
- Cohen's d: `1.558`

Interpretation:

- Myeloid/inflammatory signal exists but is more sample-dependent, especially influenced by high-depth or specific MM samples.
- This should be tested carefully in single-cell data before making manuscript claims.

### 5.4 T/NK exhaustion, endothelial, cycling

The current Visium discovery layer does not show strong sample-level separation for T/NK exhaustion or proliferation.

Interpretation:

- These programs should remain secondary exploratory tracks.
- They should not be central claims unless scRNA or external spatial validation provides stronger support.

## 6. Candidate gene results

The full ranked candidate table contains `17,963` genes after duplicate-gene and low-information filtering.

### 6.1 Plasma program candidates

High-priority plasma-program candidates for validation:

| Gene | Candidate score | MM minus control | Spatial region |
|---|---:|---:|---|
| `TXNDC5` | 6.764 | 1.750 | plasma_secretory |
| `POU2AF1` | 1.839 | 0.706 | plasma_secretory |
| `ITM2C` | 1.739 | 0.724 | plasma_secretory |
| `UBE2J1` | 1.626 | 0.668 | plasma_secretory |
| `PIM2` | 1.531 | 0.567 | plasma_secretory |
| `SEC11C` | 1.239 | 0.514 | plasma_secretory |
| `TENT5C` | 1.209 | 0.551 | plasma_secretory |
| `CD79A` | 1.183 | 0.705 | plasma_secretory |

Canonical plasma anchors:

- `JCHAIN`
- `IGHG1`
- `XBP1`
- `MZB1`
- `IGKC`
- `TNFRSF17`
- `IRF4`
- `PRDM1`
- `SDC1`
- `IGHM`
- `IGHA1`
- `SLAMF7`

Interpretation:

- Canonical plasma markers should be used as anchors and sanity checks.
- `TXNDC5`, `PIM2`, `TENT5C`, `POU2AF1`, and related plasma-program candidates are better suited for downstream validation than generic immunoglobulin markers alone.

### 6.2 Myeloid inflammatory candidates

Best current candidates:

| Gene | Candidate score | MM minus control | Spatial region |
|---|---:|---:|---|
| `S100A9` | 1.605 | 0.661 | myeloid_inflammatory |
| `S100A8` | 1.345 | 0.522 | myeloid_inflammatory |
| `CTSS` | 0.598 | 0.292 | myeloid_inflammatory |
| `LYZ` | 0.420 | 0.251 | myeloid_inflammatory |
| `TYROBP` | 0.172 | 0.131 | myeloid_inflammatory |

Interpretation:

- These candidates are biologically plausible but more sample-dependent than the plasma-secretory program.
- They need scRNA validation to confirm whether the signal reflects inflammatory monocyte/macrophage compartments rather than spot mixing.

### 6.3 Stromal / ECM candidates

Best current candidates:

| Gene | Candidate score | MM minus control | Spatial region |
|---|---:|---:|---|
| `COL1A1` | 1.540 | 0.519 | stromal_ecm |
| `COL3A1` | 1.141 | 0.358 | stromal_ecm |
| `SPARC` | 1.044 | 0.376 | stromal_ecm |
| `COL1A2` | 0.955 | 0.360 | stromal_ecm |
| `CXCL12` | 0.577 | 0.377 | stromal_ecm |
| `FN1` | 0.229 | 0.097 | stromal_ecm |
| `DCN` | 0.224 | 0.103 | stromal_ecm |

Interpretation:

- Stromal/ECM remodeling is a promising secondary direction.
- This may be valuable for translational framing if validated in non-plasma single-cell compartments.

### 6.4 Endothelial and erythroid/megakaryocyte candidates

Endothelial:

- `PECAM1`
- `ENG`
- `CLDN5`
- `VWF`
- `ESAM`

Erythroid/megakaryocyte:

- `HBB`
- `PPBP`
- `HBA2`
- `ALAS2`
- `ITGA2B`

Interpretation:

- These are currently supporting microenvironmental programs, not primary manuscript claims.

## 7. Current biological interpretation

The current GSE269875 human discovery layer supports this working model:

1. The strongest reproducible difference between MM and control spatial sections is a plasma-secretory / unfolded-protein-response-like program.
2. A stromal/ECM remodeling program is present and may provide a more interesting microenvironmental validation direction.
3. Myeloid inflammatory markers are present but need careful validation because the current effect is more sample-dependent.
4. T/NK exhaustion is not strong enough in this first sample-aware Visium pass to be a central claim.

## 8. Limitations

Current limitations:

- Only 3 control and 6 MM spatial samples are available in the discovery layer.
- Sample-level p values should be treated as exploratory because sample size is small.
- The candidate gene table is a prioritization table, not final differential-expression proof.
- Some high-scoring genes such as `B2M`, `VIM`, `TMSB4X`, `EEF2`, and `UBA52` are broad-expression genes and should be reviewed carefully before use as manuscript candidates.
- External scRNA and bulk/clinical validation are required before strong publication claims.

## 9. Go / no-go decision after this step

Go:

- The project has a stable primary plasma-secretory spatial program.
- The project has plausible secondary stromal/ECM and myeloid/inflammatory programs.
- Candidate shortlists are now available for external validation.

Condition:

- The project remains publishable only if external validation supports at least one nontrivial signature beyond canonical plasma-cell markers.

No-go trigger:

- If scRNA and bulk/clinical datasets only validate generic plasma markers and do not support stromal, myeloid, or clinically associated signatures, the manuscript will be much weaker for SCI Q2.

## 10. Recommended next step

Proceed to single-cell validation first.

Priority:

1. Use `GSE271107` or `GSE223060` processed scRNA data.
2. Validate `plasma_secretory`, `stromal_ecm`, and `myeloid_inflammatory` signatures by cell type.
3. Test whether candidate genes map to malignant plasma cells, myeloid cells, stromal/MSC cells, endothelial cells, or mixed compartments.
4. Only after this, move to bulk/clinical validation.
