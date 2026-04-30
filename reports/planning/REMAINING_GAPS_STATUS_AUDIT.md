# Remaining Gaps Status Audit

Date: 2026-04-29

## Current Main-Line Status

The current manuscript main line is complete enough for drafting:

- spatial discovery: completed using GSE269875;
- single-cell localization validation: completed using GSE271107;
- external bulk validation: completed using GSE24080 and GSE2658;
- CoMMpass/GDC clinical validation: completed for OS and ISS;
- manuscript-grade Fig. 1-5 and Results skeleton: completed.

Public enhancement now added to the route:

- Skerget et al. Nature Genetics 2024 public CoMMpass supplementary tables have been downloaded and audited as a molecular-risk annotation layer.
- Table 1 patient features match 762/762 local CoMMpass/GDC samples.
- Table 7 RNA subtype predictions match 707 local CoMMpass/GDC samples.
- This is no longer a pure MMRF-approval dependency because the public tables can directly join to the current score table.

## Fuller MMRF/CoMMpass Clinical Tables

Status:

- Not obtained locally.
- `external_bulk/CoMMpass_full_clinical` currently contains no fuller clinical files.
- `scripts/16_commppass_full_clinical_validation.py` has been created and run, but it can only scan files after the user downloads authorized clinical tables into that folder.

What is still missing:

- R-ISS components;
- PFS event/time fields;
- treatment line/regimen;
- treatment response / best overall response.

Partially addressable without fuller MMRF approval:

- detailed cytogenetic / copy-number / molecular-risk annotations may be recoverable from the Skerget et al. Nature Genetics 2024 public supplement.
- These have now passed local download, sheet inventory and ID matching for Table 1 and Table 7.

What has been found:

- MMRF Virtual Lab documentation confirms that richer CoMMpass clinical data exist.
- CoMMpass Clinical Data Overview states that the harmonized clinical dataset includes Cytogenetics/FISH, treatment details, response/relapse documentation, dates of progression/relapse/treatment change, PFS, OS, and time-to-event variables.
- Interim Analysis documentation states that IA24 is the final comprehensive release and provides Clinical Data Tables and Summary Data Files through the Virtual Lab repository.

Conclusion:

- This expansion is feasible but not completed.
- The blocking item for PFS/treatment-response remains authorized file acquisition, not analysis-code readiness.
- The molecular-risk annotation subproblem is now partly solved through public CoMMpass supplementary files.

## Public CoMMpass Molecular-Annotation Supplement

Status:

- Downloaded and parsed locally.
- First-pass molecular annotation validation completed.

Primary source:

- Skerget et al., Nature Genetics 2024, "Comprehensive molecular profiling of multiple myeloma identifies refined copy number and expression subtypes."
- The article reports a 1,143-patient CoMMpass baseline cohort and points to freely available Supplementary Tables 1-7.

Expected useful content:

- individual patient features;
- ISS and baseline laboratory fields;
- copy-number calls including 1q21, 17p13 and 13q14;
- cytogenetic high-risk labels;
- RNA subtype labels;
- mutation and structural-event records in larger supplementary tables;
- expression subtype classifier output.

Current claim boundary:

- Can support molecular-risk and subtype annotation because IDs and fields match for the current CoMMpass/GDC score table.
- Cannot be used to claim PFS or treatment-response validation unless those endpoint columns are verified after local parsing.

## Extra MM Bone Marrow Spatial Transcriptomics Validation

Status:

- A second public human MM bone marrow spatial dataset has now been identified.
- It has not yet been downloaded or analyzed locally.

Candidate dataset:

- GEO accession: `GSE299193`.
- Title: `Profiling the spatial architecture of multiple myeloma in human bone marrow trephines with spatial transcriptomics [human]`.
- Platform: Xenium In Situ Analyzer, Homo sapiens.
- Samples: 22 human trephine samples.
- Disease groups visible in GEO: control, MGUS, multiple myeloma, smouldering myeloma, relapse myeloma.
- GEO summary: subcellular spatial transcriptomics of 5,001 genes in human bone marrow in MGUS, smouldering myeloma, and multiple myeloma; 21 individuals including 7 premalignant disease and 10 active MM.
- Supplementary RAW package: `GSE299193_RAW.tar`, 76.6 GB.

Related SuperSeries:

- `GSE299207`: human + mouse SuperSeries.
- RAW package: 80.4 GB.
- Human SubSeries `GSE299193` is the better immediate target to avoid unnecessary mouse data.

Current disk status:

- D drive free space checked on 2026-04-29: about 347 GB.
- Downloading the 76.6 GB human RAW tar is feasible, but extraction and intermediate processing may require roughly 150-230 GB depending on how much Xenium output is retained.

Conclusion:

- The extra spatial-transcriptomics validation gap is no longer a discovery problem; a suitable dataset has been found.
- It is not yet a completed project result because it has not been downloaded, parsed, QC-checked, or integrated into Fig. 1-5.
- If analyzed successfully, it could become a new Fig. 6 or a supplemental validation figure.

## Original Expansion Plan Completion Matrix

| Planned component | Status | Current evidence/result | Remaining action |
|---|---|---|---|
| External bulk validation | Completed | GSE24080/GSE2658 + CoMMpass/GDC | Optional refinement only |
| External scRNA validation | Completed | GSE271107 | Optional second scRNA dataset only |
| Clinical prognosis/stage association | Partly completed | OS and ISS completed in CoMMpass/GDC | R-ISS/PFS/treatment response require fuller MMRF files |
| Public CoMMpass molecular-risk annotation | Completed first pass | Skerget et al. NG2024 Table 1 matched 762/762; Table 7 matched 707; molecular annotation associations generated | Integrate into Fig. 5 or supplement; optionally parse mutation/SV deeper |
| Extra spatial transcriptomics validation | Found but not completed | GSE299193 identified | Download, parse Xenium outputs, compute axis scores, integrate figure |
| Manuscript-grade figure consolidation | Completed first pass | Fig. 1-5, evidence table, legends | Add Fig. 6 if GSE299193 validates |
| Main manuscript draft | Completed first pass | Main text draft written | Add citations and revise after any new analyses |

## Recommended Next Step

Priority 1:

- Integrate Skerget et al. Nature Genetics 2024 public CoMMpass molecular-annotation validation into the manuscript package.
- Use it as a public substitute for the missing cytogenetic/molecular-risk layer, but not for PFS/treatment response.

Priority 2:

- Download and inspect `GSE299193` human Xenium data.
- Do not download the full `GSE299207` SuperSeries unless mouse data are explicitly needed.

Priority 3:

- Continue trying to obtain fuller MMRF/CoMMpass clinical tables from Virtual Lab / Researcher Gateway.
- Once files are available, rerun:
  - `python scripts/16_commppass_full_clinical_validation.py`

Priority 4:

- Keep the current manuscript draft moving using OS/ISS as completed clinical validation.
- Do not delay the paper solely for fuller clinical tables.

## Source Links

- GSE299193 GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299193
- GSE299207 GEO SuperSeries: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299207
- PubMed paper for GSE299193/GSE299207: https://pubmed.ncbi.nlm.nih.gov/40643106/
- Skerget et al. Nature Genetics 2024: https://www.nature.com/articles/s41588-024-01853-0
- PMC full text for Skerget et al.: https://pmc.ncbi.nlm.nih.gov/articles/PMC11387199/
- MMRF CoMMpass Clinical Data Overview: https://themmrf.github.io/docs-vlab/mmrf-resources/mmrf-commpass/clinical-overview/
- MMRF CoMMpass Interim Analysis access: https://themmrf.github.io/docs-vlab/mmrf-resources/mmrf-commpass/historic-ia/
