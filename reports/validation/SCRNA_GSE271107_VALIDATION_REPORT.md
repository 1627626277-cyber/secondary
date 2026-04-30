# GSE271107 Single-Cell Validation Report

Date: 2026-04-29

Script:

- `scripts/11_gse271107_scrna_validation.py`

Output directory:

- `analysis/scrna_gse271107_validation`

Data source:

- GEO FTP: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE271nnn/GSE271107/suppl/`

## 1. Purpose

This step validates the spatially derived candidate signatures from `GSE269875` in an independent public MM single-cell RNA-seq dataset, `GSE271107`.

Primary validation question:

- Do the spatially derived signatures map to plausible single-cell compartments and disease stages?

## 2. Dataset

Downloaded file:

- `external_scRNA/GSE271107/GSE271107_RAW.tar`
- File size: `408,852,480` bytes

Extracted files:

- 19 H5 files
- 5 healthy donor samples
- 6 MGUS samples
- 4 SMM samples
- 4 newly diagnosed MM samples

After QC:

- Total cells retained: `127,528`

QC filters:

- cells with at least 200 detected genes,
- cells with at least 500 UMIs,
- mitochondrial percentage at most 25%.

## 3. Analysis method

Because this first-pass validation uses the GEO H5 matrices directly, no author-provided fine cell-type labels were used.

Instead, the script performed marker-inferred coarse annotation using canonical marker programs:

- plasma cell,
- B cell,
- T/NK cell,
- myeloid cell,
- erythroid cell,
- megakaryocyte/platelet,
- stromal-like,
- endothelial-like,
- low-marker cells.

This is sufficient for first-pass compartment validation, but it should not be treated as final curated scRNA annotation.

Spatial signatures tested:

- `plasma_secretory`
- `myeloid_inflammatory`
- `t_nk_cytotoxic_exhaustion`
- `stromal_ecm`
- `endothelial_angiogenic`
- `erythroid_megak`
- `cycling_proliferation`

## 4. Main outputs

Important output files:

- `analysis/scrna_gse271107_validation/gse271107_cell_signature_scores.tsv.gz`
- `analysis/scrna_gse271107_validation/gse271107_sample_qc_signature_summary.tsv`
- `analysis/scrna_gse271107_validation/gse271107_signature_by_stage.tsv`
- `analysis/scrna_gse271107_validation/gse271107_signature_by_celltype.tsv`
- `analysis/scrna_gse271107_validation/gse271107_signature_by_stage_celltype.tsv`
- `analysis/scrna_gse271107_validation/gse271107_candidate_gene_by_sample.tsv`
- `analysis/scrna_gse271107_validation/gse271107_candidate_gene_by_sample_celltype.tsv`
- `analysis/scrna_gse271107_validation/gse271107_celltype_composition_by_stage.png`
- `analysis/scrna_gse271107_validation/gse271107_signature_by_celltype_heatmap.png`
- `analysis/scrna_gse271107_validation/gse271107_signature_by_stage.png`
- `analysis/scrna_gse271107_validation/gse271107_candidate_gene_dotplot.png`

## 5. Cell composition summary

Marker-inferred cell composition by disease stage:

| Stage | Cells | Plasma cells | Plasma fraction | Myeloid fraction | T/NK fraction | Erythroid fraction |
|---|---:|---:|---:|---:|---:|---:|
| HD | 27,239 | 1,463 | 0.0537 | 0.3120 | 0.1083 | 0.4506 |
| MGUS | 38,339 | 1,016 | 0.0265 | 0.2269 | 0.3246 | 0.3565 |
| SMM | 32,804 | 649 | 0.0198 | 0.1766 | 0.2892 | 0.4351 |
| MM | 29,146 | 4,879 | 0.1674 | 0.1894 | 0.1859 | 0.3608 |

Interpretation:

- MM samples show a higher marker-inferred plasma-cell fraction than HD/MGUS/SMM.
- This supports the use of GSE271107 as a first external validation dataset for plasma-cell-associated spatial signatures.

## 6. Signature validation

### 6.1 Plasma-secretory signature

Median signature score by disease stage:

| Stage | Median plasma-secretory score |
|---|---:|
| HD | 0.0797 |
| MGUS | 0.0809 |
| SMM | 0.0903 |
| MM | 0.1487 |

Median signature score by marker-inferred cell type:

| Cell type | Median plasma-secretory score |
|---|---:|
| plasma_cell | 1.3388 |
| b_cell | 0.1596 |
| endothelial_like | 0.1473 |
| t_nk_cell | 0.1337 |
| myeloid_cell | 0.0799 |
| stromal_like | 0.0691 |

Interpretation:

- The plasma-secretory signature maps strongly to marker-inferred plasma cells.
- MM samples show the highest overall stage-level plasma-secretory score.
- This provides external single-cell support for the strongest GSE269875 spatial signature.

### 6.2 Key plasma-program candidate genes

Selected gene-level results:

| Gene | Strongest cell compartment | Mean expression in strongest compartment | Detection in strongest compartment | Stage pattern |
|---|---|---:|---:|---|
| `TXNDC5` | plasma_cell | 2.1958 | 0.9486 | highest in MM |
| `JCHAIN` | plasma_cell | 2.6867 | 0.7927 | highest in MM |
| `MZB1` | plasma_cell | 2.5314 | 0.9781 | highest in MM |
| `XBP1` | plasma_cell | 1.5620 | 0.9278 | highest in MM |
| `POU2AF1` | plasma_cell / B cell | 0.4401 in plasma cells | 0.5333 | highest in MM |
| `PIM2` | plasma_cell | 0.3063 | 0.4474 | highest in MM |
| `TENT5C` | plasma_cell / erythroid | 0.6877 in plasma cells | 0.6159 | higher in MM/SMM than HD/MGUS |

Interpretation:

- `TXNDC5` is the strongest current cross-platform candidate because it is spatially enriched, plasma-cell associated in scRNA, highly detected in plasma cells, and higher in MM-stage cells.
- `MZB1`, `JCHAIN`, and `XBP1` validate the plasma-cell biology but are canonical anchors, not novel claims by themselves.
- `PIM2`, `POU2AF1`, and `TENT5C` are useful secondary validation candidates.

### 6.3 Myeloid-inflammatory signature

Median myeloid-inflammatory score by marker-inferred cell type:

| Cell type | Median myeloid-inflammatory score |
|---|---:|
| myeloid_cell | 2.7156 |
| endothelial_like | 0.2424 |
| t_nk_cell | 0.2082 |
| b_cell | 0.1759 |
| stromal_like | 0.1568 |
| plasma_cell | 0.1462 |

Selected gene-level results:

| Gene | Strongest cell compartment | Mean expression in strongest compartment | Detection in strongest compartment |
|---|---|---:|---:|
| `S100A9` | myeloid_cell | 4.5231 | 0.9687 |
| `S100A8` | myeloid_cell | 3.8319 | 0.9187 |
| `CTSS` | myeloid_cell | 2.9864 | 0.9683 |

Interpretation:

- The myeloid candidates are clearly myeloid-cell associated in GSE271107.
- However, stage-level myeloid-inflammatory score is not higher in MM than HD in this dataset.
- Therefore, this validates cell-type attribution but does not yet validate MM-stage enrichment.
- Myeloid candidates should remain secondary until validated in another scRNA dataset or clinical cohort.

### 6.4 Stromal / ECM signature

Median stromal/ECM score by marker-inferred cell type:

| Cell type | Median stromal/ECM score |
|---|---:|
| stromal_like | 2.2036 |
| megakaryocyte_platelet | 0.2216 |
| other major compartments | 0.0000 |

Selected gene-level results:

| Gene | Strongest cell compartment | Mean expression in strongest compartment | Detection in strongest compartment |
|---|---|---:|---:|
| `COL1A1` | stromal_like | 2.1262 | 0.7919 |
| `COL3A1` | stromal_like | 2.5703 | 0.8828 |
| `CXCL12` | stromal_like | 4.5140 | 1.0000 |

Interpretation:

- Stromal/ECM genes map correctly to marker-inferred stromal-like cells.
- But only 30 stromal-like cells were detected across this BMMC dataset.
- GSE271107 is therefore not sufficient as the main stromal validation dataset.
- Stromal/ECM validation should use another dataset with stronger non-hematopoietic marrow microenvironment coverage or an external spatial dataset.

### 6.5 T/NK exhaustion and proliferation

The T/NK signature maps to marker-inferred T/NK cells, but the stage-level trend is not stronger in MM.

Interpretation:

- T/NK exhaustion should not be a central claim at this stage.
- It can remain exploratory or be revisited after GSE223060 / external validation.

## 7. Main conclusion

GSE271107 provides useful first-pass external single-cell support for the spatial discovery results.

Strongly supported:

- `plasma_secretory` signature.
- `TXNDC5` as the strongest cross-platform plasma-program candidate.
- Canonical plasma anchors: `MZB1`, `JCHAIN`, `XBP1`, `TNFRSF17`, `SDC1`.

Partially supported:

- Myeloid genes `S100A8`, `S100A9`, and `CTSS` are correctly assigned to myeloid cells, but MM-stage enrichment is weak or absent in this dataset.

Weakly supported in this dataset:

- Stromal/ECM program because the dataset contains too few stromal-like cells.
- T/NK exhaustion because stage-level MM enrichment is not strong.

## 8. Publication implication

This result strengthens the project but also narrows the manuscript strategy.

Current strongest route:

- Spatial discovery identifies a plasma-secretory MM niche.
- scRNA validation confirms that this signal maps to plasma cells and is elevated in MM-stage samples.
- `TXNDC5` becomes a leading candidate for clinical/bulk validation.

Current risk:

- Plasma biology alone may be too expected.
- For stronger SCI Q2 positioning, the project still needs either:
  - a clinically relevant plasma-program score, or
  - a validated stromal/myeloid microenvironment score in another dataset.

## 9. Recommended next step

Next recommended analysis:

1. Add `GSE223060` as a second scRNA validation dataset if processed annotations are practical.
2. In parallel or immediately after that, start bulk/clinical validation for the plasma-secretory score and `TXNDC5` using `GSE24080` / `GSE2658`.

Priority decision:

- If the goal is biological robustness: do `GSE223060` next.
- If the goal is translational/Q2 manuscript strength: start bulk clinical validation next.

My recommendation:

- Start fast bulk/clinical validation next, using the now-supported plasma-secretory / `TXNDC5` axis.
