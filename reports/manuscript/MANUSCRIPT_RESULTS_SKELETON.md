# Manuscript Results Skeleton

## Result 1. Spatial transcriptomics identifies a plasma-secretory program enriched in MM bone marrow

- In GSE269875, the plasma-secretory score was higher in MM than control bone marrow samples (MM-control median difference=0.709; Cohen d=3.129; Mann-Whitney p=0.0256).
- This establishes the spatial discovery layer and motivates downstream single-cell and bulk clinical validation.
- Claim boundary: this is a spatial program-level finding, not a standalone single-gene biomarker claim.
- In the independent GSE299193 Xenium cohort, the same plasma-secretory program was higher in MM/RM than Ctrl/MGUS/SM samples (median delta=0.766; FDR=5.75e-04).
- GSE299193 validates the program-level spatial signal, but its Xenium panel does not contain TXNDC5, JCHAIN, or SDC1, so it should not be used as direct TXNDC5 validation.

## Result 2. Single-cell validation localizes the axis to plasma-cell annotated compartments

- In GSE271107, TXNDC5 showed plasma-cell expression support (mean log-normalized expression=2.196; detected=94.86%).
- The plasma-secretory program was highest in marker-inferred plasma cells compared with other broad cell-type bins.
- TXNDC5 should be presented as a spatial/single-cell localization candidate within the broader axis.

## Result 3. External GEO bulk cohorts support a clinical subtype/risk-linked module

- In GSE2658, the POU2AF1/XBP1/JCHAIN clinical subtype module was associated with 1q21 amplification.
- In GSE24080, XBP1 showed FDR-supported association with 24-month OS death.
- These results justify shifting the clinical framing from a single TXNDC5 marker to a broader plasma-secretory subtype axis.

## Result 4. CoMMpass/GDC validates OS and ISS association of the plasma-secretory axis

- In 762 baseline MMRF-COMMPASS/GDC bone marrow CD138+ RNA-seq samples, the plasma-secretory score was associated with OS event (effect=0.346; FDR=9.31e-06).
- The same score was associated with ISS ordinal stage (effect=0.132; FDR=0.0019).
- Median-split OS analysis remained significant (effect=7.356; log-rank FDR=0.0401).
- In public NG2024 CoMMpass molecular annotations, the plasma-secretory score was associated with 1q21 gain/amplification (median_feature1_minus_feature0=0.268; FDR=1.24e-05).
- In the requested adjusted Cox model, the plasma-secretory score remained associated with OS after age, sex, ISS and 1q21 adjustment (hazard_ratio_per_1sd_score=1.460; 95% CI=1.069-1.993; FDR=0.0445).

## Current Claim Boundary

- The current manuscript can claim spatial discovery, independent second spatial validation, single-cell localization, OS/ISS association in CoMMpass/GDC, and public NG2024 molecular-annotation support including 1q21 and RNA-subtype probability.
- It should not claim completed R-ISS, PFS, detailed cytogenetic high-risk, or treatment-response validation.
- Those endpoints require fuller MMRF/CoMMpass clinical files outside the currently used GDC open clinical slice.

## Draft One-Sentence Result Claim

An MM bone marrow plasma-secretory spatial program is reproduced in a second Xenium spatial cohort, localized to plasma-cell compartments, and associated with overall survival, ISS, public CoMMpass 1q21/RNA-subtype annotations, and adjusted OS models, with TXNDC5 acting as a spatial/single-cell localization candidate and POU2AF1/XBP1 forming the clinically stronger panel-validated subtype module.
