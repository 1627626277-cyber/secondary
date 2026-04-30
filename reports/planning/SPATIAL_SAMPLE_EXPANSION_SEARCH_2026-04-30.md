# Spatial Sample Expansion Search

Date: 2026-04-30

## Purpose

Address the reviewer concern that the current discovery spatial cohort is small.

Current spatial discovery:

- GSE269875: human Visium MM bone marrow, currently used as the discovery cohort.
- Discovery-level limitation: 3 control and 6 MM samples in the local mainline analysis.

The goal is to identify public or plausibly accessible spatial datasets that can add independent spatial validation or broaden the spatial evidence chain.

## Current Download Action

GSE299193 download has been resumed.

Current role:

- Primary second spatial validation cohort.
- Human bone marrow trephine Xenium.
- Public GEO dataset.
- Disease spectrum: Ctrl, MGUS, smouldering myeloma, MM and relapsed MM.
- Expected RAW tar: 76.61 GiB.
- Current local partial file is resumable.

Priority:

- Highest.

Reason:

- It is human, public, MM-specific, bone-marrow-specific, spatial transcriptomics, and has more disease-state breadth than GSE269875.

## Candidate Dataset Ranking

### Candidate 1: GSE299193

Status:

- Selected and downloading.

Source:

- GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299193
- PubMed / Blood article record: https://pubmed.ncbi.nlm.nih.gov/40643106/

Evidence from public source:

- Human bone marrow trephine spatial transcriptomics using Xenium.
- 22 human samples in GEO metadata.
- Reported as profiling the spatial architecture of multiple myeloma in human bone marrow trephine biopsy specimens.

Use in manuscript:

- Main second-spatial-cohort validation.
- Planned Fig. 6 if validation works.
- Directly addresses the small GSE269875 spatial discovery sample concern.

Risks:

- Large download and extraction burden.
- Targeted Xenium panel rather than whole transcriptome.
- Some genes in the plasma-secretory score may be absent from the panel; validation may need a reduced score using available genes.

### Candidate 2: GSE284727

Status:

- Public GEO dataset identified.
- Not yet downloaded.

Source:

- GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE284727
- Associated paper: Lutz et al., Science Immunology 2025, "Bone marrow breakout lesions act as key sites for tumor-immune cell diversification in multiple myeloma."

Public source details:

- GEO status public on 2025-02-10.
- Organism: Homo sapiens.
- GEO summary states single-cell and spatial multi-omics analysis of bone marrow-confined intramedullary disease and paired breakout lesions.
- Overall GEO design states bone marrow samples from 5 myeloma patients with breakout lesions were analyzed using 10x Genomics CITE-seq and VDJ-T sequencing.
- GEO public supplementary file: `GSE284727_RAW.tar`, approximately 4.0 GB, plus preprocessed Seurat objects.
- Personally identifiable raw human sequence files are controlled through EGA.

Use in manuscript:

- Secondary candidate.
- May support spatial/microenvironmental interpretation of breakout lesions if public processed spatial objects or spatial annotations are included.
- More reliable as scRNA/CITE-seq or lesion microenvironment context unless direct spatial expression matrices are confirmed after download.

Risks:

- GEO visible design emphasizes CITE-seq and VDJ rather than a clear public spatial expression matrix.
- Controlled EGA may hold the more sensitive/raw components.
- It is not a clean replacement for GSE299193.

Recommendation:

- Inspect after GSE299193 or if GSE299193 download/analysis fails.
- Do not make it a main spatial validation dependency until public file contents are verified.

### Candidate 3: Leukemia 2025 Daratumumab Resistance GeoMx/DSP Dataset

Status:

- Literature candidate identified.
- Not yet acquired.

Source:

- Wang et al., Leukemia 2025, "The bone marrow immune ecosystem shapes daratumumab acquired resistance in plasma cell myeloma."
- Article: https://www.nature.com/articles/s41375-025-02712-5
- Raw sequence data accession listed by the article: HRA007175 at GSA-Human.

Public source details:

- The study used paired pre-therapy and acquired-resistance bone marrow samples.
- Spatial immune ecosystem profiling used GeoMx Digital Spatial Profiler.
- GeoMx RNA and protein assays were performed on 6 paired FFPE sections from 3 subjects, with 34 areas of interest.

Use in manuscript:

- Optional treatment-resistance / spatial immune ecosystem context.
- Could be useful if accessible processed GeoMx RNA matrices are available.
- Not a primary solution to spatial discovery sample size because the patient count is small and treatment-specific.

Risks:

- HRA/GSA-Human access may require controlled access.
- GeoMx AOI-level data are not directly comparable with Visium/Xenium.
- Treatment-resistance context is biologically different from baseline MM discovery.

Recommendation:

- Keep as optional future line.
- Do not prioritize before GSE299193 and adjusted CoMMpass/NG2024 modeling.

### Candidate 4: ASH 2023 CODEX BM Trephine Cohort

Status:

- Abstract-level candidate.
- No confirmed public data found in this search.

Source:

- ASH 2023 abstract: "Spatial Dissection of the Bone Marrow Microenvironment in Multiple Myeloma By High Dimensional Multiplex Tissue Imaging."
- Abstract reports 489 bone marrow trephine biopsies and 3.1 million single cells measured by CODEX.

Use in manuscript:

- Useful as background evidence that large-scale spatial protein imaging exists in MM.
- Not usable as transcriptomic validation unless data become public or the full paper provides processed tables.

Risks:

- Protein imaging, not transcriptomics.
- No confirmed public downloadable dataset.
- Abstract-only evidence is not suitable as a primary analysis source.

Recommendation:

- Cite only if relevant after locating a full peer-reviewed article.
- Do not include in current analysis plan.

## Decision

For the current Q2 route, only GSE299193 should be treated as the direct spatial-transcriptomics sample expansion dataset.

GSE284727 is a useful backup to inspect, but it should not be described as a confirmed spatial-transcriptomics validation dataset until its public files are downloaded and inventoried.

The Leukemia GeoMx/DSP dataset and ASH CODEX cohort are useful for context and possible future work, but not immediate replacements for the GSE299193 validation line.

## Updated Action Plan

Priority 1:

- Continue GSE299193 resumable download.
- After completion, run:
  - `python scripts/17_gse299193_download_status.py`
  - `python scripts/18_gse299193_xenium_validation.py`

Priority 2:

- If GSE299193 validates the axis, add Fig. 6 and update manuscript text.

Priority 3:

- If GSE299193 fails because key genes are absent from the Xenium panel, use a reduced available-gene score and clearly state panel limitations.

Priority 4:

- If GSE299193 cannot be completed or is negative, inspect GSE284727 public files for usable processed spatial/microenvironment components.

## Note On Reviewer Hard Issue Numbering

The previous peer review listed "clinical adjustment / independent prognosis" as major issue 2 and "small spatial discovery cohort" as major issue 3.

This search primarily addresses the small spatial cohort issue. The clinical adjustment issue still requires a separate CoMMpass/NG2024 Cox or adjusted logistic-model analysis.
