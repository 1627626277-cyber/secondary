# Spatial Autocorrelation And Niche Analysis

Purpose: address the reviewer concern that the spatial component should not be limited to sample-level module-score comparisons.

Methods:

- Spot-level plasma-secretory and niche scores from GSE269875 were merged with array-row/array-column coordinates.
- Moran's I was calculated within each sample using 6-nearest-neighbor graph weights.
- Permutation p values used 199 within-sample label permutations.
- Neighbor enrichment compared the mean score of 6 nearest neighboring spots around plasma-secretory-high spots, defined as the within-sample top quartile, versus other spots.
- The focal spot was excluded from the k-nearest-neighbor set.
- Reported neighbor enrichment excludes plasma-cell marker scores and uses non-overlapping niche programs rather than plasma-secretory module genes.

Key results:

- Plasma-secretory Moran's I was evaluated in 9 samples; 9 samples had FDR < 0.05.
- Median plasma-secretory Moran's I across samples was 0.477.
- MM samples had numerically higher Moran's I than controls (median MM=0.571, median control=0.144; Mann-Whitney p=0.02381).

Top neighbor-enrichment summaries:

| neighbor_feature             | neighbor_feature_label   |   n_samples |   median_of_sample_median_differences |   samples_positive |   samples_negative |   min_nominal_p |     min_fdr |
|:-----------------------------|:-------------------------|------------:|--------------------------------------:|-------------------:|-------------------:|----------------:|------------:|
| stromal_ecm_score            | Stromal ECM              |           7 |                             0.259827  |                  7 |                  0 |    2.02054e-138 | 1.1315e-136 |
| endothelial_score            | Endothelial marker       |           7 |                             0.127072  |                  7 |                  0 |    2.60192e-97  | 7.28538e-96 |
| myeloid_score                | Myeloid marker           |           7 |                             0.106913  |                  6 |                  1 |    2.22665e-47  | 1.13357e-46 |
| immune_pan_score             | Immune pan               |           7 |                             0.0982025 |                  6 |                  0 |    2.82135e-83  | 3.15991e-82 |
| endothelial_angiogenic_score | Endothelial angiogenic   |           7 |                             0.0970048 |                  7 |                  0 |    2.45136e-85  | 4.57588e-84 |

Interpretation boundary:

- This is an exploratory spatial organization analysis, not histology-anchored niche segmentation.
- It supports non-random spatial clustering and local neighbor associations when significant, but it does not prove causal cell-cell interaction.
- Because control marrow also shows non-zero Moran's I, the conservative claim is spatial clustering within marrow tissue; disease-specific spatial autocorrelation remains limited by the small cohort size.