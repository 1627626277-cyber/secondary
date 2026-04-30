# Spatial validation and clinical association of a plasma-secretory bone marrow program in multiple myeloma

Target journal draft: BMC Medical Genomics.

## Running Title

Plasma-secretory spatial program in multiple myeloma

## Abstract

Multiple myeloma develops within a spatially organized bone marrow niche. Bulk genomic studies have defined molecular subtypes and risk features. Yet the spatial localization and clinical relevance of transcriptional programs remain less clear. We integrated public spatial transcriptomics, Xenium spatial profiling, single-cell RNA sequencing, external bulk cohorts, MMRF-COMMPASS/GDC RNA-seq, and public CoMMpass molecular annotations. The analysis focused on a plasma-secretory bone marrow program in multiple myeloma.

In GSE269875, the plasma-secretory score was higher in myeloma than control bone marrow. The sample-level median difference was 0.709, with Cohen's d of 3.129 and Mann-Whitney p=0.0256. Independent Xenium validation in GSE299193 reproduced this program-level signal across 22 samples. Active myeloma or relapsed myeloma samples showed higher plasma-secretory scores than Ctrl/MGUS/SM samples. The median difference was 0.766, with FDR=5.75e-04. A panel-covered POU2AF1/XBP1 module showed a similar difference. In GSE271107 single-cell data, TXNDC5 was consistently expressed in marker-inferred plasma cells. External bulk cohorts supported a broader clinical subtype module. The POU2AF1/XBP1/JCHAIN module was associated with 1q21 amplification in GSE2658. XBP1 was associated with 24-month overall survival death in GSE24080.

In 762 baseline MMRF-COMMPASS/GDC CD138+ RNA-seq samples, the plasma-secretory score was associated with overall survival event, ISS stage, and median-split survival. Public NG2024 CoMMpass annotations linked the score to PR RNA-subtype probability and 1q21 gain or amplification. In a Cox model adjusted for age, sex, ISS, and 1q21, the score remained associated with overall survival. The hazard ratio was 1.460 per standard deviation, with 95% CI 1.069-1.993 and FDR=0.0445.

These results support a reproducible plasma-secretory bone marrow program in multiple myeloma. TXNDC5 is best framed as a spatial and single-cell localization candidate. POU2AF1, XBP1, and JCHAIN better support the clinical subtype axis. The current public data do not complete R-ISS, PFS, or treatment-response validation.

## Keywords

multiple myeloma; spatial transcriptomics; Xenium; single-cell RNA-seq; CoMMpass; overall survival; 1q21

## Background

Multiple myeloma is a plasma-cell malignancy of the bone marrow. Its clinical course varies widely across patients. Genomic profiling has linked this heterogeneity to recurrent copy-number events, structural alterations, and expression subtypes. These bulk profiles are clinically informative. They also lose spatial context.

The bone marrow niche is not uniform. Malignant plasma cells coexist with immune, stromal, endothelial, and hematopoietic compartments. Spatial organization may shape local transcriptional states. It may also influence disease progression. Spatial and single-cell technologies can resolve this context. However, most public spatial datasets remain small and clinically sparse.

A defensible translational analysis must therefore connect several evidence layers. Spatial data can identify a tissue-level program. Single-cell data can localize the program. Bulk clinical cohorts can test outcome and risk associations. Molecular annotation can then place the program within known myeloma biology.

We applied this strategy to public multiple myeloma datasets. The initial spatial discovery analysis identified a plasma-secretory program enriched in myeloma bone marrow. This program included canonical plasma-cell and secretory pathway genes. Such biology is expected in myeloma, so a single-gene biomarker claim would be weak. We therefore framed the project around a broader plasma-secretory subtype axis.

Within this framework, TXNDC5 serves as a localization candidate. It links the spatial discovery result to plasma-cell expression in single-cell data. POU2AF1, XBP1, and JCHAIN form a more clinically useful subtype module. We tested this axis across spatial, Xenium, single-cell, bulk, and CoMMpass evidence layers.

## Results

### Spatial transcriptomics identified a plasma-secretory program in myeloma bone marrow

We first analyzed GSE269875 human bone marrow spatial transcriptomics data. Sample-level module scores were calculated for curated cell-state programs. These included plasma-secretory, myeloid-inflammatory, T/NK cytotoxic, stromal, endothelial, erythroid, and cycling programs.

The plasma-secretory program showed the strongest myeloma enrichment. Myeloma samples had higher scores than control samples. The median difference was 0.709. The Cohen's d was 3.129. The Mann-Whitney p value was 0.0256 (Fig. 2).

Gene-level ranking prioritized canonical plasma-cell and secretory markers. These included XBP1, TXNDC5, POU2AF1, SDC1, MZB1, and JCHAIN. This result established a spatial discovery signal. It did not establish a standalone clinical biomarker.

### GSE299193 reproduced the spatial signal at program level

We next tested whether the spatial signal generalized to an independent platform. GSE299193 Xenium data included 22 human bone marrow samples. The cohort contained Ctrl, MGUS, SM, MM, and relapsed MM groups.

The plasma-secretory score was higher in active MM/RM samples than Ctrl/MGUS/SM samples. The median difference was 0.766. The Mann-Whitney p value was 0.000182. The FDR was 0.000575 (Fig. 6).

A panel-covered POU2AF1/XBP1 module showed a similar pattern. The median difference was 1.068. The p value was 0.000287. The FDR was 0.000575.

The Xenium feature matrices contained MZB1, TNFRSF17, SLAMF7, IRF4, PIM2, POU2AF1, and XBP1. They did not contain TXNDC5, JCHAIN, or SDC1. GSE299193 therefore validates the program-level spatial signal. It does not directly validate those absent genes.

### Single-cell data localized the axis to plasma-cell compartments

We then analyzed GSE271107 single-cell RNA-seq data. Cells were summarized by marker-inferred cell categories. Plasma cells showed the strongest plasma-secretory score among broad cell types (Fig. 3).

TXNDC5 was consistently expressed in marker-inferred plasma cells. The mean log-normalized expression was 2.196. The detection fraction was 94.86 percent across summarized plasma-cell observations.

These findings support TXNDC5 as a localization candidate. They do not support presenting TXNDC5 as a standalone prognostic biomarker.

### External bulk cohorts supported a clinical subtype module

We evaluated independent bulk cohorts to test clinical relevance. GSE2658 and GSE24080 provided expression data with available clinical or cytogenetic annotations.

In GSE2658, the POU2AF1/XBP1/JCHAIN module was associated with 1q21 amplification. The FDR was 1.65e-05. In GSE24080, XBP1 was associated with 24-month overall survival death. The FDR was 0.0362 (Fig. 4).

These results shifted the clinical framing. The stronger clinical construct is the broader plasma-secretory axis. TXNDC5 remains a localization candidate within that axis.

### CoMMpass/GDC linked the axis to survival and ISS

We next tested the axis in 762 baseline MMRF-COMMPASS/GDC CD138+ RNA-seq samples. The plasma-secretory score was associated with overall survival event. The event-versus-nonevent median difference was 0.346. The FDR was 9.31e-06 (Fig. 5).

The same score was associated with ISS ordinal stage. The Spearman rho was 0.132. The p value was 0.000316. The FDR was 0.0019.

Median-split survival analysis also supported the association. Patients with higher plasma-secretory score had worse overall survival. The log-rank p value was 0.00668. The FDR was 0.0401.

### Public NG2024 annotations connected the axis to molecular risk

We joined public NG2024 CoMMpass molecular annotations to local CoMMpass scores. Table 1 matched 762 of 762 baseline samples. Table 7 RNA-subtype predictions matched 707 samples.

The plasma-secretory score correlated with PR RNA-subtype probability. The Spearman rho was 0.340. The FDR was 5.43e-19. The score was also higher in samples with 1q21 gain or amplification. The median difference was 0.268. The FDR was 1.24e-05.

TXNDC5 expression was associated with 1q21 gain or amplification. The median difference was 0.231. The FDR was 0.00843. POU2AF1 was associated with 17p13 deletion. The median difference was 0.337. The FDR was 0.00533.

### Adjusted models supported an independent OS association

We tested whether the CoMMpass survival association persisted after basic adjustment. The prespecified Cox model included age, sex, ISS, and 1q21 status.

The plasma-secretory score remained associated with overall survival. The hazard ratio was 1.460 per standard deviation. The 95% confidence interval was 1.069-1.993. The p value was 0.0173. The FDR was 0.0445.

The POU2AF1/XBP1/JCHAIN module also remained associated with survival. The hazard ratio was 1.434. The 95% confidence interval was 1.090-1.886. The FDR was 0.0299.

These models support covariate-adjusted association. They do not establish clinical utility.

## Discussion

This study identifies a plasma-secretory bone marrow program in multiple myeloma. The program was discovered in spatial transcriptomics. It was reproduced in an independent Xenium cohort. It localized to plasma-cell compartments in single-cell data. It was also associated with survival, ISS, RNA subtype, and 1q21 status in bulk cohorts.

The main contribution is cross-platform coherence. Plasma-cell biology alone is not novel in myeloma. The stronger finding is that a spatially enriched program connects to clinical and molecular-risk annotations. This connection persists after basic adjustment for age, sex, ISS, and 1q21.

The analysis also clarifies the role of TXNDC5. TXNDC5 is supported by spatial discovery and single-cell localization. It should be presented as a localization candidate. The clinical risk signal is better carried by the broader axis. POU2AF1, XBP1, and JCHAIN are more suitable for clinical-subtype framing.

GSE299193 materially strengthens the spatial component. It reduces dependence on the small GSE269875 discovery cohort. However, the Xenium panel lacks TXNDC5, JCHAIN, and SDC1. This limits gene-level validation. The result should therefore be described as program-level spatial validation.

Several limitations remain. First, this is a retrospective public-data analysis. Second, single-cell labels were marker-inferred rather than harmonized with a full reference atlas. Third, external bulk cohorts differ in platform and endpoint definitions. Fourth, the axis may partly reflect plasma-cell abundance. Fifth, public GDC and NG2024 files did not support complete PFS, R-ISS, or treatment-response validation.

These limitations define the next extension. Fuller MMRF clinical files could test PFS, R-ISS, treatment response, and therapy-line effects. Until then, the current manuscript should make a bounded claim. The data support a spatially reproducible, plasma-cell localized, clinically associated program. They do not support a prospective classifier or treatment-selection biomarker.

## Conclusions

This public-data integrative analysis supports a plasma-secretory bone marrow program in multiple myeloma. The program was spatially enriched in GSE269875 and reproduced at program level in GSE299193 Xenium data. Single-cell data localized the axis to plasma-cell compartments. CoMMpass/GDC and NG2024 annotations connected the axis to OS, ISS, PR subtype probability, and 1q21 status. TXNDC5 should be framed as a localization candidate. POU2AF1, XBP1, and JCHAIN are more suitable for clinical subtype framing.

## Methods

### Study design

This was a retrospective public-data integrative analysis. The workflow used six evidence layers.

The layers were spatial discovery, second spatial validation, single-cell localization, external bulk validation, CoMMpass/GDC validation, and NG2024 annotation.

The primary biological construct was a plasma-secretory bone marrow program. The clinical module contained POU2AF1, XBP1, and JCHAIN.

TXNDC5 was evaluated as a spatial and single-cell localization candidate. It was not treated as a standalone prognostic classifier.

All analyses used public data or open processed resources. No private MMRF clinical table was used for completed claims.

Analyses were run with Python 3.13.9. Key packages were pandas 2.3.3, numpy 2.3.5, scipy 1.16.3, matplotlib 3.10.6, scanpy 1.12, seaborn 0.13.2, statsmodels 0.14.5, and h5py 3.15.1.

### Spatial discovery

GSE269875 human bone marrow spatial matrices were used for discovery. Processed matrices were checked with `scripts/08_processed_spatial_matrix_qc.py`.

Preliminary clustering and marker summaries were generated with `scripts/09_preliminary_spatial_clustering.py`.

Sample-aware program discovery used `scripts/10_sample_aware_spatial_signatures.py`. The analysis scored curated marrow and immune programs.

Programs included plasma-secretory, myeloid-inflammatory, T/NK cytotoxic, stromal, endothelial, erythroid, and cycling states.

Scores were summarized at sample level. MM and control samples were compared using median differences, Cohen's d, and Mann-Whitney tests.

Spatial discovery outputs were stored in `analysis/spatial_candidate_signatures`.

### Xenium validation

GSE299193 raw Xenium files were downloaded from GEO. The raw tar file matched the expected byte size.

Validation used `scripts/18_gse299193_xenium_validation.py`. The script avoided full extraction of large image and transcript files.

Only `cell_feature_matrix.h5` files and lightweight cell metadata were extracted. Twenty-two matrices were included.

Sample groups were Ctrl, MGUS, SM, MM, and RM. Active disease was defined as MM or RM.

Non-active comparison samples were Ctrl, MGUS, and SM. Sample-level scores used genes present in each Xenium matrix.

The panel-covered clinical module used POU2AF1 and XBP1. TXNDC5, JCHAIN, and SDC1 were absent from these matrices.

Active and non-active samples were compared using Mann-Whitney tests. FDR was controlled across the Xenium association family.

Outputs were stored in `analysis/gse299193_xenium_validation`.

### Single-cell localization

GSE271107 single-cell RNA-seq data were used for localization. The workflow used `scripts/11_gse271107_scrna_validation.py`.

Cells were summarized by marker-inferred broad cell categories. Candidate genes and module scores were compared across compartments.

The primary localization endpoint was expression in marker-inferred plasma cells. Detection fraction was calculated as the fraction above zero.

Single-cell outputs were stored in `analysis/scrna_gse271107_validation`.

### Bulk validation

GSE24080 and GSE2658 were used as external bulk expression cohorts. Initial analyses used `scripts/12_bulk_clinical_validation.py`.

The clinical subtype refinement used `scripts/13_plasma_secretory_subtype_refinement.py`. That step centered POU2AF1, XBP1, and JCHAIN.

Available clinical and cytogenetic annotations were parsed from public sample records. These included 24-month OS status and FISH 1q21 amplification.

Mann-Whitney tests compared binary endpoint groups. Median-split Fisher tests were used for binary high-versus-low score summaries.

Where time-to-event information was available, log-rank tests were used. FDR correction was applied within tested association families.

Bulk outputs were stored in `analysis/bulk_clinical_validation` and `analysis/plasma_secretory_subtype_refinement`.

### CoMMpass/GDC validation

MMRF-COMMPASS/GDC RNA-seq validation used `scripts/14_commppass_gdc_validation.py`.

RNA-seq files were filtered to baseline visit-1 bone marrow CD138+ samples. The final validation table contained 762 samples.

Gene-level TPM values were log-transformed and z-scored. Module scores were calculated as mean z scores across available genes.

OS event associations used Mann-Whitney tests. ISS ordinal associations used Spearman correlation.

Median-split survival analyses used log-rank tests. FDR correction was applied across the CoMMpass association family.

CoMMpass/GDC outputs were stored in `analysis/commppass_gdc_validation`.

### NG2024 molecular annotation

Public Skerget et al. NG2024 supplementary tables were downloaded and audited with `scripts/19_skerget_ng2024_public_supplement_audit.py`.

Molecular annotation validation used `scripts/20_skerget_ng2024_molecular_annotation_validation.py`.

Tables were joined by CoMMpass patient identifier. Supplementary Table 1 matched all 762 local baseline samples.

RNA-subtype probability analyses used complete cases. The PR subtype association contained 707 complete samples.

Associations tested RNA subtype, 1q21 gain or amplification, 17p13 deletion, and cytogenetic high-risk features.

Continuous subtype probabilities used Spearman correlation. Binary annotations used Mann-Whitney tests.

Categorical RNA subtype tests used Kruskal-Wallis tests. FDR correction used the Benjamini-Hochberg method.

Adjusted models used `scripts/21_commppass_ng2024_adjusted_models.py`. Cox models used statsmodels proportional hazards regression.

The prespecified OS model adjusted for age, sex, ISS stage, and 1q21 status. Logistic and linear models used analogous covariates.

NG2024 outputs were stored in `analysis/skerget_ng2024_public_supplement` and `analysis/commppass_ng2024_adjusted_models`.

### Statistical analysis

All tests were two-sided unless stated otherwise. No parametric distribution was assumed for group comparisons.

Mann-Whitney tests compared continuous scores between binary groups. Spearman correlation tested ordinal or monotonic associations.

Kruskal-Wallis tests compared scores across RNA-subtype categories. Fisher exact tests assessed median-split binary score summaries.

Survival analyses used log-rank tests and Cox proportional hazards models. Cox models reported hazard ratios per one-standard-deviation score.

Logistic models reported odds ratios per one-standard-deviation score. Linear models reported beta coefficients for continuous subtype probabilities.

Multiple testing was controlled using Benjamini-Hochberg FDR. FDR correction was applied within each analysis family.

Analysis families were defined by cohort and endpoint class. Complete-case analysis was used for models requiring covariates.

The adjusted OS model used samples with complete age, sex, ISS, 1q21, OS time, and OS event fields.

Schoenfeld residual screening did not detect an FDR-significant PH violation for the primary score terms. The 1q21 covariate showed time-related residual structure.

Cox results are therefore reported as adjusted association models. They are not presented as prospective risk-prediction models.

### Figure generation and integrity checks

Manuscript figures were generated with `scripts/15_build_manuscript_figures.py`. Outputs were stored in `analysis/manuscript_figures`.

The cross-cohort evidence table was generated with the same script. It links each evidence layer to a primary statistic.

Numeric traceability was checked in `reports/review/STAGE2_NUMERIC_INTEGRITY_CHECK_2026-04-30.md`.

## Data Availability

All analyzed datasets were public or open-access processed resources. Spatial discovery used GSE269875. Xenium validation used GSE299193. Single-cell validation used GSE271107. Bulk validation used GSE24080 and GSE2658. CoMMpass/GDC RNA-seq and open clinical data were obtained from the MMRF-COMMPASS project. Public molecular annotations were obtained from Skerget et al. Nature Genetics 2024 supplementary tables.

## Code Availability

All analysis scripts are stored in the project `scripts` directory. Manuscript figures and evidence tables are stored in `analysis/manuscript_figures`. Validation reports are stored in `reports/validation`.

## References

1. Skerget S, Penaherrera D, Chari A, Jagannath S, Siegel DS, Vij R, et al. Comprehensive molecular profiling of multiple myeloma identifies refined copy number and expression subtypes. Nat Genet. 2024;56(9):1878-1889. doi:10.1038/s41588-024-01853-0.
2. Yip RKH, Er J, Qin L, Nguyen QH, Motyer A, Rimes JS, et al. Profiling the spatial architecture of multiple myeloma in human bone marrow trephine biopsy specimens with spatial transcriptomics. Blood. 2025;146(15):1837-1849. doi:10.1182/blood.2025028896.
3. Yu W, Zhan J, Wang Y, Cao X, Yu A, Rao Y, et al. Single-cell transcriptomics identifies PDIA4 as a marker of progression and therapeutic vulnerability in multiple myeloma. J Transl Med. 2025;23(1):1136. doi:10.1186/s12967-025-07098-7.
4. Maura F, Bolli N, Angelopoulos N, Dawson KJ, Leongamornlert D, Martincorena I, et al. Genomic landscape and chronological reconstruction of driver events in multiple myeloma. Nat Commun. 2019;10(1):3835. doi:10.1038/s41467-019-11680-1.
5. Palumbo A, Avet-Loiseau H, Oliva S, Lokhorst HM, Goldschmidt H, Rosinol L, et al. Revised International Staging System for Multiple Myeloma: A Report From International Myeloma Working Group. J Clin Oncol. 2015;33(26):2863-2869. doi:10.1200/JCO.2015.61.2267.
6. Rajkumar SV, Dimopoulos MA, Palumbo A, Blade J, Merlini G, Mateos MV, et al. International Myeloma Working Group updated criteria for the diagnosis of multiple myeloma. Lancet Oncol. 2014;15(12):e538-e548. doi:10.1016/S1470-2045(14)70442-5.
7. McShane LM, Altman DG, Sauerbrei W, Taube SE, Gion M, Clark GM, et al. Reporting recommendations for tumor marker prognostic studies (REMARK). J Natl Cancer Inst. 2005;97(16):1180-1184. doi:10.1093/jnci/dji237.
8. Wolf FA, Angerer P, Theis FJ. SCANPY: large-scale single-cell gene expression data analysis. Genome Biol. 2018;19(1):15. doi:10.1186/s13059-017-1382-0.
9. Chapman MA, Lawrence MS, Keats JJ, Cibulskis K, Sougnez C, Schinzel AC, et al. Initial genome sequencing and analysis of multiple myeloma. Nature. 2011;471(7339):467-472. doi:10.1038/nature09837.
10. Shi L, Campbell G, Jones WD, Campagne F, Wen Z, Walker SJ, et al. The MicroArray Quality Control (MAQC)-II study of common practices for the development and validation of microarray-based predictive models. Nat Biotechnol. 2010;28(8):827-838. doi:10.1038/nbt.1665.
11. Liu Q, Sung AH, Chen Z, Liu J, Huang X, Deng Y. Feature selection and classification of MAQC-II breast cancer and multiple myeloma microarray gene expression data. PLoS One. 2009;4(12):e8250. doi:10.1371/journal.pone.0008250.
12. Rajkumar SV. Multiple myeloma: 2022 update on diagnosis, risk stratification, and management. Am J Hematol. 2022;97(8):1086-1107. doi:10.1002/ajh.26590.
13. Greipp PR, San Miguel J, Durie BG, Crowley JJ, Barlogie B, Blade J, et al. International staging system for multiple myeloma. J Clin Oncol. 2005;23(15):3412-3420. doi:10.1200/JCO.2005.04.242.
14. Zhan F, Huang Y, Colla S, Stewart JP, Hanamura I, Gupta S, et al. The molecular classification of multiple myeloma. Blood. 2006;108(6):2020-2028. doi:10.1182/blood-2005-11-013458.
15. Hanamura I, Stewart JP, Huang Y, Zhan F, Santra M, Sawyer JR, et al. Frequent gain of chromosome band 1q21 in plasma-cell dyscrasias detected by fluorescence in situ hybridization: incidence increases from MGUS to relapsed myeloma and is related to prognosis and disease progression following tandem stem-cell transplantation. Blood. 2006;108(5):1724-1732. doi:10.1182/blood-2006-03-009910.
16. Barrett T, Wilhite SE, Ledoux P, Evangelista C, Kim IF, Tomashevsky M, et al. NCBI GEO: archive for functional genomics data sets - update. Nucleic Acids Res. 2013;41(Database issue):D991-D995. doi:10.1093/nar/gks1193.
17. Zhang Z, Hernandez K, Savage J, Li S, Miller D, Agrawal S, et al. Uniform genomic data analysis in the NCI Genomic Data Commons. Nat Commun. 2021;12(1):1226. doi:10.1038/s41467-021-21254-9.
18. National Center for Biotechnology Information. GEO Series GSE269875: Spatial transcriptomics unveils novel potential disease mechanisms associated with the microenvironment in multiple myeloma. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269875. Accessed 1 May 2026.
19. National Center for Biotechnology Information. GEO Series GSE299193: Profiling the spatial architecture of multiple myeloma in human bone marrow trephines with spatial transcriptomics. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299193. Accessed 1 May 2026.
20. National Center for Biotechnology Information. GEO Series GSE271107: Single-cell RNA sequencing of bone marrow aspirate samples from multiple myeloma and its precursor conditions. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE271107. Accessed 1 May 2026.
21. National Center for Biotechnology Information. GEO Series GSE24080: MAQC-II Project: Multiple myeloma data set. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE24080. Accessed 1 May 2026.
22. National Center for Biotechnology Information. GEO Series GSE2658: Gene expression profiles of multiple myeloma. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE2658. Accessed 1 May 2026.
23. National Cancer Institute Genomic Data Commons. Multiple Myeloma Research Foundation CoMMpass Study. https://gdc.cancer.gov/about-gdc/contributed-genomic-data-cancer-research/foundation-medicine/multiple-myeloma-research-foundation-mmrf. Accessed 1 May 2026.
24. Cox DR. Regression models and life-tables. J R Stat Soc Series B Stat Methodol. 1972;34:187-220.
25. Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J R Stat Soc Series B Stat Methodol. 1995;57:289-300. doi:10.1111/j.2517-6161.1995.tb02031.x.
26. Seabold S, Perktold J. Statsmodels: econometric and statistical modeling with Python. Proceedings of the 9th Python in Science Conference. 2010;92-96. https://www.statsmodels.org/. Accessed 1 May 2026.
