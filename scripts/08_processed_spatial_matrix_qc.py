from __future__ import annotations

import csv
import gzip
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.io import mmread


PROJECT = Path.cwd()
RAW = PROJECT / "geo_processed" / "GSE269875_RAW"
OUT = PROJECT / "analysis" / "spatial_qc"
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


def read_tsv_gz(path: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            rows.append(line.rstrip("\n").split("\t"))
    return rows


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


def open_mtx(path: Path):
    with gzip.open(path, "rb") as fh:
        matrix = mmread(fh).tocsr()
    return matrix


def sample_paths(gsm: str, title: str) -> dict[str, Path]:
    prefix = f"{gsm}_{title}"
    pos = RAW / f"{prefix}_tissue_positions.csv.gz"
    if not pos.exists():
        pos = RAW / f"{prefix}_tissue_positions_list.csv.gz"
    return {
        "matrix": RAW / f"{prefix}_matrix.mtx.gz",
        "barcodes": RAW / f"{prefix}_barcodes.tsv.gz",
        "features": RAW / f"{prefix}_features.tsv.gz",
        "positions": pos,
        "scalefactors": RAW / f"{prefix}_scalefactors_json.json.gz",
    }


def qc_sample(gsm: str, title: str, group: str) -> tuple[dict[str, object], pd.DataFrame]:
    paths = sample_paths(gsm, title)
    features_rows = read_tsv_gz(paths["features"])
    barcodes = [r[0] for r in read_tsv_gz(paths["barcodes"])]
    gene_symbols = [r[1] if len(r) > 1 and r[1] else r[0] for r in features_rows]
    matrix = open_mtx(paths["matrix"])
    if matrix.shape[0] != len(gene_symbols):
        raise ValueError(f"{title}: matrix gene count != feature rows")
    if matrix.shape[1] != len(barcodes):
        raise ValueError(f"{title}: matrix barcode count != barcode rows")

    counts = np.asarray(matrix.sum(axis=0)).ravel()
    genes_detected = np.asarray((matrix > 0).sum(axis=0)).ravel()
    mt_mask = np.array([g.upper().startswith("MT-") for g in gene_symbols])
    ribo_mask = np.array([g.upper().startswith(("RPL", "RPS")) for g in gene_symbols])
    mt_counts = np.asarray(matrix[mt_mask, :].sum(axis=0)).ravel() if mt_mask.any() else np.zeros(matrix.shape[1])
    ribo_counts = np.asarray(matrix[ribo_mask, :].sum(axis=0)).ravel() if ribo_mask.any() else np.zeros(matrix.shape[1])
    pct_mt = np.divide(mt_counts, counts, out=np.zeros_like(mt_counts, dtype=float), where=counts > 0) * 100
    pct_ribo = np.divide(ribo_counts, counts, out=np.zeros_like(ribo_counts, dtype=float), where=counts > 0) * 100

    spot_df = pd.DataFrame(
        {
            "GSM": gsm,
            "Title": title,
            "Group": group,
            "barcode": barcodes,
            "total_counts": counts,
            "n_genes": genes_detected,
            "pct_mt": pct_mt,
            "pct_ribo": pct_ribo,
        }
    )
    positions = read_positions(paths["positions"])
    spot_df = spot_df.merge(positions, on="barcode", how="left")

    with gzip.open(paths["scalefactors"], "rt", encoding="utf-8", errors="replace") as fh:
        scalefactors = json.load(fh)

    low_count = int((spot_df["total_counts"] < 500).sum())
    high_mt = int((spot_df["pct_mt"] > 20).sum())
    summary = {
        "GSM": gsm,
        "Title": title,
        "Group": group,
        "spots": int(spot_df.shape[0]),
        "genes_total": int(matrix.shape[0]),
        "nonzero_entries": int(matrix.nnz),
        "total_umis": int(counts.sum()),
        "median_umis_per_spot": float(np.median(counts)),
        "mean_umis_per_spot": float(np.mean(counts)),
        "median_genes_per_spot": float(np.median(genes_detected)),
        "mean_genes_per_spot": float(np.mean(genes_detected)),
        "median_pct_mt": float(np.median(pct_mt)),
        "mean_pct_mt": float(np.mean(pct_mt)),
        "median_pct_ribo": float(np.median(pct_ribo)),
        "spots_lt_500_umis": low_count,
        "spots_gt_20pct_mt": high_mt,
        "position_rows_matched": int(spot_df["in_tissue"].notna().sum()),
        "in_tissue_spots": int(pd.to_numeric(spot_df.get("in_tissue", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()),
        "tissue_hires_scalef": scalefactors.get("tissue_hires_scalef"),
        "spot_diameter_fullres": scalefactors.get("spot_diameter_fullres"),
    }
    return summary, spot_df


def make_plots(summary_df: pd.DataFrame, all_spots: pd.DataFrame) -> None:
    plt.rcParams.update({"figure.dpi": 140, "savefig.dpi": 180})

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    colors = summary_df["Group"].map({"control": "#4c78a8", "MM": "#f58518"})
    for ax, col, ylabel in [
        (axes[0, 0], "spots", "In-tissue spots"),
        (axes[0, 1], "median_umis_per_spot", "Median UMIs per spot"),
        (axes[1, 0], "median_genes_per_spot", "Median genes per spot"),
        (axes[1, 1], "median_pct_mt", "Median mitochondrial %"),
    ]:
        ax.bar(summary_df["Title"], summary_df[col], color=colors)
        ax.set_ylabel(ylabel)
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "human_spatial_qc_sample_summary.png")
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    for ax, col, xlabel in [
        (axes[0], "total_counts", "UMIs per spot"),
        (axes[1], "n_genes", "Genes per spot"),
        (axes[2], "pct_mt", "Mitochondrial %"),
    ]:
        for group, sdf in all_spots.groupby("Group"):
            ax.hist(sdf[col], bins=60, alpha=0.55, label=group)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Spot count")
        ax.legend(frameon=False)
        ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(OUT / "human_spatial_qc_distribution_overview.png")
    plt.close(fig)


def main() -> None:
    summaries: list[dict[str, object]] = []
    spot_tables: list[pd.DataFrame] = []
    for gsm, title, group in SAMPLES:
        summary, spot_df = qc_sample(gsm, title, group)
        summaries.append(summary)
        spot_tables.append(spot_df)
        spot_df.to_csv(OUT / f"{gsm}_{title}_spot_qc.tsv.gz", sep="\t", index=False, compression="gzip")
        print(
            f"{title}: spots={summary['spots']}, median_UMI={summary['median_umis_per_spot']:.1f}, "
            f"median_genes={summary['median_genes_per_spot']:.1f}, median_mt={summary['median_pct_mt']:.2f}%"
        )

    summary_df = pd.DataFrame(summaries)
    all_spots = pd.concat(spot_tables, ignore_index=True)
    summary_df.to_csv(OUT / "human_spatial_qc_sample_summary.tsv", sep="\t", index=False)
    all_spots.to_csv(OUT / "human_spatial_qc_all_spots.tsv.gz", sep="\t", index=False, compression="gzip")
    make_plots(summary_df, all_spots)

    flags = []
    for row in summaries:
        sample_flags = []
        if row["spots"] < 500:
            sample_flags.append("low_spot_count")
        if row["median_umis_per_spot"] < 1000:
            sample_flags.append("low_median_umi")
        if row["median_genes_per_spot"] < 500:
            sample_flags.append("low_median_gene")
        if row["median_pct_mt"] > 20:
            sample_flags.append("high_median_mt")
        flags.append(
            {
                "GSM": row["GSM"],
                "Title": row["Title"],
                "Group": row["Group"],
                "QC_flags": ";".join(sample_flags) if sample_flags else "pass_initial_matrix_qc",
            }
        )
    pd.DataFrame(flags).to_csv(OUT / "human_spatial_qc_flags.tsv", sep="\t", index=False)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
