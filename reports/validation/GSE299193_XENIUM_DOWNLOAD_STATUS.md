# GSE299193 Xenium Download and Validation Status

Dataset:

- GEO accession: `GSE299193`.
- Title: Profiling the spatial architecture of multiple myeloma in human bone marrow trephines with spatial transcriptomics [human].
- Platform: Xenium In Situ Analyzer, Homo sapiens.
- RAW file: `GSE299193_RAW.tar`.
- Expected RAW size: 82,255,360,000 bytes / 76.61 GiB.

Sample groups from SOFT metadata:

- Ctrl: 4 sample(s), male=2, female=2.
- MGUS: 2 sample(s), male=1, female=1.
- MM: 10 sample(s), male=5, female=5.
- RM: 1 sample(s), male=1, female=0.
- SM: 5 sample(s), male=3, female=2.

Current download status:

- Current size: 82,255,360,000 bytes / 76.61 GiB.
- Percent complete: 100.0000%.
- Remaining: 0.00 GiB.

Planned validation after download:

- List tar contents and identify Xenium cell-feature matrices.
- Extract only matrix/metadata files required for expression scoring first.
- Compute `plasma_secretory`, `clinical_subtype_module`, and marker-level TXNDC5/POU2AF1/XBP1/JCHAIN signals.
- Compare disease groups: Ctrl/MGUS/SM vs MM/RM where sample counts allow.
- Add Fig. 6 or supplemental validation figure if the signal is usable.
