# Preliminary Spatial Clustering Report

Date: 2026-04-29

## Scope

This report summarizes the first exploratory spatial clustering pass for the 9 human GSE269875 samples after:

- all 9 human samples passed sampled sequence-level species QC;
- processed spatial matrices were downloaded and checked;
- matrix-level QC showed usable but uneven sample depth.

This is an exploratory analysis. It should not yet be treated as final statistical evidence.

## Input

- Processed spatial matrices: `D:\二区\geo_processed\GSE269875_RAW`
- Matrix QC table: `D:\二区\analysis\spatial_qc\human_spatial_qc_sample_summary.tsv`

## Method

Script:

- `D:\二区\scripts\09_preliminary_spatial_clustering.py`

Main steps:

1. Loaded all 9 human spatial matrices.
2. Applied per-spot library-size normalization to 10,000 counts.
3. Applied `log1p` transformation.
4. Selected 2,500 highly variable non-mitochondrial/non-ribosomal genes.
5. Ran truncated SVD, UMAP, and KMeans clustering with 8 preliminary clusters.
6. Generated exploratory cluster markers and module scores.

## Output Files

Directory:

- `D:\二区\analysis\spatial_preliminary`

Key files:

- `combined_spot_embedding_clusters.tsv.gz`
- `combined_spot_module_scores.tsv.gz`
- `cluster_group_composition.tsv`
- `cluster_counts_by_sample.tsv`
- `cluster_top_markers.tsv`
- `group_top_markers.tsv`
- `sample_module_median_scores.tsv`
- `cluster_module_median_scores.tsv`
- `combined_umap_group_sample_cluster.png`
- `spatial_cluster_maps_all_human.png`
- `spatial_plasma_cell_score_maps_all_human.png`
- `spatial_immune_pan_score_maps_all_human.png`
- `spatial_myeloid_score_maps_all_human.png`
- `spatial_stromal_ecm_score_maps_all_human.png`

## Cluster Composition

| Cluster | MM spots | Control spots | Total spots | MM fraction |
|---|---:|---:|---:|---:|
| 0 | 785 | 0 | 785 | 1.000 |
| 1 | 1,150 | 3,836 | 4,986 | 0.231 |
| 2 | 271 | 0 | 271 | 1.000 |
| 3 | 522 | 13 | 535 | 0.976 |
| 4 | 1,929 | 60 | 1,989 | 0.970 |
| 5 | 1,234 | 201 | 1,435 | 0.860 |
| 6 | 274 | 0 | 274 | 1.000 |
| 7 | 1,055 | 21 | 1,076 | 0.980 |

Initial interpretation:

- Cluster 1 is the main control-enriched / normal-like cluster.
- Clusters 0, 2, 3, 4, 5, 6, and 7 are MM-enriched.
- Several MM-enriched clusters are strongly sample-associated, so final claims must use sample-aware statistics rather than treating all spots as independent replicates.

## First Biological Signals

### MM vs Control Exploratory Markers

Top MM-enriched genes in the spot-level exploratory comparison:

- `JCHAIN`
- `TXNDC5`
- `IGHG1`
- `B2M`
- `IGHA1`
- `CD74`
- `VIM`
- `IGKC`
- `XBP1`
- `PIM2`
- `COL1A1`
- `MZB1`
- `POU2AF1`

Interpretation:

- The first pass recovers a strong plasma-cell / immunoglobulin / unfolded-protein-response axis in MM regions.
- The appearance of `MZB1`, `XBP1`, `JCHAIN`, `IGHA1`, `IGHG1`, `IGKC`, and `TXNDC5` is biologically plausible for MM plasma-cell-rich spatial regions.

### Notable MM-Enriched Clusters

Cluster 2:

- Main sample contribution: hMM3.
- Top markers include `CCND1`, `FCRLB`, `MZB1`, `TXNIP`, `CXCR4`, `POU2AF1`, `XBP1`.
- Interpretation: strong candidate plasma-cell / malignant plasma-cell-rich region, with a possible CCND1-high signal.

Cluster 0:

- Main sample contribution: hMM5.
- Top markers include `IGHA1`, `JCHAIN`, `B2M`, `CD74`, `PIM2`, `TXNDC5`, `COL1A1`, `FGFR3`, `COL3A1`, `TNFRSF17`.
- Interpretation: plasma-cell-rich region with ECM/stromal-associated signal; needs scRNA support to separate malignant plasma-cell from stromal mixture.

Cluster 3:

- Main sample contribution: hMM2.
- Top markers include `IGKC`, `S100A8`, `S100A9`, `IGHG1`, `HBB`, `HBD`, `HBA2`, `LYZ`, `DEFA3`.
- Interpretation: immunoglobulin-rich plus myeloid/erythroid-like microenvironment signal; likely mixed marrow niche.

Cluster 7:

- Main sample contribution: hMM4.
- Top markers include `IGHG1`, `CXCL12`, `IGHM`, `CCND3`, `HBB`, `HBA2`, `PPBP`, `TXNDC5`.
- Interpretation: possible plasma-cell / stromal or marrow-support niche; requires validation.

## Module Score Signals

Sample-level median module scores suggest:

- Plasma-cell score is higher across MM samples than controls.
- hMM2 and hMM3 show the strongest matrix depth and strong plasma/myeloid-related signals.
- hMM2 shows the highest myeloid module median among MM samples.
- Stromal/ECM score is detectable in several MM samples, including hMM1, hMM2, hMM4, and hMM5.

Because spot-level expression is sparse, module-score medians can be zero for some samples. These scores should be interpreted as screening-level signals, not final quantitative evidence.

## Limitations

- This is a spot-level exploratory clustering analysis.
- Cluster composition is partly sample-associated.
- Several samples have low median UMI/gene depth, especially hMM4, hMM5, hMM6, and hHBM1.
- hMM1 has low spot count.
- Final inferential analysis must avoid treating spots as independent biological replicates.

## Decision

The project has now moved beyond data availability/QC into result generation.

The first-pass spatial analysis produces plausible MM-associated biological signals:

- plasma-cell / immunoglobulin axis,
- plasma-cell stress / unfolded-protein-response markers,
- CCND1-high cluster in hMM3,
- myeloid/inflammatory marrow niche in hMM2,
- stromal/ECM-associated signals in selected MM regions.

These are sufficient to justify moving to:

1. more robust per-sample and region-level marker analysis;
2. scRNA validation using GSE223060 / GSE271107;
3. clinical/bulk validation after candidate signature stabilization.

## Next Step

Build a more defensible candidate signature table:

- separate sample-aware MM-vs-control summaries from spot-level exploratory markers;
- compute per-sample pseudobulk and per-cluster marker consistency;
- prioritize genes that are:
  - spatially enriched in MM regions,
  - recurrent across at least several MM samples or biologically interpretable MM subregions,
  - identifiable in scRNA validation datasets,
  - testable in bulk/clinical cohorts.
