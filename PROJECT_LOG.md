# Project Log

## 2026-04-28

### Project Target

Target manuscript type: SCI Q2-leaning bioinformatics / translational medicine / tumor data-analysis paper.

Manuscript positioning:

- Public database integration.
- Spatial transcriptomics re-analysis.
- Robustness and consistency evidence.
- Hypothesis generation.

Claims must not be framed as wet-lab validation, paired-cohort validation, or mechanism closure.

### Current Stage

Stage: data governance and pilot preparation.

Completed:

- Read and reviewed the revised research report.
- Read the prior project chat.
- Confirmed that Stage 3 m6A integration and Nanopore-related content should remain deleted.
- Parsed local `GSE269875_family.soft.gz`.
- Confirmed GSE269875 has 15 samples:
  - 9 human mainline samples.
  - 6 mouse samples to isolate/exclude from mainline.
- Generated an enriched manifest:
  - `gse269875_manifest_enriched.tsv`
- Confirmed the correct first disease pilot:
  - `GSM8329293`
  - `hMM1`
  - `SRX24927515`
- Corrected a previous sample-selection error:
  - `GSM8329291` is `hHBM2`, not `hMM1`.
- Checked disk space:
  - D drive free space: about 410.75 GiB.
  - One-sample pilot is feasible.

### Files Created

- `gse269875_manifest_enriched.tsv`
- `NEXT_STEP_PILOT_RUNBOOK.md`
- `ENVIRONMENT_SETUP_NOTES.md`
- `scripts/01_enrich_gse269875_manifest.py`
- `scripts/02_check_pilot_readiness.ps1`
- `scripts/03_pilot_hMM1_species_qc_template.ps1`

### Current Blocker

Resolved for Windows-native route:

- SRA Toolkit 3.4.1 installed in the Codex workspace.
- Magic-BLAST 1.7.2 installed in the Codex workspace.
- `makeblastdb` 2.14.0+ installed with Magic-BLAST.

The original `minimap2 + samtools` route was replaced because `minimap2` is unavailable for Bioconda `win-64`.

Installed tool paths:

- `C:\Users\jz\Documents\Codex\2026-04-28\files-mentioned-by-the-user-deep\tools\sratoolkit_extract\sratoolkit.3.4.1-win64\bin`
- `C:\Users\jz\Documents\Codex\2026-04-28\files-mentioned-by-the-user-deep\tools\ncbi-magicblast-1.7.2\bin`

Helper script:

- `scripts/set_windows_toolchain_path.bat`
- `scripts/copy_toolchain_to_D_project.bat`
- `scripts/set_D_project_toolchain_path.bat`

Remaining blocker:

- The assistant currently does not have write permission to `D:\二区`, so the tools were installed in the Codex workspace rather than the project directory.
- Reference genomes `hg38.fa` and `mm10.fa` are still needed before Magic-BLAST databases can be built.
- C drive has only about 65.55 GiB free, so raw SRA/FASTQ pilot must not be run on C drive.
- D drive has about 410.75 GiB free and should be used for `sra_cache`, `fastq`, and `tmp_fasterq`.

### Next Action

User decision: use native Windows instead of WSL.

Toolchain route changed:

- Keep `ich_bioinfo` for Python/GEO metadata.
- Use official Windows SRA Toolkit for SRA download and FASTQ conversion.
- Use NCBI Magic-BLAST on Windows for sequence-level human/mouse QC, replacing the first-pass `minimap2 + samtools` plan.

Reason:

- `minimap2` is not available from Bioconda on `win-64`.
- `samtools` is also not available from Bioconda on `win-64`.
- NCBI provides Windows binaries for SRA Toolkit and Magic-BLAST.

Set the Windows-native toolchain PATH, then rerun:

```powershell
.\scripts\set_windows_toolchain_path.bat
```

Proceed to hMM1 pilot only after `hg38.fa` and `mm10.fa` are prepared and Magic-BLAST databases are built.

### 2026-04-28 hMM1 Pilot QC Update

Completed:

- Downloaded reference genomes from UCSC:
  - `D:\二区\references\hg38.fa.gz`
  - `D:\二区\references\mm10.fa.gz`
- Decompressed references:
  - `D:\二区\hg38.fa`
  - `D:\二区\mm10.fa`
- Built Magic-BLAST BLAST v4 databases:
  - `D:\二区\blastdb\hg38.*`
  - `D:\二区\blastdb\mm10.*`
- Resolved hMM1 SRA run:
  - `GSM8329293 / hMM1 / SRX24927515 -> SRR29414112`
- Downloaded `SRR29414112` with SRA Toolkit.
- Exported first 1,000,000 spots with `fastq-dump --split-files -X 1000000`.
- Identified transcript read as `SRR29414112_4.fastq` (50 bp).
- Ran Magic-BLAST against hg38 and mm10.
- Wrote QC summary:
  - `D:\二区\qc_species_hMM1\hMM1_species_qc_summary.md`
- Updated `gse269875_manifest_enriched.tsv`:
  - `GSM8329293` marked as `pass_human_sampled_magicblast`.

Pilot result:

- Human hit rate: 37.07%.
- Mouse hit rate: 6.99%.
- Human-only reads: 301,832 (30.18%).
- Mouse-only reads: 970 (0.10%).
- Human-only / mouse-only ratio: 311.17.

Decision:

- `GSM8329293 / hMM1 / SRR29414112` passes sampled sequence-level human species QC.

Next action:

- Repeat sampled QC for one healthy control sample, preferably `GSM8329290 / hHBM1 / SRX24927512`, then scale to the remaining human mainline samples.

### 2026-04-28 08:18:40 Log Sync Update

Completed:

- Confirmed that previous project logs and reports have been copied into D:\二区.
- Confirmed D:\二区\PROJECT_LOG.md is newer than the earlier Codex workspace copy and should be treated as the authoritative project log.
- Confirmed D:\二区\UPDATED_COMPLETE_PROJECT_REPORT.md contains the hMM1 pilot update and should be treated as the current complete project report.
- Kept the newer D-drive versions; no overwrite from older C-drive workspace files was performed.

Current authoritative files:

- D:\二区\PROJECT_LOG.md
- D:\二区\UPDATED_COMPLETE_PROJECT_REPORT.md
- D:\二区\ENVIRONMENT_SETUP_NOTES.md
- D:\二区\NEXT_STEP_PILOT_RUNBOOK.md
- D:\二区\qc_species_hMM1\hMM1_species_qc_summary.md

Current project status:

- Windows-native toolchain is installed under D:\二区\tools.
- hg38/mm10 reference FASTA files are prepared.
- hg38/mm10 BLAST databases are built.
- hMM1 pilot sampled Magic-BLAST species QC is complete and passed human-mainline QC.
- Next planned sample: GSM8329290 / hHBM1 / SRX24927512 for healthy-control sampled species QC.

### 2026-04-28 20:09:37 hHBM1 Download Status

Target control sample:

- GSM8329290 / hHBM1 / SRX24927512

Current download state:

- prefetch SRX24927512 --output-directory D:\二区\sra_cache --max-size 100G was started and interrupted by the user.
- The command resolved and downloaded at least two run files:
  - SRR29414117 = 2.215 GiB
  - SRR29414118 = 1.847 GiB
- Both downloaded SRA files passed db-validate and are consistent.

Clarification:

- --max-size 100G is not a request to download 100 GB.
- It is a safety ceiling that permits downloads up to 100 GB if the accession requires it.
- Actual downloaded size so far is about 4.06 GiB.

Status:

- hHBM1 sampled species QC has not started yet.
- Next step is to confirm whether SRX24927512 has additional SRR runs, then run sampled FASTQ export and Magic-BLAST QC on the downloaded run(s).

### 2026-04-28 20:22:51 hHBM1 Sampled Species QC Completed

Target control sample:

- GSM8329290 / hHBM1 / SRX24927512

Resolved run accessions:

- SRR29414117
- SRR29414118

Downloaded SRA state:

- Both run files are present under D:\二区\sra_cache.
- Both passed db-validate.

QC method:

- Exported first 1,000,000 spots per run using astq-dump --split-files -X 1000000.
- Identified read 4 as 50 bp transcript read.
- Ran Magic-BLAST against hg38 and mm10 BLAST v4 databases.

Aggregate result:

- sampled transcript reads: 2,000,000
- human hit: 1,934,721 (96.74%)
- mouse hit: 349,020 (17.45%)
- human-only: 1,585,826 (79.29%)
- mouse-only: 125 (0.01%)
- both: 348,895 (17.44%)
- neither: 65,154 (3.26%)
- human hit / mouse hit = 5.54
- human-only / mouse-only = 12,686.61

Decision:

- GSM8329290 / hHBM1 passes sampled human species QC.

Files written:

- D:\二区\qc_species_hHBM1\hHBM1_species_qc_summary.md
- D:\二区\species_filter_log.md
- D:\二区\gse269875_manifest_enriched.tsv

Next action:

- Scale sampled species QC to the remaining seven human mainline samples.

### 2026-04-28 22:41:52 hHBM2 Sampled Species QC Completed

Target sample:

- GSM8329291 / hHBM2 / SRX24927513

Resolved run accessions:

- SRR29414115
- SRR29414116

QC method:

- Exported first 1,000,000 spots per run using astq-dump --split-files -X 1000000.
- Used read 4 as 50 bp transcript read.
- Ran Magic-BLAST against hg38 and mm10.

Aggregate result:

- sampled transcript reads: 2,000,000
- human hit: 1,641,296 (82.06%)
- mouse hit: 310,830 (15.54%)
- human-only: 1,336,910 (66.85%)
- mouse-only: 6,444 (0.32%)
- both: 304,386 (15.22%)
- neither: 352,260 (17.61%)
- human hit / mouse hit = 5.28
- human-only / mouse-only = 207.47

Decision:

- GSM8329291 / hHBM2 passes sampled human species QC.

Current species QC completion:

- 3/9 human mainline samples completed and passed.

### 2026-04-28 External Validation Roadmap Added

User requested a revised four-direction plan to improve SCI Q2 feasibility:

1. External bulk/scRNA transcriptome validation.
2. Additional public MM single-cell dataset.
3. Clinical prognosis / disease-stage association.
4. Additional MM bone marrow spatial transcriptomics dataset.

Decision:

- Directions 1-3 are now mandatory manuscript-strengthening workstreams.
- Direction 4 is a high-value staged validation line, not a prerequisite for starting the main analysis.

Key datasets selected:

- GSE223060 for primary MM single-cell reference.
- GSE271107 for additional disease-stage scRNA validation.
- MMRF CoMMpass / MMRF-COMMPASS for clinical-transcriptomic validation.
- GSE24080 and GSE2658 as faster supplementary microarray prognosis cohorts.
- GSE299193 as the main external human Xenium spatial validation candidate.

### 2026-04-29 hHBM3 Sampled Species QC Completed

Target sample:

- GSM8329292 / hHBM3 / SRX24927514

Resolved run accessions:

- SRR29414113
- SRR29414114

Runtime note:

- Download plus QC completed in about 47 minutes for this two-run sample.
- D drive free space after completion: about 380.98 GiB.

QC method:

- Exported first 1,000,000 spots per run using `fastq-dump --split-files -X 1000000`.
- Used read 4 as the 50 bp transcript read.
- Ran Magic-BLAST against hg38 and mm10.

Aggregate result:

- sampled transcript reads: 2,000,000
- human hit: 1,719,739 (85.99%)
- mouse hit: 322,236 (16.11%)
- human-only: 1,404,808 (70.24%)
- mouse-only: 7,305 (0.37%)
- both: 314,931 (15.75%)
- neither: 272,956 (13.65%)
- human hit / mouse hit = 5.34
- human-only / mouse-only = 192.31

Decision:

- GSM8329292 / hHBM3 passes sampled human species QC.

Files updated:

- D:\二区\qc_species_hHBM3\hHBM3_species_qc_summary.md
- D:\二区\gse269875_manifest_enriched.tsv
- D:\二区\species_qc_remaining_human_summary.tsv
- D:\二区\species_filter_log.md
- D:\二区\PROJECT_LOG.md

Current human mainline species QC completion:

- 4/9 human mainline samples completed and passed.
- All three healthy human bone marrow controls have now passed.
- Remaining human MM samples: hMM2, hMM3, hMM4, hMM5, hMM6.

### 2026-04-29 hMM2 Sampled Species QC Completed After Read-Length Fix

Target sample:

- GSM8329294 / hMM2 / SRX24927516

Resolved run accessions:

- SRR29414110
- SRR29414111

Important technical correction:

- Initial hMM2 Magic-BLAST on raw read 4 produced an abnormally low mappable fraction.
- Inspection showed hMM2 read 4 length was 90 bp, unlike the 50 bp read 4 used by hMM1 and hHBM samples.
- The extra read tail contained polyA/adapter-like sequence.
- Script `07_batch_remaining_human_species_qc.py` was updated to trim read 4 to the first 50 bp when read 4 is longer than 50 bp.
- hMM2 was rerun using the corrected 50 bp species-QC query.

Aggregate corrected result:

- sampled transcript reads: 2,000,000
- human hit: 261,643 (13.08%)
- mouse hit: 46,050 (2.30%)
- human-only: 216,072 (10.80%)
- mouse-only: 479 (0.02%)
- both: 45,571 (2.28%)
- neither: 1,737,878 (86.89%)
- human hit / mouse hit = 5.68
- human-only / mouse-only = 451.09

Decision:

- GSM8329294 / hMM2 passes corrected sampled human species QC.
- Interpretation should mention lower mappable fraction than controls, but mouse-only evidence remains minimal after 50 bp trimming.

Files updated:

- D:\二区\scripts\07_batch_remaining_human_species_qc.py
- D:\二区\qc_species_hMM2\hMM2_species_qc_summary.md
- D:\二区\gse269875_manifest_enriched.tsv
- D:\二区\species_qc_remaining_human_summary.tsv
- D:\二区\species_filter_log.md
- D:\二区\PROJECT_LOG.md

Current human mainline species QC completion:

- 5/9 human mainline samples completed and passed.
- Completed controls: hHBM1, hHBM2, hHBM3.
- Completed MM samples: hMM1, hMM2.
- Remaining MM samples: hMM3, hMM4, hMM5, hMM6.
- D drive free space after hMM2 correction: about 375.55 GiB.

### 2026-04-29 hMM3 Sampled Species QC Completed

Target sample:

- GSM8329295 / hMM3 / SRX24927517

Resolved run accession:

- SRR29414109

Runtime note:

- Background run completed in about 34 minutes.
- Downloaded SRA size: about 2.72 GiB.
- D drive free space after completion: about 372.06 GiB.

QC method:

- Exported first 1,000,000 spots using `fastq-dump --split-files -X 1000000`.
- Used read 4 as the 50 bp transcript read.
- Ran Magic-BLAST against hg38 and mm10.

Aggregate result:

- sampled transcript reads: 1,000,000
- human hit: 676,287 (67.63%)
- mouse hit: 127,998 (12.80%)
- human-only: 548,374 (54.84%)
- mouse-only: 85 (0.01%)
- both: 127,913 (12.79%)
- neither: 323,628 (32.36%)
- human hit / mouse hit = 5.28
- human-only / mouse-only = 6451.46

Decision:

- GSM8329295 / hMM3 passes sampled human species QC.

Files updated:

- D:\二区\qc_species_hMM3\hMM3_species_qc_summary.md
- D:\二区\gse269875_manifest_enriched.tsv
- D:\二区\species_qc_remaining_human_summary.tsv
- D:\二区\species_filter_log.md
- D:\二区\PROJECT_LOG.md

Current human mainline species QC completion:

- 6/9 human mainline samples completed and passed.
- Completed controls: hHBM1, hHBM2, hHBM3.
- Completed MM samples: hMM1, hMM2, hMM3.
- Remaining MM samples: hMM4, hMM5, hMM6.

### 2026-04-29 hMM4 Sampled Species QC Completed

Target sample:

- GSM8329296 / hMM4 / SRX24927518

Resolved run accession:

- SRR29414108

Runtime note:

- Background run completed in about 39 minutes.
- Downloaded SRA size: about 2.46 GiB.
- D drive free space after completion: about 368.74 GiB.

QC method:

- Exported first 1,000,000 spots using `fastq-dump --split-files -X 1000000`.
- Used read 4 as the 50 bp transcript read.
- Ran Magic-BLAST against hg38 and mm10.

Aggregate result:

- sampled transcript reads: 1,000,000
- human hit: 135,175 (13.52%)
- mouse hit: 21,997 (2.20%)
- human-only: 113,307 (11.33%)
- mouse-only: 129 (0.01%)
- both: 21,868 (2.19%)
- neither: 864,696 (86.47%)
- human hit / mouse hit = 6.15
- human-only / mouse-only = 878.35

Decision:

- GSM8329296 / hMM4 passes sampled human species QC.
- Like hMM2, hMM4 has lower mappable fraction than hHBM controls, but mouse-only signal is minimal.

Files updated:

- D:\二区\qc_species_hMM4\hMM4_species_qc_summary.md
- D:\二区\gse269875_manifest_enriched.tsv
- D:\二区\species_qc_remaining_human_summary.tsv
- D:\二区\species_filter_log.md
- D:\二区\PROJECT_LOG.md

Current human mainline species QC completion:

- 7/9 human mainline samples completed and passed.
- Completed controls: hHBM1, hHBM2, hHBM3.
- Completed MM samples: hMM1, hMM2, hMM3, hMM4.
- Remaining MM samples: hMM5, hMM6.

### 2026-04-29 hMM5 Sampled Species QC Completed

Target sample:

- GSM8329297 / hMM5 / SRX24927519

Resolved run accessions:

- SRR29414106
- SRR29414107

Runtime note:

- Background run completed in about 77 minutes.
- Two large SRA files were downloaded: about 3.49 GiB and 3.35 GiB.
- D drive free space after completion: about 359.51 GiB.

QC method:

- Exported first 1,000,000 spots per run using `fastq-dump --split-files -X 1000000`.
- Read 4 length was 90 bp for both runs and was trimmed to the first 50 bp for species QC.
- Ran Magic-BLAST against hg38 and mm10.

Aggregate result:

- sampled transcript reads: 2,000,000
- human hit: 1,807,683 (90.38%)
- mouse hit: 292,741 (14.64%)
- human-only: 1,515,354 (75.77%)
- mouse-only: 412 (0.02%)
- both: 292,329 (14.62%)
- neither: 191,905 (9.60%)
- human hit / mouse hit = 6.18
- human-only / mouse-only = 3678.04

Decision:

- GSM8329297 / hMM5 passes corrected sampled human species QC.

Files updated:

- D:\二区\qc_species_hMM5\hMM5_species_qc_summary.md
- D:\二区\gse269875_manifest_enriched.tsv
- D:\二区\species_qc_remaining_human_summary.tsv
- D:\二区\species_filter_log.md
- D:\二区\PROJECT_LOG.md

Current human mainline species QC completion:

- 8/9 human mainline samples completed and passed.
- Completed controls: hHBM1, hHBM2, hHBM3.
- Completed MM samples: hMM1, hMM2, hMM3, hMM4, hMM5.
- Remaining MM sample: hMM6.

### 2026-04-29 hMM6 Sampled Species QC Completed; Human Mainline QC Complete

Target sample:

- GSM8329298 / hMM6 / SRX24927520

Resolved run accession:

- SRR29414105

Runtime note:

- Background run completed in about 32 minutes.
- Downloaded SRA size: about 2.30 GiB.
- D drive free space after completion: about 356.35 GiB.

QC method:

- Exported first 1,000,000 spots using `fastq-dump --split-files -X 1000000`.
- Used read 4 as the 50 bp transcript read.
- Ran Magic-BLAST against hg38 and mm10.

Aggregate result:

- sampled transcript reads: 1,000,000
- human hit: 257,148 (25.71%)
- mouse hit: 45,392 (4.54%)
- human-only: 211,966 (21.20%)
- mouse-only: 210 (0.02%)
- both: 45,182 (4.52%)
- neither: 742,642 (74.26%)
- human hit / mouse hit = 5.67
- human-only / mouse-only = 1009.36

Decision:

- GSM8329298 / hMM6 passes sampled human species QC.

Files updated:

- D:\二区\qc_species_hMM6\hMM6_species_qc_summary.md
- D:\二区\gse269875_manifest_enriched.tsv
- D:\二区\species_qc_remaining_human_summary.tsv
- D:\二区\species_filter_log.md
- D:\二区\gse269875_human_species_qc_summary.tsv
- D:\二区\PROJECT_LOG.md

Current human mainline species QC completion:

- 9/9 human mainline samples completed and passed.
- Completed controls: hHBM1, hHBM2, hHBM3.
- Completed MM samples: hMM1, hMM2, hMM3, hMM4, hMM5, hMM6.
- The project can now proceed to spatial expression matrix acquisition and downstream spatial analysis.

### 2026-04-29 GSE269875 Processed Spatial Matrix Package Acquired

Downloaded GEO processed data package:

- D:\二区\geo_processed\GSE269875_RAW.tar
- Size: 206.62 MB
- Source: GEO supplementary file for GSE269875

Extraction directory:

- D:\二区\geo_processed\GSE269875_RAW

Content check:

- 135 files extracted.
- All 9 human mainline samples have processed spatial matrix components:
  - `matrix.mtx.gz`
  - `barcodes.tsv.gz`
  - `features.tsv.gz`
  - `tissue_positions.csv.gz` or `tissue_positions_list.csv.gz`
  - `scalefactors_json.json.gz`
  - high/low resolution tissue images

Human processed matrix inventory:

| Sample | Group | Genes | Barcodes / in-tissue spots | Nonzero entries |
|---|---|---:|---:|---:|
| hHBM1 | control | 18,085 | 2,055 | 660,700 |
| hHBM2 | control | 18,085 | 822 | 505,350 |
| hHBM3 | control | 18,085 | 1,254 | 698,557 |
| hMM1 | MM | 18,085 | 373 | 256,923 |
| hMM2 | MM | 18,085 | 876 | 1,434,363 |
| hMM3 | MM | 18,085 | 977 | 1,952,439 |
| hMM4 | MM | 18,085 | 1,126 | 468,593 |
| hMM5 | MM | 18,085 | 2,993 | 535,498 |
| hMM6 | MM | 18,085 | 875 | 368,620 |

Files written:

- D:\二区\gse269875_processed_matrix_inventory.tsv

Decision:

- Processed spatial matrices are present and complete enough to start downstream spatial analysis directly.
- Full FASTQ expansion is not needed for the next analysis step unless processed matrix QC reveals serious defects.

### 2026-04-29 Human Processed Spatial Matrix QC Completed

Script added:

- D:\二区\scripts\08_processed_spatial_matrix_qc.py

QC output directory:

- D:\二区\analysis\spatial_qc

Files written:

- D:\二区\analysis\spatial_qc\human_spatial_qc_sample_summary.tsv
- D:\二区\analysis\spatial_qc\human_spatial_qc_flags.tsv
- D:\二区\analysis\spatial_qc\human_spatial_qc_all_spots.tsv.gz
- D:\二区\analysis\spatial_qc\human_spatial_qc_sample_summary.png
- D:\二区\analysis\spatial_qc\human_spatial_qc_distribution_overview.png
- D:\二区\SPATIAL_MATRIX_QC_REPORT.md

Key QC results:

| Sample | Group | Spots | Median UMIs/spot | Median genes/spot | Median MT % | Initial flag |
|---|---|---:|---:|---:|---:|---|
| hHBM1 | control | 2,055 | 232.0 | 102.0 | 3.72 | low median UMI/gene |
| hHBM2 | control | 822 | 1,242.0 | 536.5 | 2.43 | pass |
| hHBM3 | control | 1,254 | 748.5 | 329.5 | 2.37 | low median UMI/gene |
| hMM1 | MM | 373 | 465.0 | 408.0 | 6.81 | low spot count and low median UMI/gene |
| hMM2 | MM | 876 | 1,375.5 | 1,001.5 | 1.18 | pass |
| hMM3 | MM | 977 | 1,494.0 | 1,324.0 | 4.53 | pass |
| hMM4 | MM | 1,126 | 183.0 | 164.0 | 3.74 | low median UMI/gene |
| hMM5 | MM | 2,993 | 157.0 | 123.0 | 1.88 | low median UMI/gene |
| hMM6 | MM | 875 | 235.0 | 207.0 | 3.96 | low median UMI/gene |

Interpretation:

- Processed matrices are complete and usable.
- Sample depth is uneven.
- hMM2 and hMM3 are the strongest MM matrix-depth samples.
- hMM1 has few spots and should be lower-confidence for spatial heterogeneity claims.
- hMM4/hMM5/hMM6 are usable but require depth-aware normalization and sensitivity analysis.
- No broad mitochondrial-percentage failure was observed.

Decision:

- Proceed to spatial object construction and exploratory spatial clustering.
- Avoid strict universal filtering that would remove low-depth samples wholesale.
- Use sample-wise normalization and later sample-aware pseudobulk / region-level analyses.

### 2026-04-29 Preliminary Spatial Clustering Completed

Script added:

- D:\二区\scripts\09_preliminary_spatial_clustering.py

Output directory:

- D:\二区\analysis\spatial_preliminary

Main outputs:

- D:\二区\analysis\spatial_preliminary\combined_spot_embedding_clusters.tsv.gz
- D:\二区\analysis\spatial_preliminary\combined_spot_module_scores.tsv.gz
- D:\二区\analysis\spatial_preliminary\cluster_group_composition.tsv
- D:\二区\analysis\spatial_preliminary\cluster_counts_by_sample.tsv
- D:\二区\analysis\spatial_preliminary\cluster_top_markers.tsv
- D:\二区\analysis\spatial_preliminary\group_top_markers.tsv
- D:\二区\analysis\spatial_preliminary\sample_module_median_scores.tsv
- D:\二区\analysis\spatial_preliminary\combined_umap_group_sample_cluster.png
- D:\二区\analysis\spatial_preliminary\spatial_cluster_maps_all_human.png
- D:\二区\analysis\spatial_preliminary\spatial_plasma_cell_score_maps_all_human.png
- D:\二区\PRELIMINARY_SPATIAL_CLUSTERING_REPORT.md

Method summary:

- Loaded all 9 human processed spatial matrices.
- Applied per-spot 10,000-count normalization and `log1p` transformation.
- Selected 2,500 highly variable non-mitochondrial/non-ribosomal genes.
- Ran truncated SVD, UMAP, and KMeans clustering with 8 preliminary clusters.
- Computed exploratory spot-level cluster markers and module scores.

Cluster composition summary:

| Cluster | MM spots | Control spots | MM fraction |
|---|---:|---:|---:|
| 0 | 785 | 0 | 1.000 |
| 1 | 1,150 | 3,836 | 0.231 |
| 2 | 271 | 0 | 1.000 |
| 3 | 522 | 13 | 0.976 |
| 4 | 1,929 | 60 | 0.970 |
| 5 | 1,234 | 201 | 0.860 |
| 6 | 274 | 0 | 1.000 |
| 7 | 1,055 | 21 | 0.980 |

Initial biological signals:

- Cluster 1 is the main control-enriched / normal-like cluster.
- Most other clusters are MM-enriched.
- Top exploratory MM-vs-control markers include `JCHAIN`, `TXNDC5`, `IGHG1`, `B2M`, `IGHA1`, `CD74`, `VIM`, `IGKC`, `XBP1`, `PIM2`, `COL1A1`, `MZB1`, and `POU2AF1`.
- Cluster 2 is hMM3-associated and enriched for `CCND1`, `FCRLB`, `MZB1`, `TXNIP`, `CXCR4`, `POU2AF1`, and `XBP1`.
- Cluster 3 is hMM2-associated and enriched for `S100A8`, `S100A9`, `LYZ`, hemoglobin genes, and immunoglobulin genes, suggesting a mixed myeloid/erythroid/plasma-cell marrow niche.
- Cluster 0 and cluster 4 are hMM5-associated and plasma/immunoglobulin-rich.

Interpretation:

- The project has moved from QC into result generation.
- First-pass signals are biologically plausible for MM bone marrow spatial transcriptomics.
- These are still exploratory spot-level findings.
- Next analysis must use sample-aware pseudobulk / region-level summaries before making manuscript-grade statistical claims.

### 2026-04-29 Novelty and Risk Review

Work paused before further downstream analysis to check whether the project has already been done and to review current methodological risks.

Search conclusion:

- The main discovery dataset `GSE269875` has already been published in Communications Biology as a multiple myeloma bone marrow spatial transcriptomics study.
- Related MM spatial transcriptomics studies also exist, including Xenium-based human bone marrow trephine work and extramedullary myeloma spatial studies.
- A GSE269875-only atlas/reanalysis would have high novelty risk.
- A revised project remains defensible if framed as an externally validated spatial niche/signature study using spatial discovery plus scRNA and bulk/clinical validation.

Project risks identified:

- Novelty overlap with the original GSE269875 paper.
- Spot-level pseudoreplication if all spots are treated as independent observations.
- Uneven sample depth and spot count across human samples.
- Preliminary clusters partly reflect individual samples.
- Candidate genes include many canonical plasma-cell/MM markers and require careful triage.
- External scRNA, bulk/clinical, and optional independent spatial validation are still needed.

Decision:

- Do not continue as a simple GSE269875 reanalysis.
- Next analysis should create sample-aware spatial signatures and a candidate-ranking table before external validation.

File written:

- PROJECT_NOVELTY_AND_RISK_REVIEW.md

### 2026-04-29 Revised Q2 Project Plan

The project route was revised and formalized after novelty-risk review.

New route:

- Spatial discovery from `GSE269875` human Visium data.
- Sample-aware spatial niche/signature discovery instead of spot-only marker claims.
- Single-cell validation using public MM scRNA-seq datasets such as `GSE223060` and `GSE271107`.
- Bulk/clinical validation using `GSE24080`, `GSE2658`, and preferably CoMMpass if access is practical.
- Optional external spatial validation using `GSE299193` after a stable candidate shortlist exists.

Manuscript positioning:

- Do not claim this is the first MM bone marrow spatial atlas.
- Position the manuscript as an externally validated computational study of MM bone marrow spatial niche signatures.
- The expected publishable contribution is the evidence chain: spatial discovery -> cell-type attribution -> clinical transcriptomic validation.

Expected project results:

- A quality-controlled human MM bone marrow spatial analysis set.
- Sample-aware MM spatial niche maps.
- Two or three compact spatial signatures, likely covering plasma-cell stress/secretory state, inflammatory myeloid or immune-suppressed niche, and stromal/ECM remodeling.
- scRNA validation of candidate cell-type origin.
- bulk/clinical validation of at least one signature against stage, risk, survival, event-free survival, progression, or treatment-response variables.
- Optional independent Xenium/spatial validation if feasible.

Immediate next technical step:

- Build sample-aware pseudobulk summaries from current GSE269875 human matrices.
- Rank candidate genes/signatures by spatial enrichment, MM-vs-control effect, cross-sample consistency, sensitivity stability, cell-type interpretability, and external-validation feasibility.
- Produce a candidate spatial signature table before starting scRNA and clinical validation.

Estimated next-step time:

- Script development and first run: 1 to 2 hours.
- Computation on existing processed matrices: usually under 30 minutes.
- Review and report writing: 1 to 2 hours.

Project-level estimate:

- Sample-aware spatial signature discovery: 0.5 to 1 day.
- scRNA validation: 1 to 3 days.
- GEO bulk clinical validation: 1 to 2 days.
- CoMMpass validation: 2 to 7 days depending access and download workflow.
- Optional GSE299193 spatial validation: 2 to 5 days after candidate shortlist.
- Manuscript-grade figures and draft results: 2 to 4 days after main analyses stabilize.

File written:

- REVISED_Q2_PROJECT_PLAN.md

### 2026-04-29 Sample-Aware Spatial Signature Discovery

Script added:

- scripts\10_sample_aware_spatial_signatures.py

Output directory:

- analysis\spatial_candidate_signatures

Main outputs:

- candidate_spatial_signature_table.tsv
- candidate_spatial_signature_top100.tsv
- candidate_validation_shortlist.tsv
- sample_signature_scores.tsv
- signature_sensitivity_results.tsv
- gene_spatial_region_contrasts.tsv.gz
- sample_gene_mean_log_norm.tsv.gz
- sample_gene_pct_detected.tsv.gz
- sample_signature_score_heatmap.png
- signature_effects_all_samples.png
- top_candidate_genes_barplot.png

Method summary:

- Loaded all 9 human `GSE269875` processed spatial matrices.
- Used previous spot-level cluster assignments and QC metadata.
- Calculated seven biological program scores: plasma-secretory, myeloid-inflammatory, T/NK cytotoxic-exhaustion, stromal/ECM, endothelial/angiogenic, erythroid/megakaryocyte, and cycling/proliferation.
- Aggregated spot-level data to sample-level median signature scores.
- Calculated sample-level gene means and detection rates.
- Calculated within-sample high-vs-low spatial-region contrasts.
- Ranked candidate genes by MM-vs-control sample-level effect, cross-sample consistency, and spatial-region enrichment.

Key results:

- The strongest current program is `plasma_secretory`.
- All-sample `plasma_secretory` median score: MM `0.709`, control `0.000`, sample-level Cohen's d `3.129`, Mann-Whitney p `0.0256`.
- After excluding low-spot `hMM1`, `plasma_secretory` remains elevated: MM-control median difference `0.561`, Cohen's d `2.875`, p `0.0325`.
- `stromal_ecm` is the strongest secondary program: MM-control median difference `0.361`, Cohen's d `1.483`, p `0.0878`.
- `myeloid_inflammatory` signal is present but more sample-dependent: all-sample median difference `0.292`, Cohen's d `0.642`, p `0.500`.
- T/NK exhaustion and proliferation signatures are not strong enough in this pass to be central manuscript claims.

Candidate validation shortlist:

- Plasma program candidates: `TXNDC5`, `POU2AF1`, `ITM2C`, `UBE2J1`, `PIM2`, `SEC11C`, `TENT5C`, `CD79A`.
- Canonical plasma anchors: `JCHAIN`, `IGHG1`, `XBP1`, `MZB1`, `IGKC`, `TNFRSF17`, `IRF4`, `PRDM1`, `SDC1`, `IGHM`, `IGHA1`, `SLAMF7`.
- Myeloid candidates: `S100A9`, `S100A8`, `CTSS`, `LYZ`, `TYROBP`.
- Stromal/ECM candidates: `COL1A1`, `COL3A1`, `SPARC`, `COL1A2`, `CXCL12`, `FN1`, `DCN`.
- Endothelial candidates: `PECAM1`, `ENG`, `CLDN5`, `VWF`, `ESAM`.

Interpretation:

- Current discovery results support a stable MM-associated plasma-secretory spatial program and plausible secondary stromal/ECM and myeloid/inflammatory programs.
- The project is now ready for single-cell validation.
- The central publication risk remains that canonical plasma markers alone are not novel enough; external validation must support at least one nontrivial stromal, myeloid, or clinically associated signature.

File written:

- SPATIAL_SIGNATURE_DISCOVERY_REPORT.md

### 2026-04-29 GSE271107 Single-Cell Validation

Dataset:

- `GSE271107`
- GEO FTP source: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE271nnn/GSE271107/suppl/`
- Downloaded file: `external_scRNA/GSE271107/GSE271107_RAW.tar`
- File size: `408,852,480` bytes
- Extracted files: 19 H5 matrices

Script added:

- scripts\11_gse271107_scrna_validation.py

Output directory:

- analysis\scrna_gse271107_validation

Main outputs:

- gse271107_cell_signature_scores.tsv.gz
- gse271107_sample_qc_signature_summary.tsv
- gse271107_signature_by_stage.tsv
- gse271107_signature_by_celltype.tsv
- gse271107_signature_by_stage_celltype.tsv
- gse271107_candidate_gene_by_sample.tsv
- gse271107_candidate_gene_by_sample_celltype.tsv
- gse271107_celltype_composition_by_stage.png
- gse271107_signature_by_celltype_heatmap.png
- gse271107_signature_by_stage.png
- gse271107_candidate_gene_dotplot.png

Method summary:

- Parsed 5 HD, 6 MGUS, 4 SMM, and 4 newly diagnosed MM samples.
- Applied basic cell QC: >=200 genes, >=500 UMIs, <=25% mitochondrial percentage.
- Retained 127,528 cells.
- Used marker-inferred coarse compartments: plasma cell, B cell, T/NK cell, myeloid cell, erythroid cell, megakaryocyte/platelet, stromal-like, endothelial-like, low-marker.
- Scored the spatially derived signatures in each cell.

Key results:

- MM samples had higher marker-inferred plasma-cell fraction than HD/MGUS/SMM: MM `0.1674`, HD `0.0537`, MGUS `0.0265`, SMM `0.0198`.
- Plasma-secretory signature was highest in marker-inferred plasma cells: median `1.3388`.
- Stage-level plasma-secretory score was highest in MM: HD `0.0797`, MGUS `0.0809`, SMM `0.0903`, MM `0.1487`.
- `TXNDC5` was strongly plasma-cell associated: mean log-normalized expression `2.1958`, detected in `94.86%` of marker-inferred plasma cells, and highest at MM stage.
- Canonical plasma anchors `JCHAIN`, `MZB1`, and `XBP1` were also plasma-cell enriched and highest in MM.
- Myeloid candidates `S100A8`, `S100A9`, and `CTSS` mapped correctly to marker-inferred myeloid cells, but MM-stage enrichment was not supported in this dataset.
- Stromal/ECM candidates `COL1A1`, `COL3A1`, and `CXCL12` mapped to stromal-like cells, but only 30 stromal-like cells were detected; GSE271107 is not sufficient as the main stromal validation dataset.

Interpretation:

- GSE271107 supports the plasma-secretory spatial signature and prioritizes `TXNDC5` for downstream bulk/clinical validation.
- Myeloid and stromal candidates have plausible cell-type attribution but need stronger external validation before manuscript-level claims.
- The next best translational step is fast bulk/clinical validation of the plasma-secretory / `TXNDC5` axis using `GSE24080` / `GSE2658`, while keeping `GSE223060` as an additional scRNA validation dataset.

File written:

- SCRNA_GSE271107_VALIDATION_REPORT.md

### 2026-04-29 Folder Organization

Work paused before the next scientific analysis step to organize the project folder.

Actions:

- Created `README_PROJECT_STRUCTURE.md` at project root.
- Created `reports/` with subfolders:
  - `reports/planning`
  - `reports/setup`
  - `reports/analysis`
  - `reports/validation`
- Moved loose report Markdown files from the root into `reports/`.
- Created `reports/REPORT_INDEX.md`.
- Kept workflow-critical directories in place: `analysis`, `geo_processed`, `external_scRNA`, `scripts`, `sra_cache`, `qc_species_*`, `references`, and `blastdb`.

Decision:

- The project remains a pure bioinformatics / translational public-data analysis project.
- Wet-lab experiments are not required for the current target route.
- The next scientific step, when resumed, should be bulk / clinical transcriptomic validation of the `plasma_secretory` / `TXNDC5` axis.

Files written:

- README_PROJECT_STRUCTURE.md
- reports\REPORT_INDEX.md

### 2026-04-29 Bulk / Clinical Transcriptomic Validation

Purpose:

- Start the next scientific step after folder organization.
- Add a clinical/translational validation layer to the spatial discovery plus GSE271107 scRNA validation workflow.
- Keep the route as pure public-data bioinformatics; no wet-lab work is required.

Datasets used:

- `GSE24080`: GPL570 processed series matrix, 559 scored MM samples.
- `GSE2658`: GPL570 processed series matrix, 559 scored MM samples.
- `GPL570.annot.gz`: Affymetrix GPL570 probe-to-gene annotation.

Script added:

- `scripts\12_bulk_clinical_validation.py`

Output directory:

- `analysis\bulk_clinical_validation`

Main outputs:

- `bulk_clinical_sample_scores.tsv`
- `bulk_target_gene_expression.tsv`
- `bulk_signature_scores.tsv`
- `bulk_target_probe_mapping.tsv`
- `bulk_outcome_association_results.tsv`
- `bulk_validation_dataset_summary.tsv`
- `GSE24080_efs_24mo_event_boxplots.png`
- `GSE24080_os_24mo_event_boxplots.png`
- `GSE2658_SURIND_boxplots.png`
- `GSE2658_AMP_high_3plus_boxplots.png`

Method summary:

- Parsed GPL570 annotation for candidate genes and spatial signatures.
- Collapsed each target gene to the highest-variance mapped GPL570 probe within each dataset.
- Scored `plasma_secretory`, `myeloid_inflammatory`, and `stromal_ecm` programs.
- Tested GSE24080 24-month EFS and OS milestone outcomes.
- Tested GSE2658 disease-related death, disease-related survival time, and 1q21 amplification status.
- Added Benjamini-Hochberg FDR correction within each dataset/outcome/test family.

Key results:

- Both GSE24080 and GSE2658 had full target-score coverage: 559/559 samples scored for `plasma_secretory` and `TXNDC5`.
- `TXNDC5` itself did not show strong clinical association in this first-pass bulk analysis:
  - GSE24080 EFS: Mann-Whitney p `0.789`, AUC `0.492`.
  - GSE24080 OS: Mann-Whitney p `0.478`, AUC `0.475`.
  - GSE2658 disease-related death: Mann-Whitney p `0.226`, AUC `0.539`.
  - GSE2658 median-split survival log-rank p `0.718`.
- The full `plasma_secretory` score also did not show strong direct outcome association in these two cohorts:
  - GSE24080 EFS p `0.580`.
  - GSE24080 OS p `0.170`.
  - GSE2658 disease-related death p `0.437`.
- Some related plasma-program genes showed clinical/subgroup signals:
  - `XBP1` was lower in GSE24080 24-month OS death cases, Mann-Whitney p `0.0060`.
  - `JCHAIN` was higher in GSE2658 disease-related death cases, Mann-Whitney p `0.0234`.
  - `POU2AF1` median-split groups differed in GSE2658 disease-related survival, log-rank p `0.0358`.
  - `POU2AF1` and `XBP1` were strongly associated with GSE2658 1q21 amplification status, but in the lower-expression direction for 3+ copy samples.
- After FDR correction, the most robust signals were:
  - GSE24080 OS death vs `XBP1`: Mann-Whitney FDR `0.0422`.
  - GSE2658 1q21 amplification vs `POU2AF1`: Mann-Whitney FDR `3.12e-05`, Fisher FDR `1.64e-04`.
  - GSE2658 1q21 amplification vs `XBP1`: Mann-Whitney FDR `1.73e-04`.
  - GSE2658 1q21 amplification vs `JCHAIN`: Mann-Whitney FDR `0.0189`.

Interpretation:

- The project can continue and now has a third validation layer, but the first-pass clinical evidence is mixed.
- The spatial plus scRNA result remains strongest for biological localization of the `plasma_secretory` / `TXNDC5` axis.
- Direct clinical-outcome support for `TXNDC5` is currently weak, so the manuscript should not overclaim `TXNDC5` as an independent prognostic biomarker yet.
- For SCI Q2 competitiveness, the next route should broaden from a single-gene `TXNDC5` story to a plasma-secretory clinical-subtype story, prioritizing `POU2AF1`, `JCHAIN`, `XBP1`, 1q21 amplification, and preferably CoMMpass or another clinically annotated bulk cohort.

Report written:

- `reports\validation\BULK_CLINICAL_VALIDATION_REPORT.md`

Next action:

- Refine the clinical-validation layer:
  - add multiple-testing corrected result tables;
  - generate publication-ready clinical association figures;
  - test clinical subgroups/risk features where available;
  - seek CoMMpass or another clinically annotated MM bulk dataset for stronger independent validation.

### 2026-04-29 Manuscript Direction Adjustment

Updated central direction:

- The project should now be framed as:
  - spatial discovery + single-cell validation + bulk clinical validation supporting an MM bone marrow `plasma_secretory` clinical-subtype axis.
- `TXNDC5` remains a spatial and single-cell localization candidate:
  - strong in spatial discovery;
  - strong plasma-cell attribution in GSE271107;
  - not yet supported as an independent bulk clinical-outcome marker.
- `POU2AF1`, `XBP1`, and `JCHAIN` are better positioned for clinical subtype / risk-association components:
  - `XBP1` has an FDR-stable association with GSE24080 24-month OS death.
  - `POU2AF1`, `XBP1`, and `JCHAIN` have FDR-stable associations with GSE2658 1q21 amplification status.

Planning decision:

- Do not build the manuscript around a single-gene `TXNDC5` prognostic claim.
- Build the manuscript around a broader MM plasma-secretory clinical-subtype axis.
- Treat `TXNDC5` as a spatially localized and single-cell-supported candidate marker within that axis.
- Treat `POU2AF1`, `XBP1`, and `JCHAIN` as the stronger clinical/risk-linking genes for the next validation stage.

Revised next-stage plan:

1. Refine bulk clinical validation figures and tables:
   - FDR-ranked association table;
   - GSE24080 OS/EFS expression plots;
   - GSE2658 1q21 amplification plots;
   - effect-size summary for `TXNDC5`, `POU2AF1`, `XBP1`, `JCHAIN`, and the `plasma_secretory` score.
2. Re-analyze the axis as a subtype program:
   - high vs low plasma-secretory state;
   - `POU2AF1/XBP1/JCHAIN` clinical-subtype module;
   - overlap between spatial plasma-rich regions, scRNA plasma-cell state, and bulk risk association.
3. Seek an additional clinical cohort:
   - first choice: CoMMpass if accessible;
   - fallback: another GEO/ArrayExpress MM cohort with survival, risk, treatment response, or cytogenetic annotations.
4. Keep optional external spatial validation staged:
   - only use GSE299193 after the subtype axis and candidate marker set are stable.

Manuscript implication:

- The claim should be conservative and defensible:
  - "An MM bone marrow plasma-secretory spatial program is identified and validated across single-cell and bulk clinical transcriptomic cohorts."
- Avoid overclaiming:
  - no statement that `TXNDC5` alone is a validated prognostic biomarker at the current stage.

### 2026-04-29 Plasma-Secretory Clinical Subtype Refinement

Purpose:

- Continue the revised manuscript route after the direction adjustment.
- Operationalize the MM bone marrow `plasma_secretory` clinical-subtype axis.
- Separate marker roles:
  - `TXNDC5`: spatial / single-cell plasma-localization candidate.
  - `POU2AF1`, `XBP1`, `JCHAIN`: clinical subtype / risk-linking module.

Script added:

- `scripts\13_plasma_secretory_subtype_refinement.py`

Output directory:

- `analysis\plasma_secretory_subtype_refinement`

Main outputs:

- `plasma_secretory_subtype_sample_scores.tsv`
- `plasma_secretory_subtype_associations.tsv`
- `plasma_secretory_subtype_fdr_ranked.tsv`
- `plasma_secretory_subtype_effect_summary.tsv`
- `subtype_top_associations_barplot.png`
- `gse2658_module_by_1q21.png`
- `gse24080_xbp1_by_os.png`
- `gse2658_module_survival_km.png`
- `gse24080_axis_correlation_heatmap.png`
- `gse2658_axis_correlation_heatmap.png`

Method summary:

- Defined a clinical subtype module as the within-cohort mean z-score of `POU2AF1`, `XBP1`, and `JCHAIN`.
- Median-split each dataset into `module_high` and `module_low` states.
- Re-tested the module and axis genes against:
  - GSE24080 24-month EFS;
  - GSE24080 24-month OS;
  - GSE2658 disease-related death;
  - GSE2658 disease-related survival;
  - GSE2658 1q21 amplification status.
- Added FDR-ranked association tables and publication-oriented exploratory figures.

Key results:

- The strongest FDR-stable signal is the GSE2658 1q21 amplification association:
  - clinical subtype module: FDR `1.65e-05`, lower module score in 3+ copy samples.
  - `POU2AF1_z`: FDR `1.65e-05`, lower in 3+ copy samples.
  - `XBP1_z`: FDR `9.91e-05`, lower in 3+ copy samples.
  - `JCHAIN_z`: FDR `0.0122`, lower in 3+ copy samples.
- GSE24080 OS death vs `XBP1_z` remains FDR-supported:
  - FDR `0.0362`, lower `XBP1_z` in 24-month death cases.
- Survival associations in GSE2658 are still exploratory:
  - `POU2AF1_z` log-rank FDR `0.2146`.
  - This is not strong enough to claim validated prognosis.
- Axis correlation differs by cohort:
  - GSE24080 clinical subtype module has weak/moderate correlation with `plasma_secretory_score_z` and `TXNDC5_z`.
  - GSE2658 clinical subtype module is strongly correlated with `plasma_secretory_score_z` and `TXNDC5_z`, supporting axis coherence in that cohort.

Interpretation:

- The revised subtype-axis strategy is technically workable and produces stronger results than a single-gene `TXNDC5` prognostic framing.
- The most defensible current clinical statement is risk/subtype association, especially with 1q21 amplification, not validated survival prediction.
- Next project step should be either:
  - CoMMpass acquisition/validation for survival, ISS/R-ISS, cytogenetics, or treatment response;
  - or publication-figure consolidation if CoMMpass access is delayed.

Report written:

- `reports\validation\PLASMA_SECRETORY_SUBTYPE_REFINEMENT_REPORT.md`

### 2026-04-29 CoMMpass / GDC Clinical Validation

Purpose:

- Enter the next validation stage using a larger clinically annotated MM bulk RNA-seq cohort.
- Validate whether the `plasma_secretory` axis and `POU2AF1/XBP1/JCHAIN` subtype module associate with OS and ISS in CoMMpass/GDC.
- Use open GDC processed RNA-seq data only; no controlled BAM/raw sequencing data were required.

Data source:

- GDC project: `MMRF-COMMPASS`.
- Project status: open/released.
- Open RNA-seq files indexed: 859 STAR-count gene-expression files.
- Baseline visit-1 bone marrow CD138+ samples selected: 762.
- Merged RNA-seq + clinical samples: 762.
- OS events: 153.
- ISS stage available: 742.

Script added:

- `scripts\14_commppass_gdc_validation.py`

Output directory:

- `analysis\commppass_gdc_validation`

Main outputs:

- `commppass_baseline_manifest.tsv`
- `commppass_download_status.tsv`
- `commppass_target_tpm.tsv`
- `commppass_axis_clinical_scores.tsv`
- `commppass_axis_associations.tsv`
- `commppass_axis_fdr_ranked.tsv`
- `commppass_module_by_iss.png`
- `commppass_module_os_km.png`
- `commppass_top_associations_barplot.png`
- `commppass_axis_correlation_heatmap.png`

Technical notes:

- GDC access through Python/PowerShell HTTPS failed due local SSL/connection handling.
- Resolved by using `curl.exe --ssl-no-revoke`.
- Download was performed as resumable/checkpointed file-level downloads.
- Initial run downloaded 760/762 files, with 2 transient connection-reset failures.
- Rerun completed the remaining files; final download status: 762/762 successful.
- Total downloaded STAR-count files: about 3.21 GB under `external_bulk\CoMMpass_GDC\star_counts`.

Method summary:

- Selected only visit-1 bone marrow CD138+ tumor samples.
- Extracted target gene TPM values from GDC STAR-count files.
- Calculated log2(TPM + 1), within-cohort z-scores, `plasma_secretory_score_z`, and `clinical_subtype_module_score_z`.
- Clinical subtype module was defined as mean z-score of `POU2AF1`, `XBP1`, and `JCHAIN`.
- Tested associations with:
  - OS event;
  - median-split OS log-rank;
  - ISS stage III vs I/II;
  - ISS ordinal stage.

Key results:

- The `plasma_secretory` score is strongly associated with OS event:
  - Mann-Whitney p `1.55e-06`, FDR `9.31e-06`.
  - Median event-vs-nonevent delta `0.3460`.
- The `POU2AF1/XBP1/JCHAIN` clinical subtype module is also strongly associated with OS event:
  - Mann-Whitney p `1.82e-05`, FDR `5.46e-05`.
  - Median event-vs-nonevent delta `0.2813`.
- `JCHAIN_z` and `XBP1_z` both associate with OS event:
  - `JCHAIN_z` FDR `8.08e-04`.
  - `XBP1_z` FDR `0.0011`.
- `TXNDC5_z` has a weaker but FDR-supported OS event association:
  - FDR `0.0163`.
  - This supports keeping `TXNDC5` in the axis, but not as the sole clinical marker.
- ISS results support clinical-stage relevance:
  - `plasma_secretory_score_z` vs ISS ordinal: Spearman rho `0.1319`, FDR `0.0019`.
  - `XBP1_z` vs ISS stage III: FDR `0.0326`.
  - `plasma_secretory_score_z` vs ISS stage III: FDR `0.0326`.
  - clinical subtype module vs ISS ordinal: Spearman rho `0.0818`, FDR `0.0387`.
- OS log-rank results:
  - `plasma_secretory_score_z` median split log-rank p `0.00668`, FDR `0.0401`.
  - clinical subtype module log-rank FDR `0.0678`, exploratory but directionally supportive.

Interpretation:

- CoMMpass/GDC substantially strengthens the revised manuscript route.
- The strongest current claim is now:
  - MM bone marrow `plasma_secretory` subtype axis is spatially discovered, single-cell localized, and clinically associated with OS/ISS in CoMMpass.
- `TXNDC5` should remain a spatial/single-cell candidate within this axis.
- `POU2AF1/XBP1/JCHAIN` remains a useful clinical subtype module, with CoMMpass OS-event support.
- R-ISS, detailed cytogenetic high-risk, PFS, and treatment response were not available in the open GDC clinical slice and require a fuller MMRF/CoMMpass clinical table.

Report written:

- `reports\validation\COMMPASS_GDC_VALIDATION_REPORT.md`

### 2026-04-29 Post-CoMMpass Finding Sync and Next-Stage Plan

Synchronized current defensible finding:

- MM bone marrow `plasma_secretory` spatial program has now been linked across three layers:
  - spatial discovery in GSE269875;
  - single-cell localization support in GSE271107;
  - CoMMpass/GDC bulk RNA-seq clinical support for OS and ISS.
- The strongest current manuscript claim is:
  - MM bone marrow `plasma_secretory` subtype axis is spatially discovered, single-cell localized, and clinically associated with OS/ISS in CoMMpass.
- `TXNDC5` should remain framed as a spatial/single-cell localization candidate within the axis.
- `POU2AF1`, `XBP1`, and `JCHAIN` should carry the clinical subtype / risk-linking part of the manuscript.
- `plasma_secretory_score_z` remains the strongest cross-layer axis score.

Important claim boundary:

- Do not claim that R-ISS, PFS, detailed cytogenetic high-risk, or treatment-response validation has been completed.
- The current GDC open clinical slice does not contain sufficiently complete usable fields for those endpoints.
- Local inspection found OS and ISS to be usable.
- The only progression-like field currently visible in the merged GDC table is `diagnoses.0.progression_or_recurrence`, but it is uniformly unknown / not usable for PFS analysis.

External clinical-data check:

- GDC open CoMMpass data are sufficient for the current OS/ISS validation.
- Fuller R-ISS, PFS, cytogenetic high-risk, and treatment-response validation likely requires MMRF Virtual Lab / Researcher Gateway clinical files.
- MMRFBiolinks documentation indicates Researcher Gateway workflows can use patient-clinical, treatment-response, and canonical-variant datasets, but these require authorized local files.

Decision:

- Do not pause the project while waiting for fuller MMRF access.
- Proceed now with manuscript-grade figure/table consolidation based on the completed spatial, scRNA, GEO bulk, and CoMMpass/GDC evidence.
- In parallel, attempt to obtain fuller MMRF/CoMMpass clinical tables for optional strengthening of R-ISS, PFS, cytogenetic high-risk, and treatment-response analyses.

Next action plan:

1. Build a cross-cohort evidence table under `analysis\manuscript_figures`.
2. Generate publication-level figure panels:
   - study design and data flow;
   - spatial `plasma_secretory` discovery;
   - GSE271107 single-cell localization and `TXNDC5` plasma-cell signal;
   - GEO bulk subtype / risk support;
   - CoMMpass/GDC OS and ISS validation.
3. Draft `reports\manuscript\MANUSCRIPT_RESULTS_SKELETON.md` with explicit claim boundaries.
4. Add planned script `scripts\15_build_manuscript_figures.py`.
5. If fuller clinical files are obtained later, add `scripts\16_commppass_full_clinical_validation.py`.

Planning report written:

- `reports\planning\NEXT_STAGE_ACTION_PLAN.md`

### 2026-04-29 Manuscript-Grade Figure Consolidation

Purpose:

- Advance the project main line from analysis output to manuscript-grade figures and result text.
- Use high-impact primary translational genomics / oncology figure conventions as design references.
- Do not use textbooks, encyclopedia pages, blogs, or low-quality papers as figure references.

Scripts added:

- `scripts\15_build_manuscript_figures.py`
- `scripts\16_commppass_full_clinical_validation.py`

Main manuscript outputs:

- `analysis\manuscript_figures\cross_cohort_evidence_table.tsv`
- `analysis\manuscript_figures\fig1_study_design_evidence_chain.png`
- `analysis\manuscript_figures\fig2_spatial_plasma_secretory_discovery.png`
- `analysis\manuscript_figures\fig3_scrna_plasma_secretory_localization.png`
- `analysis\manuscript_figures\fig4_geo_bulk_clinical_support.png`
- `analysis\manuscript_figures\fig5_commppass_os_iss_validation.png`
- SVG and PDF versions were also generated for each figure.

Manuscript draft outputs:

- `reports\manuscript\MANUSCRIPT_RESULTS_SKELETON.md`
- `reports\manuscript\FIGURE_LEGENDS_DRAFT.md`
- `reports\manuscript\FIGURE_DESIGN_REFERENCE_NOTE.md`

Cross-cohort evidence table summary:

- Spatial discovery: GSE269875, 9 human spatial samples, `plasma_secretory` MM-vs-control median difference `0.709`, Cohen d `3.129`, p `0.0256`.
- Single-cell localization: GSE271107, TXNDC5 plasma-cell mean log-normalized expression `2.196`, detection `94.86%`.
- GEO bulk support: GSE2658 clinical subtype module association with 1q21 amplification, FDR `1.65e-05`; GSE24080 XBP1 association with 24-month OS death, FDR `0.0362`.
- CoMMpass/GDC validation: 762 baseline CD138+ RNA-seq samples; `plasma_secretory_score_z` vs OS event FDR `9.31e-06`; ISS ordinal FDR `0.0019`; median-split OS log-rank FDR `0.0401`.

Fuller clinical enhancement line:

- `scripts\16_commppass_full_clinical_validation.py` scans `external_bulk\CoMMpass_full_clinical` for R-ISS, PFS, cytogenetic high-risk, and treatment-response fields.
- Current scan found no fuller clinical files in that folder.
- Readiness report written:
  - `reports\validation\COMMPASS_FULL_CLINICAL_READINESS_REPORT.md`

Current decision:

- The main manuscript route should continue using the completed OS/ISS-supported evidence chain.
- R-ISS, PFS, cytogenetic high-risk, and treatment-response validation remain optional strengthening analyses pending authorized fuller MMRF/CoMMpass clinical files.

### 2026-04-29 Main Manuscript Draft and Fuller Clinical Acquisition Plan

Purpose:

- Continue the main manuscript route after figure consolidation.
- Write the first full main-text draft using the current completed evidence chain.
- Keep R-ISS, PFS, cytogenetic high-risk, and treatment-response validation as planned enhancements rather than completed claims.
- Restrict manuscript formatting references to high-impact primary research article conventions from SCI Q1+ style journals; do not use textbook, encyclopedia, blog, tutorial, or low-quality paper formatting.

Manuscript files written:

- `reports\manuscript\MANUSCRIPT_MAIN_TEXT_DRAFT.md`
- `reports\manuscript\MANUSCRIPT_FORMAT_REFERENCE_NOTE.md`

Main draft contents:

- Working title.
- Abstract.
- Introduction.
- Methods.
- Results.
- Discussion.
- Data availability draft.
- Draft reference anchors to verify before submission.

Central wording now used:

- The manuscript claims that an MM bone marrow `plasma_secretory` spatial program is localized to plasma-cell compartments and associated with OS and ISS clinical risk in CoMMpass/GDC.
- `TXNDC5` is framed as a spatial/single-cell localization candidate.
- `POU2AF1/XBP1/JCHAIN` and `plasma_secretory_score_z` are framed as the clinically stronger subtype axis.
- R-ISS, PFS, detailed cytogenetic high-risk, and treatment response are explicitly marked as pending fuller clinical validation.

Fuller clinical acquisition plan written:

- `reports\planning\COMMPASS_FULL_CLINICAL_ACQUISITION_PLAN.md`

Official / primary source checks summarized:

- MMRF Virtual Lab documentation indicates that the platform integrates clinical, genomic, and multi-omic data and supports access/download of harmonized datasets.
- CoMMpass Clinical Data Overview indicates that available clinical domains include Cytogenetics/FISH, treatment details, response/relapse documentation, progression-free survival, overall survival, and time-to-event variables.
- CoMMpass IA access documentation indicates that IA24 is the final comprehensive release and that Repository filters can identify Summary Data Files and Clinical Data Tables.
- MMRFBiolinks documentation states that Researcher Gateway clinical files contain more clinical information than the GDC subset, including best overall response.

Current action implication:

- Continue writing and polishing the OS/ISS-supported manuscript now.
- In parallel, user should obtain fuller MMRF/CoMMpass clinical files and place them under `external_bulk\CoMMpass_full_clinical`.
- After files are added, rerun `python scripts\16_commppass_full_clinical_validation.py` to detect candidate endpoint columns.

### 2026-04-29 Remaining Gaps Audit

Question addressed:

- Whether fuller MMRF/CoMMpass clinical tables have been found.
- Whether the extra MM bone marrow spatial transcriptomics validation dataset has been obtained.
- Which original planned components remain incomplete.

Findings:

- Fuller MMRF/CoMMpass clinical tables have not been obtained locally.
- `external_bulk\CoMMpass_full_clinical` is still empty.
- The analysis scanner `scripts\16_commppass_full_clinical_validation.py` is ready, but cannot run endpoint validation until authorized clinical files are downloaded.
- Official MMRF Virtual Lab documentation confirms that richer clinical domains exist, including Cytogenetics/FISH, treatment details, response/relapse documentation, PFS, OS, and time-to-event variables.

Extra spatial validation update:

- A second public human MM bone marrow spatial dataset has been found:
  - `GSE299193`
  - human Xenium bone marrow trephine spatial transcriptomics
  - 22 human samples
  - control, MGUS, MM, smouldering myeloma, and relapse myeloma groups
  - RAW package size: 76.6 GB
- The related SuperSeries is `GSE299207`, but the human SubSeries `GSE299193` is the preferred immediate target.
- This dataset has not yet been downloaded or analyzed.
- Current D-drive free space is about 347 GB, so the download is feasible, but extraction/intermediate processing should be planned as a large-data step.

Current completion matrix:

- External bulk validation: completed.
- External scRNA validation: completed.
- Clinical OS/ISS validation: completed.
- R-ISS/PFS/cytogenetic high-risk/treatment response: not completed; needs fuller clinical files.
- Extra spatial validation: found but not completed; needs `GSE299193` download and analysis.
- Manuscript-grade figures Fig. 1-5: completed first pass.
- Main manuscript text draft: completed first pass.

Report written:

- `reports\planning\REMAINING_GAPS_STATUS_AUDIT.md`

### 2026-04-29 GSE299193 Xenium Public Spatial Validation Started

Purpose:

- Start the previously missing second MM bone marrow spatial-transcriptomics validation line.
- Use public human `GSE299193` Xenium data rather than the larger human+mouse SuperSeries.

Official dataset confirmed:

- GEO accession: `GSE299193`.
- Title: Profiling the spatial architecture of multiple myeloma in human bone marrow trephines with spatial transcriptomics [human].
- Platform: Xenium In Situ Analyzer, Homo sapiens.
- PubMed ID: `40643106`.
- Related SuperSeries: `GSE299207`.
- RAW package: `GSE299193_RAW.tar`.
- Expected size: `82,255,360,000` bytes / `76.61` GiB.

SOFT metadata parsed:

- Total human samples: 22.
- Ctrl: 4.
- MGUS: 2.
- SM: 5.
- MM: 10.
- RM: 1.

Files and scripts added:

- `external_spatial\GSE299193\metadata\GSE299193_family.soft.gz`
- `external_spatial\GSE299193\metadata\gse299193_sample_manifest.tsv`
- `analysis\gse299193_xenium_validation\gse299193_sample_group_summary.tsv`
- `analysis\gse299193_xenium_validation\gse299193_download_status.tsv`
- `scripts\17_gse299193_download_status.py`
- `scripts\start_gse299193_download.ps1`
- `scripts\18_gse299193_xenium_validation.py`
- `reports\validation\GSE299193_XENIUM_DOWNLOAD_STATUS.md`
- `reports\validation\GSE299193_XENIUM_VALIDATION_REPORT.md`

Download status:

- Background `curl.exe` download started with resume support.
- Process ID at launch check: `7780`.
- Initial speed test: about `1.86 MB/s`.
- Estimated full download time at that speed: about `11.7` hours.
- Early progress check showed the output file growing and about `0.36%` complete.

Validation plan after download:

- Confirm RAW tar reaches expected size.
- List tar contents.
- Extract only necessary Xenium files first, especially `cell_feature_matrix.h5` and sample metadata.
- Compute sample-level `plasma_secretory_score`, `clinical_subtype_module`, and TXNDC5/POU2AF1/XBP1/JCHAIN signals.
- Compare Ctrl/MGUS/SM versus MM/RM groups.
- If signal is usable, add a new Fig. 6 or supplemental validation figure and update the manuscript draft.

Current status:

- Download is in progress.
- Xenium validation cannot complete until the 76.61 GiB RAW tar finishes downloading.

### 2026-04-29 GSE299193 Download Paused

User requested pause to rest.

Action:

- Stopped background `curl.exe` download process.
- Kept partial file for future resume:
  - `external_spatial\GSE299193\raw\GSE299193_RAW.tar`

Pause status:

- Downloaded bytes at pause: `9,041,175,150`.
- Downloaded size at pause: `8.42` GiB.
- Percent complete: `10.9916%`.
- Remaining size: `68.186` GiB.

Resume command:

- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\start_gse299193_download.ps1`

After completion:

- Run `python scripts\17_gse299193_download_status.py` to confirm complete file size.
- Then run `python scripts\18_gse299193_xenium_validation.py` to start Xenium validation.

### 2026-04-29 User-Supplied MMRF-Style Table Audit

Question:

- User supplied 10 purported MMRF/CoMMpass-style tables with patient IDs such as `MMF-001` to `MMF-005` and asked whether the data were correct.

Local cross-check:

- Searched local CoMMpass/GDC clinical and expression outputs for `MMF-001` to `MMF-005` and supplied aliquot-style IDs.
- No matches were found.
- Existing local CoMMpass/GDC identifiers use `MMRF_####`, `MMRF_####_1_BM_CD138pos`, and aliquot IDs such as `MMRF_1021_1_BM_CD138pos_T2_TSMRU_L01873`.
- `external_bulk\CoMMpass_full_clinical` remains empty, so there are no authorized fuller MMRF clinical files locally that could validate the supplied tables.

Decision:

- The supplied tables should be treated as synthetic / fictional schema examples, not valid MMRF/CoMMpass clinical data.
- They must not be used for R-ISS, PFS, cytogenetic high-risk, treatment-response validation, manuscript figures, supplementary tables, or scientific claims.

Report written:

- `reports\validation\USER_SUPPLIED_MMRF_TABLE_AUDIT.md`

### 2026-04-29 Route Adjustment: Q2 Mainline Without Required Fuller MMRF

Decision:

- The project will no longer depend on fuller MMRF/CoMMpass clinical data as a required condition for submission.
- Fuller MMRF clinical access remains useful, but is now a future enhancement rather than a blocker.

New mainline:

- spatial discovery;
- single-cell localization;
- multi-bulk clinical validation;
- second spatial cohort validation.

Revised manuscript claim:

- An MM bone marrow `plasma_secretory` spatial program is discovered in spatial transcriptomics, localized to plasma-cell compartments by single-cell RNA-seq, supported by external bulk cohorts, associated with OS and ISS in CoMMpass/GDC, and externally tested in a second human MM bone marrow spatial dataset.

Claims no longer required for the mainline:

- R-ISS validation;
- complete PFS validation;
- treatment-response validation;
- definitive clinical classifier performance;
- prospective clinical utility.

Current mainline status:

- GSE269875 spatial discovery: completed.
- GSE271107 single-cell validation: completed.
- GSE24080/GSE2658 external bulk validation: completed.
- CoMMpass/GDC open OS/ISS validation: completed.
- Manuscript Fig. 1-5: completed first pass.
- Main text draft: completed first pass.
- GSE299193 second spatial validation: public dataset found; download paused at 8.42 GiB / 76.61 GiB; analysis scripts prepared.

Next priority:

- Resume and complete `GSE299193_RAW.tar` download.
- Run `scripts\18_gse299193_xenium_validation.py`.
- If validated, add Fig. 6 and update manuscript text.

MMRF plan preserved:

- If MMRF Virtual Lab / Researcher Gateway approval arrives later, download fuller clinical files to `external_bulk\CoMMpass_full_clinical`.
- Run `scripts\16_commppass_full_clinical_validation.py`.
- Use any valid R-ISS/PFS/cytogenetic high-risk/treatment-response fields as an optional enhanced clinical validation layer.

Planning report written:

- `reports\planning\Q2_NO_MMRF_MAINLINE_PLAN.md`

### 2026-04-29 Public CoMMpass NG2024 Supplement Added To Q2 Route

Question addressed:

- Whether public CoMMpass molecular and clinical annotation content from Skerget et al., Nature Genetics 2024 can strengthen the revised Q2 route after moving fuller MMRF clinical data to a future-enhancement track.

Source checked:

- Skerget et al., Nature Genetics 2024, "Comprehensive molecular profiling of multiple myeloma identifies refined copy number and expression subtypes."
- The article describes the CoMMpass cohort as 1,143 newly diagnosed MM patients with WGS/WES/RNA-seq and longitudinal clinical follow-up.
- The Nature Genetics article states that Supplementary Tables 1-7 are freely available and include patient features and molecular annotation resources.

Decision:

- Add a new public CoMMpass molecular-annotation validation line to the Q2 main route.
- This line should be attempted before waiting for controlled fuller MMRF approval because it is public, small-to-moderate in size for the highest-priority tables, and directly relevant to cytogenetic / copy-number / expression-subtype annotation.

Updated Q2 route:

1. GSE269875 spatial discovery.
2. GSE271107 single-cell localization.
3. GSE24080/GSE2658 bulk validation.
4. CoMMpass/GDC open OS and ISS validation.
5. Skerget et al. Nature Genetics 2024 public CoMMpass molecular-annotation validation.
6. GSE299193 second public spatial validation.
7. Fuller MMRF clinical access only as future enhancement for PFS, R-ISS and treatment-response endpoints.

What the public NG2024 supplement may add:

- ISS and baseline laboratory context.
- Copy-number calls including 1q21, 17p13 and 13q14.
- Cytogenetic high-risk annotation.
- RNA expression subtype labels.
- Mutation and structural-event annotation if larger tables are parsed.
- Expression subtype classifier output.

Claim boundary:

- These files may support molecular-risk and subtype validation if IDs match the current CoMMpass/GDC score table.
- They do not automatically complete PFS, treatment-response, best-overall-response, or therapy-line validation.
- Those endpoints remain assigned to the fuller MMRF / CoMMpass clinical access plan.

Next planned script:

- `scripts\19_skerget_ng2024_public_supplement_audit.py`

Planned outputs:

- `external_bulk\Skerget_NG2024_CoMMpass_public_supplement`
- `analysis\skerget_ng2024_public_supplement`
- `reports\validation\SKERGET_NG2024_PUBLIC_SUPPLEMENT_AUDIT.md`

Files updated:

- `reports\planning\Q2_NO_MMRF_MAINLINE_PLAN.md`
- `reports\planning\PUBLIC_COMMPASS_NG2024_SUPPLEMENT_PLAN.md`
- `reports\planning\REMAINING_GAPS_STATUS_AUDIT.md`
- `reports\REPORT_INDEX.md`
- `README_PROJECT_STRUCTURE.md`
- `PROJECT_LOG.md`

### 2026-04-30 Skerget NG2024 Public CoMMpass Supplement Download And Validation

Purpose:

- Execute the newly added public CoMMpass molecular-annotation route.
- Use Skerget et al., Nature Genetics 2024 public supplementary tables as a substitute for the missing controlled molecular/cytogenetic part of fuller MMRF access.

Scripts added:

- `scripts\19_skerget_ng2024_public_supplement_audit.py`
- `scripts\20_skerget_ng2024_molecular_annotation_validation.py`

Downloaded public supplementary files:

- Supplementary Table 1: individual patient features and data dictionary, 0.68 MB.
- Supplementary Table 2: somatic SNV/INDEL events, 71.3 MB.
- Supplementary Table 3: somatic structural events, 8.39 MB.
- Supplementary Table 4: expression and fusion matrix, 206.5 MB.
- Supplementary Table 5: copy-number and allele-frequency matrix, 490.4 MB.
- Supplementary Table 6: gene-level LOF/GOF states, 48.1 MB.
- Supplementary Table 7: gene-expression subtype classifier results, 0.11 MB.

Download directory:

- `external_bulk\Skerget_NG2024_CoMMpass_public_supplement`

Audit outputs:

- `analysis\skerget_ng2024_public_supplement\download_manifest.tsv`
- `analysis\skerget_ng2024_public_supplement\workbook_inventory.tsv`
- `analysis\skerget_ng2024_public_supplement\id_match_summary.tsv`
- `reports\validation\SKERGET_NG2024_PUBLIC_SUPPLEMENT_AUDIT.md`

ID matching result:

- Table 1 `Patient_ID` matched 762/762 local CoMMpass/GDC samples.
- Table 7 RNA subtype predictions matched 707 local CoMMpass/GDC samples.
- This confirms that the public NG2024 tables can be directly joined to the current CoMMpass score table.

Molecular annotation validation outputs:

- `analysis\skerget_ng2024_public_supplement\commppass_scores_with_ng2024_annotations.tsv`
- `analysis\skerget_ng2024_public_supplement\ng2024_molecular_annotation_associations.tsv`
- `analysis\skerget_ng2024_public_supplement\ng2024_molecular_annotation_fdr_ranked.tsv`
- `analysis\skerget_ng2024_public_supplement\ng2024_top_molecular_annotation_associations.png`
- `analysis\skerget_ng2024_public_supplement\ng2024_key_molecular_annotation_boxplots.png`
- `reports\validation\SKERGET_NG2024_MOLECULAR_ANNOTATION_VALIDATION_REPORT.md`

First-pass key results:

- RNA subtype strongly associates with the current plasma-secretory / clinical subtype axis:
  - `RNA_Subtype_Name` vs `JCHAIN_z`: FDR `2.43e-23`.
  - `RNA_Subtype_Name` vs `clinical_subtype_module_score_z`: FDR `8.93e-21`.
  - PR subtype probability vs `plasma_secretory_score_z`: Spearman rho `0.3399`, FDR `5.43e-19`.
  - `RNA_Subtype_Name` vs `plasma_secretory_score_z`: FDR `1.09e-13`.
- Clinically relevant annotation support:
  - `Cp_1q21_Call` vs `plasma_secretory_score_z`: n `680`, delta `0.2676`, FDR `1.24e-05`.
  - `ISS_Stage` vs `plasma_secretory_score_z`: n `742`, rho `0.1319`, FDR `0.00138`.
  - `IMWG_Risk_Class` vs `plasma_secretory_score_z`: n `630`, rho `0.1342`, FDR `0.00287`.
  - `Cp_17p13_Call` vs `POU2AF1_z`: n `680`, delta `0.3367`, FDR `0.00532`.
  - `Cp_1q21_Call` vs `TXNDC5_z`: n `680`, delta `0.2310`, FDR `0.00843`.

Interpretation:

- The public NG2024 supplement is usable and materially improves the Q2 route.
- It gives the project a real public CoMMpass molecular-risk / expression-subtype annotation layer.
- This partly compensates for not having fuller MMRF clinical access.
- It still does not complete PFS, R-ISS, treatment-response, or therapy-line validation.

Current next priority:

- Integrate NG2024 molecular annotation validation into the manuscript evidence table and figure package.
- Then resume GSE299193 download for the second spatial validation.

File written:

- D:\二区\EXTERNAL_VALIDATION_ROADMAP.md

### 2026-04-30 GSE299193 Download Resumed And Spatial Sample Expansion Search

Purpose:

- Proceed with the external spatial-validation line before rewriting manuscript figures.
- Search for additional public MM spatial datasets that could supplement the small GSE269875 spatial discovery cohort.
- Keep claim boundaries clear: this action addresses the spatial sample-size weakness, not the separate clinical independent-prognosis/model-adjustment weakness.

Actions completed:

- Refreshed GSE299193 download status with `scripts\17_gse299193_download_status.py`.
- Refreshed the GSE299193 validation placeholder with `scripts\18_gse299193_xenium_validation.py`; validation is still blocked until the RAW tar is complete.
- Resumed the resumable background download through `scripts\start_gse299193_download.ps1`.
- Confirmed active background `curl.exe` process:
  - PID: `13468`.
  - Start time: `2026-04-30 12:23:48`.
- Confirmed the local partial file is actively growing:
  - Earlier status: `9,041,175,150` bytes.
  - Latest status at this log update: `13,411,607,150` bytes.
  - Completion: `16.3048%`.
  - Remaining: `64.116 GiB`.

Spatial sample expansion search result:

- `GSE299193` remains the highest-priority direct public validation dataset:
  - human MM bone marrow trephine spatial transcriptomics;
  - public GEO dataset;
  - disease-state breadth includes control / MGUS / smouldering myeloma / MM / relapsed MM;
  - expected RAW tar size is `82,255,360,000` bytes.
- `GSE284727` was identified as a backup public dataset:
  - useful to inspect later;
  - not yet confirmed as a clean public spatial-expression matrix;
  - currently should not replace GSE299193 in the main route.
- A Leukemia 2025 GeoMx/DSP daratumumab-resistance dataset was identified as optional future context:
  - small patient count;
  - treatment-specific;
  - access may be controlled.
- A large ASH CODEX cohort was identified only as abstract/context evidence:
  - no confirmed public transcriptomic dataset;
  - not suitable for current analysis dependency.

Planning report added:

- `reports\planning\SPATIAL_SAMPLE_EXPANSION_SEARCH_2026-04-30.md`

Current decision:

- Continue GSE299193 as the direct solution for the spatial sample-size weakness.
- Do not present GSE284727 or GeoMx/CODEX as completed validation.
- After GSE299193 completes, run:
  - `python scripts\17_gse299193_download_status.py`
  - `python scripts\18_gse299193_xenium_validation.py`

Estimated download time at the observed log speed:

- Recent `curl` log shows approximately `7-9 MB/s`.
- If sustained, remaining download time is approximately `2-3 hours`.
- If NCBI FTP speed drops, this may extend substantially; the download is resumable.

### 2026-04-30 CoMMpass / NG2024 Adjusted Model Validation

Purpose:

- Continue work while GSE299193 downloads in the background.
- Address the reviewer concern that earlier CoMMpass/GDC clinical evidence was mostly univariate association evidence.
- Test whether the plasma-secretory axis remains associated with OS and public molecular-risk annotations after basic covariate adjustment.

Script added:

- `scripts\21_commppass_ng2024_adjusted_models.py`

Input:

- `analysis\skerget_ng2024_public_supplement\commppass_scores_with_ng2024_annotations.tsv`

Models completed:

- Cox proportional hazards:
  - OS ~ score + age + sex + ISS.
  - OS ~ score + age + sex + ISS + cytogenetic high-risk.
- Logistic regression:
  - ISS III ~ score + age + sex.
  - IMWG non-standard risk / cytogenetic high-risk / 1q21 / 17p13 ~ score + age + sex + ISS.
- Linear model:
  - PR RNA-subtype probability ~ score + age + sex + ISS.

Outputs:

- `analysis\commppass_ng2024_adjusted_models\commppass_ng2024_adjusted_model_results.tsv`
- `analysis\commppass_ng2024_adjusted_models\commppass_ng2024_adjusted_model_fdr_ranked.tsv`
- `analysis\commppass_ng2024_adjusted_models\commppass_ng2024_adjusted_model_forestplot.png`
- `analysis\commppass_ng2024_adjusted_models\commppass_ng2024_adjusted_model_forestplot.pdf`
- `reports\validation\COMMPASS_NG2024_ADJUSTED_MODEL_REPORT.md`

Key first-pass adjusted results:

- Completed adjusted models: `48`.
- FDR < 0.05 adjusted findings: `18`.
- Plasma-secretory score remained associated with PR RNA-subtype probability after age, sex and ISS adjustment:
  - beta `0.0941`, FDR `8.45e-09`, n `690`.
- Plasma-secretory score remained associated with 1q21 gain/amplification after age, sex and ISS adjustment:
  - OR `1.8725`, 95% CI `1.4085-2.4894`, FDR `1.89e-04`, n `660`.
- JCHAIN remained associated with OS after age, sex, ISS and cytogenetic high-risk adjustment:
  - HR `1.5257`, 95% CI `1.2303-1.8920`, FDR `0.0011`, n `630`.
- Plasma-secretory score remained associated with OS after age, sex and ISS adjustment:
  - HR `1.5571`, 95% CI `1.1772-2.0596`, FDR `0.0092`, n `742`.
- Plasma-secretory score also remained associated with OS after adding cytogenetic high-risk:
  - HR `1.5466`, 95% CI `1.1373-2.1034`, FDR `0.0218`, n `630`.

Interpretation:

- This materially strengthens the public-data Q2 route because the CoMMpass/NG2024 evidence is no longer limited to unadjusted association tables.
- It still cannot be written as PFS, R-ISS or treatment-response validation because those endpoints are not present in the current public/open tables.
- The correct manuscript wording is "covariate-adjusted association evidence", not "independent prospective prognostic biomarker" or "validated clinical test".

### 2026-04-30 Manuscript Integration, Requested 1q21 Cox Model, And Project Cleanup Review

Purpose:

- Slow, careful manuscript strengthening while GSE299193 downloads in the background.
- Repair NG2024 figure logic and integrate NG2024 evidence into manuscript-level outputs.
- Add the requested Cox model: OS ~ plasma-secretory score + age + sex + ISS + 1q21.
- Re-review the whole project and classify active, support, optional, historical, and non-evidence assets.

Scripts updated:

- `scripts\20_skerget_ng2024_molecular_annotation_validation.py`
  - Changed the NG2024 top-association plot to rank by `-log10(FDR)`.
  - Stopped plotting mixed raw effect metrics on one axis.
  - Replaced weaker key-boxplot pairings with supported molecular-risk pairs.
- `scripts\21_commppass_ng2024_adjusted_models.py`
  - Added Cox model with `Cp_1q21_Call` covariate.
  - Requested model now included for all score variables, including plasma-secretory score.
- `scripts\15_build_manuscript_figures.py`
  - Added NG2024 molecular annotation and adjusted-model inputs.
  - Added NG2024/adjusted-model rows to `cross_cohort_evidence_table.tsv`.
  - Updated Fig. 1 evidence-chain wording.
  - Expanded Fig. 5 to include CoMMpass/GDC, NG2024 1q21/RNA-subtype support, and adjusted models.

Manuscript files updated:

- `reports\manuscript\MANUSCRIPT_MAIN_TEXT_DRAFT.md`
- `reports\manuscript\MANUSCRIPT_RESULTS_SKELETON.md`
- `reports\manuscript\FIGURE_LEGENDS_DRAFT.md`
- `analysis\manuscript_figures\cross_cohort_evidence_table.tsv`
- `analysis\manuscript_figures\fig1_study_design_evidence_chain.*`
- `analysis\manuscript_figures\fig5_commppass_os_iss_validation.*`

Requested adjusted model result:

- Model: OS ~ plasma-secretory score + age + sex + ISS + 1q21.
- n `660`.
- OS events `128`.
- HR per 1 SD plasma-secretory score `1.4596`.
- 95% CI `1.0690-1.9928`.
- p `0.0173`.
- FDR `0.0445`.

Updated evidence table additions:

- NG2024 PR RNA-subtype probability vs plasma-secretory score:
  - Spearman rho `0.340`, FDR `5.43e-19`, n `707`.
- NG2024 1q21 gain/amplification vs plasma-secretory score:
  - median delta `0.268`, FDR `1.24e-05`, n `680`.
- NG2024 1q21 gain/amplification vs TXNDC5:
  - median delta `0.231`, FDR `0.00843`, n `680`.
- Adjusted OS model with age, sex, ISS and 1q21:
  - plasma-secretory score HR `1.460`, FDR `0.0445`, n `660`.

New project review / cleanup plan:

- `reports\planning\PROJECT_REVIEW_AND_CLEANUP_PLAN_2026-04-30.md`

Key review conclusion:

- The project remains viable for an SCI Q2 public-data bioinformatics / translational oncology route.
- The project is stronger than the previous review state because the stale-manuscript, NG2024-plotting, and unadjusted-only issues have been materially addressed.
- Submission should still wait for either GSE299193 validation or a clear decision to present GSE299193 as attempted/partial validation.

File classification completed:

- Active manuscript assets: current manuscript draft, figure legends, results skeleton, Fig. 1-5 and evidence table.
- Active analysis scripts: scripts `08-15`, `17-21`, plus `start_gse299193_download.ps1`.
- Support/provenance assets: scripts `01-07`, species-QC folders, references, blastdb, tools, SRA/FASTQ temporary folders.
- Future optional assets: fuller MMRF script/report and spatial expansion search plan.
- Historical/superseded planning: earlier complete/revised/roadmap reports and pilot runbook.
- Not-for-evidence assets: user-supplied MMRF-style audit and any pasted/roleplay-style tables not sourced from official files.

GSE299193 download note:

- During this work, the previous `curl` download was interrupted by the remote server:
  - `curl: (56) schannel: server closed abruptly`.
- The partial file was preserved and the resumable download was restarted.
- New active `curl.exe` PID: `31792`.
- Latest checked status after restart:
  - `17,932,137,110` bytes.
  - `16.701 GiB`.
  - `21.8006%`.
  - remaining `59.906 GiB`.

### 2026-04-30 GSE299193 Download Watchdog

User requested continuous monitoring because they cannot keep chatting in this thread while the large GSE299193 file downloads.

Implemented:

- `scripts\monitor_gse299193_download.ps1`
  - Checks the partial tar size every 120 seconds.
  - Detects whether a `curl.exe` process is still downloading `GSE299193_RAW.tar`.
  - Automatically restarts resumable download if the remote server closes the connection or `curl` exits early.
  - Refreshes `reports\validation\GSE299193_XENIUM_DOWNLOAD_STATUS.md`.
  - Writes heartbeat status to `reports\validation\GSE299193_DOWNLOAD_WATCHDOG.md`.
- `scripts\start_gse299193_monitor.ps1`
  - Starts the watchdog as a hidden background PowerShell process.
  - Avoids duplicate watchdog instances.

Latest watchdog-confirmed status:

- Watchdog PID: `1048`.
- Active `curl.exe` PID: `16296`.
- Downloaded: `24,481,474,724` bytes / `22.8 GiB`.
- Percent complete: `29.7628%`.
- Remaining: `53.806 GiB`.

Important operational note:

- NCBI has already closed the connection multiple times.
- This is expected for a very large FTP/HTTPS transfer and does not invalidate the partial file.
- The watchdog is now responsible for automatic resume until the expected size `82,255,360,000` bytes is reached.

### 2026-04-30 GSE299193 Completed Download And Xenium Validation

User reported that the GSE299193 download had completed. Verification confirmed:

- `GSE299193_RAW.tar` expected bytes: `82,255,360,000`.
- Current bytes: `82,255,360,000`.
- Status: `100%`, complete.

Validation performed:

- Updated `scripts\18_gse299193_xenium_validation.py` to avoid unnecessary extraction of large transcript and morphology files.
- Extracted only sample-level `*_cell_feature_matrix.h5` and lightweight `*_cells.csv.gz` files.
- Fixed matrix discovery to match GSE299193 file naming pattern: `*cell_feature_matrix.h5`.
- Analyzed 22 Xenium sample matrices:
  - Ctrl: 4.
  - MGUS: 2.
  - SM: 5.
  - MM: 10.
  - RM: 1.

Primary GSE299193 results:

- Active MM/RM vs Ctrl/MGUS/SM:
  - `plasma_secretory_score_z`: median delta `0.766`, Mann-Whitney p `0.000182`, FDR `0.000575`, n `11/11`.
  - `clinical_module_score_z` / panel-covered `POU2AF1/XBP1` module: median delta `1.068`, p `0.000287`, FDR `0.000575`, n `10/11`.
  - `XBP1_mean_log1p`: median delta `0.257`, FDR `0.000575`, n `10/11`.
  - `POU2AF1_mean_log1p`: median delta `0.210`, FDR `0.00123`, n `10/11`.

Panel limitation:

- Present in extracted Xenium matrices:
  - `MZB1`, `TNFRSF17`, `SLAMF7`, `IRF4`, `PIM2`, `POU2AF1`, `XBP1`.
- Absent from extracted Xenium matrices:
  - `TXNDC5`, `JCHAIN`, `SDC1`.
- Interpretation:
  - GSE299193 is valid as second spatial program-level validation.
  - GSE299193 must not be claimed as direct TXNDC5/JCHAIN validation.

Outputs created or updated:

- `reports\validation\GSE299193_XENIUM_VALIDATION_REPORT.md`
- `analysis\gse299193_xenium_validation\gse299193_sample_axis_scores.tsv`
- `analysis\gse299193_xenium_validation\gse299193_axis_group_associations.tsv`
- `analysis\gse299193_xenium_validation\gse299193_xenium_axis_validation.*`
- `analysis\manuscript_figures\fig6_gse299193_xenium_spatial_validation.*`
- `analysis\manuscript_figures\cross_cohort_evidence_table.tsv`
- `reports\manuscript\MANUSCRIPT_MAIN_TEXT_DRAFT.md`
- `reports\manuscript\FIGURE_LEGENDS_DRAFT.md`
- `reports\manuscript\MANUSCRIPT_RESULTS_SKELETON.md`
- `reports\planning\PROJECT_REVIEW_AND_CLEANUP_PLAN_2026-04-30.md`
- `reports\planning\Q2_NO_MMRF_MAINLINE_PLAN.md`

Updated project judgment:

- The previous major hard point, "lack of a second spatial validation cohort", is now materially resolved.
- The paper is stronger for an SCI Q2 public-data translational bioinformatics route.
- Remaining work is now mainly manuscript quality control:
  - formal citation verification;
  - final figure polishing;
  - claim-boundary audit;
  - deciding whether Fig. 6 is main or supplemental;
  - optional fuller MMRF clinical validation if access is approved later.

### 2026-04-30 Academic Pipeline Stage 2 Writing Pass

User invoked the academic-paper, academic-pipeline, academic-paper-reviewer, and nature-polishing skills for the next writing stage.

Skill availability:

- Loaded:
  - `academic-paper`
  - `academic-pipeline`
  - `academic-paper-reviewer`
- Not available in current session:
  - `nature-polishing`
- Fallback:
  - used high-impact primary research writing conventions already captured in manuscript/figure-format notes, without claiming that the unavailable skill was loaded.

Pipeline interpretation:

- Current stage: Stage 2 WRITE.
- Research and analysis materials already exist.
- Immediate task: polish the manuscript for a Q2 bioinformatics/translational oncology route, then run a pre-submission review roadmap.
- Citation verification is treated as the next Stage 2.5 integrity gate, not as completed in this writing pass.

Outputs created:

- `reports\manuscript\MANUSCRIPT_MAIN_TEXT_Q2_POLISHED_PASS1.md`
  - Q2-oriented rewritten manuscript pass.
  - Integrates GSE299193 as independent second spatial program-level validation.
  - Keeps TXNDC5 as a spatial/single-cell localization candidate rather than a standalone prognostic marker.
  - Keeps PFS, treatment response, definitive R-ISS, and direct GSE299193 TXNDC5/JCHAIN/SDC1 validation outside completed claims.
- `reports\review\PRE_SUBMISSION_REVIEW_ROADMAP_2026-04-30.md`
  - Simulated pre-submission review roadmap.
  - Current simulated decision: major revision before submission.
  - Blocking issues:
    - formal citation integrity;
    - more reproducible Methods detail;
    - panel-specific GSE299193 framing;
    - conservative TXNDC5 language;
    - manuscript-ready evidence table.

Updated:

- `reports\REPORT_INDEX.md`

Next recommended stage:

- Stage 2.5 integrity verification:
  - verify all references and dataset citations from primary sources;
  - add reproducibility details to Methods;
  - convert the evidence table into a manuscript-ready table;
  - expand figure legends panel by panel.

### 2026-04-30 Academic Pipeline Stage 2.5 Numeric Integrity Check

User invoked:

- `academic-paper`
- `academic-pipeline`
- `academic-paper-reviewer`
- `nature-polishing`

Correction to the previous log entry:

- The earlier entry recorded `nature-polishing` as unavailable.
- In this run, the skill file was found and loaded from `C:\Users\jz\.codex\skills\nature-polishing\SKILL.md`.
- The new Stage 2 polished draft should therefore be treated as using the named writing-polish workflow.

Files confirmed:

- `reports\manuscript\MANUSCRIPT_STAGE2_POLISHED_Q2_DRAFT.md`
- `reports\manuscript\CITATION_VERIFICATION_STAGE2.md`
- `reports\review\STAGE2_INTERNAL_REVIEW_AND_NEXT_REVISION_PLAN.md`

Numeric integrity check performed:

- Compared the manuscript's key numeric claims against local result TSV files.
- Checked GSE269875 spatial discovery statistics.
- Checked GSE299193 Xenium sample counts and MM/RM versus Ctrl/MGUS/SM statistics.
- Checked GSE271107 TXNDC5 plasma-cell expression summary.
- Checked GSE2658 and GSE24080 external bulk validation results.
- Checked CoMMpass/GDC OS and ISS associations.
- Checked NG2024 molecular annotation associations.
- Checked adjusted CoMMpass/NG2024 Cox models.

Result:

- No fatal numeric mismatch was found for the main manuscript claims.
- Current status is "pass with revision notes".

Main remaining cautions:

- The current manuscript still has a Methods Summary rather than a full reproducibility-grade Methods section.
- GSE299193 must be framed as program-level validation because TXNDC5, JCHAIN, and SDC1 are absent from the extracted Xenium matrices.
- NG2024 Table 7 overlap should be explained as complete-case n `707` in association tests, despite a larger pre-filter ID overlap in the audit table.
- External bulk results should be described as associations, not as uniform directional replication.
- References still need final target-journal formatting and source verification.

Output created:

- `reports\review\STAGE2_NUMERIC_INTEGRITY_CHECK_2026-04-30.md`

Updated:

- `reports\REPORT_INDEX.md`

Additional Stage 2.5 manuscript work:

- Expanded `reports\manuscript\MANUSCRIPT_STAGE2_POLISHED_Q2_DRAFT.md` from a Methods Summary into a reproducibility-grade Methods section.
- Added software versions:
  - Python 3.13.9.
  - pandas 2.3.3.
  - numpy 2.3.5.
  - scipy 1.16.3.
  - matplotlib 3.10.6.
  - scanpy 1.12.
  - seaborn 0.13.2.
  - statsmodels 0.14.5.
  - h5py 3.15.1.
- Added exact script paths for spatial discovery, Xenium validation, single-cell localization, bulk validation, CoMMpass/GDC validation, NG2024 annotation, adjusted modeling, and figure generation.
- Created `reports\manuscript\FIGURE_REPRODUCIBILITY_TABLE_STAGE2.md`.
- The reproducibility table links each Fig. 1-6 panel group to scripts, primary TSV outputs, and current claim boundaries.
- Ran a full internal review after Methods expansion.
- Created `reports\review\STAGE2_FULL_REVIEW_AFTER_METHODS_2026-04-30.md`.

Updated post-review judgment:

- Editorial decision remains major revision before submission.
- Q2 potential remains positive.
- Current estimated submission readiness is about `68%`.
- Fuller MMRF clinical access would strengthen the paper, but it is no longer required for the main public-data Q2 route.

Blocking items before submission:

- Finalize citations and reference style.
- Expand figure legends panel by panel.
- Add proportional hazards assumption status.
- Choose a target journal and adapt formatting.

Immediate fixes completed after review:

- Added a formal `Statistical analysis` subsection to `reports\manuscript\MANUSCRIPT_STAGE2_POLISHED_Q2_DRAFT.md`.
- Added plasma-cell abundance as an explicit limitation in the Discussion.
- Added a Cox model caveat that formal proportional hazards stress testing remains a presubmission check.
- Expanded `reports\manuscript\FIGURE_LEGENDS_DRAFT.md` into panel-level legends for Fig. 1-6.
- Corrected the Fig. 6 legend to use left/middle/right panel descriptions because the generated Fig. 6 does not currently carry A-C panel letters.

Next recommended stage:

- Convert the preliminary references into a formal target-journal bibliography.
- Select a target journal and adapt formatting.

### 2026-05-01 Cox PH Assumption Check

Added and ran:

- `scripts\22_commppass_cox_ph_assumption_check.py`

Method:

- Used statsmodels PHReg Schoenfeld residuals.
- Tested residual correlation with log(event time).
- Applied Benjamini-Hochberg FDR correction across tested covariate-level screens.

Primary results:

- Plasma-secretory score in OS adjusted for age, sex, ISS, 1q21:
  - n `660`, events `128`, rho `-0.0637`, p `0.4752`, FDR `0.7777`.
- POU2AF1/XBP1/JCHAIN module in OS adjusted for age, sex, ISS, 1q21:
  - n `660`, events `128`, rho `-0.0585`, p `0.5122`, FDR `0.7889`.

Interpretation:

- No FDR-significant PH-screen violation was detected for the two primary score terms.
- The 1q21 covariate showed a time-related residual signal and should be treated as a modeling caution.
- The manuscript language was updated to report Cox results as adjusted association models, not prospective prediction models.

Outputs:

- `analysis\commppass_cox_ph_assumption\commppass_cox_ph_schoenfeld_tests.tsv`
- `analysis\commppass_cox_ph_assumption\commppass_cox_ph_schoenfeld_score_residuals.png`
- `analysis\commppass_cox_ph_assumption\commppass_cox_ph_schoenfeld_score_residuals.pdf`
- `analysis\commppass_cox_ph_assumption\commppass_cox_ph_schoenfeld_score_residuals.svg`
- `reports\validation\COMMPASS_COX_PH_ASSUMPTION_CHECK.md`

### 2026-05-01 Reference Library And Target-Journal Adaptation

Reference collection:

- Added `scripts\23_collect_reference_library.py`.
- Created `references\REFERENCE_LIBRARY.tsv`.
- Created `references\REFERENCES_VANCOUVER_NUMBERED_DRAFT.md`.
- Created `references\downloaded_pdfs_manifest.tsv`.
- Downloaded open-access full-text PDFs into `references\pdf`.

Reference strategy:

- Use Vancouver / numbered biomedical style.
- Cite primary dataset resources directly for GEO and GDC.
- Cite Skerget et al. Nature Genetics 2024 for public CoMMpass molecular annotation.
- Cite Yip et al. Blood 2025 and GSE299193 separately because the analyzed GEO accession and related article must both be tracked.

Manuscript updates:

- Replaced the previous `Reference Anchors` section in `reports\manuscript\MANUSCRIPT_STAGE2_POLISHED_Q2_DRAFT.md` with a formal numbered reference list.
- Created `reports\manuscript\MANUSCRIPT_BMC_MEDICAL_GENOMICS_TARGET_DRAFT.md`.
- Created `reports\manuscript\TARGET_JOURNAL_ADAPTATION_BMC_MEDICAL_GENOMICS.md`.

Target-journal decision:

- Primary target is now BMC Medical Genomics.
- BMC Cancer is not the preferred first target because computational-only biomarker papers face higher validation-risk language there.
- The current paper should be framed as public-data medical-genomics integration, not as a finished biomarker-validation paper.

### 2026-05-01 Git Repository Setup

User requested a git/GitHub setup for `D:\二区`.

Findings:

- System-level `git` was not available in the current PowerShell PATH.
- `gh` GitHub CLI was not installed.
- `winget` was available, but system-level Git installation was cancelled by the UAC/admin installer flow.

Resolution:

- Downloaded PortableGit `2.54.0.windows.1` into `D:\二区\tools`.
- Extracted PortableGit to `D:\二区\tools\PortableGit`.
- Initialized a local git repository in `D:\二区`.
- Renamed the default branch to `main`.
- Added `.gitignore` to protect large raw data, reference genomes, SRA files, FASTQ files, H5 matrices, BLAST databases, local toolchains, and downloaded PDFs from accidental tracking.

Current git state:

- Local repository exists at `D:\二区\.git`.
- Remote GitHub repository was not created because `gh` is not available and no authenticated CLI token is present.
- No commit was made because git author name/email were not configured in this repository.

### 2026-05-01 GitHub Connector Recheck And Submission-Preparation Status

GitHub connector recheck:

- GitHub app authentication is active.
- Authenticated GitHub login: `1627626277-cyber`.
- Account email reported by the connector: `1627626277@qq.com`.
- GitHub app installation was detected for the user account.
- Repository listing returned zero accessible repositories.
- The connector exposes repository listing, file, branch, issue, and PR operations, but no create-new-repository operation is available in this session.

Repository action taken:

- Kept `D:\二区` as the local git repository.
- Kept current branch as `main`.
- Tightened `.gitignore` to exclude compressed intermediate result tables and run logs from version control.
- Created `reports\planning\GITHUB_REPOSITORY_SETUP_STATUS_2026-05-01.md`.
- Configured local git author information from the connected GitHub profile.
- Created initial local commit `93910dd` with message `Initial manuscript project snapshot`.

Current interpretation:

- GitHub is connected, but Codex cannot create the remote repository through the currently available connector tools.
- The practical next step is either manual creation of an empty GitHub repository under `1627626277-cyber`, or installation/authentication of GitHub CLI.
- Until a remote exists, the project is versioned locally on branch `main`.

Manuscript stage:

- The project has entered submission-preparation.
- This means manuscript, figures, references, model checks, and review files are being organized for target-journal upload.
- This does not mean the paper has already been submitted.

Submission-preparation assets currently available:

- `reports\manuscript\MANUSCRIPT_BMC_MEDICAL_GENOMICS_TARGET_DRAFT.md`
- `reports\manuscript\TARGET_JOURNAL_ADAPTATION_BMC_MEDICAL_GENOMICS.md`
- `reports\manuscript\SUBMISSION_PREP_CHECKLIST_BMC_MEDICAL_GENOMICS.md`
- `reports\manuscript\FIGURE_LEGENDS_DRAFT.md`
- `reports\manuscript\FIGURE_REPRODUCIBILITY_TABLE_STAGE2.md`
- `reports\review\STAGE2_NUMERIC_INTEGRITY_CHECK_2026-04-30.md`
- `reports\review\STAGE2_FULL_REVIEW_AFTER_METHODS_2026-04-30.md`
- `reports\validation\COMMPASS_COX_PH_ASSUMPTION_CHECK.md`
- `references\REFERENCE_LIBRARY.tsv`
- `references\REFERENCES_VANCOUVER_NUMBERED_DRAFT.md`

Main scientific position at this checkpoint:

- The no-MMRF public-data route remains feasible for an SCI Q2-style submission.
- The core claim is a spatially reproducible and clinically associated plasma-secretory program in multiple myeloma.
- GSE269875 provides spatial discovery.
- GSE299193 provides second spatial program-level validation.
- GSE271107 provides single-cell localization support.
- GSE24080/GSE2658 and CoMMpass/GDC provide bulk clinical association support.
- NG2024/Skerget public CoMMpass annotations strengthen molecular-risk and subtype interpretation.

Claim boundaries:

- Do not claim R-ISS, PFS, or treatment-response validation as completed.
- Do not claim GSE299193 directly validates TXNDC5 or JCHAIN, because those genes are absent from the analyzed Xenium panel.
- Do not describe the score as a prospective clinical classifier.

Remaining before actual submission:

- Finalize author information, affiliations, funding, conflict-of-interest, ethics, and data-availability statements.
- Decide main and supplementary figure packaging.
- Cross-check in-text citation numbering against the final reference list.
- Prepare cover letter.
- Upload through the selected journal portal after final quality control.

### 2026-05-01 Submission-Package Preparation Started

User created a GitHub repository intended as `二区`, then reported that the repository name was changed to `secondary`.

GitHub status:

- GitHub connector detected the updated target repository as `1627626277-cyber/secondary`.
- The repository display URL is `https://github.com/1627626277-cyber/secondary`.
- The local repository remote was updated to `https://github.com/1627626277-cyber/secondary.git`.
- Local non-interactive `git push` did not complete; the latest attempt failed with `Could not resolve host: github.com`.
- Through the GitHub connector, `README.md` was updated and `CODE_AVAILABILITY.md` was created in `1627626277-cyber/secondary`.
- This establishes the final intended code-availability URL, but full local repository push remains incomplete.

Submission-package work completed:

- Created `submission\bmc_medical_genomics_2026-05-01`.
- Created submission index, title-page draft, declarations draft, cover-letter draft, data/code availability draft, and editorial QC checklist.
- Added BMC-style Declarations to `reports\manuscript\MANUSCRIPT_BMC_MEDICAL_GENOMICS_TARGET_DRAFT.md`.
- Converted the abstract to the BMC Research Article structured format: Background, Methods, Results, Conclusions.
- Reordered main-text sections to the BMC-compatible sequence: Background, Methods, Results, Discussion, Conclusions.
- Added first-pass in-text numbered citations to the manuscript.
- Completed stage-1 citation coverage audit: all 26 references are now cited at least once in the manuscript body.
- Reordered the manuscript reference list and in-text citation numbers according to Vancouver first-appearance order.
- Created `submission\bmc_medical_genomics_2026-05-01\CITATION_AUDIT_STAGE1.md`.
- Added reproducible formatting script `scripts\24_prepare_bmc_submission_package.py`.
- Generated editable DOCX manuscript:
  - `submission\bmc_medical_genomics_2026-05-01\MANUSCRIPT_BMC_MEDICAL_GENOMICS_SUBMISSION_DRAFT.docx`
- Generated editable DOCX cover letter:
  - `submission\bmc_medical_genomics_2026-05-01\COVER_LETTER_DRAFT.docx`
- Render-checked the DOCX files with the artifact-tool workflow.

Formatting status:

- Main manuscript DOCX uses one-inch margins, double spacing, page numbering, and Word line-numbering metadata.
- Page numbering rendered correctly.
- Line numbering should be confirmed in Word/WPS before upload because the artifact renderer did not visibly display line numbers.

Author and declaration status:

- Author English name set as `Zhuang Jiang`.
- Chinese name confirmed by user; manuscript English form set as `Zhuang Jiang`.
- Affiliation set as `Guangdong University of Petrochemical Technology (GDUPT), Maoming, Guangdong, China`.
- ORCID updated to `https://orcid.org/0009-0007-4388-5901`.
- Corresponding author email updated to `1627626277@qq.com`.
- Detailed postal correspondence address remains to be confirmed only if required by the journal portal.
- Funding statement set to no specific funding.
- Competing interests statement set to no competing interests.
- Single-author contribution draft added as `Z.J. conceived the study, designed the analysis strategy, curated public datasets, interpreted the results, prepared the manuscript, and approved the submitted version.`

Figure and table decision:

- Keep Fig. 6 as a main figure because it addresses the second-spatial-validation weakness.
- Keep the cross-cohort evidence table as main Table 1 because it summarizes the public-data evidence chain and claim boundaries.

Current submission stage:

- The project is now in active pre-submission preparation.
- It is not yet ready for journal upload until the detailed postal address if required, Word/WPS line-number confirmation, complete GitHub push or archive, DOI/URL live-link verification, final figure upload checks, and final portal metadata are completed.

### 2026-05-01 ORCID And Author Metadata Correction

User provided an ORCID screenshot for the author profile.

Confirmed author metadata:

- Manuscript name: `Zhuang Jiang`.
- Chinese name confirmed by user; manuscript English form: `Zhuang Jiang`.
- ORCID iD: `0009-0007-4388-5901`.
- ORCID URL: `https://orcid.org/0009-0007-4388-5901`.
- Corresponding author email: `1627626277@qq.com`.
- Manuscript affiliation remains `Guangdong University of Petrochemical Technology (GDUPT), Maoming, Guangdong, China`.

Corrections made:

- Updated title page author metadata.
- Updated cover-letter signature email.
- Updated editorial QC checklist.
- Updated submission-preparation checklist.
- Added `submission\bmc_medical_genomics_2026-05-01\AUTHOR_AND_ORCID_STATUS.md`.
- Corrected garbled project path text in the submission-package support files.
- Removed unintended Pandoc-generated oversized title blocks from the manuscript and cover-letter DOCX generation.
- Regenerated and render-checked the DOCX package after ORCID insertion.
- Added approximate manuscript word count excluding references: 2,819.
- Synchronized `references\REFERENCES_VANCOUVER_NUMBERED_DRAFT.md` to the final manuscript reference order.
- Added `submission\bmc_medical_genomics_2026-05-01\CITATION_AUDIT_STAGE2_FINAL.md`.
- Final numeric citation coverage and high-level claim-placement screen passed; DOI/URL live-link verification remains before upload.

Important external cleanup:

- The ORCID screenshot shows an employment entry as `Fo Guang Shan: Kaohsiung City, TW` with `master (GDUPT)`.
- This should not be used as the manuscript affiliation.
- If this was entered by mistake, it should be corrected directly on ORCID before final submission.

GitHub push status:

- Local commit `4de5be0` was created for the ORCID and final citation-preparation update.
- `git push -u origin main` timed out.
- A non-interactive connectivity check failed with `Failed to connect to github.com port 443`.
- Full local repository push remains pending because the local Git command cannot currently reach GitHub over HTTPS from this environment.

### 2026-05-01 Pre-Writing Planning And Journal Requirement Check

The project entered academic-pipeline Stage 2 writing planning for BMC Medical Genomics.

Official requirement conclusions:

- BMC Medical Genomics Research article title page requires full author names, institutional addresses, and corresponding-author indication.
- Therefore the address placeholder should not remain in the manuscript.
- The GDUPT Guandu campus official address was used for the manuscript title page: `Guangdong University of Petrochemical Technology (GDUPT), 139 Guandu 2nd Road, Maoming 525000, Guangdong, China`.
- BMC requires editable manuscript files, double-line spacing, line and page numbering, structured abstract, declarations, public data availability, and figure/table upload checks.

Planning file created:

- `reports\manuscript\PRE_WRITING_PLAN_BMC_MEDICAL_GENOMICS_2026-05-01.md`

Next writing focus:

- Results-first rewrite linked to Fig. 1-6 and Table 1.
- Methods tightening for reproducibility.
- Discussion limitation discipline.
- Final figure/table packaging and reviewer-style critique before final integrity verification.
