# GSE269875 Species Filter Log

## Current Rule

Human mainline candidates are retained only when GEO metadata identifies `Homo sapiens` on `GPL30173` and sequence-level sampled Magic-BLAST QC supports human-dominant mapping against hg38 versus mm10.

Mouse samples are isolated from the human mainline and must not be mixed into human downstream analyses.

## Completed Sequence QC

| GSM | Title | SRX | SRR | Role | QC status | Key evidence |
|---|---|---|---|---|---|---|
| GSM8329293 | hMM1 | SRX24927515 | SRR29414112 | human MM pilot | pass_human_sampled_magicblast | human-only 30.18%, mouse-only 0.10%, human-only/mouse-only 311.17 |
| GSM8329290 | hHBM1 | SRX24927512 | SRR29414117; SRR29414118 | human control pilot | pass_human_sampled_magicblast | aggregate human-only 79.29%, mouse-only 0.01%, human-only/mouse-only 12,686.61 |
| GSM8329291 | hHBM2 | SRX24927513 | SRR29414115; SRR29414116 | human control mainline | pass_human_sampled_magicblast | aggregate human-only 66.85%, mouse-only 0.32%, human-only/mouse-only 207.47 |
| GSM8329292 | hHBM3 | SRX24927514 | SRR29414113; SRR29414114 | human control mainline | pass_human_sampled_magicblast | aggregate human-only 70.24%, mouse-only 0.37%, human-only/mouse-only 192.31 |
| GSM8329294 | hMM2 | SRX24927516 | SRR29414110; SRR29414111 | human MM mainline | pass_human_sampled_magicblast | read 4 was 90 bp and trimmed to first 50 bp; aggregate human-only 10.80%, mouse-only 0.02%, human-only/mouse-only 451.09 |
| GSM8329295 | hMM3 | SRX24927517 | SRR29414109 | human MM mainline | pass_human_sampled_magicblast | aggregate human-only 54.84%, mouse-only 0.01%, human-only/mouse-only 6451.46 |
| GSM8329296 | hMM4 | SRX24927518 | SRR29414108 | human MM mainline | pass_human_sampled_magicblast | aggregate human-only 11.33%, mouse-only 0.01%, human-only/mouse-only 878.35 |
| GSM8329297 | hMM5 | SRX24927519 | SRR29414106; SRR29414107 | human MM mainline | pass_human_sampled_magicblast | read 4 was 90 bp and trimmed to first 50 bp; aggregate human-only 75.77%, mouse-only 0.02%, human-only/mouse-only 3678.04 |
| GSM8329298 | hMM6 | SRX24927520 | SRR29414105 | human MM mainline | pass_human_sampled_magicblast | aggregate human-only 21.20%, mouse-only 0.02%, human-only/mouse-only 1009.36 |

## Pending Human Mainline QC

All nine human mainline samples have completed sampled sequence-level species QC.

## Mouse-Isolated Samples

- GSM8329284 / YFP1 / Mus musculus / GPL30172
- GSM8329285 / YFP2 / Mus musculus / GPL30172
- GSM8329286 / MM1 / Mus musculus / GPL30172
- GSM8329287 / MM2 / Mus musculus / GPL30172
- GSM8329288 / MM3 / Mus musculus / GPL30172
- GSM8329289 / MM4 / Mus musculus / GPL30172

