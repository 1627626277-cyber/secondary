from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc
import seaborn as sns
from scipy.sparse import csr_matrix, issparse


PROJECT = Path.cwd()
DATA = PROJECT / "external_scRNA" / "GSE271107" / "raw_h5"
SPATIAL = PROJECT / "analysis" / "spatial_candidate_signatures"
OUT = PROJECT / "analysis" / "scrna_gse271107_validation"
OUT.mkdir(parents=True, exist_ok=True)

SIGNATURES = {
    "plasma_secretory": [
        "SDC1",
        "MZB1",
        "XBP1",
        "JCHAIN",
        "TNFRSF17",
        "SLAMF7",
        "PRDM1",
        "TXNDC5",
        "PIM2",
        "IRF4",
    ],
    "myeloid_inflammatory": ["LYZ", "LST1", "S100A8", "S100A9", "TYROBP", "FCGR3A", "FCN1", "CTSS", "CXCL8", "IL1B"],
    "t_nk_cytotoxic_exhaustion": [
        "CD3D",
        "CD3E",
        "TRAC",
        "NKG7",
        "GNLY",
        "GZMB",
        "PRF1",
        "PDCD1",
        "CTLA4",
        "LAG3",
        "TIGIT",
        "HAVCR2",
        "TOX",
    ],
    "stromal_ecm": ["COL1A1", "COL1A2", "COL3A1", "DCN", "LUM", "CXCL12", "VCAM1", "FN1", "SPARC", "POSTN"],
    "endothelial_angiogenic": ["PECAM1", "VWF", "KDR", "CLDN5", "ENG", "FLT1", "ESAM"],
    "erythroid_megak": ["HBB", "HBA1", "HBA2", "ALAS2", "PPBP", "PF4", "ITGA2B", "GP9"],
    "cycling_proliferation": ["MKI67", "TOP2A", "PCNA", "TYMS", "UBE2C", "BIRC5", "STMN1"],
}

CELL_MARKERS = {
    "plasma_cell": ["SDC1", "MZB1", "XBP1", "JCHAIN", "TNFRSF17", "SLAMF7", "IRF4", "PRDM1"],
    "b_cell": ["MS4A1", "CD79A", "CD79B", "CD19", "CD37", "BANK1"],
    "t_nk_cell": ["CD3D", "CD3E", "TRAC", "NKG7", "GNLY", "GZMB", "PRF1", "KLRD1"],
    "myeloid_cell": ["LYZ", "LST1", "S100A8", "S100A9", "FCGR3A", "TYROBP", "FCN1", "CTSS"],
    "erythroid_cell": ["HBB", "HBA1", "HBA2", "ALAS2", "AHSP"],
    "megakaryocyte_platelet": ["PPBP", "PF4", "ITGA2B", "GP9", "NRGN"],
    "stromal_like": ["COL1A1", "COL1A2", "COL3A1", "DCN", "LUM", "CXCL12", "VCAM1"],
    "endothelial_like": ["PECAM1", "VWF", "KDR", "CLDN5", "ENG", "FLT1", "ESAM"],
}

STAGE_ORDER = ["HD", "MGUS", "SMM", "MM"]


def parse_sample(path: Path) -> dict[str, str]:
    match = re.match(r"(GSM\d+)_(.+)\.h5$", path.name)
    if not match:
        raise ValueError(f"Unexpected H5 filename: {path.name}")
    gsm = match.group(1)
    sample = match.group(2)
    sample_upper = sample.upper()
    if sample_upper.startswith("HD"):
        stage = "HD"
    elif sample_upper.startswith("MGUS"):
        stage = "MGUS"
    elif sample_upper.startswith("SMM"):
        stage = "SMM"
    elif sample_upper.startswith("MM"):
        stage = "MM"
    else:
        stage = sample.split("_")[0]
    return {"GSM": gsm, "sample": sample, "stage": stage}


def as_csr(x) -> csr_matrix:
    if issparse(x):
        return x.tocsr()
    return csr_matrix(x)


def normalize_log1p(x: csr_matrix) -> csr_matrix:
    totals = np.asarray(x.sum(axis=1)).ravel()
    factors = np.divide(10000.0, totals, out=np.zeros_like(totals, dtype=float), where=totals > 0)
    y = x.multiply(factors[:, None]).tocsr()
    y.data = np.log1p(y.data)
    return y


def gene_index(symbols: list[str]) -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    for idx, symbol in enumerate(symbols):
        out.setdefault(symbol.upper(), []).append(idx)
    return out


def score_gene_set(x_log: csr_matrix, mapping: dict[str, list[int]], genes: list[str]) -> tuple[np.ndarray, list[str]]:
    idx: list[int] = []
    present: list[str] = []
    for gene in genes:
        found = mapping.get(gene.upper(), [])
        if found:
            idx.extend(found)
            present.append(gene)
    if not idx:
        return np.zeros(x_log.shape[0]), present
    return np.asarray(x_log[:, idx].mean(axis=1)).ravel(), present


def expression_summary(x_log: csr_matrix, mapping: dict[str, list[int]], genes: list[str]) -> pd.DataFrame:
    rows = []
    detected = x_log.copy()
    detected.data = np.ones_like(detected.data)
    for gene in genes:
        idx = mapping.get(gene.upper(), [])
        if not idx:
            rows.append({"gene": gene, "present": False, "mean_log_norm": 0.0, "pct_detected": 0.0})
            continue
        sub = x_log[:, idx]
        gene_expr = np.asarray(sub.mean(axis=1)).ravel()
        gene_det = np.asarray((sub > 0).max(axis=1).toarray()).ravel()
        rows.append(
            {
                "gene": gene,
                "present": True,
                "mean_log_norm": float(np.mean(gene_expr)),
                "pct_detected": float(np.mean(gene_det)),
            }
        )
    return pd.DataFrame(rows)


def load_candidate_genes() -> list[str]:
    path = SPATIAL / "candidate_validation_shortlist.tsv"
    if not path.exists():
        return sorted({gene for genes in SIGNATURES.values() for gene in genes})
    df = pd.read_csv(path, sep="\t")
    return df["gene"].dropna().astype(str).drop_duplicates().tolist()


def assign_cell_types(cell_score_df: pd.DataFrame) -> pd.Series:
    marker_cols = [f"{name}_marker_score" for name in CELL_MARKERS]
    max_col = cell_score_df[marker_cols].idxmax(axis=1)
    max_score = cell_score_df[marker_cols].max(axis=1)
    assigned = max_col.str.replace("_marker_score", "", regex=False)
    assigned = assigned.where(max_score >= 0.05, "low_marker")
    return assigned


def process_sample(path: Path, candidate_genes: list[str]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    info = parse_sample(path)
    adata = sc.read_10x_h5(path)
    symbols = [str(x) for x in adata.var_names]
    x_raw = as_csr(adata.X)
    total_counts = np.asarray(x_raw.sum(axis=1)).ravel()
    n_genes = np.asarray((x_raw > 0).sum(axis=1)).ravel()
    mt_mask = np.array([s.upper().startswith("MT-") for s in symbols])
    mt_counts = np.asarray(x_raw[:, mt_mask].sum(axis=1)).ravel() if mt_mask.any() else np.zeros(x_raw.shape[0])
    pct_mt = np.divide(mt_counts, total_counts, out=np.zeros_like(mt_counts, dtype=float), where=total_counts > 0) * 100
    keep = (n_genes >= 200) & (total_counts >= 500) & (pct_mt <= 25)
    x_raw = x_raw[keep].tocsr()
    total_counts = total_counts[keep]
    n_genes = n_genes[keep]
    pct_mt = pct_mt[keep]
    barcodes = np.asarray(adata.obs_names)[keep]
    x_log = normalize_log1p(x_raw)
    mapping = gene_index(symbols)

    cell = pd.DataFrame(
        {
            "GSM": info["GSM"],
            "sample": info["sample"],
            "stage": info["stage"],
            "barcode": barcodes,
            "total_counts": total_counts,
            "n_genes": n_genes,
            "pct_mt": pct_mt,
        }
    )
    presence_rows = []
    for name, genes in SIGNATURES.items():
        scores, present = score_gene_set(x_log, mapping, genes)
        cell[f"{name}_score"] = scores
        presence_rows.append(
            {
                "GSM": info["GSM"],
                "sample": info["sample"],
                "gene_set_type": "spatial_signature",
                "gene_set": name,
                "n_requested": len(genes),
                "n_present": len(present),
                "genes_present": ",".join(present),
            }
        )
    for name, genes in CELL_MARKERS.items():
        scores, present = score_gene_set(x_log, mapping, genes)
        cell[f"{name}_marker_score"] = scores
        presence_rows.append(
            {
                "GSM": info["GSM"],
                "sample": info["sample"],
                "gene_set_type": "cell_marker",
                "gene_set": name,
                "n_requested": len(genes),
                "n_present": len(present),
                "genes_present": ",".join(present),
            }
        )
    cell["marker_inferred_cell_type"] = assign_cell_types(cell)

    gene_summary = expression_summary(x_log, mapping, candidate_genes)
    gene_summary.insert(0, "stage", info["stage"])
    gene_summary.insert(0, "sample", info["sample"])
    gene_summary.insert(0, "GSM", info["GSM"])

    gene_by_type_parts = []
    for ctype, sub in cell.groupby("marker_inferred_cell_type"):
        if sub.shape[0] < 10:
            continue
        idx = sub.index.to_numpy()
        part = expression_summary(x_log[idx], mapping, candidate_genes)
        part.insert(0, "marker_inferred_cell_type", ctype)
        part.insert(0, "stage", info["stage"])
        part.insert(0, "sample", info["sample"])
        part.insert(0, "GSM", info["GSM"])
        part.insert(4, "n_cells", sub.shape[0])
        gene_by_type_parts.append(part)
    gene_by_type = pd.concat(gene_by_type_parts, ignore_index=True) if gene_by_type_parts else pd.DataFrame()

    sample_summary = {
        "GSM": info["GSM"],
        "sample": info["sample"],
        "stage": info["stage"],
        "cells_raw": int(adata.n_obs),
        "cells_after_qc": int(x_raw.shape[0]),
        "median_counts": float(np.median(total_counts)),
        "median_genes": float(np.median(n_genes)),
        "median_pct_mt": float(np.median(pct_mt)),
    }
    for col in [c for c in cell.columns if c.endswith("_score") and not c.endswith("_marker_score")]:
        sample_summary[f"median_{col}"] = float(cell[col].median())
    sample_summary_df = pd.DataFrame([sample_summary])

    return cell, pd.DataFrame(presence_rows), gene_summary, gene_by_type, sample_summary_df


def make_plots(cell: pd.DataFrame, gene_by_type: pd.DataFrame) -> None:
    score_cols = [c for c in cell.columns if c.endswith("_score") and not c.endswith("_marker_score")]
    stage_type = cell.groupby(["stage", "marker_inferred_cell_type"]).size().reset_index(name="cells")
    total = stage_type.groupby("stage")["cells"].transform("sum")
    stage_type["fraction"] = stage_type["cells"] / total
    pivot = stage_type.pivot(index="stage", columns="marker_inferred_cell_type", values="fraction").reindex(STAGE_ORDER).fillna(0)
    fig, ax = plt.subplots(figsize=(10, 4.8))
    pivot.plot(kind="bar", stacked=True, ax=ax, width=0.85)
    ax.set_ylabel("Cell fraction")
    ax.set_xlabel("")
    ax.set_title("GSE271107 marker-inferred cell composition")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "gse271107_celltype_composition_by_stage.png", dpi=180)
    plt.close(fig)

    score_summary = (
        cell.groupby("marker_inferred_cell_type")[score_cols]
        .median()
        .sort_values("plasma_secretory_score", ascending=False)
    )
    z = (score_summary - score_summary.mean(axis=0)) / score_summary.std(axis=0).replace(0, np.nan)
    z = z.fillna(0)
    fig, ax = plt.subplots(figsize=(10, 5.2))
    sns.heatmap(z, cmap="coolwarm", center=0, ax=ax, cbar_kws={"label": "column z-score"})
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("Spatial signature activity by marker-inferred cell type")
    fig.tight_layout()
    fig.savefig(OUT / "gse271107_signature_by_celltype_heatmap.png", dpi=180)
    plt.close(fig)

    stage_scores = cell.groupby("stage")[score_cols].median().reindex(STAGE_ORDER)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    stage_scores.plot(marker="o", ax=ax)
    ax.set_ylabel("Median score")
    ax.set_xlabel("")
    ax.set_title("Spatial signature activity by disease stage")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "gse271107_signature_by_stage.png", dpi=180)
    plt.close(fig)

    genes = [
        "TXNDC5",
        "PIM2",
        "TENT5C",
        "POU2AF1",
        "S100A8",
        "S100A9",
        "CTSS",
        "COL1A1",
        "COL3A1",
        "CXCL12",
        "PECAM1",
        "JCHAIN",
        "MZB1",
        "XBP1",
    ]
    dot = gene_by_type[gene_by_type["gene"].isin(genes)].copy()
    dot = dot.groupby(["marker_inferred_cell_type", "gene"], as_index=False).agg(
        mean_log_norm=("mean_log_norm", "mean"),
        pct_detected=("pct_detected", "mean"),
        n_cells=("n_cells", "sum"),
    )
    cell_order = (
        dot.groupby("marker_inferred_cell_type")["mean_log_norm"].sum().sort_values(ascending=False).index.tolist()
    )
    gene_order = [g for g in genes if g in set(dot["gene"])]
    x_map = {g: i for i, g in enumerate(gene_order)}
    y_map = {c: i for i, c in enumerate(cell_order)}
    dot["x"] = dot["gene"].map(x_map)
    dot["y"] = dot["marker_inferred_cell_type"].map(y_map)
    fig, ax = plt.subplots(figsize=(11, 5.8))
    sizes = 20 + dot["pct_detected"].clip(0, 1) * 420
    sca = ax.scatter(dot["x"], dot["y"], s=sizes, c=dot["mean_log_norm"], cmap="viridis", alpha=0.85)
    ax.set_xticks(range(len(gene_order)))
    ax.set_xticklabels(gene_order, rotation=45, ha="right")
    ax.set_yticks(range(len(cell_order)))
    ax.set_yticklabels(cell_order)
    ax.set_title("Candidate gene expression by marker-inferred cell type")
    ax.grid(alpha=0.15)
    fig.colorbar(sca, ax=ax, label="Mean log-normalized expression")
    fig.tight_layout()
    fig.savefig(OUT / "gse271107_candidate_gene_dotplot.png", dpi=180)
    plt.close(fig)


def main() -> None:
    candidate_genes = load_candidate_genes()
    h5_files = sorted(DATA.glob("*.h5"))
    if not h5_files:
        raise FileNotFoundError(f"No H5 files found in {DATA}")

    cell_parts = []
    presence_parts = []
    gene_parts = []
    gene_type_parts = []
    sample_summary_parts = []
    for path in h5_files:
        print(f"Processing {path.name}")
        cell, presence, gene_summary, gene_by_type, sample_summary = process_sample(path, candidate_genes)
        cell_parts.append(cell)
        presence_parts.append(presence)
        gene_parts.append(gene_summary)
        if not gene_by_type.empty:
            gene_type_parts.append(gene_by_type)
        sample_summary_parts.append(sample_summary)

    cell_df = pd.concat(cell_parts, ignore_index=True)
    presence_df = pd.concat(presence_parts, ignore_index=True)
    gene_df = pd.concat(gene_parts, ignore_index=True)
    gene_type_df = pd.concat(gene_type_parts, ignore_index=True) if gene_type_parts else pd.DataFrame()
    sample_summary_df = pd.concat(sample_summary_parts, ignore_index=True)

    cell_df.to_csv(OUT / "gse271107_cell_signature_scores.tsv.gz", sep="\t", index=False, compression="gzip")
    presence_df.to_csv(OUT / "gse271107_gene_set_presence.tsv", sep="\t", index=False)
    gene_df.to_csv(OUT / "gse271107_candidate_gene_by_sample.tsv", sep="\t", index=False)
    gene_type_df.to_csv(OUT / "gse271107_candidate_gene_by_sample_celltype.tsv", sep="\t", index=False)
    sample_summary_df.to_csv(OUT / "gse271107_sample_qc_signature_summary.tsv", sep="\t", index=False)

    score_cols = [c for c in cell_df.columns if c.endswith("_score") and not c.endswith("_marker_score")]
    celltype_signature = cell_df.groupby("marker_inferred_cell_type")[score_cols].median().reset_index()
    stage_signature = cell_df.groupby("stage")[score_cols].median().reindex(STAGE_ORDER).reset_index()
    stage_celltype_signature = (
        cell_df.groupby(["stage", "marker_inferred_cell_type"])[score_cols].median().reset_index()
    )
    celltype_signature.to_csv(OUT / "gse271107_signature_by_celltype.tsv", sep="\t", index=False)
    stage_signature.to_csv(OUT / "gse271107_signature_by_stage.tsv", sep="\t", index=False)
    stage_celltype_signature.to_csv(OUT / "gse271107_signature_by_stage_celltype.tsv", sep="\t", index=False)

    make_plots(cell_df, gene_type_df)
    print(f"Cells after QC: {cell_df.shape[0]}")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
