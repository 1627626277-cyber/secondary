# Spatial plasma-secretory marrow programme linked to myeloma risk

Target journal draft: BMC Medical Genomics.
Revised manuscript — 2026-05-02 (post-review revision, Nature-polished).

## Running Title

Spatial plasma-secretory programme in myeloma

## Abstract

### Background

Multiple myeloma develops within a spatially organised bone marrow niche. Bulk genomic studies have defined molecular subtypes and risk features. The spatial localisation and clinical relevance of transcriptional programmes remain less clear.

### Methods

We integrated public spatial transcriptomics, Xenium spatial profiling, single-cell RNA sequencing, external bulk cohorts, MMRF-COMMPASS/GDC RNA-seq, and public CoMMpass molecular annotations. Module scores were tested across GSE269875, GSE299193, GSE271107, GSE24080, GSE2658, CoMMpass/GDC, and NG2024/Skerget public CoMMpass supplementary annotations. Spatial organisation was assessed using spot-level Moran's I and nearest-neighbour enrichment. Survival associations were evaluated using log-rank tests and Cox models with sensitivity adjustment for PR subtype probability, proliferation, cytogenetic risk, and public purity or tumour-burden proxies.

### Results

In GSE269875, the plasma-secretory score was higher in myeloma than control bone marrow. The sample-level median difference was 0.709, with Cohen's d 3.129 and Mann-Whitney p=0.0256. Spot-level analysis showed non-random spatial organisation of the programme. Plasma-secretory Moran's I was significant in 9 of 9 samples, with median Moran's I 0.477. Cross-programme comparison showed that stromal ECM (median 0.383) and myeloid-inflammatory (median 0.352) programmes also exhibited spatial autocorrelation, consistent with structured marrow architecture. The plasma-secretory spatial organisation was more disease-associated. Independent Xenium analysis in GSE299193 reproduced the programme-level signal across 22 samples. Active or relapsed myeloma samples had higher plasma-secretory scores than Ctrl/MGUS/SM samples, with median difference 0.766 and FDR=5.75e-04. In GSE271107 single-cell data, the axis localised to marker-inferred plasma-cell compartments. In CoMMpass/GDC and public NG2024 annotations, the score was associated with OS, ISS, PR RNA-subtype probability, and 1q21 gain or amplification. The basic adjusted OS model showed HR 1.460 per standard deviation, FDR=0.0485. The association persisted after low-purity adjustment (HR 1.553, FDR=0.0358), arguing against a purity-surrogate interpretation. It was attenuated after additional PR and proliferation adjustment (HR 1.150, FDR=0.444). This attenuation indicates molecular-context dependence rather than independence from known risk biology. A logistic model linked the plasma-secretory score to 1q21 status after full molecular-context adjustment (OR 1.396, FDR=0.0467).

### Conclusions

These results support a spatially reproducible plasma-secretory bone marrow programme linked to PR/proliferation/1q21 molecular-risk context in multiple myeloma. The spatial information adds tissue-level organisation and partial molecular-context-independent associations beyond bulk RNA subtype classification. The programme should not be presented as a fully independent clinical biomarker. TXNDC5 is best framed as a spatial and single-cell localisation candidate. POU2AF1, XBP1, and JCHAIN better support the subtype-axis interpretation. Current public data do not complete R-ISS, PFS, or treatment-response validation.

## Keywords

multiple myeloma; spatial transcriptomics; Xenium; single-cell RNA-seq; CoMMpass; overall survival; 1q21

## Background

Multiple myeloma is a plasma-cell malignancy of the bone marrow. Its clinical course varies widely across patients. Genomic profiling has linked this heterogeneity to recurrent copy-number events, structural alterations, and expression subtypes [1-9]. These bulk profiles are clinically informative. They also lose spatial context.

The bone marrow niche is not uniform. Malignant plasma cells coexist with immune, stromal, endothelial, and haematopoietic compartments. Spatial organisation may shape local transcriptional states. It may also influence disease progression. Recent myeloma spatial and single-cell studies show that this context can be resolved at tissue and cellular scales [10,11]. Most public spatial datasets remain small and clinically sparse.

A defensible translational analysis must therefore connect several evidence layers. Spatial data can identify a tissue-level programme and test whether it is locally organised rather than randomly distributed. Single-cell data can localise the programme. Bulk clinical cohorts can test retrospective outcome and risk associations. Molecular annotation can then place the programme within known myeloma biology [12].

We applied this strategy to public multiple myeloma datasets. The initial spatial discovery analysis identified a plasma-secretory programme enriched in myeloma bone marrow. This programme included canonical plasma-cell and secretory-pathway genes. Such biology is expected in myeloma. The novelty is not the rediscovery of plasma-cell markers or a new single-gene biomarker. We therefore framed the project around a spatially reproducible plasma-secretory state linked to PR-like molecular risk and 1q21-associated clinical context.

Within this framework, TXNDC5 serves as a localisation candidate. It links the spatial discovery result to plasma-cell expression in single-cell data. POU2AF1, XBP1, and JCHAIN form a more clinically useful subtype module. We tested this axis across spatial, Xenium, single-cell, bulk, and CoMMpass evidence layers.

## Methods

### Study design

This was a retrospective public-data integrative analysis. The workflow used six evidence layers. It was designed as a claim-bounded evidence chain rather than as a de novo clinical biomarker study.

The layers were spatial discovery, independent Xenium spatial reproducibility, single-cell localisation, external bulk association, CoMMpass/GDC retrospective clinical association, and NG2024 molecular annotation [1,10,11,13-20].

The primary biological construct was a plasma-secretory bone marrow programme. The clinical module contained POU2AF1, XBP1, and JCHAIN.

TXNDC5 was evaluated as a spatial and single-cell localisation candidate. It was not treated as a standalone prognostic classifier.

All analyses used public data or open processed resources. No private MMRF clinical table was used for completed claims.

Analyses were run with Python 3.13.9. Key packages were pandas 2.3.3, numpy 2.3.5, scipy 1.16.3, matplotlib 3.10.6, scanpy 1.12, seaborn 0.13.2, statsmodels 0.14.5, and h5py 3.15.1 [21,22].

### Operational definition of the plasma-secretory programme

In this study, "plasma-secretory programme" refers to a module score constructed as the mean of standardised expression values of six prespecified genes: TXNDC5, POU2AF1, XBP1, JCHAIN, MZB1, and SDC1. The term "programme" denotes a statistical transcriptional module derived from public transcriptomic data. It does not imply verified transcriptional co-regulation, shared upstream signalling, or functional coupling beyond what the individual genes' known biology supports. The module score has operational continuity with the PR RNA subtype defined by Skerget et al. (2024). The spatial analysis tests whether the module shows tissue-level spatial organisation beyond what bulk RNA-seq subtype classification captures.

### Score construction and missing-data rules

Expression values were analysed in the normalised scale available for each public dataset. Where count-like values were provided, log transformation was applied. Within each cohort, gene-level values used for module scoring were standardised before score construction.

Module scores were calculated as the mean of available standardised genes. Genes absent from a platform were not imputed. A module was scored only when at least one prespecified gene was present. Platform coverage was reported when absent genes affected interpretation. A cohort-by-module gene coverage table and an all-tested-association inventory were generated with `scripts/30_module_coverage_and_testing_inventory.py`.

For spatial and Xenium datasets, spot-level or cell-level gene values were summarised to sample-level scores before group comparisons. The main plasma-secretory module contained TXNDC5, POU2AF1, XBP1, JCHAIN, MZB1, and SDC1. The clinical subtype module contained POU2AF1, XBP1, and JCHAIN. For single-cell data, candidate genes and module scores were summarised by marker-inferred cell category and sample-aware strata where available.

Missing clinical, cytogenetic, subtype, or covariate fields were handled by endpoint-specific complete-case analysis. Denominators therefore differ across analyses and are reported with each result when they affect interpretation.

### Candidate gene selection transparency

The six plasma-secretory module genes were selected from the GSE269875 spatial candidate ranking (script `scripts/10_sample_aware_spatial_signatures.py`). They were the top-ranked genes overlapping plasma-cell and secretory-pathway annotation. The ranking used sample-level z-score differences between MM and control groups. The six-gene threshold was chosen to balance pathway coverage with module interpretability. All six genes have prior literature support for plasma-cell or secretory-pathway biology. Alternative thresholds would produce overlapping but not identical gene sets. The present module should be interpreted as one representative plasma-secretory gene set rather than a uniquely optimal set. The clinical subtype module (POU2AF1, XBP1, JCHAIN) was selected from the discovery set as the subset with the strongest cross-platform clinical association signal in external bulk cohorts.

### Spatial discovery

GSE269875 human bone marrow spatial matrices were used for discovery [15]. Processed matrices were checked with `scripts/08_processed_spatial_matrix_qc.py`.

Preliminary clustering and marker summaries were generated with `scripts/09_preliminary_spatial_clustering.py`.

Sample-aware programme discovery used `scripts/10_sample_aware_spatial_signatures.py`. The analysis scored curated marrow and immune programmes.

Programmes included plasma-secretory, myeloid-inflammatory, T/NK cytotoxic, stromal, endothelial, erythroid, and cycling states.

Scores were summarised at sample level. MM and control samples were compared using median differences, Cohen's d, and Mann-Whitney tests.

Spatial organisation was tested with `scripts/28_spatial_autocorrelation_niche_analysis.py`. Spot-level module scores for all seven curated programmes (plasma-secretory, myeloid-inflammatory, T/NK cytotoxic, stromal ECM, endothelial angiogenic, cycling proliferation, and erythroid) were merged with array-row and array-column coordinates. Moran's I was calculated within each sample using a 6-nearest-neighbour graph and 199 within-sample label permutations. The permutation count of 199 was chosen as a fixed budget balancing computational efficiency with stable p-value estimation at the α=0.05 level. P-values at or near zero reflect that no permuted arrangement produced an I value as extreme as the observed value for the tested spots. Local neighbourhood enrichment compared the mean score of nearest neighbours around plasma-secretory-high spots, defined as the within-sample top quartile, with the corresponding neighbour scores around other spots. The focal spot was excluded from each neighbour set. Primary neighbourhood summaries used non-overlapping niche programmes and omitted plasma-cell marker scores to reduce circularity with the plasma-secretory definition.

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

### Single-cell localisation

GSE271107 single-cell RNA-seq data were used for localisation [11,17]. The workflow used `scripts/11_gse271107_scrna_validation.py`.

Cells were filtered using minimum 200 detected genes, minimum 500 total counts, and maximum 25% mitochondrial reads. Across 19 samples, 143,748 raw cells and 127,528 post-QC cells were summarised. Cells were assigned to marker-inferred broad cell categories using canonical marker sets from the original GSE271107 publication. These labels are marker-inferred rather than reference-atlas-harmonised. Cells with ambiguous marker profiles were retained under their best-match category. Malignant and normal plasma cells were not separated because the reference data lack a validated malignant-plasma-cell classifier. Candidate genes and module scores were compared across compartments.

The primary localisation endpoint was expression in marker-inferred plasma-cell compartments. Detection fraction was calculated as the fraction above zero. The analysis did not attempt malignant-versus-normal plasma-cell separation. It is therefore interpreted as compartment localisation rather than malignant-specific localisation.

Single-cell outputs were stored in `analysis/scrna_gse271107_validation`.

### Bulk association

GSE24080 and GSE2658 were used as external bulk expression cohorts [18,19,23,24]. Initial analyses used `scripts/12_bulk_clinical_validation.py`.

The clinical subtype refinement used `scripts/13_plasma_secretory_subtype_refinement.py`. That step centred on POU2AF1, XBP1, and JCHAIN.

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

The prespecified OS model adjusted for age, sex, ISS stage, and 1q21 status. Logistic and linear models used analogous covariates. Sensitivity models were generated with `scripts/29_commppass_sensitivity_models.py`. These added PR subtype probability, proliferation score, 17p13 deletion, high-risk cytogenetics, low-purity probability, or CMMC tumour-burden proxy where available.

NG2024 outputs were stored in `analysis/skerget_ng2024_public_supplement` and `analysis/commppass_ng2024_adjusted_models`.

### Statistical analysis

All tests were two-sided unless stated otherwise. No parametric distribution was assumed for group comparisons.

Mann-Whitney tests compared continuous scores between binary groups. Spearman correlation tested ordinal or monotonic associations.

Kruskal-Wallis tests compared scores across RNA-subtype categories. Fisher exact tests assessed median-split binary score summaries.

Survival analyses used log-rank tests and Cox proportional hazards models. Cox models reported hazard ratios per one-standard-deviation score [25].

Logistic models reported odds ratios per one-standard-deviation score. Linear models reported beta coefficients for continuous subtype probabilities.

Multiple testing was controlled using Benjamini-Hochberg FDR. FDR correction was applied within each analysis family [26].

Analysis families were defined by cohort and endpoint class. Separate FDR families were used for spatial discovery, Xenium reproducibility, single-cell localisation, external bulk associations, CoMMpass/GDC clinical associations, NG2024 molecular annotations, spatial organisation analyses, and adjusted model families. Formal supplementary tables provide cohort-by-module gene coverage, all tested associations, and Cox sensitivity models.

The adjusted OS model used samples with complete age, sex, ISS, 1q21, OS time, and OS event fields.

The primary adjusted Cox model tested OS as a retrospective association endpoint. It was not trained, tuned, or validated as a prospective risk-prediction model.

Schoenfeld residual screening did not detect an FDR-significant PH violation for the primary score terms. The 1q21 covariate showed time-related residual structure.

Cox results are therefore reported as adjusted association models. They are not presented as prospective risk-prediction models.

### Figure generation and integrity checks

Manuscript figures were generated with `scripts/15_build_manuscript_figures.py`. Spatial organisation and sensitivity figures were finalised with `scripts/31_build_review_hardening_figure.py`. Outputs were stored in `analysis/manuscript_figures`.

The cross-cohort evidence table was generated with the same script. It links each evidence layer to a primary statistic.

Numeric traceability was checked in `reports/review/STAGE2_NUMERIC_INTEGRITY_CHECK_2026-04-30.md`.

A supplementary reproducibility appendix lists accession-level inputs, main scripts, output directories, and figure-panel traceability.

## Results

### Cross-cohort design defined a bounded evidence chain

The study was organised as a sequential evidence chain rather than as a single-cohort biomarker screen (Fig. 1). Spatial discovery was performed in GSE269875. Independent spatial reproducibility was tested in GSE299193 Xenium data. Single-cell localisation was assessed in GSE271107. External bulk support was evaluated in GSE24080 and GSE2658. Clinical and molecular-risk associations were tested in MMRF-COMMPASS/GDC and public NG2024 CoMMpass annotations.

Table 1 summarises the evidence levels and the claim boundary assigned to each dataset. The analysis supports a spatially reproducible and retrospectively associated plasma-secretory programme linked to molecular-risk context. It does not establish a prospective clinical classifier, a treatment-selection marker, or completed R-ISS, PFS, or treatment-response validation.

### Spatial transcriptomics identified the plasma-secretory programme (Fig. 2)

In GSE269875, sample-level module scoring showed that the plasma-secretory programme was the most enriched curated programme in myeloma bone marrow spatial samples. Myeloma samples had higher plasma-secretory scores than control bone marrow samples. The median difference was 0.709, with Cohen's d of 3.129 and Mann-Whitney p=0.0256 (Fig. 2A,B).

The spatial candidate ranking also prioritised plasma-cell and secretory-pathway genes. These included XBP1, TXNDC5, POU2AF1, SDC1, MZB1, and JCHAIN (Fig. 2C). This result defined the discovery axis used in later analyses. It was not interpreted as evidence that any single gene is a standalone clinical biomarker.

Spot-level spatial organisation analysis showed that the plasma-secretory score was not randomly distributed across the tissue grids. Plasma-secretory Moran's I was FDR-significant in all 9 GSE269875 samples, with median Moran's I 0.477 (Fig. 3A). MM samples had higher Moran's I than controls in this small cohort (median 0.571 versus 0.144; Mann-Whitney p=0.0238).

Spatial autocorrelation was not unique to the plasma-secretory programme. Cross-programme Moran's I comparison showed that stromal ECM (median 0.383) and myeloid-inflammatory (median 0.352) programmes also exhibited strong spatial autocorrelation across all samples. This is consistent with the structured multicompartment architecture of bone marrow tissue. The plasma-secretory programme showed the highest median Moran's I among the seven curated programmes (Supplementary Table S4). In control bone marrow alone, myeloid-inflammatory (median 0.352) and stromal ECM (median 0.215) programmes showed higher spatial autocorrelation than plasma-secretory (median 0.144). This indicates that plasma-secretory spatial organisation is more disease-associated than the spatial organisation of other marrow programmes. This interpretation is limited by the small discovery cohort (n=9) and is reported as exploratory spatial screening rather than a validated disease-specific spatial signature.

Plasma-secretory-high spots showed local enrichment of non-overlapping stromal ECM, endothelial, myeloid, immune, and cycling neighbour programmes. The focal spot was excluded and plasma-cell marker scores were omitted from the primary neighbour analysis (Fig. 3B). This supports spatial clustering and exploratory niche association. It does not prove causal cell-cell interaction.

### Independent Xenium data reproduced the programme-level spatial signal (Fig. 4)

The spatial discovery signal was then tested in GSE299193. This independent Xenium dataset contained 22 human bone marrow samples from Ctrl, MGUS, SM, MM, and relapsed MM groups. Active MM/RM samples showed higher plasma-secretory scores than Ctrl/MGUS/SM samples. The median difference was 0.766, with Mann-Whitney p=0.000182 and FDR=0.000575 (Fig. 4, left).

A Xenium panel-covered POU2AF1/XBP1 module showed a concordant active-disease pattern. The median difference was 1.068, with p=0.000287 and FDR=0.000575 (Fig. 4, middle). The extracted Xenium matrices contained MZB1, TNFRSF17, SLAMF7, IRF4, PIM2, POU2AF1, and XBP1. TXNDC5, JCHAIN, and SDC1 were absent (Fig. 4, right). GSE299193 therefore strengthens the spatial reproducibility claim at programme level. It does not directly reproduce the absent genes.

### Single-cell data localised the axis to plasma-cell compartments (Fig. 5)

GSE271107 single-cell RNA-seq data were used to localise the spatial programme across marker-inferred cell categories. After QC, 127,528 cells from 19 samples were included. These spanned HD, MGUS, SMM, and MM stages. Plasma-cell compartments showed the strongest plasma-secretory programme score among broad cell groups (Fig. 5B).

TXNDC5 was consistently expressed in marker-inferred plasma-cell compartments. Across 8,007 marker-inferred plasma cells from 19 sample-level strata, TXNDC5 detection was 96.44% on a cell-weighted basis. The unweighted mean across plasma-cell sample strata was 94.86% (HD 1,463 cells; MGUS 1,016; SMM 649; MM 4,879; Fig. 5A). This supports TXNDC5 as a spatial and single-cell localisation candidate within the plasma-secretory axis. It does not support presenting TXNDC5 as a standalone prognostic biomarker or as a malignant-plasma-cell-specific marker.

### External bulk cohorts supported a clinical subtype module (Fig. 6)

External GEO bulk cohorts were used to test whether the spatially identified axis connected to clinical or cytogenetic annotations outside the spatial datasets. In GSE2658, the POU2AF1/XBP1/JCHAIN module was associated with FISH 1q21 amplification (FDR=1.65e-05). In GSE24080, XBP1 was associated with 24-month overall survival death (FDR=0.0362; Fig. 6).

These findings supported the use of a broader clinical subtype module rather than a TXNDC5-only interpretation. The GSE2658 module effect direction was not identical to the CoMMpass direction. This result is therefore described as external association support rather than uniform directional replication across all platforms. Possible explanations include platform differences, sample composition, FISH cutoff differences, therapy-era effects, expression-platform normalisation, and incomplete equivalence of module-gene coverage across cohorts.

### CoMMpass/GDC linked the axis to OS, ISS, and molecular risk (Fig. 7)

The axis was next evaluated in 762 baseline MMRF-COMMPASS/GDC bone marrow CD138+ RNA-seq samples. The plasma-secretory score was associated with overall survival event. The event-versus-nonevent median difference was 0.346, with FDR=9.31e-06 (Fig. 7A,B). Median-split survival analysis also supported an OS association. The log-rank p was 0.00668, with FDR=0.0401 (Fig. 7C).

The same score showed an ordinal association with ISS stage (Spearman rho=0.132, p=0.000316, FDR=0.0019). These analyses link the axis to retrospective clinical risk features. They do not test R-ISS, PFS, or treatment response.

Public NG2024 CoMMpass molecular annotations further placed the axis in a known molecular-risk context. Local baseline CoMMpass samples matched public Skerget et al. patient-feature annotations for 762 of 762 patients. A total of 707 complete cases were available for RNA-subtype probability analyses. The plasma-secretory score correlated with PR RNA-subtype probability (Spearman rho=0.340, FDR=5.43e-19). It was also higher in samples with 1q21 gain or amplification (median difference 0.268, FDR=1.24e-05; Fig. 7E,F).

Gene-level NG2024 analyses were consistent with the candidate framing. TXNDC5 expression was associated with 1q21 gain or amplification (median difference 0.231, FDR=0.00843). POU2AF1 was associated with 17p13 deletion (median difference 0.337, FDR=0.00533). These observations provide molecular annotation support for the axis. They do not constitute a completed clinical assay.

### Adjusted models constrained the OS interpretation (Fig. 8)

Finally, we tested whether the CoMMpass survival association persisted after adjustment. The prespecified basic Cox model included age, sex, ISS stage, and 1q21 status. In 660 complete cases, the plasma-secretory score was associated with overall survival. The hazard ratio was 1.460 per standard deviation (95% CI 1.069-1.993, p=0.0173, FDR=0.0485; Fig. 8).

The association was sensitive to molecular-context covariates. After adding PR subtype probability, the HR was 1.317 with FDR=0.200. After adding both PR subtype probability and proliferation score, the HR was 1.150 with FDR=0.444. The association remained nominally supported in the model adding del17p and high-risk cytogenetics (HR 1.449, FDR=0.0493). It also persisted in the model adding low-purity probability (HR 1.553, FDR=0.0358). It did not persist in the smaller CMMC tumour-burden proxy model (n=262, FDR=0.269). The sensitivity direction is informative. Adjusting for a public purity proxy strengthened rather than weakened the HR. This argues against the interpretation that the plasma-secretory score is merely a tumour-purity surrogate. Instead, the attenuation by PR probability and proliferation score indicates that the OS association is molecular-context-dependent rather than purity-driven. These results support a PR/proliferation/1q21 molecular-risk context rather than an independent clinical biomarker. A logistic model still linked the plasma-secretory score to 1q21 status after adjustment for age, sex, ISS, PR probability, proliferation, and low-purity probability. The odds ratio was 1.396 per standard deviation, with FDR=0.0467.

## Discussion

This study identifies a plasma-secretory bone marrow programme in multiple myeloma. The programme was discovered in spatial transcriptomics. It showed non-random spatial organisation and local neighbourhood enrichment. It was reproduced in an independent Xenium cohort. It localised to plasma-cell compartments in single-cell data. It was also associated with survival, ISS, RNA subtype, and 1q21 status in bulk cohorts.

The main contribution is cross-platform coherence. Plasma-cell biology alone is not novel in myeloma. The stronger finding is that a spatially enriched and spatially clustered programme connects to PR-like subtype probability, proliferation context, 1q21 status, and retrospective OS association. The OS association persists after basic adjustment for age, sex, ISS, and 1q21. It is attenuated after adding PR subtype probability and proliferation score. This attenuation is informative. It places the programme within known molecular-risk biology rather than establishing an independent clinical biomarker.

### What spatial information adds beyond bulk molecular classification

A central interpretive question is whether the plasma-secretory spatial signal is merely a spatial readout of the PR RNA subtype defined by Skerget et al. (2024). Alternatively, the tissue-level analysis may contribute information beyond bulk classification. The plasma-secretory score correlates with PR subtype probability (Spearman rho=0.340, FDR=5.43e-19). This confirms substantial overlap. The adjusted Cox models show that the OS signal is attenuated after PR and proliferation adjustment. This is consistent with molecular-context dependence.

Two observations support incremental spatial information. First, the spatial organisation analysis shows that the plasma-secretory programme is non-randomly distributed in tissue (median Moran's I 0.477). This spatial autocorrelation is more disease-associated than the autocorrelation of other marrow programmes. Those programmes are spatially structured in both MM and control bone marrow. This tissue-level organisation is not captured by bulk RNA-seq subtype classification. It may reflect local niche effects on plasma-cell transcriptional state. Second, the 1q21 association persists in a logistic model after full adjustment for PR probability, proliferation, and low-purity probability (OR 1.396, FDR=0.0467). This suggests that a component of the axis is not fully subsumed by the PR subtype classification. Together, these observations support a model in which the plasma-secretory transcriptional state is partly captured by bulk RNA subtype. It retains tissue-level spatial organisation and cytogenetic associations that are not fully resolved by subtype alone.

The present public data do not resolve whether spatial clustering reflects plasma-cell-intrinsic transcriptional programmes, microenvironment-driven expression states, or a spatially varying mixture of plasma-cell subclones. This remains an important direction for spatial multi-omics studies with matched genetic and transcriptional readouts.

This interpretation is consistent with recent bone marrow niche, myeloma precursor, and outcome-linked single-cell atlas work. That body of work places myeloma biology in a multicompartment marrow context rather than in tumour-intrinsic expression alone [27-29]. It is also consistent with tumour-marker and prediction-reporting guidance. The present study reports retrospective association and context dependence. It is not a trained clinical prediction model or prospective biomarker assay [12,30].

The analysis also clarifies the role of TXNDC5. TXNDC5 is supported by spatial discovery and single-cell localisation. It should be presented as a localisation candidate. The clinical risk signal is better carried by the broader axis. POU2AF1, XBP1, and JCHAIN are more suitable for clinical-subtype framing.

GSE299193 materially strengthens the spatial component. It reduces dependence on the small GSE269875 discovery cohort. The Xenium panel lacks TXNDC5, JCHAIN, and SDC1. This limits gene-level reproducibility. The result should therefore be described as programme-level spatial reproducibility. The Xenium data also include pre-malignant samples (MGUS and SMM). These were grouped as non-active controls in the primary comparison. Exploratory inspection of individual MGUS and SMM scores showed intermediate values between Ctrl and MM. This is consistent with a continuum rather than a binary transition. This observation is preliminary given the small per-group sample sizes. It warrants dedicated precursor-condition spatial studies.

Several limitations remain. First, this is a retrospective public-data analysis. Second, single-cell labels were marker-inferred rather than harmonised with a full reference atlas. Malignant and normal plasma cells were not separated. Third, external bulk cohorts differ in platform, FISH cutoff, treatment era, endpoint definition, and module-gene coverage. These differences may explain the non-identical direction observed in GSE2658. Fourth, the axis partly reflects plasma-cell abundance and tumour-burden context. The low-purity and CMMC sensitivity models partially address this issue in CoMMpass. They do not replace direct flow cytometry or histology-anchored tumour-content measurement. Fifth, public GDC and NG2024 files did not support complete PFS, R-ISS, or treatment-response validation.

Sixth, this study was conducted and written by a single author. The analysis scripts, figure-generation code, and result tables are available for independent verification. The lack of a second analyst for independent code review and cross-validation of interpretive decisions is a methodological limitation. Multi-analyst studies may identify interpretive nuances or alternative analytical choices that a single analyst could miss.

These limitations define the next extension. Fuller MMRF clinical files could test PFS, R-ISS, treatment response, and therapy-line effects. Independent analytical replication with alternative module definitions and statistical frameworks would strengthen confidence in the core findings. Until then, the current manuscript should make a bounded claim. The data support a spatially reproducible, plasma-cell localised programme linked to molecular-risk context and retrospective clinical association. They do not support a prospective classifier, independent prognostic biomarker, or treatment-selection marker.

## Conclusions

This public-data integrative analysis supports a spatially reproducible plasma-secretory bone marrow programme in multiple myeloma. The programme was spatially enriched and spatially clustered in GSE269875. It was reproduced at programme level in GSE299193 Xenium data. Cross-programme spatial autocorrelation analysis showed that stromal and myeloid programmes also exhibit tissue-level organisation. The plasma-secretory spatial autocorrelation was more disease-associated. Single-cell data localised the axis to plasma-cell compartments. CoMMpass/GDC and NG2024 annotations connected the axis to OS, ISS, PR subtype probability, proliferation context, and 1q21 status. Sensitivity models indicate that the OS association is not independent of PR/proliferation biology. It is not merely a tumour-purity surrogate. TXNDC5 should be framed as a localisation candidate. POU2AF1, XBP1, and JCHAIN are more suitable for subtype-axis framing. The spatial component adds tissue-level information beyond bulk molecular classification. This remains a molecular-context-dependent programme rather than an independent clinical biomarker.

## Declarations

### Ethics approval and consent to participate

Not applicable. This study analysed publicly available, de-identified datasets. It did not involve new recruitment of human participants, new collection of human specimens, or access to directly identifiable private information.

### Consent for publication

Not applicable.

### Availability of data and materials

The datasets supporting the conclusions of this article are available in public repositories. Spatial discovery used GEO accession GSE269875. Xenium spatial reproducibility used GEO accession GSE299193. Single-cell localisation used GEO accession GSE271107. Bulk association used GEO accessions GSE24080 and GSE2658. CoMMpass/GDC RNA-seq and open clinical data were obtained from the NCI Genomic Data Commons MMRF-COMMPASS project. Public CoMMpass molecular annotations were obtained from the supplementary tables of Skerget et al. Nature Genetics 2024. Dataset accessions and primary source links are listed in the References.

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
12. McShane LM, Altman DG, Sauerbrei W, Taube SE, Gion M, Clark GM, et al. Reporting recommendations for tumour marker prognostic studies (REMARK). J Natl Cancer Inst. 2005;97(16):1180-1184. doi:10.1093/jnci/dji237.
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
28. Boiarsky R, Haradhvala NJ, Alberge JB, Sklavenitis-Pistofidis R, Mouhieddine TH, Zavidij O, et al. Single cell characterization of myeloma and its precursor conditions reveals transcriptional signatures of early tumourigenesis. Nat Commun. 2022;13:7040. doi:10.1038/s41467-022-33944-z.
29. Pilcher WC, Yao L, Gonzalez-Kozlova E, Pita-Juarez Y, Karagkouni D, Acharya CR, et al. A single-cell atlas characterizes dysregulation of the bone marrow immune microenvironment associated with outcomes in multiple myeloma. Nat Cancer. 2026;7:224-246. doi:10.1038/s43018-025-01072-4.
30. Collins GS, Moons KGM, Dhiman P, Riley RD, Beam AL, Van Calster B, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. BMJ. 2024;385:e078378. doi:10.1136/bmj-2023-078378.


![Figure 1](D:/二区/analysis/manuscript_figures/fig1_study_design_evidence_chain.png)

Figure 1. Cross-cohort study design and evidence chain. The workflow starts from spatial discovery in GSE269875, adds second spatial reproducibility in GSE299193 Xenium, proceeds through single-cell localisation in GSE271107, external GEO bulk association in GSE24080/GSE2658, and retrospective clinical association plus molecular annotation in MMRF-COMMPASS/GDC and public NG2024 CoMMpass annotations.


![Figure 2](D:/二区/analysis/manuscript_figures/fig2_spatial_plasma_secretory_discovery.png)

Figure 2. Spatial discovery of the plasma-secretory programme. Sample-level MM versus control differences are shown for the plasma-secretory score, followed by effect-size ranking across spatial programmes and selected axis-associated candidate genes.


![Figure 3](D:/二区/analysis/manuscript_figures/fig3_spatial_organization.png)

Figure 3. Spatial organisation of the plasma-secretory programme in GSE269875. Moran's I was calculated within each sample using 6-nearest-neighbour graph weights and 199 within-sample label permutations. Plasma-secretory Moran's I was FDR-significant in all 9 samples and was higher in MM than control samples in this small cohort (median 0.571 versus 0.144; Mann-Whitney p=0.0238), although control marrow also showed non-zero autocorrelation. Neighbour enrichment compares nearest-neighbour niche-programme scores around plasma-secretory-high spots with those around other spots. Focal spots are excluded and plasma-cell marker scores are omitted from this primary neighbour analysis to reduce circularity.


![Figure 4](D:/二区/analysis/manuscript_figures/fig4_gse299193_xenium_spatial_reproducibility.png)

Figure 4. Independent GSE299193 Xenium spatial reproducibility. Sample-level Xenium matrices show higher plasma-secretory and POU2AF1/XBP1 module scores in active MM/RM samples compared with Ctrl/MGUS/SM samples. The heatmap displays axis genes covered by the Xenium panel. TXNDC5, JCHAIN and SDC1 are absent from this Xenium panel and are therefore not claimed as directly reproduced in this cohort.


![Figure 5](D:/二区/analysis/manuscript_figures/fig5_scrna_plasma_secretory_localization.png)

Figure 5. Single-cell localisation of the plasma-secretory axis. Dot size indicates detection fraction and colour indicates mean log-normalised expression across marker-inferred cell types. The plasma-cell compartment shows the strongest plasma-secretory programme localisation. TXNDC5 detection is reported across 8,007 marker-inferred plasma cells from 19 sample-level strata: 96.44% cell-weighted detection and 94.86% unweighted mean detection across strata. TXNDC5 is retained as a localisation candidate rather than a standalone prognostic biomarker.


![Figure 6](D:/二区/analysis/manuscript_figures/fig6_external_bulk_clinical_support.png)

Figure 6. External GEO bulk support for the clinical subtype axis. Ranked association statistics summarise subtype and risk links in GSE24080 and GSE2658. Boxplots show representative associations with 1q21 amplification and 24-month OS milestone status.


![Figure 7](D:/二区/analysis/manuscript_figures/fig7_commppass_ng2024_association.png)

Figure 7. CoMMpass/GDC retrospective clinical association and public NG2024 molecular annotation. The plasma-secretory score and related subtype module show association with OS event, ISS stage, median-split overall survival, public NG2024 RNA subtype probability, and 1q21 copy-number annotation. Basic adjusted Cox/logistic models summarise associations after age, sex, ISS and 1q21 adjustment where applicable.


![Figure 8](D:/二区/analysis/manuscript_figures/fig8_commppass_sensitivity_models.png)

Figure 8. CoMMpass OS sensitivity models. Hazard ratios are reported per 1-SD plasma-secretory score increase. Models sequentially add PR subtype probability, proliferation, high-risk cytogenetic features, low-purity probability, or CMMC tumour-burden proxy to the base age, sex, ISS, and 1q21 model. Attenuation after PR/proliferation adjustment supports molecular-context dependence rather than independent clinical biomarker evidence.
