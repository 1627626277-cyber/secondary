# Stage 2 Citation Verification Notes

Date: 2026-04-30

Purpose:

- Record which manuscript source claims have been checked against primary or high-quality sources.
- Flag items that still need final reference formatting before submission.
- Avoid using textbooks, blogs, encyclopedia pages or low-quality papers as scientific references.

## Verified Sources

### Skerget et al. Nature Genetics 2024

Source:

- Nature Genetics article: https://www.nature.com/articles/s41588-024-01853-0

Verified details:

- Title: "Comprehensive molecular profiling of multiple myeloma identifies refined copy number and expression subtypes".
- Published: 19 August 2024.
- Journal: Nature Genetics.
- Volume/pages: 56, 1878-1889.
- DOI: 10.1038/s41588-024-01853-0.
- CoMMpass cohort described as a longitudinal observational study of newly diagnosed MM patients.
- The paper reports whole-genome, whole-exome and RNA sequencing at diagnosis and progression.
- The paper reports 8 copy-number and 12 expression subtypes.

Use in manuscript:

- Public NG2024 CoMMpass molecular annotation.
- RNA subtype and copy-number annotation context.

### GSE269875

Source:

- GEO accession page: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269875

Verified details:

- Status: public on 2025-06-09.
- Title: "Spatial transcriptomics unveils novel potential disease mechanisms associated with the microenvironment in Multiple Myeloma".
- Organisms: Homo sapiens and Mus musculus.
- Overall design includes healthy and MM bone marrow samples.
- Human bone marrow biopsies from healthy individuals and MM patients are included.

Use in manuscript:

- Spatial discovery cohort.

### GSE271107

Source:

- GEO accession page: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE271107

Verified details:

- Status: public on 2024-07-04.
- Title: "Single-cell RNA sequencing of bone marrow aspirate samples from multiple myeloma and its precursor conditions".
- Organism: Homo sapiens.
- GEO summary reports 4 newly diagnosed MM, 6 MGUS, 4 SMM and 5 healthy donor samples.

Use in manuscript:

- Single-cell localization validation.

### GSE24080

Source:

- GEO accession page: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE24080

Verified details:

- Status: public on 2010-09-11.
- Title: "MAQC-II Project: Multiple myeloma (MM) data set".
- Platform: Affymetrix Human Genome U133 Plus 2.0 Array.
- Samples: 559.
- Summary states CD138-enriched plasma-cell expression profiling in newly diagnosed MM.
- Summary states two-year OS and EFS milestone endpoints.

Use in manuscript:

- External bulk validation with 24-month OS death.

### GSE2658

Source:

- GEO accession page: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE2658

Verified details:

- Status: public on 2006-06-01.
- Title: "Gene Expression Profiles of Multiple Myeloma".
- Samples are pretreatment bone marrow aspirates from MM patients.
- Design includes CD138-selected plasma cells from newly diagnosed MM.
- Platform: Affymetrix Human Genome U133 Plus 2.0 Array.
- Samples: 559.

Use in manuscript:

- External bulk validation with cytogenetic and 1q21-associated analyses.

### GSE299193 and related Blood 2025 spatial paper

Sources:

- Local GEO SOFT metadata and downloaded raw tar were used for GSE299193.
- Related Blood article: https://www.sciencedirect.com/science/article/pii/S0006497125016702

Verified details from the Blood article:

- Title: "Profiling the spatial architecture of multiple myeloma in human bone marrow trephine biopsy specimens with spatial transcriptomics".
- Journal: Blood.
- Volume/pages: 146, 1837-1849.
- DOI: 10.1182/blood.2025028896.
- The paper reports subcellular spatial transcriptomics of 5001 genes.
- It includes healthy, premalignant and active myeloma samples.

Important caution:

- The Blood article data availability line mentions GSE299207.
- The local analysis used GSE299193 raw files downloaded from GEO.
- Final manuscript should cite the relevant publication and the exact GEO accession separately.

### NCI GDC / MMRF-COMMPASS

Source:

- NCI GDC MMRF page: https://gdc.cancer.gov/about-gdc/contributed-genomic-data-cancer-research/foundation-medicine/multiple-myeloma-research-foundation-mmrf

Verified details:

- CoMMpass is described as a longitudinal observational study.
- The study enrolled around 1000 newly diagnosed myeloma patients.
- GDC provides MMRF genomic data, including RNA sequencing.
- Protected data require dbGaP access through phs000748.

Use in manuscript:

- CoMMpass/GDC RNA-seq and open clinical slice.
- Claim boundary for missing fuller clinical endpoints.

## Items Requiring Final Formatting

- Convert all reference anchors to the target journal style.
- Confirm whether the target journal prefers Vancouver numbering or author-year.
- Confirm final citation for GSE299193 versus GSE299207.
- Add GEO database citation if the journal requires database citation.
- Add GDC data portal citation or access date.
- Add software/package citations once Methods are expanded.

