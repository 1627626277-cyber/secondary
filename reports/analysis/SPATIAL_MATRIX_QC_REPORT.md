# GSE269875 Human Processed Spatial Matrix QC Report

Date: 2026-04-29

## Purpose

This report summarizes the first QC pass on the processed spatial transcriptomics matrices from GSE269875 after all 9 human mainline samples passed sampled sequence-level species QC.

## Input

Processed GEO package:

- `D:\二区\geo_processed\GSE269875_RAW.tar`
- Extracted to `D:\二区\geo_processed\GSE269875_RAW`

Each human mainline sample has:

- `matrix.mtx.gz`
- `barcodes.tsv.gz`
- `features.tsv.gz`
- `tissue_positions.csv.gz` or `tissue_positions_list.csv.gz`
- `scalefactors_json.json.gz`
- high/low resolution tissue images

## Outputs

- `D:\二区\analysis\spatial_qc\human_spatial_qc_sample_summary.tsv`
- `D:\二区\analysis\spatial_qc\human_spatial_qc_flags.tsv`
- `D:\二区\analysis\spatial_qc\human_spatial_qc_all_spots.tsv.gz`
- `D:\二区\analysis\spatial_qc\human_spatial_qc_sample_summary.png`
- `D:\二区\analysis\spatial_qc\human_spatial_qc_distribution_overview.png`

## Sample-Level QC Summary

| Sample | Group | Spots | Total UMIs | Median UMIs/spot | Median genes/spot | Median MT % | Initial QC flag |
|---|---|---:|---:|---:|---:|---:|---|
| hHBM1 | control | 2,055 | 1,671,816 | 232.0 | 102.0 | 3.72 | low median UMI/gene |
| hHBM2 | control | 822 | 1,211,995 | 1,242.0 | 536.5 | 2.43 | pass |
| hHBM3 | control | 1,254 | 1,737,889 | 748.5 | 329.5 | 2.37 | low median UMI/gene |
| hMM1 | MM | 373 | 327,460 | 465.0 | 408.0 | 6.81 | low spot count and low median UMI/gene |
| hMM2 | MM | 876 | 2,478,616 | 1,375.5 | 1,001.5 | 1.18 | pass |
| hMM3 | MM | 977 | 3,014,615 | 1,494.0 | 1,324.0 | 4.53 | pass |
| hMM4 | MM | 1,126 | 607,510 | 183.0 | 164.0 | 3.74 | low median UMI/gene |
| hMM5 | MM | 2,993 | 735,652 | 157.0 | 123.0 | 1.88 | low median UMI/gene |
| hMM6 | MM | 875 | 448,104 | 235.0 | 207.0 | 3.96 | low median UMI/gene |

## Interpretation

The processed spatial matrices are complete and usable for downstream analysis. All 9 human samples have matching matrix, barcode, feature, spatial-position, scale-factor, and tissue-image files.

The main technical issue is not missing data but uneven matrix depth:

- Stronger matrix-depth samples: hHBM2, hMM2, hMM3.
- Moderate/usable samples: hHBM3, hMM1, hMM6.
- Lower-depth samples requiring caution: hHBM1, hMM4, hMM5.
- hMM1 has the fewest spots and should be treated as lower-confidence for spatial heterogeneity claims.
- hMM5 has many spots but low median UMI/gene depth; it may still be useful for spatial coverage, but per-spot expression interpretation needs caution.

Mitochondrial percentages are not globally high. This suggests the main QC limitation is library depth / detected genes rather than obvious mitochondrial degradation.

## Decision

Proceed to downstream spatial analysis using processed matrices.

Do not perform full FASTQ expansion at this stage because:

- Processed matrices are present for all 9 human samples.
- Sequence-level species QC has already confirmed human-mainline identity.
- The current bottleneck is biological/spatial signal extraction and sample-depth normalization, not missing raw-data reconstruction.

## Recommended Analysis Handling

Use a conservative but not over-destructive QC strategy:

- Keep all 9 samples for initial exploration.
- Use sample-wise normalization before any cross-sample comparison.
- Avoid a strict universal UMI cutoff that removes low-depth samples wholesale.
- Run sensitivity analyses:
  - all 9 samples,
  - higher-depth subset,
  - MM-only robustness excluding the weakest sample if needed.
- For differential analysis, avoid treating spots as independent biological replicates without sample-aware aggregation.
- Prefer sample-aware pseudobulk / region-level summaries for final statistical claims.

## Next Step

Build human spatial objects and generate:

- per-sample spatial count maps,
- UMI/gene spatial feature plots,
- first-pass normalization and highly variable genes,
- low-dimensional embedding / clustering per sample,
- preliminary MM vs control exploratory marker table.
