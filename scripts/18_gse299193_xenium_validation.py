from __future__ import annotations

import math
import re
import tarfile
from pathlib import Path

import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import sparse, stats


PROJECT = Path.cwd()
BASE = PROJECT / "external_spatial" / "GSE299193"
RAW_TAR = BASE / "raw" / "GSE299193_RAW.tar"
META = BASE / "metadata"
SELECTED = BASE / "selected_xenium_files"
OUT = PROJECT / "analysis" / "gse299193_xenium_validation"
REPORTS = PROJECT / "reports" / "validation"

EXPECTED_BYTES = 82_255_360_000
PLASMA_SECRETORY_GENES = ["SDC1", "MZB1", "XBP1", "JCHAIN", "TNFRSF17", "SLAMF7", "PRDM1", "TXNDC5", "PIM2", "IRF4"]
CLINICAL_MODULE_GENES = ["POU2AF1", "XBP1", "JCHAIN"]
AXIS_GENES = sorted(set(PLASMA_SECRETORY_GENES + CLINICAL_MODULE_GENES))
GROUP_ORDER = ["Ctrl", "MGUS", "SM", "MM", "RM"]
PALETTE = {
    "Ctrl": "#4C78A8",
    "MGUS": "#72B7B2",
    "SM": "#F2CF5B",
    "MM": "#C44E52",
    "RM": "#8C1D40",
}


def configure_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8,
            "axes.titlesize": 9,
            "axes.labelsize": 8,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "legend.fontsize": 7,
            "figure.titlesize": 11,
            "axes.linewidth": 0.8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def require_complete_tar() -> bool:
    if not RAW_TAR.exists():
        return False
    return RAW_TAR.stat().st_size == EXPECTED_BYTES


def read_manifest() -> pd.DataFrame:
    path = META / "gse299193_sample_manifest.tsv"
    if not path.exists():
        raise FileNotFoundError(f"Run scripts/17_gse299193_download_status.py first: missing {path}")
    return pd.read_csv(path, sep="\t")


def sample_from_member(name: str) -> str | None:
    m = re.search(r"(GSM\d+)", name)
    return m.group(1) if m else None


def list_tar_members() -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    with tarfile.open(RAW_TAR, "r") as tar:
        for member in tar:
            rows.append(
                {
                    "name": member.name,
                    "size": member.size,
                    "is_file": member.isfile(),
                    "sample": sample_from_member(member.name) or "",
                }
            )
    inv = pd.DataFrame(rows)
    inv.to_csv(OUT / "gse299193_tar_inventory.tsv", sep="\t", index=False)
    return inv


def select_members(inv: pd.DataFrame) -> pd.DataFrame:
    patterns = [
        r"cell_feature_matrix\.h5$",
        r"cells\.csv\.gz$",
        r"experiment\.xenium$",
        r"metrics_summary\.csv$",
        r"analysis_summary\.html$",
    ]
    regex = re.compile("|".join(patterns), flags=re.IGNORECASE)
    selected = inv[inv["is_file"] & inv["name"].map(lambda x: bool(regex.search(str(x))))].copy()
    selected.to_csv(OUT / "gse299193_selected_tar_members.tsv", sep="\t", index=False)
    return selected


def extract_selected(selected: pd.DataFrame) -> None:
    if selected.empty:
        return
    names = set(selected["name"])
    SELECTED.mkdir(parents=True, exist_ok=True)
    with tarfile.open(RAW_TAR, "r") as tar:
        for member in tar:
            if member.name not in names:
                continue
            target = SELECTED / member.name
            if target.exists() and target.stat().st_size == member.size:
                continue
            tar.extract(member, path=SELECTED)


def decode_array(values: np.ndarray) -> list[str]:
    out: list[str] = []
    for value in values:
        if isinstance(value, bytes):
            out.append(value.decode("utf-8", errors="replace"))
        else:
            out.append(str(value))
    return out


def read_10x_h5_matrix(path: Path) -> tuple[sparse.csc_matrix, list[str], list[str]]:
    with h5py.File(path, "r") as h5:
        matrix_group = h5["matrix"]
        data = matrix_group["data"][:]
        indices = matrix_group["indices"][:]
        indptr = matrix_group["indptr"][:]
        shape = tuple(matrix_group["shape"][:])
        mat = sparse.csc_matrix((data, indices, indptr), shape=shape)
        features_group = matrix_group["features"]
        names = decode_array(features_group["name"][:])
        barcodes = decode_array(matrix_group["barcodes"][:])
    return mat, names, barcodes


def summarize_h5(path: Path, sample: str) -> dict[str, object]:
    mat, genes, barcodes = read_10x_h5_matrix(path)
    gene_index = {gene.upper(): i for i, gene in enumerate(genes)}
    row: dict[str, object] = {
        "sample": sample,
        "h5_file": str(path.relative_to(PROJECT)),
        "n_genes": len(genes),
        "n_cells": len(barcodes),
        "n_nonzero": int(mat.nnz),
    }
    for gene in AXIS_GENES:
        idx = gene_index.get(gene.upper())
        if idx is None:
            row[f"{gene}_present"] = False
            row[f"{gene}_mean_log1p"] = np.nan
            row[f"{gene}_pct_detected"] = np.nan
            continue
        vals = mat.getrow(idx).toarray().ravel()
        row[f"{gene}_present"] = True
        row[f"{gene}_mean_log1p"] = float(np.mean(np.log1p(vals)))
        row[f"{gene}_pct_detected"] = float(np.mean(vals > 0))
    plasma_values = [row[f"{g}_mean_log1p"] for g in PLASMA_SECRETORY_GENES if row.get(f"{g}_present") is True]
    clinical_values = [row[f"{g}_mean_log1p"] for g in CLINICAL_MODULE_GENES if row.get(f"{g}_present") is True]
    row["plasma_secretory_raw_score"] = float(np.mean(plasma_values)) if plasma_values else np.nan
    row["plasma_secretory_n_genes"] = len(plasma_values)
    row["clinical_module_raw_score"] = float(np.mean(clinical_values)) if clinical_values else np.nan
    row["clinical_module_n_genes"] = len(clinical_values)
    return row


def zscore(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    std = values.std(skipna=True)
    if pd.isna(std) or std == 0:
        return pd.Series(np.nan, index=series.index)
    return (values - values.mean(skipna=True)) / std


def compare_groups(scores: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    comparisons = [
        ("MM_vs_Ctrl", ["MM"], ["Ctrl"]),
        ("MM_RM_vs_Ctrl_MGUS_SM", ["MM", "RM"], ["Ctrl", "MGUS", "SM"]),
        ("Active_vs_non_active", ["MM", "RM"], ["Ctrl", "MGUS", "SM"]),
    ]
    variables = ["plasma_secretory_score_z", "clinical_module_score_z", "TXNDC5_mean_log1p", "XBP1_mean_log1p", "JCHAIN_mean_log1p", "POU2AF1_mean_log1p"]
    for contrast, high_groups, low_groups in comparisons:
        for variable in variables:
            high = pd.to_numeric(scores.loc[scores["condition"].isin(high_groups), variable], errors="coerce").dropna()
            low = pd.to_numeric(scores.loc[scores["condition"].isin(low_groups), variable], errors="coerce").dropna()
            row = {
                "contrast": contrast,
                "variable": variable,
                "high_groups": ",".join(high_groups),
                "low_groups": ",".join(low_groups),
                "n_high": len(high),
                "n_low": len(low),
                "median_high": high.median() if len(high) else np.nan,
                "median_low": low.median() if len(low) else np.nan,
                "delta_high_minus_low": (high.median() - low.median()) if len(high) and len(low) else np.nan,
                "mannwhitney_p": np.nan,
            }
            if len(high) >= 2 and len(low) >= 2:
                row["mannwhitney_p"] = float(stats.mannwhitneyu(high, low, alternative="two-sided").pvalue)
            rows.append(row)
    assoc = pd.DataFrame(rows)
    p = pd.to_numeric(assoc["mannwhitney_p"], errors="coerce")
    valid = p.notna()
    assoc["mannwhitney_fdr"] = np.nan
    if valid.any():
        order = np.argsort(p[valid].to_numpy())
        ranked = p[valid].to_numpy()[order]
        n = len(ranked)
        adjusted = ranked * n / np.arange(1, n + 1)
        adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
        adjusted = np.clip(adjusted, 0, 1)
        valid_index = assoc.index[valid].to_numpy()
        assoc.loc[valid_index[order], "mannwhitney_fdr"] = adjusted
    assoc.to_csv(OUT / "gse299193_axis_group_associations.tsv", sep="\t", index=False)
    return assoc


def clean_axis(ax: mpl.axes.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#E5E7EB", linewidth=0.6)
    ax.set_axisbelow(True)


def save_figure(fig: mpl.figure.Figure, stem: str) -> None:
    fig.tight_layout()
    for suffix in [".png", ".svg", ".pdf"]:
        fig.savefig(OUT / f"{stem}{suffix}", dpi=350, bbox_inches="tight")
    plt.close(fig)


def plot_scores(scores: pd.DataFrame, assoc: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.8), gridspec_kw={"width_ratios": [1.1, 1.1, 1.35]})
    for ax, variable, ylabel, title in [
        (axes[0], "plasma_secretory_score_z", "Plasma-secretory score z", "Plasma-secretory axis"),
        (axes[1], "clinical_module_score_z", "Clinical module score z", "POU2AF1/XBP1 module"),
    ]:
        data = [scores.loc[scores["condition"] == group, variable].dropna().to_numpy(float) for group in GROUP_ORDER]
        bp = ax.boxplot(data, patch_artist=True, showfliers=False, widths=0.5)
        for patch, group in zip(bp["boxes"], GROUP_ORDER):
            patch.set(facecolor=PALETTE.get(group, "#9CA3AF"), alpha=0.72, edgecolor="#222222", linewidth=0.8)
        for i, values in enumerate(data, start=1):
            rng = np.random.default_rng(299193 + i)
            if len(values):
                ax.scatter(np.full(len(values), i) + rng.normal(0, 0.04, len(values)), values, s=16, color="#222222", alpha=0.75, linewidths=0)
                ax.text(i, np.nanmax(values) + 0.06, f"n={len(values)}", ha="center", va="bottom", fontsize=7)
        ax.set_xticks(range(1, len(GROUP_ORDER) + 1))
        ax.set_xticklabels(GROUP_ORDER)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        clean_axis(ax)

    candidate_heat_genes = ["MZB1", "TNFRSF17", "SLAMF7", "IRF4", "PIM2", "POU2AF1", "XBP1"]
    heat_genes = [
        gene
        for gene in candidate_heat_genes
        if f"{gene}_mean_log1p" in scores.columns and pd.to_numeric(scores[f"{gene}_mean_log1p"], errors="coerce").notna().any()
    ]
    grouped = scores.groupby("condition")[[f"{g}_mean_log1p" for g in heat_genes]].mean().reindex(GROUP_ORDER)
    mat = grouped.to_numpy(float)
    im = axes[2].imshow(mat, aspect="auto", cmap="Reds")
    axes[2].set_yticks(range(len(GROUP_ORDER)))
    axes[2].set_yticklabels(GROUP_ORDER)
    axes[2].set_xticks(range(len(heat_genes)))
    axes[2].set_xticklabels(heat_genes, rotation=45, ha="right")
    axes[2].set_title("Panel-covered axis genes")
    for spine in axes[2].spines.values():
        spine.set_visible(False)
    cbar = fig.colorbar(im, ax=axes[2], fraction=0.046, pad=0.04)
    cbar.set_label("Mean log1p count")
    fig.suptitle("GSE299193 Xenium validation of the plasma-secretory program", x=0.01, ha="left", fontweight="bold")
    save_figure(fig, "gse299193_xenium_axis_validation")


def write_report(scores: pd.DataFrame | None, assoc: pd.DataFrame | None, status: str) -> None:
    lines = [
        "# GSE299193 Xenium Spatial Validation Report",
        "",
        f"Status: {status}",
        "",
    ]
    if scores is None or scores.empty:
        lines.extend(
            [
                "The RAW tar has not yet been fully downloaded or no usable `cell_feature_matrix.h5` files were found.",
                "",
                "Next action:",
                "",
                "- Continue/resume `GSE299193_RAW.tar` download.",
                "- Rerun `python scripts/18_gse299193_xenium_validation.py` after the tar reaches the expected size.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                f"Samples analyzed: {len(scores)}",
                "",
                "Panel coverage:",
                "",
            ]
        )
        present_rows = []
        for gene in AXIS_GENES:
            col = f"{gene}_present"
            if col in scores.columns:
                present_rows.append((gene, int(pd.to_numeric(scores[col], errors="coerce").fillna(False).astype(bool).sum())))
        for gene, n_present in present_rows:
            lines.append(f"- `{gene}` present in {n_present}/{len(scores)} sample matrices.")
        lines.extend(
            [
                "",
                "Interpretation boundary:",
                "",
                "- GSE299193 supports the plasma-secretory / POU2AF1-XBP1 program at the second spatial-cohort level.",
                "- GSE299193 does not directly validate `TXNDC5`, `JCHAIN`, or `SDC1` because these genes are absent from the extracted Xenium feature matrices.",
                "",
                "Primary outputs:",
                "",
                "- `analysis/gse299193_xenium_validation/gse299193_sample_axis_scores.tsv`",
                "- `analysis/gse299193_xenium_validation/gse299193_axis_group_associations.tsv`",
                "- `analysis/gse299193_xenium_validation/gse299193_xenium_axis_validation.png`",
                "",
            ]
        )
        if assoc is not None and not assoc.empty:
            top = assoc.sort_values("mannwhitney_fdr", na_position="last").head(8)
            lines.append("Top association rows:")
            lines.append("")
            for _, row in top.iterrows():
                p = row["mannwhitney_p"]
                fdr = row["mannwhitney_fdr"]
                p_text = "NA" if pd.isna(p) else f"{p:.3g}"
                fdr_text = "NA" if pd.isna(fdr) else f"{fdr:.3g}"
                lines.append(
                    f"- {row['contrast']} / {row['variable']}: delta={row['delta_high_minus_low']:.3f}, p={p_text}, FDR={fdr_text}, n={int(row['n_high'])}/{int(row['n_low'])}."
                )
            lines.append("")
    (REPORTS / "GSE299193_XENIUM_VALIDATION_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    configure_style()
    OUT.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    SELECTED.mkdir(parents=True, exist_ok=True)

    if not require_complete_tar():
        current = RAW_TAR.stat().st_size if RAW_TAR.exists() else 0
        write_report(None, None, f"waiting for complete RAW tar ({current:,}/{EXPECTED_BYTES:,} bytes)")
        print(f"RAW tar is incomplete: {current:,}/{EXPECTED_BYTES:,} bytes")
        return

    manifest = read_manifest()
    inv = list_tar_members()
    selected = select_members(inv)
    extract_selected(selected)

    h5_files = sorted(SELECTED.rglob("*cell_feature_matrix.h5"))
    if not h5_files:
        write_report(None, None, "complete tar found, but no cell_feature_matrix.h5 was extracted")
        print("No cell_feature_matrix.h5 files found in selected extraction.")
        return

    rows: list[dict[str, object]] = []
    for h5 in h5_files:
        sample = sample_from_member(str(h5)) or ""
        rows.append(summarize_h5(h5, sample))
    scores = pd.DataFrame(rows)
    scores = scores.merge(manifest, left_on="sample", right_on="geo_accession", how="left")
    scores["plasma_secretory_score_z"] = zscore(scores["plasma_secretory_raw_score"])
    scores["clinical_module_score_z"] = zscore(scores["clinical_module_raw_score"])
    scores.to_csv(OUT / "gse299193_sample_axis_scores.tsv", sep="\t", index=False)

    assoc = compare_groups(scores)
    plot_scores(scores, assoc)
    write_report(scores, assoc, "completed first-pass Xenium sample-level validation")
    print(f"Analyzed {len(scores)} H5 files.")
    print(f"Wrote outputs to {OUT}")


if __name__ == "__main__":
    main()
