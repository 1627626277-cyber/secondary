# Figure Reproducibility Table

Date: 2026-04-30

Purpose:

- Link each manuscript figure to the generating script.
- Link each figure to the primary result tables used for claims.
- Support reviewer-facing reproducibility and internal audit.

## Figure-Level Traceability

| Figure | Main content | Generating script | Primary result files | Manuscript claim supported |
|---|---|---|---|---|
| Fig. 1 | Cross-cohort study design and evidence chain | `scripts/15_build_manuscript_figures.py` | `analysis/manuscript_figures/cross_cohort_evidence_table.tsv` | The study integrates spatial discovery, second spatial validation, single-cell localization, external bulk validation, CoMMpass/GDC validation, and NG2024 annotation. |
| Fig. 2 | GSE269875 spatial discovery | `scripts/10_sample_aware_spatial_signatures.py`; `scripts/15_build_manuscript_figures.py` | `analysis/spatial_candidate_signatures/sample_signature_scores.tsv`; `analysis/spatial_candidate_signatures/signature_sensitivity_results.tsv`; `analysis/manuscript_figures/cross_cohort_evidence_table.tsv` | The plasma-secretory program is enriched in MM bone marrow spatial samples. |
| Fig. 3 | GSE271107 single-cell localization | `scripts/11_gse271107_scrna_validation.py`; `scripts/15_build_manuscript_figures.py` | `analysis/scrna_gse271107_validation/gse271107_signature_by_celltype.tsv`; `analysis/scrna_gse271107_validation/gse271107_candidate_gene_by_sample_celltype.tsv`; `analysis/manuscript_figures/cross_cohort_evidence_table.tsv` | TXNDC5 and the plasma-secretory axis localize to marker-inferred plasma cells. |
| Fig. 4 | External GEO bulk support | `scripts/12_bulk_clinical_validation.py`; `scripts/13_plasma_secretory_subtype_refinement.py`; `scripts/15_build_manuscript_figures.py` | `analysis/plasma_secretory_subtype_refinement/plasma_secretory_subtype_fdr_ranked.tsv`; `analysis/plasma_secretory_subtype_refinement/plasma_secretory_subtype_effect_summary.tsv`; `analysis/bulk_clinical_validation/bulk_outcome_association_results.tsv` | The clinical subtype module is associated with 1q21 amplification, and XBP1 is associated with 24-month OS death. |
| Fig. 5 | CoMMpass/GDC and NG2024 validation | `scripts/14_commppass_gdc_validation.py`; `scripts/20_skerget_ng2024_molecular_annotation_validation.py`; `scripts/21_commppass_ng2024_adjusted_models.py`; `scripts/15_build_manuscript_figures.py` | `analysis/commppass_gdc_validation/commppass_axis_fdr_ranked.tsv`; `analysis/skerget_ng2024_public_supplement/ng2024_molecular_annotation_associations.tsv`; `analysis/commppass_ng2024_adjusted_models/commppass_ng2024_adjusted_model_results.tsv` | The plasma-secretory score is associated with OS, ISS, PR subtype probability, 1q21 status, and adjusted OS risk. |
| Fig. 6 | GSE299193 Xenium validation | `scripts/18_gse299193_xenium_validation.py`; `scripts/15_build_manuscript_figures.py` | `analysis/gse299193_xenium_validation/gse299193_sample_group_summary.tsv`; `analysis/gse299193_xenium_validation/gse299193_axis_group_associations.tsv`; `analysis/gse299193_xenium_validation/gse299193_sample_axis_scores.tsv` | The plasma-secretory program is independently higher in active MM/RM Xenium samples than Ctrl/MGUS/SM samples. |

## Output Files

| Figure | PNG | SVG | PDF |
|---|---|---|---|
| Fig. 1 | `analysis/manuscript_figures/fig1_study_design_evidence_chain.png` | `analysis/manuscript_figures/fig1_study_design_evidence_chain.svg` | `analysis/manuscript_figures/fig1_study_design_evidence_chain.pdf` |
| Fig. 2 | `analysis/manuscript_figures/fig2_spatial_plasma_secretory_discovery.png` | `analysis/manuscript_figures/fig2_spatial_plasma_secretory_discovery.svg` | `analysis/manuscript_figures/fig2_spatial_plasma_secretory_discovery.pdf` |
| Fig. 3 | `analysis/manuscript_figures/fig3_scrna_plasma_secretory_localization.png` | `analysis/manuscript_figures/fig3_scrna_plasma_secretory_localization.svg` | `analysis/manuscript_figures/fig3_scrna_plasma_secretory_localization.pdf` |
| Fig. 4 | `analysis/manuscript_figures/fig4_geo_bulk_clinical_support.png` | `analysis/manuscript_figures/fig4_geo_bulk_clinical_support.svg` | `analysis/manuscript_figures/fig4_geo_bulk_clinical_support.pdf` |
| Fig. 5 | `analysis/manuscript_figures/fig5_commppass_os_iss_validation.png` | `analysis/manuscript_figures/fig5_commppass_os_iss_validation.svg` | `analysis/manuscript_figures/fig5_commppass_os_iss_validation.pdf` |
| Fig. 6 | `analysis/manuscript_figures/fig6_gse299193_xenium_spatial_validation.png` | `analysis/manuscript_figures/fig6_gse299193_xenium_spatial_validation.svg` | `analysis/manuscript_figures/fig6_gse299193_xenium_spatial_validation.pdf` |

## Known Boundaries

1. Fig. 6 validates the program at panel level.

It does not directly validate TXNDC5, JCHAIN, or SDC1 because those genes are absent from the extracted GSE299193 Xenium matrices.

2. Fig. 4 should use association language.

The GSE2658 1q21 association is significant, but the direction is not identical to CoMMpass.

3. Fig. 5 supports adjusted association.

It does not prove prospective clinical utility.
