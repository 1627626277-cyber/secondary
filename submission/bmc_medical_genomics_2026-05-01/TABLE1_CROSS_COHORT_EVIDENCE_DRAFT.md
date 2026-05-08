# Table 1. Cross-Cohort Evidence Chain And Manuscript Claim Boundary

| Evidence layer | Figure | Cohort (n) | Main result | Claim boundary |
|---|---:|---|---:|---|---|
| Study design | Fig. 1 | Seven public/open data resources | Sequential spatial, single-cell, bulk, and molecular annotation workflow | Integrative public-data framework |
| Spatial discovery | Fig. 2 | GSE269875 (n=9 spatial samples: 6 MM, 3 Ctrl) | MM-control plasma-secretory median difference 0.709; Cohen's d 3.129; p=0.0256 | Discovery signal |
| Spatial organization cross-program | Fig. 3 | GSE269875 (9 spot-level grids, 7 programs) | Plasma-secretory median Moran's I 0.477 (highest among 7 programs); stromal ECM 0.383; myeloid-inflammatory 0.352 | Exploratory spatial clustering; plasma-secretory more disease-associated than other marrow programs |
| Second spatial reproducibility | Fig. 4 | GSE299193 (n=22 Xenium samples) | Active MM/RM vs Ctrl/MGUS/SM median diff 0.766; FDR=0.000575 | Program-level spatial reproducibility (not gene-level for TXNDC5/JCHAIN/SDC1) |
| Single-cell localization | Fig. 5 | GSE271107 (n=19 samples, 127,528 post-QC cells) | TXNDC5 detected in 96.44% of 8,007 marker-inferred plasma cells | Plasma-cell compartment localization; malignant vs normal not separated |
| External bulk support | Fig. 6 | GSE2658 (n=559), GSE24080 (n=217) | Clinical module associated with 1q21 amplification; XBP1 associated with 24-month OS death | Subtype/risk association; direction not uniform across platforms |
| CoMMpass/GDC clinical association | Fig. 7 | 762 baseline CD138+ RNA-seq samples | Plasma-secretory score associated with OS event (FDR=9.31e-06), ISS (rho=0.132, FDR=0.0019) | Retrospective clinical association |
| Public NG2024 annotation | Fig. 7 | 762 matched CoMMpass patients (707 RNA-subtype complete) | Score correlated with PR subtype probability (rho=0.340, FDR=5.43e-19); associated with 1q21 gain/amp (FDR=1.24e-05) | Molecular-risk context |
| Adjusted and sensitivity models | Fig. 8 | 660 basic; 613 PR/proliferation; 6 model specifications | Basic OS HR 1.460 (FDR=0.0485); low-purity model HR 1.553 (FDR=0.0358); attenuated after PR+proliferation (HR 1.150, FDR=0.444); 1q21 fully-adjusted OR 1.396 (FDR=0.0467) | Molecular-risk-context association; not independent of PR/proliferation; not a purity surrogate |

Note: Table 1 is intended as a main manuscript table. Claim boundaries are deliberately conservative because the analysis does not complete R-ISS, PFS, treatment-response, or prospective clinical-utility validation.
