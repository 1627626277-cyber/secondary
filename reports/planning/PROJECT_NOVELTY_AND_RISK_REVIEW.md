# Project Novelty and Risk Review

Date: 2026-04-29

Scope: pause downstream computation, check whether the planned project has already been done, and review current project risks based on local logs.

## 1. Search conclusion

### 1.1 The main discovery dataset has already been published

The exact core spatial dataset `GSE269875` is already associated with a peer-reviewed paper:

- Title: Characterization of the bone marrow architecture of multiple myeloma using spatial transcriptomics
- Journal: Communications Biology
- Published: 2025-11-20
- Dataset: `GSE269875`
- Article: https://www.nature.com/articles/s42003-025-08975-z
- GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269875

The paper already analyzed mouse and human FFPE bone marrow Visium spatial transcriptomics in multiple myeloma. Its reported biological themes include malignant plasma-cell-enriched spatial areas, remote/border/hotspot zones, T-cell exhaustion gradients, NETosis, IL-17 signaling, and microenvironmental remodeling.

Implication: our project cannot be framed as the first spatial transcriptomic atlas of multiple myeloma bone marrow, and a GSE269875-only reanalysis has high novelty risk.

### 1.2 Similar MM spatial transcriptomics studies also exist

Other closely related work has already appeared:

- Blood 2025: Profiling the spatial architecture of multiple myeloma in human bone marrow trephine biopsy specimens with spatial transcriptomics. This used Xenium-based spatial profiling of human bone marrow trephines. PubMed: https://pubmed.ncbi.nlm.nih.gov/40643106/
- Blood 2024: Spatial transcriptomics reveals profound subclonal heterogeneity and T-cell dysfunction in extramedullary myeloma. PubMed: https://pubmed.ncbi.nlm.nih.gov/39172759/
- GSE299193 is linked to the Xenium bone marrow trephine MM study and may be useful as an optional external spatial validation resource. Search result: https://www.omicsdi.org/dataset/geo/GSE299193

Implication: the field already contains MM spatial microenvironment papers. A publishable project must avoid generic claims such as "spatial landscape of MM" and instead make a sharper, externally validated, clinically connected claim.

### 1.3 Exact planned integration was not found in quick search

In the quick search, I did not find a clearly identical published project that combines:

- independent QC and reanalysis of GSE269875,
- sample-aware spatial niche or signature discovery,
- validation in public MM scRNA-seq datasets,
- validation in bulk/clinical MM cohorts such as CoMMpass, GSE24080, or GSE2658,
- optional comparison to an independent MM spatial dataset such as GSE299193.

This does not prove complete novelty, but it suggests the revised integrated validation route is still defensible.

## 2. Current local project status

The project has completed the data-governance and initial spatial-analysis foundation:

- All 9 human GSE269875 samples passed sampled species QC.
- The GEO processed spatial matrices were downloaded and inventoried.
- All 9 human matrices contain expression matrix, barcode, feature, spatial-position, image, and scale-factor files.
- Matrix QC found usable but uneven spatial data.
- Preliminary clustering produced biologically plausible MM-enriched and control-enriched spot clusters.
- Early exploratory MM-vs-control signals include `JCHAIN`, `TXNDC5`, `IGHG1`, `B2M`, `IGHA1`, `CD74`, `VIM`, `IGKC`, `XBP1`, `PIM2`, `COL1A1`, `MZB1`, and `POU2AF1`.

Current local reports:

- `D:\二区\SPATIAL_MATRIX_QC_REPORT.md`
- `D:\二区\PRELIMINARY_SPATIAL_CLUSTERING_REPORT.md`
- `D:\二区\EXTERNAL_VALIDATION_ROADMAP.md`
- `D:\二区\gse269875_human_species_qc_summary.tsv`
- `D:\二区\gse269875_processed_matrix_inventory.tsv`

## 3. Main risks and whether they can be solved

| Risk | Evidence from current project | Severity | Can it be solved? | Must solve now? |
|---|---|---:|---|---|
| Novelty overlap with GSE269875 original paper | Same dataset already published in Communications Biology with MM bone marrow ST analysis | High | Yes, by changing the project from atlas/reanalysis to externally validated spatial-signature study | Yes |
| Generic spatial MM topic is crowded | Blood 2024/2025 and related work already study MM spatial microenvironment | High | Yes, by narrowing to a new computational/clinical angle | Yes |
| Spot-level pseudoreplication | Current clustering and markers are spot-level exploratory results; spots are not independent patient samples | High | Yes, by using sample-aware pseudobulk, per-sample region summaries, and sensitivity analyses | Yes |
| Sample-depth heterogeneity | QC shows hMM2/hMM3 are strongest, while hMM1/hMM4/hMM5/hMM6 have lower depth or fewer spots | High | Yes, by depth-aware normalization, per-sample QC strata, and robustness checks | Yes |
| Some clusters are sample-associated | Current cluster notes show hMM2-, hMM3-, and hMM5-associated clusters | High | Yes, by separating biological niche signals from patient/sample-specific effects | Yes |
| Candidate genes are common plasma-cell/MM markers | `JCHAIN`, `XBP1`, `MZB1`, `IGH*`, `TNFRSF17` are expected MM/plasma-cell biology | Medium-high | Partly; they are useful for validation but not enough as novel findings | Yes, during candidate triage |
| External validation not yet executed | Roadmap exists, but scRNA/bulk/clinical validation is not yet done | High | Yes, by adding GSE223060/GSE271107 and bulk/clinical cohorts | Later, after candidate/signature shortlist |
| Clinical relevance not yet demonstrated | No survival, stage, treatment response, or risk association has been computed yet | High | Yes, if public MM clinical cohorts have usable metadata | Later, but mandatory before manuscript submission |
| External spatial validation not yet included | GSE299193/Xenium is possible but platform compatibility may be difficult | Medium | Possibly; use as optional validation, not as core dependency | Later |
| Full FASTQ expansion not done | Species QC used sampled reads; processed matrices came from GEO | Low for current plan | Yes if needed, but not necessary for current processed-matrix analysis | No |

## 4. What must be fixed before further downstream claims

The next analysis should not be another round of broad exploratory plots. It should solve the current high-risk methodological issues:

1. Reframe the research question.
   - Avoid: "first spatial transcriptomic atlas of MM bone marrow."
   - Use: "spatially derived MM bone marrow niche signatures with independent single-cell and clinical transcriptomic validation."

2. Replace spot-level claims with sample-aware claims.
   - Aggregate expression by sample, group, and spatial region or cluster.
   - Use sample-level effect sizes instead of treating all spots as independent observations.
   - Report sensitivity excluding low-depth or low-spot samples.

3. Triage candidate genes/signatures.
   - Separate canonical plasma-cell markers from potentially useful niche, immune, stromal, stress-response, and prognostic signals.
   - Do not overclaim common markers as novel discoveries.

4. Build an external-validation-ready candidate table.
   - Each candidate should have spatial evidence, sample-level consistency, cell-type plausibility, and a validation route.

## 5. What can wait until later

These parts are important for publication strength but do not need to be solved before the next local analysis step:

- scRNA-seq validation using public MM single-cell datasets.
- bulk/clinical validation using CoMMpass or GEO bulk cohorts.
- survival/stage/treatment-response association.
- independent spatial validation with GSE299193 or another spatial cohort.
- full FASTQ expansion of all runs.

## 6. Recommendation

The project can continue, but only under the revised strategy.

The current plan is not strong enough if it remains a GSE269875-only spatial reanalysis. It becomes potentially publishable for an SCI Q2 bioinformatics/translational medicine/tumor data-analysis journal if we convert it into an externally validated computational study:

- discovery: GSE269875 human spatial transcriptomics,
- rigor: sample-aware spatial niche/signature analysis,
- biological validation: public MM scRNA-seq,
- clinical relevance: public bulk/clinical MM cohorts,
- optional strengthening: independent Xenium/spatial comparison.

Immediate next technical step: create a sample-aware spatial signature and candidate-ranking table from GSE269875, then use that table to drive external scRNA and clinical validation.
