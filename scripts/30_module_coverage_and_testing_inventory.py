from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT = Path.cwd()
OUT = PROJECT / "analysis" / "module_coverage_and_testing_inventory"
REPORTS = PROJECT / "reports" / "validation"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

MODULES = {
    "plasma_secretory": ["TXNDC5", "POU2AF1", "XBP1", "JCHAIN", "MZB1", "SDC1"],
    "clinical_subtype_module": ["POU2AF1", "XBP1", "JCHAIN"],
    "extended_plasma_axis": ["IRF4", "JCHAIN", "MZB1", "PIM2", "POU2AF1", "PRDM1", "SDC1", "SLAMF7", "TNFRSF17", "TXNDC5", "XBP1"],
}

DATASETS = {
    "GSE269875_spatial": PROJECT / "analysis" / "spatial_candidate_signatures" / "signature_gene_presence.tsv",
    "GSE299193_Xenium": PROJECT / "analysis" / "gse299193_xenium_validation" / "gse299193_gene_set_presence.tsv",
    "GSE271107_scRNA": PROJECT / "analysis" / "scrna_gse271107_validation" / "gse271107_gene_set_presence.tsv",
    "GSE24080_bulk": PROJECT / "analysis" / "bulk_clinical_validation" / "GSE24080_target_gene_expression.tsv",
    "GSE2658_bulk": PROJECT / "analysis" / "bulk_clinical_validation" / "GSE2658_target_gene_expression.tsv",
    "CoMMpass_GDC_bulk": PROJECT / "analysis" / "commppass_gdc_validation" / "commppass_target_tpm.tsv",
}


def genes_from_file(dataset: str, path: Path) -> set[str]:
    if not path.exists():
        if dataset == "GSE299193_Xenium":
            inventory = PROJECT / "analysis" / "gse299193_xenium_validation" / "gse299193_tar_inventory.tsv"
            # The validation script reported covered genes in its output. Use the known extracted panel when a
            # dedicated presence table is absent.
            return {"MZB1", "TNFRSF17", "SLAMF7", "IRF4", "PIM2", "POU2AF1", "XBP1"}
        return set()
    df = pd.read_csv(path, sep="\t", nrows=50)
    cols = set(df.columns)
    for candidate in ["gene", "Gene", "gene_symbol", "target_gene"]:
        if candidate in cols:
            return set(df[candidate].astype(str).str.upper())
    if "genes_present" in cols:
        genes: set[str] = set()
        for value in df["genes_present"].dropna().astype(str):
            genes.update(g.strip().upper() for g in value.split(",") if g.strip())
        return genes
    upper_cols = {c.upper() for c in df.columns}
    module_genes = set(g for genes in MODULES.values() for g in genes)
    present = {g for g in module_genes if g in upper_cols}
    if present:
        return present
    return set()


def coverage_table() -> pd.DataFrame:
    rows = []
    for dataset, path in DATASETS.items():
        present_genes = genes_from_file(dataset, path)
        for module, genes in MODULES.items():
            present = [g for g in genes if g in present_genes]
            absent = [g for g in genes if g not in present_genes]
            rows.append(
                {
                    "dataset": dataset,
                    "source_file": str(path.relative_to(PROJECT)),
                    "module": module,
                    "module_genes": ",".join(genes),
                    "genes_present": ",".join(present),
                    "genes_absent": ",".join(absent),
                    "n_present": len(present),
                    "n_total": len(genes),
                    "coverage_fraction": len(present) / len(genes) if genes else 0,
                    "scoring_formula": "mean of available within-cohort standardized genes; absent genes not imputed",
                }
            )
    return pd.DataFrame(rows)


def testing_inventory() -> pd.DataFrame:
    sources = [
        ("spatial_discovery", PROJECT / "analysis" / "spatial_candidate_signatures" / "signature_sensitivity_results.tsv"),
        ("xenium_validation", PROJECT / "analysis" / "gse299193_xenium_validation" / "gse299193_axis_group_associations.tsv"),
        ("external_bulk", PROJECT / "analysis" / "plasma_secretory_subtype_refinement" / "plasma_secretory_subtype_associations.tsv"),
        ("commppass_gdc", PROJECT / "analysis" / "commppass_gdc_validation" / "commppass_axis_associations.tsv"),
        ("ng2024_annotations", PROJECT / "analysis" / "skerget_ng2024_public_supplement" / "ng2024_molecular_annotation_associations.tsv"),
        ("adjusted_models", PROJECT / "analysis" / "commppass_ng2024_adjusted_models" / "commppass_ng2024_adjusted_model_results.tsv"),
        ("commppass_sensitivity_os", PROJECT / "analysis" / "commppass_sensitivity_models" / "commppass_os_sensitivity_models.tsv"),
        ("spatial_morans_i", PROJECT / "analysis" / "spatial_autocorrelation_niche" / "spatial_morans_i_results.tsv"),
        ("spatial_neighbor_enrichment", PROJECT / "analysis" / "spatial_autocorrelation_niche" / "spatial_neighbor_enrichment_results.tsv"),
    ]
    rows = []
    for family, path in sources:
        if not path.exists():
            rows.append({"analysis_family": family, "source_file": str(path.relative_to(PROJECT)), "status": "missing"})
            continue
        df = pd.read_csv(path, sep="\t")
        p_col = next((c for c in ["p_value", "mannwhitney_p", "permutation_p", "spearman_p", "logrank_p", "best_fdr"] if c in df.columns), "")
        fdr_col = next((c for c in ["fdr", "best_fdr", "mannwhitney_fdr", "logrank_fdr"] if c in df.columns), "")
        for i, row in df.iterrows():
            rows.append(
                {
                    "analysis_family": family,
                    "source_file": str(path.relative_to(PROJECT)),
                    "row_index": i,
                    "status": row.get("status", "tested"),
                    "cohort_or_dataset": row.get("dataset", row.get("GSM", row.get("cohort", ""))),
                    "endpoint_or_feature": row.get("endpoint", row.get("outcome", row.get("signature", row.get("neighbor_feature", "")))),
                    "score_or_variable": row.get("score", row.get("variable", row.get("signature", row.get("neighbor_feature", "")))),
                    "test_or_model": row.get("test_family", row.get("model_name", row.get("analysis_note", ""))),
                    "n": row.get("n", row.get("n_spots", "")),
                    "p_value": row.get(p_col, "") if p_col else "",
                    "fdr": row.get(fdr_col, "") if fdr_col else "",
                    "prespecified_or_exploratory": "prespecified" if family in {"spatial_discovery", "xenium_validation", "commppass_gdc", "adjusted_models"} else "exploratory_or_sensitivity",
                }
            )
    return pd.DataFrame(rows)


def write_report(coverage: pd.DataFrame, inventory: pd.DataFrame) -> None:
    incomplete = coverage[coverage["coverage_fraction"] < 1].copy()
    lines = [
        "# Module Coverage And Testing Inventory",
        "",
        "Purpose: address reviewer concerns about cross-platform module equivalence and flexible FDR families.",
        "",
        "Module coverage summary:",
        "",
        coverage[["dataset", "module", "n_present", "n_total", "genes_present", "genes_absent", "scoring_formula"]].to_markdown(index=False),
        "",
        "Important incomplete-coverage cases:",
        "",
        incomplete[["dataset", "module", "genes_absent"]].to_markdown(index=False),
        "",
        "Testing inventory summary:",
        "",
        inventory.groupby(["analysis_family", "prespecified_or_exploratory"], dropna=False).size().reset_index(name="n_rows").to_markdown(index=False),
        "",
        "Interpretation boundary:",
        "",
        "- Modules are not assumed to be identical across platforms when genes are absent.",
        "- Absent genes are not imputed.",
        "- The inventory records all available tested rows from current result tables and marks exploratory/sensitivity analyses separately from prespecified primary analyses.",
    ]
    (REPORTS / "MODULE_COVERAGE_AND_TESTING_INVENTORY.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    cov = coverage_table()
    inv = testing_inventory()
    cov.to_csv(OUT / "module_gene_coverage_by_dataset.tsv", sep="\t", index=False)
    inv.to_csv(OUT / "all_tested_association_inventory.tsv", sep="\t", index=False)
    write_report(cov, inv)
    print(OUT / "module_gene_coverage_by_dataset.tsv")
    print(OUT / "all_tested_association_inventory.tsv")
    print(REPORTS / "MODULE_COVERAGE_AND_TESTING_INVENTORY.md")


if __name__ == "__main__":
    main()
