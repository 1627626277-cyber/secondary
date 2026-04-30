# Draft Figure Legends

## Figure 1

Cross-cohort study design and evidence chain.

The workflow starts with spatial discovery in GSE269875. It then tests independent spatial reproducibility in GSE299193 Xenium data. Single-cell localization is evaluated in GSE271107. External bulk support is evaluated in GSE24080 and GSE2658. Clinical and molecular validation uses MMRF-COMMPASS/GDC RNA-seq and public NG2024 CoMMpass annotations. The lower annotation summarizes the current claim boundary. The study supports a spatially reproducible and clinically associated program. It does not establish a prospective treatment-selection biomarker.

## Figure 2

Spatial discovery of the plasma-secretory program in GSE269875.

**A**, Sample-level plasma-secretory scores in MM and control bone marrow spatial samples. The comparison uses median difference, Cohen's d, and a Mann-Whitney test.

**B**, Effect-size ranking of curated spatial programs. Programs include plasma-secretory, myeloid-inflammatory, T/NK cytotoxic, stromal, endothelial, erythroid, and cycling signatures.

**C**, Candidate gene ranking within the spatial discovery analysis. Plasma-cell and secretory genes include XBP1, TXNDC5, POU2AF1, SDC1, MZB1, and JCHAIN.

## Figure 3

Single-cell localization of the plasma-secretory axis in GSE271107.

**A**, Candidate gene expression across marker-inferred cell types. Dot size represents detection fraction. Color represents mean log-normalized expression.

**B**, Plasma-secretory program localization across broad cell categories. Plasma-cell compartments show the strongest program enrichment.

**C**, Disease-stage trend summary for the axis. The plot provides localization support rather than a survival endpoint.

TXNDC5 is interpreted as a plasma-cell localization candidate. It is not treated as a standalone prognostic biomarker.

## Figure 4

External GEO bulk support for the clinical subtype axis.

**A**, Ranked association statistics from GSE24080 and GSE2658. The panel summarizes tested gene, module, cytogenetic, and outcome associations.

**B**, GSE2658 association between the POU2AF1/XBP1/JCHAIN clinical subtype module and FISH 1q21 amplification. The result is interpreted as an association, not as directional replication across every platform.

**C**, GSE24080 association between XBP1 and 24-month OS death. The analysis uses public milestone outcome annotation.

## Figure 5

CoMMpass/GDC clinical validation and public NG2024 molecular annotation.

**A**, CoMMpass/GDC association ranking for plasma-secretory and related gene scores. The cohort contains baseline visit-1 bone marrow CD138+ RNA-seq samples.

**B**, Plasma-secretory score distribution by OS event status. The comparison uses a Mann-Whitney test with FDR correction.

**C**, Median-split overall survival analysis. The survival comparison uses a log-rank test.

**D**, Adjusted CoMMpass/NG2024 models. Cox models estimate OS association after adjustment for age, sex, ISS, and 1q21.

**E**, NG2024 1q21 copy-number annotation association. Public CoMMpass molecular annotations are joined to local RNA-seq scores by patient identifier.

**F**, Public NG2024 molecular annotation summary. The panel links the axis to PR RNA subtype probability and molecular-risk features.

These analyses support adjusted association. They do not prove clinical utility.

## Figure 6

Independent GSE299193 Xenium spatial validation.

Left panel, sample-level plasma-secretory scores across Ctrl, MGUS, SM, MM, and RM groups. Active disease is defined as MM or RM.

Middle panel, panel-covered POU2AF1/XBP1 module scores across disease groups. The module is calculated only from genes present in the Xenium feature matrices.

Right panel, heatmap of axis genes covered by the Xenium panel. Covered genes include MZB1, TNFRSF17, SLAMF7, IRF4, PIM2, POU2AF1, and XBP1.

TXNDC5, JCHAIN, and SDC1 are absent from the extracted Xenium matrices. GSE299193 therefore validates the program-level spatial signal. It does not directly validate those absent genes.
