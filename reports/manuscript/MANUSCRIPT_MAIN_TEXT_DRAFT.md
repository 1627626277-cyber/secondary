# Manuscript Main Text Draft

Working title:

Spatial discovery and clinical validation of a plasma-secretory bone marrow program in multiple myeloma

## Abstract

Multiple myeloma (MM) is a plasma-cell malignancy with substantial clinical and molecular heterogeneity. Although bulk genomic studies have refined molecular subtypes and risk features, the spatial organization of transcriptional programs within MM bone marrow and their connection to clinical phenotypes remain incompletely resolved. Here, we integrated public spatial transcriptomics, Xenium spatial transcriptomics, single-cell RNA sequencing, external bulk expression cohorts, MMRF-COMMPASS/GDC RNA-seq, and public CoMMpass molecular annotations from Skerget et al. Nature Genetics 2024 to evaluate a bone marrow plasma-secretory axis in MM.

In spatial transcriptomics from GSE269875, a plasma-secretory program was enriched in MM compared with control bone marrow samples (MM-control median difference 0.709; Cohen d 3.129; Mann-Whitney p=0.0256). Independent Xenium validation in GSE299193 reproduced the program-level signal across 22 bone marrow samples, with higher plasma-secretory scores in MM/RM than Ctrl/MGUS/SM samples (median delta=0.766; FDR=5.75e-04) and similar support for a POU2AF1/XBP1 module (median delta=1.068; FDR=5.75e-04). Single-cell validation in GSE271107 localized this axis to marker-inferred plasma cells, with TXNDC5 showing consistent plasma-cell expression support (mean log-normalized expression 2.196; detection 94.86%). External bulk expression analyses supported a broader clinical subtype module, particularly POU2AF1/XBP1/JCHAIN, with association to 1q21 amplification in GSE2658 (FDR=1.65e-05) and 24-month OS death for XBP1 in GSE24080 (FDR=0.0362). In 762 baseline MMRF-COMMPASS/GDC bone marrow CD138+ RNA-seq samples, the plasma-secretory score was associated with OS event (FDR=9.31e-06), ISS ordinal stage (FDR=0.0019), and median-split overall survival (log-rank FDR=0.0401). Public NG2024 CoMMpass annotations further linked the plasma-secretory score to PR RNA-subtype probability (Spearman rho=0.340; FDR=5.43e-19) and 1q21 gain/amplification (median delta=0.268; FDR=1.24e-05). In an adjusted Cox model, the plasma-secretory score remained associated with OS after age, sex, ISS, and 1q21 adjustment (HR=1.460 per 1 SD; 95% CI 1.069-1.993; FDR=0.0445).

These results support a cross-platform plasma-secretory MM bone marrow axis that is spatially enriched, reproduced in an independent Xenium cohort, localized to plasma-cell compartments, associated with clinical risk in CoMMpass, and supported by public molecular-risk annotations. TXNDC5 is best interpreted as a spatial/single-cell localization candidate within this axis, while POU2AF1/XBP1/JCHAIN provide stronger clinical subtype linkage. GSE299193 supports program-level spatial validation but does not directly validate TXNDC5, JCHAIN, or SDC1 because these genes were absent from the extracted Xenium feature matrices. R-ISS, PFS, and treatment-response validation remain pending fuller MMRF/CoMMpass clinical tables.

Keywords:

- multiple myeloma
- spatial transcriptomics
- single-cell RNA-seq
- CoMMpass
- plasma cell
- bone marrow microenvironment
- overall survival

## Introduction

Multiple myeloma is characterized by malignant plasma-cell expansion within the bone marrow and by marked inter-patient heterogeneity in clinical outcome, treatment response, and molecular architecture. Large genomic resources such as MMRF-CoMMpass have shown that MM is not a single molecular entity, but a collection of expression and copy-number subtypes with distinct risk associations. At the same time, MM progression occurs in a spatially structured bone marrow niche, where malignant plasma cells interact with immune, stromal, endothelial, and hematopoietic compartments.

Most clinically oriented MM transcriptomic studies rely on bulk CD138+ tumor profiling or targeted clinical annotations. These datasets are powerful for outcome analysis but provide limited direct information about the spatial or cellular compartment in which a candidate program is expressed. Conversely, spatial and single-cell datasets provide localization but often have smaller sample sizes and limited clinical follow-up. A robust translational analysis therefore requires a cross-platform strategy: spatial discovery to identify a tissue-level program, single-cell validation to establish cellular localization, and larger clinical bulk cohorts to test whether the same program carries clinical relevance.

We initially evaluated MM bone marrow spatial transcriptomics to identify candidate transcriptional programs enriched in disease tissue. The strongest reproducible signal was a plasma-secretory program containing canonical plasma-cell and secretory pathway genes. Because canonical plasma-cell biology alone is expected in MM and would not be sufficient as a clinically meaningful claim, we reframed the project around a broader plasma-secretory subtype axis. In this framework, TXNDC5 is treated as a spatial and single-cell localization candidate, whereas POU2AF1, XBP1, and JCHAIN form a clinical subtype module suitable for outcome and risk-association testing.

Here, we integrate GSE269875 spatial transcriptomics, GSE299193 Xenium spatial transcriptomics, GSE271107 single-cell RNA-seq, GSE24080 and GSE2658 external bulk cohorts, MMRF-COMMPASS/GDC baseline RNA-seq, and public CoMMpass NG2024 molecular annotations to test whether the MM bone marrow plasma-secretory program is spatially enriched, independently reproduced, cell-type localized, and clinically/molecularly associated with OS, ISS, RNA subtype, and 1q21 copy-number state. The central claim is deliberately bounded: the current open/public data support spatial program validation, OS, ISS, RNA-subtype, and molecular-annotation analyses, but do not support definitive R-ISS, PFS, or treatment-response validation.

## Methods

### Study design

This was a retrospective public-data integrative bioinformatics study. The analysis proceeded in six stages:

1. spatial discovery in GSE269875;
2. second spatial validation in GSE299193 Xenium;
3. single-cell localization validation in GSE271107;
4. external bulk expression validation in GSE24080 and GSE2658;
5. clinical validation in MMRF-COMMPASS/GDC baseline bone marrow CD138+ RNA-seq;
6. public CoMMpass molecular-annotation and adjusted-model validation using the Skerget et al. Nature Genetics 2024 supplementary tables.

All analyses were performed using processed public expression matrices or open-access processed RNA-seq outputs. No new human participant data were generated.

### Spatial transcriptomics discovery

GSE269875 human bone marrow spatial transcriptomics samples were processed from available matrices. Candidate module scores were calculated for curated cell-state and microenvironmental programs, including plasma-secretory, myeloid inflammatory, T/NK cytotoxic, stromal ECM, endothelial angiogenic, erythroid/megakaryocytic, and cycling/proliferation signatures. Sample-level disease enrichment was tested by comparing MM and control samples using median module scores, Cohen's d, and Mann-Whitney tests.

The plasma-secretory program was selected for downstream validation because it showed the strongest sample-level MM enrichment among candidate programs. Gene-level candidate prioritization combined sample-level MM-control expression differences, effect size, detection rate, and spatial region linkage.

### GSE299193 Xenium second spatial validation

GSE299193 raw Xenium files were downloaded from GEO and validated by exact expected file size. To avoid unnecessary full extraction of morphology and transcript-level files, only sample-level `cell_feature_matrix.h5` and lightweight cell metadata files were extracted from the raw tar archive. Twenty-two Xenium sample matrices were analyzed, including Ctrl, MGUS, smoldering MM, MM, and relapsed MM groups. Plasma-secretory and clinical-module scores were calculated from genes available in the Xenium panel, followed by sample-level comparisons between active MM/RM samples and Ctrl/MGUS/SM samples using Mann-Whitney tests and FDR correction.

The extracted Xenium feature matrices contained MZB1, TNFRSF17, SLAMF7, IRF4, PIM2, POU2AF1, and XBP1, but did not contain TXNDC5, JCHAIN, or SDC1. Therefore, GSE299193 was used as an independent program-level spatial validation cohort, not as a direct TXNDC5 or JCHAIN validation dataset.

### Single-cell validation

GSE271107 single-cell RNA-seq data were used to validate cellular localization. Cells were assigned broad marker-inferred categories, including plasma cells, B cells, myeloid cells, T/NK cells, stromal-like cells, endothelial-like cells, erythroid cells, and megakaryocyte/platelet-like cells. Candidate gene expression and signature scores were summarized by inferred cell type and disease stage. TXNDC5 was evaluated as a localization candidate within marker-inferred plasma cells.

### External bulk cohort validation

GSE24080 and GSE2658 were analyzed as external bulk expression validation cohorts. Target genes and module scores were extracted for the plasma-secretory axis and the POU2AF1/XBP1/JCHAIN clinical subtype module. Associations were tested with available milestone survival, disease-related death, and cytogenetic risk annotations. FDR adjustment was applied within tested association families.

### CoMMpass/GDC clinical validation

Open MMRF-COMMPASS/GDC processed RNA-seq files were indexed and filtered to baseline visit-1 bone marrow CD138+ tumor samples. STAR-count gene-expression files were downloaded and target gene TPM values were extracted. Gene-level log2(TPM+1) values were converted to within-cohort z-scores. The plasma-secretory score was calculated from curated plasma-secretory genes, and the clinical subtype module was calculated as the mean z-score of POU2AF1, XBP1, and JCHAIN.

Clinical endpoints available in the open GDC clinical slice included OS event, OS time, and ISS stage. Associations were tested using Mann-Whitney tests for binary endpoints, Spearman correlation for ISS ordinal stage, and median-split log-rank tests for OS. FDR correction was applied across tested variables within endpoint/test families.

### Public NG2024 molecular annotation and adjusted modeling

Public CoMMpass molecular annotations were obtained from Skerget et al. Nature Genetics 2024 supplementary tables. Patient-feature annotations and RNA-subtype predictions were joined to the local CoMMpass/GDC score table by patient identifier. Table 1 matched 762 of 762 local baseline CoMMpass/GDC samples, and Table 7 RNA-subtype predictions matched 707 samples.

First-pass molecular-annotation associations tested binary copy-number/cytogenetic calls, ordinal clinical or laboratory variables, categorical RNA/CNA subtypes, and RNA-subtype probabilities against plasma-secretory and marker-level z-scores. FDR correction was applied across tested associations. Adjusted models then tested whether the plasma-secretory axis remained associated with OS or molecular-risk endpoints after basic covariate adjustment. The prespecified Cox model requested for manuscript strengthening was OS ~ plasma-secretory score + age + sex + ISS + 1q21. Additional Cox, logistic, and linear models evaluated OS, ISS III, IMWG non-standard risk, cytogenetic high-risk, 1q21, 17p13, and PR RNA-subtype probability.

### Claim-boundary handling

The open GDC clinical slice and public NG2024 supplementary tables did not provide sufficient usable fields for complete PFS or treatment-response validation. These endpoints were therefore not claimed as completed validations. A separate fuller clinical-data readiness workflow was prepared for future MMRF Virtual Lab / Researcher Gateway files.

## Results

### Spatial transcriptomics identifies a plasma-secretory program enriched in MM bone marrow

The spatial discovery analysis compared sample-level signature scores between MM and control bone marrow in GSE269875. Among the tested programs, plasma-secretory showed the strongest MM enrichment. The median plasma-secretory score was higher in MM than in controls, with an MM-control median difference of 0.709, Cohen d of 3.129, and Mann-Whitney p=0.0256 (Fig. 2A). Effect-size ranking across spatial programs confirmed that plasma-secretory was the leading disease-associated program (Fig. 2B).

Gene-level candidate ranking identified canonical and region-linked plasma-secretory genes, including XBP1, TXNDC5, POU2AF1, SDC1, MZB1, and JCHAIN (Fig. 2C). These results established a spatially enriched plasma-secretory program in MM bone marrow, but did not by themselves establish a clinical biomarker. Therefore, downstream validation focused on whether this spatial program localized to plasma-cell compartments and whether the broader axis carried clinical relevance in independent bulk cohorts.

Independent spatial validation in GSE299193 Xenium supported the same program-level signal (Fig. 6). Across 22 human bone marrow Xenium matrices, the plasma-secretory score was higher in active MM/RM samples than in Ctrl/MGUS/SM samples (median delta=0.766; Mann-Whitney p=0.000182; FDR=0.000575). The panel-covered POU2AF1/XBP1 module showed a similar difference (median delta=1.068; p=0.000287; FDR=0.000575). These results reduce the concern that the spatial finding is limited to GSE269875 alone. However, GSE299193 cannot be used as direct TXNDC5, JCHAIN, or SDC1 validation because these genes were absent from the extracted Xenium feature matrices.

### Single-cell validation localizes the axis to plasma-cell annotated compartments

Single-cell validation in GSE271107 supported plasma-cell localization of the axis. Across broad marker-inferred cell types, the plasma-secretory score was highest in plasma cells (Fig. 3B). Dot-plot analysis of TXNDC5, POU2AF1, XBP1, and JCHAIN showed strongest axis-gene expression within the plasma-cell compartment, with JCHAIN, XBP1, and TXNDC5 displaying prominent plasma-cell signal (Fig. 3A). TXNDC5 showed mean log-normalized expression of 2.196 in plasma cells and was detected in 94.86% of marker-inferred plasma-cell observations summarized across samples.

Disease-stage summaries showed higher plasma-secretory scores in MM than in HD, MGUS, and SMM groups in this single-cell dataset (Fig. 3C). These findings support TXNDC5 as a spatial/single-cell localization candidate, but they also reinforce that the clinically stronger interpretation should be made at the broader plasma-secretory axis level rather than as a single-gene TXNDC5 prognostic claim.

### External bulk cohorts support a clinical subtype/risk-linked module

To test whether the spatially discovered axis had independent clinical or subtype relevance, we analyzed GSE24080 and GSE2658. In GSE2658, the POU2AF1/XBP1/JCHAIN clinical subtype module was associated with FISH 1q21 amplification status (FDR=1.65e-05), and POU2AF1 and XBP1 showed strong individual associations with the same cytogenetic endpoint. In GSE24080, XBP1 was associated with 24-month OS death (FDR=0.0362).

These analyses indicated that the clinical signal was more coherent for the POU2AF1/XBP1/JCHAIN subtype module and the broader plasma-secretory axis than for TXNDC5 alone (Fig. 4). The external bulk results therefore justified retaining TXNDC5 as a localization candidate while assigning the clinical subtype and risk-association role to the broader module.

### CoMMpass/GDC and NG2024 validate clinical and molecular associations of the plasma-secretory axis

We next tested the plasma-secretory axis in MMRF-COMMPASS/GDC using 762 baseline visit-1 bone marrow CD138+ RNA-seq samples. OS events were available for the cohort, and ISS stage was available for 742 samples. The plasma-secretory score was associated with OS event (Mann-Whitney p=1.55e-06; FDR=9.31e-06; event-vs-nonevent median delta=0.346; Fig. 5B). The POU2AF1/XBP1/JCHAIN clinical subtype module was also associated with OS event (FDR=5.46e-05), and individual JCHAIN, XBP1, TXNDC5, and POU2AF1 signals were FDR-supported to varying degrees.

The plasma-secretory score was also associated with ISS ordinal stage (Spearman rho=0.132; p=0.000316; FDR=0.0019; Fig. 5A). Median-split survival analysis showed that patients with higher plasma-secretory score had worse OS than the lower-score group (log-rank p=0.00668; FDR=0.0401; Fig. 5C). Together, these CoMMpass/GDC results provide the strongest current clinical support for the project: the spatially discovered plasma-secretory axis is associated with OS and ISS in an independent large MM bulk RNA-seq cohort.

Public NG2024 CoMMpass annotations extended this evidence to molecular subtype and copy-number features. The plasma-secretory score was associated with PR RNA-subtype probability (Spearman rho=0.340; FDR=5.43e-19) and RNA subtype class (FDR=1.09e-13). It was also higher in samples with 1q21 gain/amplification calls (median delta=0.268; FDR=1.24e-05; Fig. 5E-F). TXNDC5 showed a separate association with 1q21 gain/amplification (median delta=0.231; FDR=0.00843), while POU2AF1 was associated with 17p13 deletion (median delta=0.337; FDR=0.00533).

Adjusted models further reduced the risk that the CoMMpass result was purely an unadjusted association. In the requested Cox model including age, sex, ISS, and 1q21 status, the plasma-secretory score remained associated with OS (HR=1.460 per 1 SD; 95% CI 1.069-1.993; p=0.0173; FDR=0.0445; Fig. 5D). The POU2AF1/XBP1/JCHAIN clinical subtype module also remained associated with OS under the same adjustment (HR=1.434; 95% CI 1.090-1.886; FDR=0.0299). These results support covariate-adjusted association evidence, but they do not establish prospective clinical utility.

### Current evidence chain and claim boundary

The final cross-cohort evidence chain supports a bounded translational claim: an MM bone marrow plasma-secretory program is spatially enriched, reproduced at the program level in an independent Xenium spatial cohort, localized to plasma-cell compartments in single-cell data, supported by external GEO bulk cohorts, associated with OS and ISS in CoMMpass/GDC, linked to public NG2024 RNA-subtype and 1q21 annotations, and retained in basic adjusted OS models. This evidence is sufficient to proceed with a manuscript centered on the plasma-secretory clinical subtype axis.

However, the current analysis does not complete validation for PFS or treatment response. R-ISS remains unavailable as a direct public endpoint unless all required laboratory and cytogenetic components can be reconstructed under accepted clinical definitions. These endpoints require fuller MMRF/CoMMpass clinical files, such as harmonized clinical tables, treatment-response tables, survival/progression tables, and cytogenetic or canonical-variant annotations from MMRF Virtual Lab or Researcher Gateway releases.

## Discussion

This study identifies and validates a plasma-secretory MM bone marrow axis across spatial, Xenium, single-cell, external bulk, and CoMMpass/GDC clinical layers. The key strength of the analysis is not the rediscovery of plasma-cell biology alone, but the integration of spatial reproducibility, localization, and clinical validation. Spatial transcriptomics identified the program in MM bone marrow tissue; GSE299193 Xenium reproduced the program-level signal in an independent spatial cohort; single-cell RNA-seq localized the signal to plasma-cell annotated compartments; external bulk cohorts connected the axis to subtype and risk features; and CoMMpass/GDC linked the axis to OS and ISS.

The results refine the role of TXNDC5. TXNDC5 was spatially enriched and strongly detected in plasma cells, supporting it as a localization candidate within the axis. Nevertheless, first-pass external clinical evidence did not support presenting TXNDC5 as a standalone prognostic marker, and GSE299193 did not contain TXNDC5 in the extracted Xenium panel. The more defensible clinical construct is the broader plasma-secretory axis, especially the POU2AF1/XBP1/JCHAIN clinical subtype module and the curated plasma-secretory score.

The CoMMpass/GDC and NG2024 validation substantially strengthens the manuscript. In a large baseline CD138+ RNA-seq cohort, the plasma-secretory score was associated with OS event, ISS stage, median-split OS, PR RNA-subtype probability, and 1q21 gain/amplification. The requested adjusted Cox model showed that the plasma-secretory score remained associated with OS after adjustment for age, sex, ISS, and 1q21. These results connect the spatially discovered axis to clinically meaningful risk features. Importantly, the effect should be interpreted as a subtype/risk-associated transcriptional program rather than a fully validated clinical classifier. Prospective validation and treatment-stratified analyses would be required before clinical deployment.

Several limitations should be emphasized. First, GSE299193 now provides independent spatial program-level validation, but its Xenium panel lacks TXNDC5, JCHAIN, and SDC1, so it cannot validate every candidate gene from the discovery signature. Second, single-cell validation used marker-inferred cell categories rather than a fully harmonized reference atlas. Third, external bulk cohorts differ in platform, annotation, and endpoint definitions. Fourth, the open GDC clinical slice and public NG2024 supplements still lack sufficient complete fields for PFS and treatment-response analyses. These limitations are partly mitigated by the multi-cohort consistency of the plasma-secretory axis and adjusted CoMMpass/NG2024 models, but they should remain explicit in the manuscript.

Future work should prioritize fuller MMRF/CoMMpass clinical integration. The most valuable additions would be R-ISS, PFS, first-line treatment response, treatment class, and high-risk cytogenetic annotations. If these data can be obtained through MMRF Virtual Lab or Researcher Gateway, the current pipeline can be extended to test whether the plasma-secretory axis remains associated with risk after adjustment for established clinical and genomic variables.

## Data Availability Draft

All datasets used in the current analysis are public or open-access processed datasets. Spatial transcriptomics discovery data were obtained from GSE269875. Independent Xenium spatial validation used GSE299193. Single-cell RNA-seq validation used GSE271107. External bulk validation used GSE24080 and GSE2658. CoMMpass/GDC processed RNA-seq and open clinical data were obtained from the GDC MMRF-COMMPASS project. Public CoMMpass molecular annotations were obtained from Skerget et al. Nature Genetics 2024 supplementary tables. Fuller MMRF/CoMMpass clinical analyses involving PFS and treatment response were not performed in the current draft because the required controlled clinical files were not available locally.

## Draft Reference Anchors To Verify Before Submission

- MMRF-COMMPASS molecular subtyping and genomic landscape papers.
- Skerget et al. Nature Genetics 2024 CoMMpass molecular-profiling supplementary tables.
- MMRF Virtual Lab / CoMMpass clinical data documentation.
- GDC MMRF-COMMPASS data access documentation.
- Primary spatial transcriptomics source for GSE269875.
- Primary Xenium spatial transcriptomics source for GSE299193.
- Primary single-cell RNA-seq source for GSE271107.
- Primary cohort publications or GEO records for GSE24080 and GSE2658.
