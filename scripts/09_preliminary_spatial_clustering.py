from __future__ import annotations

import gzip
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import umap
from scipy.io import mmread
from scipy.sparse import csr_matrix, vstack
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler


PROJECT = Path.cwd()
RAW = PROJECT / "geo_processed" / "GSE269875_RAW"
QC = PROJECT / "analysis" / "spatial_qc"
OUT = PROJECT / "analysis" / "spatial_preliminary"
OUT.mkdir(parents=True, exist_ok=True)

SAMPLES = [
    ("GSM8329290", "hHBM1", "control"),
    ("GSM8329291", "hHBM2", "control"),
    ("GSM8329292", "hHBM3", "control"),
    ("GSM8329293", "hMM1", "MM"),
    ("GSM8329294", "hMM2", "MM"),
    ("GSM8329295", "hMM3", "MM"),
    ("GSM8329296", "hMM4", "MM"),
    ("GSM8329297", "hMM5", "MM"),
    ("GSM8329298", "hMM6", "MM"),
]

MODULES = {
    "plasma_cell": ["SDC1", "MZB1", "XBP1", "JCHAIN", "TNFRSF17", "SLAMF7", "PRDM1"],
    "immune_pan": ["PTPRC", "LST1", "TYROBP", "NKG7", "CD3D", "MS4A1"],
    "t_cell_nk": ["CD3D", "CD3E", "TRAC", "NKG7", "GNLY", "GZMB"],
    "myeloid": ["LYZ", "LST1", "S100A8", "S100A9", "FCGR3A", "TYROBP"],
    "stromal_ecm": ["COL1A1", "COL1A2", "DCN", "LUM", "CXCL12", "VCAM1"],
    "endothelial": ["PECAM1", "VWF", "KDR", "CLDN5", "ENG"],
}


def read_tsv_gz(path: Path) -> list[list[str]]:
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
        return [line.rstrip("\n").split("\t") for line in fh]


def read_positions(path: Path) -> pd.DataFrame:
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
        first = fh.readline().strip().split(",")
        has_header = first and first[0].lower() in {"barcode", "barcodes"}
        if has_header:
            cols = first
            rows = [line.rstrip("\n").split(",") for line in fh if line.strip()]
        else:
            cols = [
                "barcode",
                "in_tissue",
                "array_row",
                "array_col",
                "pxl_row_in_fullres",
                "pxl_col_in_fullres",
            ]
            rows = [first] + [line.rstrip("\n").split(",") for line in fh if line.strip()]
    df = pd.DataFrame(rows, columns=cols[: len(rows[0])])
    for col in ["in_tissue", "array_row", "array_col", "pxl_row_in_fullres", "pxl_col_in_fullres"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def paths(gsm: str, title: str) -> dict[str, Path]:
    prefix = f"{gsm}_{title}"
    pos = RAW / f"{prefix}_tissue_positions.csv.gz"
    if not pos.exists():
        pos = RAW / f"{prefix}_tissue_positions_list.csv.gz"
    return {
        "matrix": RAW / f"{prefix}_matrix.mtx.gz",
        "barcodes": RAW / f"{prefix}_barcodes.tsv.gz",
        "features": RAW / f"{prefix}_features.tsv.gz",
        "positions": pos,
    }


def load_sample(gsm: str, title: str, group: str):
    p = paths(gsm, title)
    features = read_tsv_gz(p["features"])
    symbols = [r[1] if len(r) > 1 and r[1] else r[0] for r in features]
    barcodes = [r[0] for r in read_tsv_gz(p["barcodes"])]
    with gzip.open(p["matrix"], "rb") as fh:
        x = mmread(fh).tocsr().T.tocsr()
    if x.shape[0] != len(barcodes):
        raise ValueError(f"{title}: barcode count mismatch")
    positions = read_positions(p["positions"])
    meta = pd.DataFrame({"GSM": gsm, "Title": title, "Group": group, "barcode": barcodes})
    meta = meta.merge(positions, on="barcode", how="left")
    return x, symbols, meta


def log_normalize(x: csr_matrix) -> csr_matrix:
    totals = np.asarray(x.sum(axis=1)).ravel()
    factors = np.divide(10000.0, totals, out=np.zeros_like(totals, dtype=float), where=totals > 0)
    y = x.multiply(factors[:, None]).tocsr()
    y.data = np.log1p(y.data)
    return y


def module_scores(x_log: csr_matrix, symbols: list[str], meta: pd.DataFrame) -> pd.DataFrame:
    symbol_to_idx: dict[str, list[int]] = {}
    for i, s in enumerate(symbols):
        symbol_to_idx.setdefault(s.upper(), []).append(i)
    out = meta[["GSM", "Title", "Group", "barcode"]].copy()
    present_rows = []
    for module, genes in MODULES.items():
        idx = []
        present = []
        for gene in genes:
            found = symbol_to_idx.get(gene.upper(), [])
            if found:
                idx.extend(found)
                present.append(gene)
        if idx:
            out[f"{module}_score"] = np.asarray(x_log[:, idx].mean(axis=1)).ravel()
        else:
            out[f"{module}_score"] = 0.0
        present_rows.append({"module": module, "genes_requested": ",".join(genes), "genes_present": ",".join(present)})
    pd.DataFrame(present_rows).to_csv(OUT / "module_gene_presence.tsv", sep="\t", index=False)
    return out


def compute_markers(x_log: csr_matrix, symbols: list[str], labels: np.ndarray, prefix: str, top_n: int = 30) -> None:
    rows = []
    detected = x_log.copy()
    detected.data = np.ones_like(detected.data)
    for label in sorted(pd.unique(labels)):
        mask = labels == label
        out_mask = ~mask
        if mask.sum() < 10 or out_mask.sum() < 10:
            continue
        mean_in = np.asarray(x_log[mask].mean(axis=0)).ravel()
        mean_out = np.asarray(x_log[out_mask].mean(axis=0)).ravel()
        pct_in = np.asarray(detected[mask].mean(axis=0)).ravel()
        pct_out = np.asarray(detected[out_mask].mean(axis=0)).ravel()
        score = (mean_in - mean_out) * np.maximum(pct_in - pct_out, 0)
        top = np.argsort(score)[::-1][:top_n]
        for rank, idx in enumerate(top, start=1):
            rows.append(
                {
                    "comparison": prefix,
                    "label": label,
                    "rank": rank,
                    "gene": symbols[idx],
                    "mean_in_log_norm": mean_in[idx],
                    "mean_out_log_norm": mean_out[idx],
                    "log_norm_difference": mean_in[idx] - mean_out[idx],
                    "pct_in": pct_in[idx],
                    "pct_out": pct_out[idx],
                    "score": score[idx],
                }
            )
    pd.DataFrame(rows).to_csv(OUT / f"{prefix}_top_markers.tsv", sep="\t", index=False)


def plot_umap(meta: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    for ax, col, title in [
        (axes[0], "Group", "Group"),
        (axes[1], "Title", "Sample"),
        (axes[2], "cluster", "Cluster"),
    ]:
        for value, sdf in meta.groupby(col):
            ax.scatter(sdf["UMAP1"], sdf["UMAP2"], s=4, alpha=0.75, label=str(value))
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.legend(markerscale=3, fontsize=7, frameon=False, ncol=2)
    fig.tight_layout()
    fig.savefig(OUT / "combined_umap_group_sample_cluster.png", dpi=180)
    plt.close(fig)


def plot_spatial_clusters(meta: pd.DataFrame) -> None:
    fig, axes = plt.subplots(3, 3, figsize=(12, 12))
    for ax, (_, row) in zip(axes.ravel(), pd.DataFrame(SAMPLES, columns=["GSM", "Title", "Group"]).iterrows()):
        sdf = meta[meta["Title"] == row["Title"]]
        ax.scatter(
            sdf["pxl_col_in_fullres"],
            -sdf["pxl_row_in_fullres"],
            c=sdf["cluster"].astype(int),
            s=8,
            cmap="tab10",
            alpha=0.85,
            linewidths=0,
        )
        ax.set_title(f"{row['Title']} ({row['Group']})")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal", adjustable="box")
    fig.tight_layout()
    fig.savefig(OUT / "spatial_cluster_maps_all_human.png", dpi=180)
    plt.close(fig)


def plot_module_maps(meta: pd.DataFrame, module_df: pd.DataFrame, module: str) -> None:
    score_col = f"{module}_score"
    merged = meta.merge(module_df[["GSM", "barcode", score_col]], on=["GSM", "barcode"], how="left")
    fig, axes = plt.subplots(3, 3, figsize=(12, 12))
    vmax = float(np.nanquantile(merged[score_col], 0.98))
    for ax, (_, row) in zip(axes.ravel(), pd.DataFrame(SAMPLES, columns=["GSM", "Title", "Group"]).iterrows()):
        sdf = merged[merged["Title"] == row["Title"]]
        sc = ax.scatter(
            sdf["pxl_col_in_fullres"],
            -sdf["pxl_row_in_fullres"],
            c=sdf[score_col],
            s=8,
            cmap="magma",
            vmin=0,
            vmax=vmax if vmax > 0 else None,
            alpha=0.85,
            linewidths=0,
        )
        ax.set_title(f"{row['Title']} {module}")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal", adjustable="box")
    fig.colorbar(sc, ax=axes.ravel().tolist(), shrink=0.6)
    fig.savefig(OUT / f"spatial_{module}_score_maps_all_human.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def summarize_clusters(meta: pd.DataFrame, module_df: pd.DataFrame) -> None:
    cluster_counts = (
        meta.groupby(["cluster", "Group", "Title"]).size().reset_index(name="spots")
    )
    cluster_counts.to_csv(OUT / "cluster_counts_by_sample.tsv", sep="\t", index=False)
    cluster_group = meta.groupby(["cluster", "Group"]).size().unstack(fill_value=0)
    for col in ["control", "MM"]:
        if col not in cluster_group:
            cluster_group[col] = 0
    cluster_group["total"] = cluster_group["control"] + cluster_group["MM"]
    cluster_group["MM_fraction"] = cluster_group["MM"] / cluster_group["total"].replace(0, np.nan)
    cluster_group.to_csv(OUT / "cluster_group_composition.tsv", sep="\t")

    score_cols = [c for c in module_df.columns if c.endswith("_score")]
    merged = meta[["GSM", "Title", "Group", "barcode", "cluster"]].merge(
        module_df[["GSM", "barcode", *score_cols]], on=["GSM", "barcode"], how="left"
    )
    merged.groupby(["cluster", "Group"])[score_cols].median().reset_index().to_csv(
        OUT / "cluster_module_median_scores.tsv", sep="\t", index=False
    )
    merged.groupby(["Title", "Group"])[score_cols].median().reset_index().to_csv(
        OUT / "sample_module_median_scores.tsv", sep="\t", index=False
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    plot_df = cluster_group.sort_index()
    x = np.arange(plot_df.shape[0])
    ax.bar(x, plot_df["control"], label="control", color="#4c78a8")
    ax.bar(x, plot_df["MM"], bottom=plot_df["control"], label="MM", color="#f58518")
    ax.set_xticks(x)
    ax.set_xticklabels(plot_df.index.astype(str))
    ax.set_xlabel("Cluster")
    ax.set_ylabel("Spot count")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "cluster_group_composition.png", dpi=180)
    plt.close(fig)


def main() -> None:
    xs = []
    metas = []
    symbols_ref = None
    for gsm, title, group in SAMPLES:
        x, symbols, meta = load_sample(gsm, title, group)
        if symbols_ref is None:
            symbols_ref = symbols
        elif symbols != symbols_ref:
            raise ValueError(f"{title}: feature order differs")
        xs.append(x)
        metas.append(meta)
        print(f"Loaded {title}: {x.shape[0]} spots x {x.shape[1]} genes")
    symbols = symbols_ref or []
    x_raw = vstack(xs, format="csr")
    meta = pd.concat(metas, ignore_index=True)
    qc = pd.read_csv(QC / "human_spatial_qc_all_spots.tsv.gz", sep="\t")
    meta = meta.merge(
        qc[["GSM", "barcode", "total_counts", "n_genes", "pct_mt", "pct_ribo"]],
        on=["GSM", "barcode"],
        how="left",
    )

    x_log = log_normalize(x_raw)
    detected = np.asarray((x_raw > 0).sum(axis=0)).ravel()
    mean = np.asarray(x_log.mean(axis=0)).ravel()
    sq_mean = np.asarray(x_log.multiply(x_log).mean(axis=0)).ravel()
    var = sq_mean - mean * mean
    exclude = np.array([s.upper().startswith(("MT-", "RPL", "RPS")) for s in symbols])
    eligible = np.where((detected >= 30) & (~exclude))[0]
    top_n = min(2500, eligible.size)
    hvg = eligible[np.argsort(var[eligible])[::-1][:top_n]]
    pd.DataFrame({"gene": np.array(symbols)[hvg], "variance": var[hvg], "detected_spots": detected[hvg]}).to_csv(
        OUT / "highly_variable_genes_preliminary.tsv", sep="\t", index=False
    )
    print(f"Selected {top_n} HVGs")

    svd = TruncatedSVD(n_components=30, random_state=7)
    pcs = svd.fit_transform(x_log[:, hvg])
    pcs = StandardScaler().fit_transform(pcs)
    meta["PC1"] = pcs[:, 0]
    meta["PC2"] = pcs[:, 1]
    reducer = umap.UMAP(n_neighbors=25, min_dist=0.25, random_state=7)
    emb = reducer.fit_transform(pcs[:, :20])
    meta["UMAP1"] = emb[:, 0]
    meta["UMAP2"] = emb[:, 1]
    km = KMeans(n_clusters=8, random_state=7, n_init=25)
    meta["cluster"] = km.fit_predict(pcs[:, :20]).astype(str)
    meta.to_csv(OUT / "combined_spot_embedding_clusters.tsv.gz", sep="\t", index=False, compression="gzip")

    mod = module_scores(x_log, symbols, meta)
    mod.to_csv(OUT / "combined_spot_module_scores.tsv.gz", sep="\t", index=False, compression="gzip")

    compute_markers(x_log, symbols, meta["cluster"].to_numpy(), "cluster")
    compute_markers(x_log, symbols, meta["Group"].to_numpy(), "group")
    summarize_clusters(meta, mod)
    plot_umap(meta)
    plot_spatial_clusters(meta)
    for module in ["plasma_cell", "immune_pan", "myeloid", "stromal_ecm"]:
        plot_module_maps(meta, mod, module)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
