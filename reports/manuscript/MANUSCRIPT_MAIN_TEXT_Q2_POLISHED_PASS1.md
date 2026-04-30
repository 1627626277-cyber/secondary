# Manuscript Main Text - Q2 Polishing Pass 1

Working title:

Spatial and clinical validation of a plasma-secretory bone marrow program in multiple myeloma

## Abstract

Multiple myeloma (MM) develops within a spatially organized bone marrow ecosystem, yet most clinically informative MM transcriptomic resources are bulk CD138+ tumor profiles that do not directly resolve tissue context. We integrated public spatial transcriptomics, Xenium spatial profiling, single-cell RNA-seq, external bulk cohorts, MMRF-COMMPASS/GDC RNA-seq, and public CoMMpass molecular annotations to evaluate whether a bone marrow plasma-secretory transcriptional program is spatially reproducible and clinically associated in MM.

In GSE269875 spatial transcriptomics, a curated plasma-secretory program was enriched in MM relative to control bone marrow samples (median difference 0.709; Cohen's d 3.129; Mann-Whitney p=0.0256). Independent Xenium validation in GSE299193 reproduced this program-level signal across 22 bone marrow samples, with higher plasma-secretory scores in active MM/RM than Ctrl/MGUS/SM samples (median delta 0.766; FDR=5.75e-04). A panel-covered POU2AF1/XBP1 module showed concordant enrichment in the same contrast (median delta 1.068; FDR=5.75e-04). In GSE271107 single-cell RNA-seq, the plasma-secretory axis localized to marker-inferred plasma-cell compartments, and TXNDC5 showed consistent plasma-cell expression support (mean log-normalized expression 2.196; detection 94.86%). External bulk analyses connected the broader module to clinical and cytogenetic annotations, including association of the POU2AF1/XBP1/JCHAIN module with 1q21 amplification in GSE2658 (FDR=1.65e-05) and association of XBP1 with 24-month OS death in GSE24080 (FDR=0.0362). In 762 baseline MMRF-COMMPASS/GDC bone marrow CD138+ RNA-seq samples, the plasma-secretory score was associated with OS event (FDR=9.31e-06), ISS stage (FDR=0.0019), and median-split OS (log-rank FDR=0.0401). Public NG2024 CoMMpass annotations further linked the score to PR RNA-subtype probability (Spearman rho=0.340; FDR=5.43e-19) and 1q21 gain/amplification (median delta=0.268; FDR=1.24e-05). In an adjusted Cox model, the plasma-secretory score remained associated with OS after adjustment for age, sex, ISS, and 1q21 status (HR=1.460 per 1 SD; 95% CI 1.069-1.993; FDR=0.0445).

These results support a cross-platform plasma-secretory MM bone marrow axis that is spatially enriched, reproduced in an independent Xenium cohort, localized to plasma-cell compartments, and associated with clinical and molecular-risk features in CoMMpass. TXNDC5 is best interpreted as a spatial/single-cell localization candidate, whereas the broader plasma-secretory program and the POU2AF1/XBP1-centered module provide the stronger clinical association signal. GSE299193 does not directly validate TXNDC5, JCHAIN, or SDC1 because these genes were absent from the extracted Xenium feature matrices. PFS, treatment-response, and definitive R-ISS analyses remain dependent on fuller controlled CoMMpass clinical files.

Keywords: multiple myeloma; spatial transcriptomics; Xenium; single-cell RNA-seq; CoMMpass; plasma-secretory program; overall survival; 1q21

## Introduction

Multiple myeloma is a plasma-cell malignancy shaped by both tumor-intrinsic transcriptional states and the bone marrow microenvironment. Large genomic resources, including MMRF-CoMMpass, have refined copy-number, mutational, and expression-based subtypes of MM, but these bulk profiles do not reveal where a transcriptional program is located within bone marrow tissue. Conversely, spatial and single-cell datasets provide tissue or cellular resolution but often have smaller sample sizes and limited clinical annotation. A clinically credible spatial-transcriptomic claim in MM therefore requires evidence across complementary data layers rather than a single discovery cohort.

We focused on a plasma-secretory transcriptional program discovered in MM bone marrow spatial transcriptomics. Because plasma-cell biology is expected in MM, the central question is not whether plasma-cell markers are present, but whether the same program is reproducible across spatial data, localizes to relevant cellular compartments, and aligns with independent clinical or molecular-risk features. This distinction is important for avoiding an overextended single-gene biomarker claim.

The project was therefore framed around a bounded subtype-axis model. TXNDC5 is retained as a spatial and single-cell localization candidate within the axis. POU2AF1, XBP1, and JCHAIN define a clinically oriented subtype module in bulk cohorts, although GSE299193 Xenium panel coverage supports POU2AF1/XBP1 but not JCHAIN. The broader curated plasma-secretory score is used for cross-platform validation because it is more robust to platform-specific gene-panel differences than any single gene.

Here, we integrate GSE269875 spatial transcriptomics, GSE299193 Xenium spatial transcriptomics, GSE271107 single-cell RNA-seq, GSE24080 and GSE2658 external bulk cohorts, MMRF-COMMPASS/GDC baseline RNA-seq, and public CoMMpass NG2024 molecular annotations. We test whether the MM bone marrow plasma-secretory program is spatially enriched, independently reproduced, plasma-cell localized, and associated with OS, ISS, RNA subtype, and 1q21 copy-number state. The claim is explicitly limited to retrospective public-data association and validation; R-ISS, PFS, and treatment-response validation are not claimed as complete.

## Methods

### Study design and data layers

This retrospective public-data study used six evidence layers: spatial discovery in GSE269875, second spatial validation in GSE299193 Xenium, single-cell localization in GSE271107, external bulk validation in GSE24080 and GSE2658, clinical validation in MMRF-COMMPASS/GDC baseline CD138+ RNA-seq, and molecular-annotation validation using public NG2024 CoMMpass supplementary tables. All analyses used public or open-access processed expression resources; no new human participant data were generated.

### Spatial discovery and second spatial validation

In GSE269875, curated sample-level module scores were calculated for plasma-secretory, myeloid inflammatory, T/NK cytotoxic, stromal ECM, endothelial angiogenic, erythroid/megakaryocytic, and cycling/proliferation programs. MM and control samples were compared using median module scores, Cohen's d, and Mann-Whitney tests. Gene-level candidate prioritization combined MM-control expression differences, effect size, detection rate, and spatial-region linkage.

GSE299193 raw Xenium data were downloaded from GEO and validated against the expected raw tar size. To minimize unnecessary disk use, only sample-level `cell_feature_matrix.h5` and lightweight cell metadata files were extracted for first-pass validation. Twenty-two Xenium matrices were analyzed across Ctrl, MGUS, SM, MM, and RM groups. Plasma-secretory and clinical-module scores were calculated from genes available in the Xenium panel. Active MM/RM samples were compared with Ctrl/MGUS/SM samples using Mann-Whitney tests with FDR correction. The extracted Xenium matrices contained MZB1, TNFRSF17, SLAMF7, IRF4, PIM2, POU2AF1, and XBP1, but not TXNDC5, JCHAIN, or SDC1; GSE299193 was therefore treated as program-level spatial validation rather than direct validation of those absent genes.

### Single-cell and external bulk validation

GSE271107 single-cell RNA-seq was used to evaluate cellular localization. Cells were summarized using broad marker-inferred categories, including plasma-cell, B-cell, myeloid, T/NK, stromal-like, endothelial-like, erythroid, and megakaryocyte/platelet-like compartments. Candidate gene expression and module scores were summarized by inferred cell type and disease stage.

GSE24080 and GSE2658 were used as external bulk validation cohorts. Target genes and module scores were extracted for the plasma-secretory axis and POU2AF1/XBP1/JCHAIN clinical subtype module. Available milestone survival, disease-related death, and cytogenetic-risk annotations were tested using cohort-appropriate non-parametric comparisons and FDR correction.

### CoMMpass/GDC and NG2024 validation

Open MMRF-COMMPASS/GDC processed RNA-seq files were filtered to baseline visit-1 bone marrow CD138+ tumor samples. Gene-level TPM values were extracted from STAR-count files, transformed as log2(TPM+1), and converted to within-cohort z-scores. The plasma-secretory score was calculated from curated plasma-secretory genes, and the clinical subtype module was calculated as the mean z-score of POU2AF1, XBP1, and JCHAIN.

Open GDC clinical endpoints included OS event, OS time, and ISS stage. Associations were tested using Mann-Whitney tests for binary endpoints, Spearman correlation for ordinal ISS, and median-split log-rank tests for OS. Public NG2024 CoMMpass molecular annotations from Skerget et al. were joined by patient identifier. Table 1 matched 762 of 762 local baseline CoMMpass/GDC samples, and Table 7 RNA-subtype predictions matched 707 samples. First-pass NG2024 analyses tested copy-number/cytogenetic calls, RNA subtype, and subtype probabilities against plasma-secretory and marker-level scores. Adjusted models evaluated whether the plasma-secretory axis retained association with OS or molecular-risk endpoints after covariate adjustment; the prespecified Cox model was OS ~ plasma-secretory score + age + sex + ISS + 1q21.

## Results

### Spatial transcriptomics identifies and independently reproduces a plasma-secretory MM bone marrow program

In GSE269875, the plasma-secretory program showed the strongest MM enrichment among tested spatial programs. The median plasma-secretory score was higher in MM than control bone marrow samples, with an MM-control median difference of 0.709, Cohen's d of 3.129, and Mann-Whitney p=0.0256. Candidate gene ranking highlighted canonical and region-linked plasma-secretory genes, including XBP1, TXNDC5, POU2AF1, SDC1, MZB1, and JCHAIN.

GSE299193 provided independent second-spatial-cohort validation. Across 22 Xenium matrices, the plasma-secretory score was higher in active MM/RM than Ctrl/MGUS/SM samples (median delta=0.766; Mann-Whitney p=0.000182; FDR=0.000575). The panel-covered POU2AF1/XBP1 module showed a similar active-disease enrichment (median delta=1.068; p=0.000287; FDR=0.000575). This result materially reduces the concern that the spatial signal is limited to a single discovery dataset. The interpretation remains bounded because the Xenium panel lacks TXNDC5, JCHAIN, and SDC1.

### Single-cell data localize the axis to plasma-cell compartments

In GSE271107, the plasma-secretory score was highest in marker-inferred plasma cells compared with other broad cell-type categories. TXNDC5, POU2AF1, XBP1, and JCHAIN showed strongest axis-gene expression in the plasma-cell compartment, with TXNDC5 showing mean log-normalized expression of 2.196 and detection in 94.86% of marker-inferred plasma-cell observations summarized across samples. Disease-stage summaries further supported higher plasma-secretory activity in MM than HD, MGUS, and SMM groups. These results support TXNDC5 as a localization candidate within the axis, not as a standalone prognostic marker.

### External bulk cohorts connect the axis to subtype and risk annotations

External bulk cohorts supported the clinical relevance of the broader module. In GSE2658, the POU2AF1/XBP1/JCHAIN clinical subtype module was associated with FISH 1q21 amplification (FDR=1.65e-05). In GSE24080, XBP1 was associated with 24-month OS death (FDR=0.0362). These findings support a clinical subtype interpretation centered on the broader plasma-secretory program and POU2AF1/XBP1/JCHAIN module rather than a single-gene TXNDC5 prognostic model.

### CoMMpass/GDC and NG2024 validate clinical and molecular associations

In 762 baseline MMRF-COMMPASS/GDC bone marrow CD138+ RNA-seq samples, the plasma-secretory score was associated with OS event (Mann-Whitney p=1.55e-06; FDR=9.31e-06; event-vs-nonevent median delta=0.346). The clinical subtype module was also associated with OS event (FDR=5.46e-05). The plasma-secretory score was associated with ISS ordinal stage (Spearman rho=0.132; p=0.000316; FDR=0.0019), and median-split OS analysis showed worse OS in the higher-score group (log-rank p=0.00668; FDR=0.0401).

Public NG2024 CoMMpass annotations extended the signal to molecular-risk features. The plasma-secretory score tracked PR RNA-subtype probability (Spearman rho=0.340; FDR=5.43e-19) and RNA subtype class (FDR=1.09e-13). It was higher in samples with 1q21 gain/amplification calls (median delta=0.268; FDR=1.24e-05). TXNDC5 was associated with NG2024 1q21 gain/amplification (median delta=0.231; FDR=0.00843), while POU2AF1 was associated with 17p13 deletion (median delta=0.337; FDR=0.00533).

Adjusted modeling reduced the concern that the CoMMpass signal was purely unadjusted. In the prespecified Cox model including age, sex, ISS, and 1q21 status, the plasma-secretory score remained associated with OS (HR=1.460 per 1 SD; 95% CI 1.069-1.993; p=0.0173; FDR=0.0445). The POU2AF1/XBP1/JCHAIN clinical subtype module also retained OS association under the same adjustment (HR=1.434; 95% CI 1.090-1.886; FDR=0.0299).

## Discussion

This study supports a bounded but coherent translational model: an MM bone marrow plasma-secretory program is spatially enriched, independently reproduced at the program level in a Xenium cohort, localized to plasma-cell compartments, and associated with clinical and molecular-risk features in CoMMpass. The strength of the work lies in cross-platform convergence rather than discovery of a previously unknown plasma-cell marker.

The analysis also clarifies how TXNDC5 should be presented. TXNDC5 is supported as a spatial and single-cell localization candidate, and it shows NG2024 molecular-risk association with 1q21 gain/amplification. However, it should not be framed as the central standalone prognostic biomarker. The more defensible construct is the broader plasma-secretory subtype axis, with POU2AF1/XBP1/JCHAIN carrying stronger bulk clinical linkage and POU2AF1/XBP1 receiving second spatial support in GSE299193 because of Xenium panel coverage.

The addition of GSE299193 substantially improves the manuscript. The prior spatial discovery sample-size concern is now partly mitigated by an independent human MM bone marrow Xenium cohort. The GSE299193 result is not a full gene-by-gene replication of the discovery signature because TXNDC5, JCHAIN, and SDC1 are absent from the extracted feature matrices. Nevertheless, the available panel genes reproduce the active-disease plasma-secretory program and POU2AF1/XBP1 module, which is the correct evidentiary use of this cohort.

Clinical interpretation should remain conservative. CoMMpass/GDC and NG2024 support OS, ISS, RNA-subtype, 1q21, and adjusted OS associations. These are clinically relevant retrospective associations, not proof of prospective classifier utility. PFS, treatment response, and definitive R-ISS validation require fuller controlled CoMMpass clinical tables or another curated clinical cohort.

The main limitations are platform heterogeneity, incomplete clinical endpoints in open public data, marker-inferred single-cell annotations, and Xenium panel constraints. These limitations do not invalidate the current Q2 manuscript route, but they must be stated directly. The manuscript should claim spatial reproducibility and clinical association of a plasma-secretory axis, not clinical deployment readiness.

## Data Availability

Spatial transcriptomics discovery data were obtained from GSE269875. Independent Xenium spatial validation used GSE299193. Single-cell RNA-seq validation used GSE271107. External bulk validation used GSE24080 and GSE2658. CoMMpass/GDC processed RNA-seq and open clinical data were obtained from the GDC MMRF-COMMPASS project. Public CoMMpass molecular annotations were obtained from the Skerget et al. Nature Genetics 2024 supplementary tables. Fuller MMRF/CoMMpass clinical analyses involving PFS and treatment response were not performed because the required controlled clinical files were not available locally.

## Citation Anchors Requiring Formal Verification

- MMRF-COMMPASS primary molecular profiling and subtype papers.
- Skerget et al. Nature Genetics 2024 CoMMpass molecular-profiling supplementary tables.
- GDC MMRF-COMMPASS data access documentation.
- Primary GEO/source publication for GSE269875.
- Primary GEO/source publication for GSE299193.
- Primary GEO/source publication for GSE271107.
- Primary cohort publications or GEO records for GSE24080 and GSE2658.

## Current Claim Boundary

Supported now:

- spatial discovery in GSE269875;
- second spatial program-level validation in GSE299193;
- plasma-cell localization in GSE271107;
- external bulk subtype/risk support in GSE24080/GSE2658;
- OS/ISS association in CoMMpass/GDC;
- public NG2024 molecular-risk support;
- adjusted OS association after age, sex, ISS, and 1q21.

Not supported yet:

- definitive R-ISS validation;
- PFS validation;
- treatment-response or therapy-line validation;
- prospective classifier performance;
- direct GSE299193 validation of TXNDC5/JCHAIN/SDC1.
