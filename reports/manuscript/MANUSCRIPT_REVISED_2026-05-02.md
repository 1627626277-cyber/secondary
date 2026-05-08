# A spatially reproducible plasma-secretory bone marrow program linked to molecular risk in multiple myeloma

Target journal draft: BMC Medical Genomics.
Revised manuscript — 2026-05-02 (post-review revision).

## Running Title

Spatial plasma-secretory program in myeloma

## Abstract

### Background

Multiple myeloma develops within a spatially organized bone marrow niche. Bulk genomic studies have defined molecular subtypes and risk features, but the spatial localization and clinical relevance of transcriptional programs remain less clear.

### Methods

We integrated public spatial transcriptomics, Xenium spatial profiling, single-cell RNA sequencing, external bulk cohorts, MMRF-COMMPASS/GDC RNA-seq, and public CoMMpass molecular annotations. Module scores were tested across GSE269875, GSE299193, GSE271107, GSE24080, GSE2658, CoMMpass/GDC, and NG2024/Skerget public CoMMpass supplementary annotations. Spatial organization was assessed using spot-level Moran's I and nearest-neighbor enrichment. Survival associations were evaluated using log-rank tests and Cox models with sensitivity adjustment for PR subtype probability, proliferation, cytogenetic risk, and public purity or tumor-burden proxies.

### Results

In GSE269875, the plasma-secretory score was higher in myeloma than control bone marrow, with sample-level median difference 0.709, Cohen's d 3.129, and Mann-Whitney p=0.0256. Spot-level analysis showed non-random spatial organization of the program, with plasma-secretory Moran's I significant in 9 of 9 samples and median Moran's I 0.477; cross-program comparison showed that stromal ECM (median 0.383) and myeloid-inflammatory (median 0.352) programs also exhibited spatial autocorrelation, consistent with structured marrow architecture, but plasma-secretory spatial organization was more disease-associated. Independent Xenium analysis in GSE299193 reproduced the program-level signal across 22 samples; active myeloma or relapsed myeloma samples had higher plasma-secretory scores than Ctrl/MGUS/SM samples, with median difference 0.766 and FDR=5.75e-04. In GSE271107 single-cell data, the axis localized to marker-inferred plasma-cell compartments. In CoMMpass/GDC and public NG2024 annotations, the score was associated with OS, ISS, PR RNA-subtype probability, and 1q21 gain or amplification. The basic adjusted OS model showed HR 1.460 per standard deviation, FDR=0.0485. The association persisted after low-purity adjustment (HR 1.553, FDR=0.0358), arguing against a purity-surrogate interpretation, but was attenuated after additional PR and proliferation adjustment (HR 1.150, FDR=0.444). This attenuation indicates molecular-context dependence rather than independence from known risk biology. A logistic model linked the plasma-secretory score to 1q21 status after full molecular-context adjustment (OR 1.396, FDR=0.0467).

### Conclusions

These results support a spatially reproducible plasma-secretory bone marrow program that is linked to PR/proliferation/1q21 molecular-risk context in multiple myeloma. The spatial information adds tissue-level organization and partial molecular-context-independent associations beyond bulk RNA subtype classification, but the program should not be presented as a fully independent clinical biomarker. TXNDC5 is best framed as a spatial and single-cell localization candidate, whereas POU2AF1, XBP1, and JCHAIN better support the subtype-axis interpretation. Current public data do not complete R-ISS, PFS, or treatment-response validation.

## Keywords

multiple myeloma; spatial transcriptomics; Xenium; single-cell RNA-seq; CoMMpass; overall survival; 1q21

## Background

Multiple myeloma is a plasma-cell malignancy of the bone marrow. Its clinical course varies widely across patients. Genomic profiling has linked this heterogeneity to recurrent copy-number events, structural alterations, and expression subtypes [1-9]. These bulk profiles are clinically informative. They also lose spatial context.

The bone marrow niche is not uniform. Malignant plasma cells coexist with immune, stromal, endothelial, and hematopoietic compartments. Spatial organization may shape local transcriptional states. It may also influence disease progression. Recent myeloma spatial and single-cell studies show that this context can be resolved at tissue and cellular scales [10,11]. However, most public spatial datasets remain small and clinically sparse.

A defensible translational analysis must therefore connect several evidence layers. Spatial data can identify a tissue-level program and test whether it is locally organized rather than randomly distributed. Single-cell data can localize the program. Bulk clinical cohorts can test retrospective outcome and risk associations. Molecular annotation can then place the program within known myeloma biology [12].

We applied this strategy to public multiple myeloma datasets. The initial spatial discovery analysis identified a plasma-secretory program enriched in myeloma bone marrow. This program included canonical plasma-cell and secretory pathway genes. Such biology is expected in myeloma, so the novelty is not the rediscovery of plasma-cell markers or a new single-gene biomarker. We therefore framed the project around a spatially reproducible plasma-secretory state linked to PR-like molecular risk and 1q21-associated clinical context.

Within this framework, TXNDC5 serves as a localization candidate. It links the spatial discovery result to plasma-cell expression in single-cell data. POU2AF1, XBP1, and JCHAIN form a more clinically useful subtype module. We tested this axis across spatial, Xenium, single-cell, bulk, and CoMMpass evidence layers.

## Methods

### Study design

This was a retrospective public-data integrative analysis. The workflow used six evidence layers and was designed as a claim-bounded evidence chain rather than as a de novo clinical biomarker study.

The layers were spatial discovery, independent Xenium spatial reproducibility, single-cell localization, external bulk association, CoMMpass/GDC retrospective clinical association, and NG2024 molecular annotation [1,10,11,13-20].

The primary biological construct was a plasma-secretory bone marrow program. The clinical module contained POU2AF1, XBP1, and JCHAIN.

TXNDC5 was evaluated as a spatial and single-cell localization candidate. It was not treated as a standalone prognostic classifier.

All analyses used public data or open processed resources. No private MMRF clinical table was used for completed claims.

Analyses were run with Python 3.13.9. Key packages were pandas 2.3.3, numpy 2.3.5, scipy 1.16.3, matplotlib 3.10.6, scanpy 1.12, seaborn 0.13.2, statsmodels 0.14.5, and h5py 3.15.1 [21,22].

### Operational definition of the plasma-secretory program

In this study, "plasma-secretory program" refers to a module score constructed as the mean of standardized expression values of six prespecified genes: TXNDC5, POU2AF1, XBP1, JCHAIN, MZB1, and SDC1. The term "program" denotes a statistical transcriptional module derived from public transcriptomic data; it does not imply verified transcriptional co-regulation, shared upstream signaling, or functional coupling beyond what the individual genes' known biology supports. The module score has operational continuity with the PR RNA subtype defined by Skerget et al. (2024), and the spatial analysis tests whether the module shows tissue-level spatial organization beyond what bulk RNA-seq subtype classification captures.

### Score construction and missing-data rules

Expression values were analyzed in the normalized scale available for each public dataset or after log transformation where count-like values were provided. Within each cohort, gene-level values used for module scoring were standardized before score construction.

Module scores were calculated as the mean of available standardized genes. Genes absent from a platform were not imputed. A module was scored only when at least one prespecified gene was present, and platform coverage was reported when absent genes affected interpretation. A cohort-by-module gene coverage table and an all-tested-association inventory were generated with `scripts/30_module_coverage_and_testing_inventory.py`.

For spatial and Xenium datasets, spot-level or cell-level gene values were summarized to sample-level scores before group comparisons. The main plasma-secretory module contained TXNDC5, POU2AF1, XBP1, JCHAIN, MZB1, and SDC1. The clinical subtype module contained POU2AF1, XBP1, and JCHAIN. For single-cell data, candidate genes and module scores were summarized by marker-inferred cell category and sample-aware strata where available.

Missing clinical, cytogenetic, subtype, or covariate fields were handled by endpoint-specific complete-case analysis. Denominators therefore differ across analyses and are reported with each result when they affect interpretation.

### Candidate gene selection transparency

The six plasma-secretory module genes were selected from the GSE269875 spatial candidate ranking (script `scripts/10_sample_aware_spatial_signatures.py`) as the top-ranked genes overlapping plasma-cell and secretory-pathway annotation. The ranking used sample-level z-score differences between MM and control groups, and the six-gene threshold was chosen to balance pathway coverage with module interpretability. All six genes have prior literature support for plasma-cell or secretory-pathway biology. Alternative thresholds would produce overlapping but not identical gene sets; the present module should be interpreted as one representative plasma-secretory gene set rather than a uniquely optimal set. The clinical subtype module (POU2AF1, XBP1, JCHAIN) was selected from the discovery set as the subset with the strongest cross-platform clinical association signal in external bulk cohorts.

### Spatial discovery

GSE269875 human bone marrow spatial matrices were used for discovery [15]. Processed matrices were checked with `scripts/08_processed_spatial_matrix_qc.py`.

Preliminary clustering and marker summaries were generated with `scripts/09_preliminary_spatial_clustering.py`.

Sample-aware program discovery used `scripts/10_sample_aware_spatial_signatures.py`. The analysis scored curated marrow and immune programs.

Programs included plasma-secretory, myeloid-inflammatory, T/NK cytotoxic, stromal, endothelial, erythroid, and cycling states.

Scores were summarized at sample level. MM and control samples were compared using median differences, Cohen's d, and Mann-Whitney tests.

Spatial organization was tested with `scripts/28_spatial_autocorrelation_niche_analysis.py`. Spot-level module scores for all seven curated programs (plasma-secretory, myeloid-inflammatory, T/NK cytotoxic, stromal ECM, endothelial angiogenic, cycling proliferation, and erythroid) were merged with array-row and array-column coordinates. Moran's I was calculated within each sample using a 6-nearest-neighbor graph and 199 within-sample label permutations. The permutation count of 199 was chosen as a fixed budget balancing computational efficiency with stable p-value estimation at the α=0.05 level; p-values at or near zero reflect that no permuted arrangement produced an I value as extreme as the observed value for the tested spots. Local neighborhood enrichment compared the mean score of nearest neighbors around plasma-secretory-high spots, defined as the within-sample top quartile, with the corresponding neighbor scores around other spots. The focal spot was excluded from each neighbor set. Primary neighborhood summaries used non-overlapping niche programs and omitted plasma-cell marker scores to reduce circularity with the plasma-secretory definition.

Spatial discovery outputs were stored in `analysis/spatial_candidate_signatures`.

### Xenium spatial reproducibility

GSE299193 raw Xenium files were downloaded from GEO [10,16]. The raw tar file matched the expected byte size.

Reproducibility testing used `scripts/18_gse299193_xenium_validation.py`. The script avoided full extraction of large image and transcript files.

Only `cell_feature_matrix.h5` files and lightweight cell metadata were extracted. Twenty-two matrices were included.

Sample groups were Ctrl, MGUS, SM, MM, and RM. Active disease was defined as MM or RM.

Non-active comparison samples were Ctrl, MGUS, and SM. Sample-level scores used genes present in each Xenium matrix.

The panel-covered clinical module used POU2AF1 and XBP1. TXNDC5, JCHAIN, and SDC1 were absent from these matrices.

Active and non-active samples were compared using Mann-Whitney tests. FDR was controlled across the Xenium association family.

Outputs were stored in `analysis/gse299193_xenium_validation`.

### Single-cell localization

GSE271107 single-cell RNA-seq data were used for localization [11,17]. The workflow used `scripts/11_gse271107_scrna_validation.py`.

Cells were filtered using minimum 200 detected genes, minimum 500 total counts, and maximum 25% mitochondrial reads. Across 19 samples, 143,748 raw cells and 127,528 post-QC cells were summarized. Cells were assigned to marker-inferred broad cell categories using canonical marker sets from the original GSE271107 publication. These labels are marker-inferred rather than reference-atlas-harmonized, and cells with ambiguous marker profiles were retained under their best-match category. Malignant and normal plasma cells were not separated because the reference data lack a validated malignant-plasma-cell classifier. Candidate genes and module scores were compared across compartments.

The primary localization endpoint was expression in marker-inferred plasma-cell compartments. Detection fraction was calculated as the fraction above zero. The analysis did not attempt malignant-versus-normal plasma-cell separation and is therefore interpreted as compartment localization rather than malignant-specific localization.

Single-cell outputs were stored in `analysis/scrna_gse271107_validation`.

### Bulk association

GSE24080 and GSE2658 were used as external bulk expression cohorts [18,19,23,24]. Initial analyses used `scripts/12_bulk_clinical_validation.py`.

The clinical subtype refinement used `scripts/13_plasma_secretory_subtype_refinement.py`. That step centered POU2AF1, XBP1, and JCHAIN.

Available clinical and cytogenetic annotations were parsed from public sample records. These included 24-month OS status and FISH 1q21 amplification.

Mann-Whitney tests compared binary endpoint groups. Median-split Fisher tests were used for binary high-versus-low score summaries.

Where time-to-event information was available, log-rank tests were used. FDR correction was applied within tested association families.

Bulk outputs were stored in `analysis/bulk_clinical_validation` and `analysis/plasma_secretory_subtype_refinement`.

### CoMMpass/GDC retrospective clinical association

MMRF-COMMPASS/GDC RNA-seq association testing used `scripts/14_commppass_gdc_validation.py` [14,20].

RNA-seq files were filtered to baseline visit-1 bone marrow CD138+ samples. The final association table contained 762 samples.

Gene-level TPM values were log-transformed and z-scored. Module scores were calculated as mean z scores across available genes.

OS event associations used Mann-Whitney tests. ISS ordinal associations used Spearman correlation.

Median-split survival analyses used log-rank tests. FDR correction was applied across the CoMMpass association family.

CoMMpass/GDC outputs were stored in `analysis/commppass_gdc_validation`.

### NG2024 molecular annotation

Public Skerget et al. NG2024 supplementary tables were downloaded and audited with `scripts/19_skerget_ng2024_public_supplement_audit.py` [1].

Molecular annotation analysis used `scripts/20_skerget_ng2024_molecular_annotation_validation.py`.

Tables were joined by CoMMpass patient identifier. The public Skerget et al. patient-feature table matched all 762 local baseline samples.

RNA-subtype probability analyses used complete cases. The PR subtype association contained 707 complete samples.

Associations tested RNA subtype, 1q21 gain or amplification, 17p13 deletion, and cytogenetic high-risk features.

Continuous subtype probabilities used Spearman correlation. Binary annotations used Mann-Whitney tests.

Categorical RNA subtype tests used Kruskal-Wallis tests. FDR correction used the Benjamini-Hochberg method.

Adjusted models used `scripts/21_commppass_ng2024_adjusted_models.py`. Cox models used statsmodels proportional hazards regression.

The prespecified OS model adjusted for age, sex, ISS stage, and 1q21 status. Logistic and linear models used analogous covariates. Sensitivity models were generated with `scripts/29_commppass_sensitivity_models.py` and added PR subtype probability, proliferation score, 17p13 deletion, high-risk cytogenetics, low-purity probability, or CMMC tumor-burden proxy where available.

NG2024 outputs were stored in `analysis/skerget_ng2024_public_supplement` and `analysis/commppass_ng2024_adjusted_models`.

### Statistical analysis

All tests were two-sided unless stated otherwise. No parametric distribution was assumed for group comparisons.

Mann-Whitney tests compared continuous scores between binary groups. Spearman correlation tested ordinal or monotonic associations.

Kruskal-Wallis tests compared scores across RNA-subtype categories. Fisher exact tests assessed median-split binary score summaries.

Survival analyses used log-rank tests and Cox proportional hazards models. Cox models reported hazard ratios per one-standard-deviation score [25].

Logistic models reported odds ratios per one-standard-deviation score. Linear models reported beta coefficients for continuous subtype probabilities.

Multiple testing was controlled using Benjamini-Hochberg FDR. FDR correction was applied within each analysis family [26].

Analysis families were defined by cohort and endpoint class. Separate FDR families were used for spatial discovery, Xenium reproducibility, single-cell localization, external bulk associations, CoMMpass/GDC clinical associations, NG2024 molecular annotations, spatial organization analyses, and adjusted model families. Formal supplementary tables provide cohort-by-module gene coverage, all tested associations, and Cox sensitivity models.

The adjusted OS model used samples with complete age, sex, ISS, 1q21, OS time, and OS event fields.

The primary adjusted Cox model tested OS as a retrospective association endpoint. It was not trained, tuned, or validated as a prospective risk-prediction model.

Schoenfeld residual screening did not detect an FDR-significant PH violation for the primary score terms. The 1q21 covariate showed time-related residual structure.

Cox results are therefore reported as adjusted association models. They are not presented as prospective risk-prediction models.

### Figure generation and integrity checks

Manuscript figures were generated with `scripts/15_build_manuscript_figures.py`; spatial organization and sensitivity figures were finalized with `scripts/31_build_review_hardening_figure.py`. Outputs were stored in `analysis/manuscript_figures`.

The cross-cohort evidence table was generated with the same script. It links each evidence layer to a primary statistic.

Numeric traceability was checked in `reports/review/STAGE2_NUMERIC_INTEGRITY_CHECK_2026-04-30.md`.

A supplementary reproducibility appendix lists accession-level inputs, main scripts, output directories, and figure-panel traceability.

## Results

### Cross-cohort design defined a bounded evidence chain

The study was organized as a sequential evidence chain rather than as a single-cohort biomarker screen (Fig. 1). Spatial discovery was performed in GSE269875, independent spatial reproducibility was tested in GSE299193 Xenium data, single-cell localization was assessed in GSE271107, external bulk support was evaluated in GSE24080 and GSE2658, and clinical and molecular-risk associations were tested in MMRF-COMMPASS/GDC and public NG2024 CoMMpass annotations.

Table 1 summarizes the evidence levels and the claim boundary assigned to each dataset. The analysis supports a spatially reproducible and retrospectively associated plasma-secretory program linked to molecular-risk context. It does not establish a prospective clinical classifier, a treatment-selection marker, or completed R-ISS, PFS, or treatment-response validation.

### Spatial transcriptomics identified the plasma-secretory program (Fig. 2)

In GSE269875, sample-level module scoring showed that the plasma-secretory program was the most enriched curated program in myeloma bone marrow spatial samples. Myeloma samples had higher plasma-secretory scores than control bone marrow samples, with a median difference of 0.709, Cohen's d of 3.129, and Mann-Whitney p=0.0256 (Fig. 2A,B).

The spatial candidate ranking also prioritized plasma-cell and secretory-pathway genes, including XBP1, TXNDC5, POU2AF1, SDC1, MZB1, and JCHAIN (Fig. 2C). This result defined the discovery axis used in later analyses. It was not interpreted as evidence that any single gene is a standalone clinical biomarker.

Spot-level spatial organization analysis showed that the plasma-secretory score was not randomly distributed across the tissue grids. Plasma-secretory Moran's I was FDR-significant in all 9 GSE269875 samples, with median Moran's I 0.477 (Fig. 3A). MM samples had higher Moran's I than controls in this small cohort (median 0.571 versus 0.144; Mann-Whitney p=0.0238).

Spatial autocorrelation was not unique to the plasma-secretory program. Cross-program Moran's I comparison showed that stromal ECM (median 0.383) and myeloid-inflammatory (median 0.352) programs also exhibited strong spatial autocorrelation across all samples, consistent with the structured multicompartment architecture of bone marrow tissue. The plasma-secretory program showed the highest median Moran's I among the seven curated programs (Supplementary Table S4). In control bone marrow alone, myeloid-inflammatory (median 0.352) and stromal ECM (median 0.215) programs showed higher spatial autocorrelation than plasma-secretory (median 0.144), indicating that plasma-secretory spatial organization is more disease-associated than the spatial organization of other marrow programs. This interpretation is limited by the small discovery cohort (n=9) and is reported as exploratory spatial screening rather than a validated disease-specific spatial signature.

Plasma-secretory-high spots showed local enrichment of non-overlapping stromal ECM, endothelial, myeloid, immune, and cycling neighbor programs after excluding the focal spot and omitting plasma-cell marker scores from the primary neighbor analysis (Fig. 3B). This supports spatial clustering and exploratory niche association, but it does not prove causal cell-cell interaction.

### Independent Xenium data reproduced the program-level spatial signal (Fig. 4)

The spatial discovery signal was then tested in GSE299193, an independent Xenium dataset containing 22 human bone marrow samples from Ctrl, MGUS, SM, MM, and relapsed MM groups. Active MM/RM samples showed higher plasma-secretory scores than Ctrl/MGUS/SM samples, with a median difference of 0.766, Mann-Whitney p=0.000182, and FDR=0.000575 (Fig. 4, left).

A Xenium panel-covered POU2AF1/XBP1 module showed a concordant active-disease pattern, with median difference 1.068, p=0.000287, and FDR=0.000575 (Fig. 4, middle). The extracted Xenium matrices contained MZB1, TNFRSF17, SLAMF7, IRF4, PIM2, POU2AF1, and XBP1, but not TXNDC5, JCHAIN, or SDC1 (Fig. 4, right). GSE299193 therefore strengthens the spatial reproducibility claim at program level, while not directly reproducing the absent genes.

### Single-cell data localized the axis to plasma-cell compartments (Fig. 5)

GSE271107 single-cell RNA-seq data were used to localize the spatial program across marker-inferred cell categories. After QC, 127,528 cells from 19 samples were included, spanning HD, MGUS, SMM, and MM stages. Plasma-cell compartments showed the strongest plasma-secretory program score among broad cell groups (Fig. 5B).

TXNDC5 was consistently expressed in marker-inferred plasma-cell compartments. Across 8,007 marker-inferred plasma cells from 19 sample-level strata, TXNDC5 detection was 96.44% on a cell-weighted basis, while the unweighted mean across plasma-cell sample strata was 94.86% (HD 1,463 cells; MGUS 1,016; SMM 649; MM 4,879; Fig. 5A). This supports TXNDC5 as a spatial and single-cell localization candidate within the plasma-secretory axis. It does not support presenting TXNDC5 as a standalone prognostic biomarker or as a malignant-plasma-cell-specific marker.

### External bulk cohorts supported a clinical subtype module (Fig. 6)

External GEO bulk cohorts were used to test whether the spatially identified axis connected to clinical or cytogenetic annotations outside the spatial datasets. In GSE2658, the POU2AF1/XBP1/JCHAIN module was associated with FISH 1q21 amplification (FDR=1.65e-05). In GSE24080, XBP1 was associated with 24-month overall survival death (FDR=0.0362; Fig. 6).

These findings supported the use of a broader clinical subtype module rather than a TXNDC5-only interpretation. Because the GSE2658 module effect direction was not identical to the CoMMpass direction, this result is described as external association support rather than uniform directional replication across all platforms. Possible explanations include platform differences, sample composition, FISH cutoff differences, therapy-era effects, expression-platform normalization, and incomplete equivalence of module-gene coverage across cohorts.

### CoMMpass/GDC linked the axis to OS, ISS, and molecular risk (Fig. 7)

The axis was next evaluated in 762 baseline MMRF-COMMPASS/GDC bone marrow CD138+ RNA-seq samples. The plasma-secretory score was associated with overall survival event, with event-versus-nonevent median difference 0.346 and FDR=9.31e-06 (Fig. 7A,B). Median-split survival analysis also supported an OS association, with log-rank p=0.00668 and FDR=0.0401 (Fig. 7C).

The same score showed an ordinal association with ISS stage (Spearman rho=0.132, p=0.000316, FDR=0.0019). These analyses link the axis to retrospective clinical risk features, but they do not test R-ISS, PFS, or treatment response.

Public NG2024 CoMMpass molecular annotations further placed the axis in a known molecular-risk context. Local baseline CoMMpass samples matched public Skerget et al. patient-feature annotations for 762 of 762 patients, and 707 complete cases were available for RNA-subtype probability analyses. The plasma-secretory score correlated with PR RNA-subtype probability (Spearman rho=0.340, FDR=5.43e-19) and was higher in samples with 1q21 gain or amplification (median difference 0.268, FDR=1.24e-05; Fig. 7E,F).

Gene-level NG2024 analyses were consistent with the candidate framing. TXNDC5 expression was associated with 1q21 gain or amplification (median difference 0.231, FDR=0.00843), and POU2AF1 was associated with 17p13 deletion (median difference 0.337, FDR=0.00533). These observations provide molecular annotation support for the axis, not a completed clinical assay.

### Adjusted models constrained the OS interpretation (Fig. 8)

Finally, we tested whether the CoMMpass survival association persisted after adjustment. The prespecified basic Cox model included age, sex, ISS stage, and 1q21 status. In 660 complete cases, the plasma-secretory score was associated with overall survival, with hazard ratio 1.460 per standard deviation, 95% CI 1.069-1.993, p=0.0173, and FDR=0.0485 (Fig. 8).

The association was sensitive to molecular-context covariates. After adding PR subtype probability, the HR was 1.317 with FDR=0.200. After adding both PR subtype probability and proliferation score, the HR was 1.150 with FDR=0.444. The association remained nominally supported in the model adding del17p and high-risk cytogenetics (HR 1.449, FDR=0.0493) and in the model adding low-purity probability (HR 1.553, FDR=0.0358), but not in the smaller CMMC tumor-burden proxy model (n=262, FDR=0.269). The sensitivity direction is informative: adjusting for a public purity proxy strengthened rather than weakened the HR, arguing against the interpretation that the plasma-secretory score is merely a tumor-purity surrogate. Instead, the attenuation by PR probability and proliferation score indicates that the OS association is molecular-context-dependent rather than purity-driven. These results support a PR/proliferation/1q21 molecular-risk context rather than an independent clinical biomarker. A logistic model still linked the plasma-secretory score to 1q21 status after adjustment for age, sex, ISS, PR probability, proliferation, and low-purity probability, with odds ratio 1.396 per standard deviation and FDR=0.0467.

## Discussion

This study identifies a plasma-secretory bone marrow program in multiple myeloma. The program was discovered in spatial transcriptomics. It showed non-random spatial organization and local neighborhood enrichment. It was reproduced in an independent Xenium cohort. It localized to plasma-cell compartments in single-cell data. It was also associated with survival, ISS, RNA subtype, and 1q21 status in bulk cohorts.

The main contribution is cross-platform coherence. Plasma-cell biology alone is not novel in myeloma. The stronger finding is that a spatially enriched and spatially clustered program connects to PR-like subtype probability, proliferation context, 1q21 status, and retrospective OS association. The OS association persists after basic adjustment for age, sex, ISS, and 1q21, but is attenuated after adding PR subtype probability and proliferation score. This attenuation is informative: it places the program within known molecular-risk biology rather than establishing an independent clinical biomarker.

### What spatial information adds beyond bulk molecular classification

A central interpretive question is whether the plasma-secretory spatial signal is merely a spatial readout of the PR RNA subtype defined by Skerget et al. (2024), or whether the tissue-level analysis contributes information beyond bulk classification. The plasma-secretory score correlates with PR subtype probability (Spearman rho=0.340, FDR=5.43e-19), confirming a substantial overlap. The adjusted Cox models show that the OS signal is attenuated after PR and proliferation adjustment, consistent with molecular-context dependence.

However, two observations support incremental spatial information. First, the spatial organization analysis shows that the plasma-secretory program is non-randomly distributed in tissue (median Moran's I 0.477), and this spatial autocorrelation is more disease-associated than the autocorrelation of other marrow programs, which are spatially structured in both MM and control bone marrow. This tissue-level organization is not captured by bulk RNA-seq subtype classification and may reflect local niche effects on plasma-cell transcriptional state. Second, the 1q21 association persists in a logistic model after full adjustment for PR probability, proliferation, and low-purity probability (OR 1.396, FDR=0.0467), suggesting that a component of the axis is not fully subsumed by the PR subtype classification. Together, these observations support a model in which the plasma-secretory transcriptional state is partly captured by bulk RNA subtype, but retains tissue-level spatial organization and cytogenetic associations that are not fully resolved by subtype alone.

The present public data do not resolve whether spatial clustering reflects plasma-cell-intrinsic transcriptional programs, microenvironment-driven expression states, or a spatially varying mixture of plasma-cell subclones. This remains an important direction for spatial multi-omics studies with matched genetic and transcriptional readouts.

This interpretation is consistent with recent bone marrow niche, myeloma precursor, and outcome-linked single-cell atlas work, which places myeloma biology in a multicompartment marrow context rather than in tumor-intrinsic expression alone [27-29]. It is also consistent with tumor-marker and prediction-reporting guidance: the present study reports retrospective association and context dependence, not a trained clinical prediction model or prospective biomarker assay [12,30].

The analysis also clarifies the role of TXNDC5. TXNDC5 is supported by spatial discovery and single-cell localization. It should be presented as a localization candidate. The clinical risk signal is better carried by the broader axis. POU2AF1, XBP1, and JCHAIN are more suitable for clinical-subtype framing.

GSE299193 materially strengthens the spatial component. It reduces dependence on the small GSE269875 discovery cohort. However, the Xenium panel lacks TXNDC5, JCHAIN, and SDC1. This limits gene-level reproducibility. The result should therefore be described as program-level spatial reproducibility. The Xenium data also include pre-malignant samples (MGUS and SMM) that were grouped as non-active controls in the primary comparison. Exploratory inspection of individual MGUS and SMM scores showed intermediate values between Ctrl and MM, consistent with a continuum rather than a binary transition. This observation is preliminary given the small per-group sample sizes and warrants dedicated precursor-condition spatial studies.

Several limitations remain. First, this is a retrospective public-data analysis. Second, single-cell labels were marker-inferred rather than harmonized with a full reference atlas, and malignant and normal plasma cells were not separated. Third, external bulk cohorts differ in platform, FISH cutoff, treatment era, endpoint definition, and module-gene coverage, which may explain the non-identical direction observed in GSE2658. Fourth, the axis partly reflects plasma-cell abundance and tumor-burden context. The low-purity and CMMC sensitivity models partially address this issue in CoMMpass, but they do not replace direct flow cytometry or histology-anchored tumor-content measurement. Fifth, public GDC and NG2024 files did not support complete PFS, R-ISS, or treatment-response validation.

Sixth, this study was conducted and written by a single author. While the analysis scripts, figure-generation code, and result tables are available for independent verification, the lack of a second analyst for independent code review and cross-validation of interpretive decisions is a methodological limitation. Multi-analyst studies may identify interpretive nuances or alternative analytical choices that a single analyst could miss.

These limitations define the next extension. Fuller MMRF clinical files could test PFS, R-ISS, treatment response, and therapy-line effects. Independent analytical replication with alternative module definitions and statistical frameworks would strengthen confidence in the core findings. Until then, the current manuscript should make a bounded claim. The data support a spatially reproducible, plasma-cell localized program linked to molecular-risk context and retrospective clinical association. They do not support a prospective classifier, independent prognostic biomarker, or treatment-selection marker.

## Conclusions

This public-data integrative analysis supports a spatially reproducible plasma-secretory bone marrow program in multiple myeloma. The program was spatially enriched and spatially clustered in GSE269875 and reproduced at program level in GSE299193 Xenium data. Cross-program spatial autocorrelation analysis showed that stromal and myeloid programs also exhibit tissue-level organization, but plasma-secretory spatial autocorrelation was more disease-associated. Single-cell data localized the axis to plasma-cell compartments. CoMMpass/GDC and NG2024 annotations connected the axis to OS, ISS, PR subtype probability, proliferation context, and 1q21 status, with sensitivity models indicating that the OS association is not independent of PR/proliferation biology but is not merely a tumor-purity surrogate. TXNDC5 should be framed as a localization candidate. POU2AF1, XBP1, and JCHAIN are more suitable for subtype-axis framing. The spatial component adds tissue-level information beyond bulk molecular classification, but this remains a molecular-context-dependent program rather than an independent clinical biomarker.

## Declarations

### Ethics approval and consent to participate

Not applicable. This study analyzed publicly available, de-identified datasets and did not involve new recruitment of human participants, new collection of human specimens, or access to directly identifiable private information.

### Consent for publication

Not applicable.

### Availability of data and materials

The datasets supporting the conclusions of this article are available in public repositories. Spatial discovery used GEO accession GSE269875. Xenium spatial reproducibility used GEO accession GSE299193. Single-cell localization used GEO accession GSE271107. Bulk association used GEO accessions GSE24080 and GSE2658. CoMMpass/GDC RNA-seq and open clinical data were obtained from the NCI Genomic Data Commons MMRF-COMMPASS project. Public CoMMpass molecular annotations were obtained from the supplementary tables of Skerget et al. Nature Genetics 2024. Dataset accessions and primary source links are listed in the References.

### Code availability

The public code and compact-result repository is `https://github.com/1627626277-cyber/secondary`.

### Competing interests

The author declares that there are no competing interests.

### Funding

No specific funding was received for this work.

### Authors' contributions

Z.J. is the sole author. Z.J. conceived the study, designed and performed the analysis, curated the public datasets, generated the figures, interpreted the results, wrote and revised the manuscript, and approved the final version. This statement should be revised if additional authors are added before submission.

### Acknowledgements

The author(s) acknowledge the investigators and participants associated with the public GEO, GDC, and CoMMpass resources used in this study.

## References

1. Skerget S, Penaherrera D, Chari A, Jagannath S, Siegel DS, Vij R, et al. Comprehensive molecular profiling of multiple myeloma identifies refined copy number and expression subtypes. Nat Genet. 2024;56(9):1878-1889. doi:10.1038/s41588-024-01853-0.
2. Maura F, Bolli N, Angelopoulos N, Dawson KJ, Leongamornlert D, Martincorena I, et al. Genomic landscape and chronological reconstruction of driver events in multiple myeloma. Nat Commun. 2019;10(1):3835. doi:10.1038/s41467-019-11680-1.
3. Palumbo A, Avet-Loiseau H, Oliva S, Lokhorst HM, Goldschmidt H, Rosinol L, et al. Revised International Staging System for Multiple Myeloma: A Report From International Myeloma Working Group. J Clin Oncol. 2015;33(26):2863-2869. doi:10.1200/JCO.2015.61.2267.
4. Rajkumar SV, Dimopoulos MA, Palumbo A, Blade J, Merlini G, Mateos MV, et al. International Myeloma Working Group updated criteria for the diagnosis of multiple myeloma. Lancet Oncol. 2014;15(12):e538-e548. doi:10.1016/S1470-2045(14)70442-5.
5. Chapman MA, Lawrence MS, Keats JJ, Cibulskis K, Sougnez C, Schinzel AC, et al. Initial genome sequencing and analysis of multiple myeloma. Nature. 2011;471(7339):467-472. doi:10.1038/nature09837.
6. Rajkumar SV. Multiple myeloma: 2022 update on diagnosis, risk stratification, and management. Am J Hematol. 2022;97(8):1086-1107. doi:10.1002/ajh.26590.
7. Greipp PR, San Miguel J, Durie BG, Crowley JJ, Barlogie B, Blade J, et al. International staging system for multiple myeloma. J Clin Oncol. 2005;23(15):3412-3420. doi:10.1200/JCO.2005.04.242.
8. Zhan F, Huang Y, Colla S, Stewart JP, Hanamura I, Gupta S, et al. The molecular classification of multiple myeloma. Blood. 2006;108(6):2020-2028. doi:10.1182/blood-2005-11-013458.
9. Hanamura I, Stewart JP, Huang Y, Zhan F, Santra M, Sawyer JR, et al. Frequent gain of chromosome band 1q21 in plasma-cell dyscrasias detected by fluorescence in situ hybridization: incidence increases from MGUS to relapsed myeloma and is related to prognosis and disease progression following tandem stem-cell transplantation. Blood. 2006;108(5):1724-1732. doi:10.1182/blood-2006-03-009910.
10. Yip RKH, Er J, Qin L, Nguyen QH, Motyer A, Rimes JS, et al. Profiling the spatial architecture of multiple myeloma in human bone marrow trephine biopsy specimens with spatial transcriptomics. Blood. 2025;146(15):1837-1849. doi:10.1182/blood.2025028896.
11. Yu W, Zhan J, Wang Y, Cao X, Yu A, Rao Y, et al. Single-cell transcriptomics identifies PDIA4 as a marker of progression and therapeutic vulnerability in multiple myeloma. J Transl Med. 2025;23(1):1136. doi:10.1186/s12967-025-07098-7.
12. McShane LM, Altman DG, Sauerbrei W, Taube SE, Gion M, Clark GM, et al. Reporting recommendations for tumor marker prognostic studies (REMARK). J Natl Cancer Inst. 2005;97(16):1180-1184. doi:10.1093/jnci/dji237.
13. Barrett T, Wilhite SE, Ledoux P, Evangelista C, Kim IF, Tomashevsky M, et al. NCBI GEO: archive for functional genomics data sets - update. Nucleic Acids Res. 2013;41(Database issue):D991-D995. doi:10.1093/nar/gks1193.
14. Zhang Z, Hernandez K, Savage J, Li S, Miller D, Agrawal S, et al. Uniform genomic data analysis in the NCI Genomic Data Commons. Nat Commun. 2021;12(1):1226. doi:10.1038/s41467-021-21254-9.
15. National Center for Biotechnology Information. GEO Series GSE269875: Spatial transcriptomics unveils novel potential disease mechanisms associated with the microenvironment in multiple myeloma. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269875. Accessed 1 May 2026.
16. National Center for Biotechnology Information. GEO Series GSE299193: Profiling the spatial architecture of multiple myeloma in human bone marrow trephines with spatial transcriptomics. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299193. Accessed 1 May 2026.
17. National Center for Biotechnology Information. GEO Series GSE271107: Single-cell RNA sequencing of bone marrow aspirate samples from multiple myeloma and its precursor conditions. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE271107. Accessed 1 May 2026.
18. National Center for Biotechnology Information. GEO Series GSE24080: MAQC-II Project: Multiple myeloma data set. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE24080. Accessed 1 May 2026.
19. National Center for Biotechnology Information. GEO Series GSE2658: Gene expression profiles of multiple myeloma. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE2658. Accessed 1 May 2026.
20. National Cancer Institute Genomic Data Commons. Multiple Myeloma Research Foundation CoMMpass Study. https://gdc.cancer.gov/about-gdc/contributed-genomic-data-cancer-research/foundation-medicine/multiple-myeloma-research-foundation-mmrf. Accessed 1 May 2026.
21. Wolf FA, Angerer P, Theis FJ. SCANPY: large-scale single-cell gene expression data analysis. Genome Biol. 2018;19(1):15. doi:10.1186/s13059-017-1382-0.
22. Seabold S, Perktold J. Statsmodels: econometric and statistical modeling with Python. Proceedings of the 9th Python in Science Conference. 2010;92-96. https://www.statsmodels.org/. Accessed 1 May 2026.
23. Shi L, Campbell G, Jones WD, Campagne F, Wen Z, Walker SJ, et al. The MicroArray Quality Control (MAQC)-II study of common practices for the development and validation of microarray-based predictive models. Nat Biotechnol. 2010;28(8):827-838. doi:10.1038/nbt.1665.
24. Liu Q, Sung AH, Chen Z, Liu J, Huang X, Deng Y. Feature selection and classification of MAQC-II breast cancer and multiple myeloma microarray gene expression data. PLoS One. 2009;4(12):e8250. doi:10.1371/journal.pone.0008250.
25. Cox DR. Regression models and life-tables. J R Stat Soc Series B Stat Methodol. 1972;34:187-220.
26. Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J R Stat Soc Series B Stat Methodol. 1995;57:289-300. doi:10.1111/j.2517-6161.1995.tb02031.x.
27. de Jong MME, Chen L, Raaijmakers MHGP, Cupedo T. Bone marrow inflammation in haematological malignancies. Nat Rev Immunol. 2024;24:543-558. doi:10.1038/s41577-024-01003-x.
28. Boiarsky R, Haradhvala NJ, Alberge JB, Sklavenitis-Pistofidis R, Mouhieddine TH, Zavidij O, et al. Single cell characterization of myeloma and its precursor conditions reveals transcriptional signatures of early tumorigenesis. Nat Commun. 2022;13:7040. doi:10.1038/s41467-022-33944-z.
29. Pilcher WC, Yao L, Gonzalez-Kozlova E, Pita-Juarez Y, Karagkouni D, Acharya CR, et al. A single-cell atlas characterizes dysregulation of the bone marrow immune microenvironment associated with outcomes in multiple myeloma. Nat Cancer. 2026;7:224-246. doi:10.1038/s43018-025-01072-4.
30. Collins GS, Moons KGM, Dhiman P, Riley RD, Beam AL, Van Calster B, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. BMJ. 2024;385:e078378. doi:10.1136/bmj-2023-078378.
