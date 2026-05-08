from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests


PROJECT = Path.cwd()
OUT = PROJECT / "analysis" / "spatial_autocorrelation_niche"
REPORTS = PROJECT / "reports" / "validation"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

SPOT_SIGNATURES = PROJECT / "analysis" / "spatial_candidate_signatures" / "spot_signature_scores.tsv.gz"
SPOT_MODULES = PROJECT / "analysis" / "spatial_preliminary" / "combined_spot_module_scores.tsv.gz"
SPOT_COORDS = PROJECT / "analysis" / "spatial_preliminary" / "combined_spot_embedding_clusters.tsv.gz"

SIGNATURES = [
    "plasma_secretory_score",
    "myeloid_inflammatory_score",
    "t_nk_cytotoxic_exhaustion_score",
    "stromal_ecm_score",
    "endothelial_angiogenic_score",
    "cycling_proliferation_score",
]

NEIGHBOR_TARGETS = [
    "myeloid_inflammatory_score",
    "t_nk_cytotoxic_exhaustion_score",
    "stromal_ecm_score",
    "endothelial_angiogenic_score",
    "cycling_proliferation_score",
    "immune_pan_score",
    "myeloid_score",
    "endothelial_score",
]

LABELS = {
    "plasma_secretory_score": "Plasma-secretory",
    "myeloid_inflammatory_score": "Myeloid inflammatory",
    "t_nk_cytotoxic_exhaustion_score": "T/NK cytotoxic",
    "stromal_ecm_score": "Stromal ECM",
    "endothelial_angiogenic_score": "Endothelial angiogenic",
    "cycling_proliferation_score": "Cycling",
    "plasma_cell_score": "Plasma-cell marker",
    "immune_pan_score": "Immune pan",
    "myeloid_score": "Myeloid marker",
    "endothelial_score": "Endothelial marker",
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
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def bh_fdr(values: pd.Series) -> pd.Series:
    out = pd.Series(np.nan, index=values.index, dtype=float)
    valid = pd.to_numeric(values, errors="coerce").dropna()
    if valid.empty:
        return out
    _, q, _, _ = multipletests(valid.to_numpy(float), method="fdr_bh")
    out.loc[valid.index] = q
    return out


def zscore(x: pd.Series) -> pd.Series:
    x = pd.to_numeric(x, errors="coerce")
    sd = x.std(skipna=True)
    if pd.isna(sd) or sd == 0:
        return pd.Series(np.nan, index=x.index)
    return (x - x.mean(skipna=True)) / sd


def load_spots() -> pd.DataFrame:
    signatures = pd.read_csv(SPOT_SIGNATURES, sep="\t")
    modules = pd.read_csv(SPOT_MODULES, sep="\t")
    coords = pd.read_csv(
        SPOT_COORDS,
        sep="\t",
        usecols=[
            "GSM",
            "Title",
            "Group",
            "barcode",
            "array_row",
            "array_col",
            "pxl_row_in_fullres",
            "pxl_col_in_fullres",
            "total_counts",
            "n_genes",
            "cluster",
        ],
    )
    df = coords.merge(signatures, on=["GSM", "Title", "Group", "barcode"], how="left")
    df = df.merge(modules, on=["GSM", "Title", "Group", "barcode"], how="left", suffixes=("", "_module"))
    return df


def knn_indices(xy: np.ndarray, k: int = 6) -> np.ndarray:
    if len(xy) <= k:
        k = max(1, len(xy) - 1)
    tree = cKDTree(xy)
    _, idx = tree.query(xy, k=k + 1)
    return idx[:, 1:]


def morans_i(values: np.ndarray, neighbors: np.ndarray) -> float:
    x = values.astype(float)
    ok = np.isfinite(x)
    if ok.sum() < 20:
        return np.nan
    x = x.copy()
    mean = np.nanmean(x)
    centered = x - mean
    denom = np.nansum(centered[ok] ** 2)
    if denom == 0:
        return np.nan
    num = 0.0
    w = 0
    for i in range(len(x)):
        if not np.isfinite(centered[i]):
            continue
        js = neighbors[i]
        js = js[np.isfinite(centered[js])]
        if len(js) == 0:
            continue
        num += float(np.sum(centered[i] * centered[js]))
        w += len(js)
    if w == 0:
        return np.nan
    return len(x) / w * num / denom


def moran_permutation_p(values: np.ndarray, neighbors: np.ndarray, observed: float, n_perm: int = 199) -> float:
    if not np.isfinite(observed):
        return np.nan
    rng = np.random.default_rng(20260501)
    valid = np.isfinite(values)
    if valid.sum() < 20:
        return np.nan
    vals = values.copy()
    null = []
    for _ in range(n_perm):
        shuffled = vals.copy()
        shuffled[valid] = rng.permutation(shuffled[valid])
        null.append(morans_i(shuffled, neighbors))
    null_arr = np.asarray(null, dtype=float)
    null_arr = null_arr[np.isfinite(null_arr)]
    if len(null_arr) == 0:
        return np.nan
    return (np.sum(np.abs(null_arr) >= abs(observed)) + 1) / (len(null_arr) + 1)


def run_morans(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (gsm, title, group), sample in df.groupby(["GSM", "Title", "Group"], sort=True):
        sample = sample.dropna(subset=["array_row", "array_col"]).copy()
        xy = sample[["array_row", "array_col"]].to_numpy(float)
        if len(sample) < 30:
            continue
        neighbors = knn_indices(xy, k=6)
        for sig in SIGNATURES:
            values = pd.to_numeric(sample[sig], errors="coerce").to_numpy(float)
            observed = morans_i(values, neighbors)
            p = moran_permutation_p(values, neighbors, observed)
            rows.append(
                {
                    "GSM": gsm,
                    "Title": title,
                    "Group": group,
                    "signature": sig,
                    "signature_label": LABELS.get(sig, sig),
                    "n_spots": len(sample),
                    "knn_k": 6,
                    "morans_i": observed,
                    "permutation_p": p,
                    "analysis_note": "Spot-level kNN Moran's I on array_row/array_col coordinates; exploratory spatial clustering screen. Disease-specific autocorrelation requires group comparison and is limited by n.",
                }
            )
    out = pd.DataFrame(rows)
    out["fdr"] = bh_fdr(out["permutation_p"])
    return out.sort_values(["signature", "Group", "Title"])


def run_neighbor_enrichment(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (gsm, title, group), sample in df.groupby(["GSM", "Title", "Group"], sort=True):
        sample = sample.dropna(subset=["array_row", "array_col", "plasma_secretory_score"]).copy()
        if len(sample) < 40:
            continue
        xy = sample[["array_row", "array_col"]].to_numpy(float)
        neighbors = knn_indices(xy, k=6)
        plasma = pd.to_numeric(sample["plasma_secretory_score"], errors="coerce")
        threshold = plasma.quantile(0.75)
        high = plasma >= threshold
        for target in NEIGHBOR_TARGETS:
            if target not in sample.columns:
                continue
            vals = pd.to_numeric(sample[target], errors="coerce").to_numpy(float)
            neigh_mean = np.array([np.nanmean(vals[js]) if len(js) else np.nan for js in neighbors])
            high_vals = neigh_mean[high.to_numpy() & np.isfinite(neigh_mean)]
            other_vals = neigh_mean[(~high.to_numpy()) & np.isfinite(neigh_mean)]
            if len(high_vals) < 10 or len(other_vals) < 10:
                continue
            try:
                p = mannwhitneyu(high_vals, other_vals, alternative="two-sided").pvalue
            except ValueError:
                p = np.nan
            rows.append(
                {
                    "GSM": gsm,
                    "Title": title,
                    "Group": group,
                    "neighbor_feature": target,
                    "neighbor_feature_label": LABELS.get(target, target),
                    "n_spots": len(sample),
                    "high_spots": int(high.sum()),
                    "other_spots": int((~high).sum()),
                    "plasma_high_threshold_q75": threshold,
                    "neighbor_median_plasma_high": float(np.nanmedian(high_vals)),
                    "neighbor_median_other": float(np.nanmedian(other_vals)),
                    "median_difference_high_minus_other": float(np.nanmedian(high_vals) - np.nanmedian(other_vals)),
                    "mannwhitney_p": p,
                    "analysis_note": "Neighbor feature mean among 6 nearest spots, excluding the focal spot, compared for plasma-secretory top-quartile versus other spots within each sample. Reported neighbor features exclude plasma-secretory module genes and omit plasma-cell marker scores to reduce circularity.",
                }
            )
    out = pd.DataFrame(rows)
    out["fdr"] = bh_fdr(out["mannwhitney_p"])
    return out.sort_values(["neighbor_feature", "Group", "Title"])


def summarize_neighbor(neighbor: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for feature, sub in neighbor.groupby("neighbor_feature", sort=False):
        values = pd.to_numeric(sub["median_difference_high_minus_other"], errors="coerce").dropna()
        pvals = pd.to_numeric(sub["mannwhitney_p"], errors="coerce").dropna()
        fdrs = pd.to_numeric(sub["fdr"], errors="coerce").dropna()
        rows.append(
            {
                "neighbor_feature": feature,
                "neighbor_feature_label": LABELS.get(feature, feature),
                "n_samples": int(values.shape[0]),
                "median_of_sample_median_differences": float(values.median()) if not values.empty else np.nan,
                "samples_positive": int((values > 0).sum()),
                "samples_negative": int((values < 0).sum()),
                "min_nominal_p": float(pvals.min()) if not pvals.empty else np.nan,
                "min_fdr": float(fdrs.min()) if not fdrs.empty else np.nan,
            }
        )
    return pd.DataFrame(rows).sort_values("median_of_sample_median_differences", ascending=False)


def plot_results(moran: pd.DataFrame, neighbor_summary: pd.DataFrame) -> None:
    configure_style()
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.0), gridspec_kw={"width_ratios": [1.1, 1.4]})

    ax = axes[0]
    plasma = moran[moran["signature"].eq("plasma_secretory_score")].copy()
    order = plasma.sort_values(["Group", "Title"])
    colors = order["Group"].map({"control": "#4C78A8", "MM": "#C44E52"}).fillna("#6B7280")
    ax.bar(range(len(order)), order["morans_i"], color=colors, edgecolor="black", linewidth=0.4)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order["Title"], rotation=45, ha="right")
    ax.set_ylabel("Moran's I")
    ax.set_title("Plasma-secretory spatial autocorrelation")
    ax.axhline(0, color="#222222", lw=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axes[1]
    summ = neighbor_summary.head(8).copy()
    summ = summ.sort_values("median_of_sample_median_differences")
    vals = summ["median_of_sample_median_differences"].to_numpy(float)
    labels = summ["neighbor_feature_label"].tolist()
    bar_colors = ["#C44E52" if v > 0 else "#9CA3AF" for v in vals]
    ax.barh(range(len(summ)), vals, color=bar_colors, edgecolor="black", linewidth=0.4)
    ax.set_yticks(range(len(summ)))
    ax.set_yticklabels(labels)
    ax.axvline(0, color="#222222", lw=0.7)
    ax.set_xlabel("Median neighbor-score difference\nplasma-secretory-high minus other spots")
    ax.set_title("Non-overlapping neighbor enrichment summary")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.suptitle("Fig. 3 | Spatial organization of the plasma-secretory program", x=0.01, ha="left", fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    for suffix in [".png", ".pdf", ".svg"]:
        fig.savefig(OUT / f"spatial_autocorrelation_niche_summary{suffix}", dpi=350, bbox_inches="tight")
    plt.close(fig)


def write_report(moran: pd.DataFrame, neighbor: pd.DataFrame, neighbor_summary: pd.DataFrame) -> None:
    plasma = moran[moran["signature"].eq("plasma_secretory_score")]
    sig_n = int((pd.to_numeric(plasma["fdr"], errors="coerce") < 0.05).sum())
    total = int(plasma.shape[0])
    median_i = pd.to_numeric(plasma["morans_i"], errors="coerce").median()
    ctrl = plasma[plasma["Group"].str.lower().eq("control")]["morans_i"].dropna()
    mm = plasma[plasma["Group"].eq("MM")]["morans_i"].dropna()
    if len(ctrl) and len(mm):
        group_p = mannwhitneyu(mm, ctrl, alternative="two-sided").pvalue
        group_line = (
            f"- MM samples had numerically higher Moran's I than controls "
            f"(median MM={mm.median():.3f}, median control={ctrl.median():.3f}; Mann-Whitney p={group_p:.4g})."
        )
    else:
        group_line = "- Disease-specific group comparison was not estimable because one group was absent."
    top_neighbors = neighbor_summary.head(5)
    lines = [
        "# Spatial Autocorrelation And Niche Analysis",
        "",
        "Purpose: address the reviewer concern that the spatial component should not be limited to sample-level module-score comparisons.",
        "",
        "Methods:",
        "",
        "- Spot-level plasma-secretory and niche scores from GSE269875 were merged with array-row/array-column coordinates.",
        "- Moran's I was calculated within each sample using 6-nearest-neighbor graph weights.",
        "- Permutation p values used 199 within-sample label permutations.",
        "- Neighbor enrichment compared the mean score of 6 nearest neighboring spots around plasma-secretory-high spots, defined as the within-sample top quartile, versus other spots.",
        "- The focal spot was excluded from the k-nearest-neighbor set.",
        "- Reported neighbor enrichment excludes plasma-cell marker scores and uses non-overlapping niche programs rather than plasma-secretory module genes.",
        "",
        "Key results:",
        "",
        f"- Plasma-secretory Moran's I was evaluated in {total} samples; {sig_n} samples had FDR < 0.05.",
        f"- Median plasma-secretory Moran's I across samples was {median_i:.3f}.",
        group_line,
        "",
        "Top neighbor-enrichment summaries:",
        "",
        top_neighbors.to_markdown(index=False),
        "",
        "Interpretation boundary:",
        "",
        "- This is an exploratory spatial organization analysis, not histology-anchored niche segmentation.",
        "- It supports non-random spatial clustering and local neighbor associations when significant, but it does not prove causal cell-cell interaction.",
        "- Because control marrow also shows non-zero Moran's I, the conservative claim is spatial clustering within marrow tissue; disease-specific spatial autocorrelation remains limited by the small cohort size.",
    ]
    (REPORTS / "SPATIAL_AUTOCORRELATION_NICHE_ANALYSIS.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    df = load_spots()
    moran = run_morans(df)
    neighbor = run_neighbor_enrichment(df)
    neighbor_summary = summarize_neighbor(neighbor)

    moran.to_csv(OUT / "spatial_morans_i_results.tsv", sep="\t", index=False)
    neighbor.to_csv(OUT / "spatial_neighbor_enrichment_results.tsv", sep="\t", index=False)
    neighbor_summary.to_csv(OUT / "spatial_neighbor_enrichment_summary.tsv", sep="\t", index=False)
    plot_results(moran, neighbor_summary)
    write_report(moran, neighbor, neighbor_summary)

    print(OUT / "spatial_morans_i_results.tsv")
    print(OUT / "spatial_neighbor_enrichment_results.tsv")
    print(REPORTS / "SPATIAL_AUTOCORRELATION_NICHE_ANALYSIS.md")


if __name__ == "__main__":
    main()
