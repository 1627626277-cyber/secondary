# Revised Q2 Project Plan

Date: 2026-04-29

Target: SCI Q2 bioinformatics / translational medicine / tumor data-analysis journal

Working title:

Spatially derived bone marrow niche signatures in multiple myeloma with single-cell and clinical transcriptomic validation

## 1. Strategic decision

The project should no longer be framed as a first atlas or a simple reanalysis of `GSE269875`, because the original GSE269875 spatial transcriptomics study has already been published.

The revised publishable angle is:

1. Use `GSE269875` human Visium samples as the spatial discovery layer.
2. Derive sample-aware MM bone marrow niche signatures rather than spot-only marker lists.
3. Validate cell-type attribution with public MM single-cell RNA-seq.
4. Validate clinical relevance with bulk/clinical MM transcriptomic cohorts.
5. Optionally validate spatial localization in an independent Xenium/spatial dataset.

The central claim should be:

Spatially localized MM bone marrow niche programs can be identified from Visium data and supported by independent single-cell and clinical transcriptomic evidence.

## 2. Core research questions

Primary question:

- Which MM bone marrow spatial niches or gene programs are reproducible across human MM spatial samples and distinguish MM from healthy bone marrow?

Validation questions:

- Which cell types carry these spatially derived genes or signatures in independent MM single-cell datasets?
- Are the spatial signatures associated with disease stage, risk, survival, event-free survival, progression, or treatment response in public bulk/clinical MM cohorts?
- Do the strongest spatial signatures show similar localization or disease-stage trends in an independent spatial dataset?

## 3. Hypotheses

H1. MM bone marrow sections contain reproducible plasma-cell-rich, immune/inflammatory, and stromal-remodeling spatial programs.

H2. A subset of spatially enriched genes can be assigned to interpretable cell states, including malignant plasma cells, inflammatory myeloid cells, exhausted T/NK cells, stromal/MSC-like cells, endothelial cells, and erythroid/megakaryocyte compartments.

H3. A compact spatial-niche signature has measurable clinical relevance in independent MM bulk transcriptomic cohorts.

H4. Not every canonical plasma-cell marker is publishable as a novel finding; novelty should come from spatial organization, cross-dataset validation, and clinical association.

## 4. Data architecture

### Discovery layer

- Dataset: `GSE269875`
- Local status: available in `D:\二区`
- Human samples: 3 healthy bone marrow controls and 6 MM bone marrow samples
- Current status:
  - 9/9 human samples passed sampled species QC.
  - Processed spatial matrices are available.
  - Initial matrix QC and exploratory clustering are complete.

### Single-cell validation layer

Priority datasets:

- `GSE223060`: large MM bone marrow mononuclear-cell scRNA-seq reference.
- `GSE271107`: healthy donor / MGUS / SMM / newly diagnosed MM scRNA-seq progression reference.

Use:

- Validate candidate gene cell-type specificity.
- Confirm whether spatial signatures map to plasma cells, immune cells, stromal cells, endothelial cells, or mixed microenvironment states.
- Avoid over-forced integration at the beginning; use marker-level and pseudobulk validation first.

### Bulk / clinical validation layer

Priority datasets:

- Fast route: `GSE24080` and `GSE2658` for MM expression and outcome-linked validation.
- Strong route: MMRF CoMMpass for RNA-seq plus richer clinical metadata.

Use:

- Build one to three spatially derived scores.
- Test association with survival, event-free survival, disease stage, risk, and response variables where available.
- Use clinical validation as a core paper-strengthening step, not as optional decoration.

### Optional external spatial layer

Candidate:

- `GSE299193`: human bone marrow trephine Xenium spatial transcriptomics.

Use:

- Validate only a short candidate signature or localization pattern.
- Do not make it the first dependency because it is larger and platform compatibility is more complex.

## 5. Analysis modules

### Module A: sample-aware spatial discovery

Goal:

- Convert the current exploratory spot-level clustering into manuscript-grade sample-aware evidence.

Tasks:

- Recompute per-sample QC summaries and identify analysis inclusion tiers.
- Label broad spatial programs using marker modules:
  - plasma-cell / MM load,
  - immune / T-NK,
  - myeloid / inflammatory,
  - stromal / ECM,
  - endothelial / angiogenic,
  - erythroid / megakaryocyte,
  - stress / secretory / unfolded-protein-response.
- Create per-sample and per-region pseudobulk matrices.
- Compare MM vs control using sample-level or region-level summaries.
- Run sensitivity analyses:
  - all samples,
  - excluding low-spot hMM1,
  - excluding low-depth samples,
  - hMM2/hMM3-only strong-depth subset as a stability check.

Outputs:

- sample-aware candidate gene table,
- sample-by-region signature matrix,
- sensitivity table,
- spatial maps for the strongest signatures,
- revised figure-ready UMAP/spatial panels.

### Module B: candidate ranking

Goal:

- Produce a defensible shortlist for external validation.

Candidate scoring criteria:

- spatial enrichment strength,
- MM-vs-control effect size,
- cross-sample consistency,
- not purely driven by one patient/sample,
- interpretable cell-type source,
- detectable in scRNA and bulk datasets,
- potential clinical association,
- not merely a generic immunoglobulin/plasma-cell marker.

Expected candidate groups:

- Plasma-cell stress/secretory program: examples may include `XBP1`, `MZB1`, `TXNDC5`, `JCHAIN`, `TNFRSF17`, `PIM2`.
- Myeloid/inflammatory niche: examples may include `S100A8`, `S100A9`, `LYZ`, `CXCL8` if detected.
- Stromal/ECM remodeling niche: examples may include `COL1A1`, `COL3A1`, `CXCL12`, stromal activation genes.
- Immune suppression/exhaustion niche: candidate genes depend on robust detection and scRNA support.

Rule:

- Individual canonical genes are not enough. The manuscript should emphasize compact signatures and spatial niche programs.

### Module C: single-cell validation

Goal:

- Prove that spatial candidates have plausible cellular origin and disease-state relevance.

Tasks:

- Download processed scRNA datasets where available.
- Build or use major cell-type labels.
- Score spatial signatures in single-cell data.
- Validate candidate expression by cell type and disease stage.
- Use pseudobulk by sample/cell type where metadata permits.

Outputs:

- dot plot of candidate genes by cell type,
- heatmap of signature activity by cell type,
- disease-stage signature trend if GSE271107 metadata supports it,
- scRNA-based interpretation table.

### Module D: bulk / clinical validation

Goal:

- Convert spatial biology into translational relevance.

Tasks:

- Build expression matrices and clinical metadata for the fast GEO bulk cohorts first.
- Score each spatial signature per patient.
- Test high-score vs low-score association with OS/EFS/PFS or available outcome variables.
- Test association with stage/risk variables when available.
- Use CoMMpass after the fast GEO proof-of-concept or when access is ready.

Outputs:

- Kaplan-Meier curves,
- Cox model or logistic/linear association table,
- forest plot across cohorts,
- final validated signature table.

### Module E: optional external spatial validation

Goal:

- Strengthen reviewer confidence that spatial localization is not GSE269875-specific.

Tasks:

- Only after a stable shortlist exists, evaluate GSE299193 availability and storage.
- Check whether candidate genes are included in the Xenium panel.
- Validate cell-neighborhood or stage-localization trends.

Outputs:

- external spatial validation map,
- concordance table between Visium discovery and Xenium validation,
- optional supplementary figure.

## 6. Expected manuscript results

Expected if the project succeeds:

1. A quality-controlled human MM bone marrow spatial discovery dataset.
2. A sample-aware map of MM-enriched spatial niches rather than only spot-level clusters.
3. Two or three compact spatial signatures, likely including:
   - MM plasma-cell stress/secretory signature,
   - inflammatory myeloid or immune-suppressed niche signature,
   - stromal/ECM remodeling signature.
4. scRNA validation showing which cell types carry each signature.
5. bulk/clinical validation showing at least one signature has disease-stage, risk, survival, or event-related association.
6. Optional independent spatial validation if GSE299193 is feasible.

Best-case paper story:

- MM bone marrow contains spatially organized plasma-cell-rich and inflammatory/stromal niches.
- These niches can be reduced to compact transcriptomic signatures.
- The signatures are traceable to specific cell states in scRNA data.
- At least one signature is clinically relevant in independent MM cohorts.

Realistic paper story:

- A rigorous reanalysis of public MM spatial transcriptomics identifies sample-aware spatial niche programs.
- Independent scRNA and bulk validation support biological interpretation and translational relevance.
- The work provides reusable candidate signatures and a reproducible analysis framework.

Fallback paper story:

- If clinical survival associations are weak, the project can still become a spatial-to-single-cell validation paper, but Q2 competitiveness will be lower.

## 7. Immediate next step

The next computation should be Module A and Module B:

1. Build sample-aware pseudobulk summaries from the current GSE269875 human matrices.
2. Quantify region/signature activity per sample.
3. Rank candidate genes/signatures using cross-sample consistency and sensitivity checks.
4. Produce `candidate_spatial_signature_table.tsv`.

Estimated local runtime:

- Script development and first run: 1 to 2 hours.
- Matrix computation itself: usually under 30 minutes because processed matrices are already local.
- QC review and report writing: 1 to 2 hours.

Expected output files:

- `analysis/spatial_candidate_signatures/sample_region_pseudobulk.tsv.gz`
- `analysis/spatial_candidate_signatures/sample_signature_scores.tsv`
- `analysis/spatial_candidate_signatures/candidate_spatial_signature_table.tsv`
- `SPATIAL_SIGNATURE_DISCOVERY_REPORT.md`

## 8. Project-level timeline estimate

If downloads are stable and processed data are available:

- Phase 1: sample-aware spatial signature discovery: 0.5 to 1 day.
- Phase 2: single-cell validation: 1 to 3 days depending dataset format and metadata.
- Phase 3: GEO bulk clinical validation: 1 to 2 days.
- Phase 4: CoMMpass validation: 2 to 7 days depending access and data retrieval.
- Phase 5: optional GSE299193 spatial validation: 2 to 5 days after candidate shortlist.
- Phase 6: manuscript-grade figures and draft results section: 2 to 4 days after main analyses stabilize.

Practical expectation:

- A strong internal analysis package can be built in several days.
- A manuscript-grade SCI Q2 submission package will likely require 1 to 3 weeks of iterative analysis, validation, figure cleanup, and writing.

## 9. Decision gates

Continue strongly if:

- at least one nontrivial spatial signature is consistent across multiple MM samples,
- scRNA validation assigns the signature to plausible MM microenvironment cell types,
- at least one bulk/clinical cohort shows disease-stage, risk, survival, or event association.

Continue with reduced ambition if:

- spatial and scRNA validation are solid but clinical association is weak.

Stop or redesign if:

- all candidate signals are driven by one sample,
- candidates are only generic immunoglobulin/plasma-cell markers,
- no external scRNA or bulk cohort supports the signatures.
