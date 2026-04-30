# GSE269875 Next Step: hMM1 Pilot

Target journal strategy: SCI Q2-leaning bioinformatics / translational medicine / tumor data-analysis journals.

## Current Decision

Proceed with a one-sample pilot before scaling to all 9 human mainline samples.

The correct first disease pilot is:

| Field | Value |
|---|---|
| GEO sample | GSM8329293 |
| Title | hMM1 |
| Role | Human MM pilot |
| SRA experiment | SRX24927515 |

Do not use `GSM8329291` as the MM pilot. It is `hHBM2`, a human healthy bone marrow sample.

## Why This Step Matters

This pilot addresses the first reviewer-critical weakness: whether the human spatial transcriptomics mainline is free from mouse contamination or metadata confusion. The project should not move to deconvolution until this check is reproducible.

## Files Created Here

- `gse269875_manifest_enriched.tsv`: enriched sample manifest generated from local SOFT metadata.
- `scripts/01_enrich_gse269875_manifest.py`: rebuilds the enriched manifest.
- `scripts/02_check_pilot_readiness.ps1`: checks disk, reference files, and required tools.
- `scripts/03_pilot_hMM1_species_qc_template.ps1`: template for prefetch, fasterq-dump, and hg38/mm10 mapping QC.

## Required Before Running Pilot

In the `ich_bioinfo` environment, these tools must exist:

- `prefetch`
- `fasterq-dump`
- `vdb-dump`
- `minimap2`
- `samtools`

The current environment check found `GEOparse` and `pandas`, but not the SRA/minimap2/samtools toolchain.

## Disk Rule

Keep at least 300 GiB free before running full `fasterq-dump` for a single sample. Current D drive free space was about 410.75 GiB, so the pilot is feasible if the same space remains available.

The template script uses:

```powershell
--temp D:\二区\tmp_fasterq
--disk-limit 300GB
--size-check only
```

This follows the sra-tools guidance that `fasterq-dump` may need substantial temporary space, with worst-case temporary usage up to about 10x the final output size depending on mode and input.

## Scale-Up Rule

After hMM1 passes:

1. Run the same QC for hHBM1 as a control pilot.
2. Run all remaining human mainline samples one at a time.
3. Do not keep all FASTQ files unless extra storage is available.
4. Record each sample in `species_filter_log.md`.

## Manuscript Boundary

All downstream claims should remain: public-data integration, trend support, robustness evidence, hypothesis generation. Do not claim paired validation, wet-lab validation, or mechanism closure.
