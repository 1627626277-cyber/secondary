from __future__ import annotations

import gzip
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.io import mmread
from scipy.sparse import csr_matrix, vstack
from scipy.stats import mannwhitneyu


PROJECT = Path.cwd()
RAW = PROJECT / "geo_processed" / "GSE269875_RAW"
PRELIM = PROJECT / "analysis" / "spatial_preliminary"
OUT = PROJECT / "analysis" / "spatial_candidate_signatures"
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
    "myeloid_inflammatory": [
        "LYZ",
        "LST1",
        "S100A8",
        "S100A9",
        "TYROBP",
        "FCGR3A",
        "FCN1",
        "CTSS",
        "CXCL8",
        "IL1B",
    ],
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
    "stromal_ecm": [
        "COL1A1",
        "COL1A2",
        "COL3A1",
        "DCN",
        "LUM",
        "CXCL12",
        "VCAM1",
        "FN1",
        "SPARC",
        "POSTN",
    ],
    "endothelial_angiogenic": ["PECAM1", "VWF", "KDR", "CLDN5", "ENG", "FLT1", "ESAM"],
    "erythroid_megak": ["HBB", "HBA1", "HBA2", "ALAS2", "PPBP", "PF4", "ITGA2B", "GP9"],
    "cycling_proliferation": ["MKI67", "TOP2A", "PCNA", "TYMS", "UBE2C", "BIRC5", "STMN1"],
}

CANONICAL_PLASMA = {
    "SDC1",
    "MZB1",
    "XBP1",
    "JCHAIN",
    "TNFRSF17",
    "SLAMF7",
    "PRDM1",
    "IRF4",
    "IGHG1",
    "IGHG2",
    "IGHG3",
    "IGHG4",
    "IGHA1",
    "IGHA2",
    "IGHM",
    "IGKC",
    "IGLC1",
    "IGLC2",
    "IGLC3",
    "IGLC6",
    "IGLC7",
}

PLASMA_PROGRAM_CANDIDATES = {
    "TXNDC5",
    "PIM2",
    "POU2AF1",
    "TENT5C",
    "SEC11C",
    "UBE2J1",
    "ITM2C",
    "CD79A",
}

BROAD_EXPRESSION_REVIEW = {
    "B2M",
    "VIM",
    "OAZ1",
    "TMSB4X",
    "TMSB10",
    "EEF2",
    "UBA52",
    "CYBA",
    "FBXW7",
    "OGT",
    "TAPBP",
    "CIRBP",
}


def read_tsv_gz(path: Path) -> list[list[str]]:
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
        return [line.rstrip("\n").split("\t") for line in fh]


def sample_paths(gsm: str, title: str) -> dict[str, Path]:
    prefix = f"{gsm}_{title}"
    return {
        "matrix": RAW / f"{prefix}_matrix.mtx.gz",
        "barcodes": RAW / f"{prefix}_barcodes.tsv.gz",
        "features": RAW / f"{prefix}_features.tsv.gz",
    }


def load_sample(gsm: str, title: str, group: str) -> tuple[csr_matrix, list[str], pd.DataFrame]:
    paths = sample_paths(gsm, title)
    features = read_tsv_gz(paths["features"])
    symbols = [r[1] if len(r) > 1 and r[1] else r[0] for r in features]
    barcodes = [r[0] for r in read_tsv_gz(paths["barcodes"])]
    with gzip.open(paths["matrix"], "rb") as fh:
        x = mmread(fh).tocsr().T.tocsr()
    if x.shape[0] != len(barcodes):
        raise ValueError(f"{title}: barcode count mismatch")
    meta = pd.DataFrame({"GSM": gsm, "Title": title, "Group": group, "barcode": barcodes})
    return x, symbols, meta


def log_normalize(x: csr_matrix) -> csr_matrix:
    totals = np.asarray(x.sum(axis=1)).ravel()
    factors = np.divide(10000.0, totals, out=np.zeros_like(totals, dtype=float), where=totals > 0)
    y = x.multiply(factors[:, None]).tocsr()
    y.data = np.log1p(y.data)
    return y


def safe_mannwhitney(mm: np.ndarray, control: np.ndarray) -> float:
    if len(np.unique(np.concatenate([mm, control]))) < 2:
        return 1.0
    try:
        return float(mannwhitneyu(mm, control, alternative="two-sided").pvalue)
    except ValueError:
        return 1.0


def cohen_d(mm: np.ndarray, control: np.ndarray) -> float:
    mm_sd = np.var(mm, ddof=1) if len(mm) > 1 else 0.0
    ctrl_sd = np.var(control, ddof=1) if len(control) > 1 else 0.0
    pooled = np.sqrt(((len(mm) - 1) * mm_sd + (len(control) - 1) * ctrl_sd) / max(len(mm) + len(control) - 2, 1))
    if pooled == 0:
        return 0.0
    return float((np.mean(mm) - np.mean(control)) / pooled)


def module_scores(x_log: csr_matrix, symbols: list[str], meta: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    symbol_to_idx: dict[str, list[int]] = {}
    for i, symbol in enumerate(symbols):
        symbol_to_idx.setdefault(symbol.upper(), []).append(i)

    scores = meta[["GSM", "Title", "Group", "barcode"]].copy()
    presence = []
    for name, genes in SIGNATURES.items():
        idx: list[int] = []
        present: list[str] = []
        for gene in genes:
            found = symbol_to_idx.get(gene.upper(), [])
            if found:
                idx.extend(found)
                present.append(gene)
        if idx:
            scores[f"{name}_score"] = np.asarray(x_log[:, idx].mean(axis=1)).ravel()
        else:
            scores[f"{name}_score"] = 0.0
        presence.append(
            {
                "signature": name,
                "genes_requested": ",".join(genes),
                "genes_present": ",".join(present),
                "n_present": len(present),
            }
        )
    return scores, pd.DataFrame(presence)


def sample_gene_tables(
    x_log: csr_matrix, x_raw: csr_matrix, symbols: list[str], meta: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows_mean = []
    rows_pct = []
    detected = x_raw.copy()
    detected.data = np.ones_like(detected.data)
    for title, sdf in meta.groupby("Title", sort=False):
        idx = sdf.index.to_numpy()
        group = str(sdf["Group"].iloc[0])
        gsm = str(sdf["GSM"].iloc[0])
        mean_log = np.asarray(x_log[idx].mean(axis=0)).ravel()
        pct = np.asarray(detected[idx].mean(axis=0)).ravel()
        for gene_idx, gene in enumerate(symbols):
            rows_mean.append(
                {
                    "GSM": gsm,
                    "Title": title,
                    "Group": group,
                    "gene": gene,
                    "mean_log_norm": mean_log[gene_idx],
                }
            )
            rows_pct.append(
                {
                    "GSM": gsm,
                    "Title": title,
                    "Group": group,
                    "gene": gene,
                    "pct_detected": pct[gene_idx],
                }
            )
    return pd.DataFrame(rows_mean), pd.DataFrame(rows_pct)


def broad_category(gene: str, best_region: str) -> str:
    g = gene.upper()
    if g in CANONICAL_PLASMA or g.startswith(("IGH", "IGK", "IGL")):
        return "canonical_plasma_support"
    if g in {x.upper() for x in SIGNATURES["myeloid_inflammatory"]}:
        return "myeloid_inflammatory"
    if g in {x.upper() for x in SIGNATURES["stromal_ecm"]}:
        return "stromal_ecm"
    if g in {x.upper() for x in SIGNATURES["t_nk_cytotoxic_exhaustion"]}:
        return "t_nk_or_exhaustion"
    if g in {x.upper() for x in SIGNATURES["endothelial_angiogenic"]}:
        return "endothelial_angiogenic"
    if g in {x.upper() for x in SIGNATURES["erythroid_megak"]}:
        return "erythroid_megak"
    if g in {x.upper() for x in SIGNATURES["cycling_proliferation"]}:
        return "cycling_proliferation"
    return f"region_linked_{best_region.replace('_score', '')}"


def spatial_region_contrasts(
    x_log: csr_matrix, symbols: list[str], meta: pd.DataFrame, scores: pd.DataFrame
) -> pd.DataFrame:
    score_cols = [c for c in scores.columns if c.endswith("_score")]
    merged = meta[["GSM", "Title", "Group", "barcode"]].merge(
        scores[["GSM", "barcode", *score_cols]], on=["GSM", "barcode"], how="left"
    )
    rows = []
    for score_col in score_cols:
        sample_deltas = []
        for title, sdf in merged.groupby("Title", sort=False):
            if sdf.shape[0] < 40:
                continue
            q75 = float(sdf[score_col].quantile(0.75))
            high_mask_local = sdf[score_col].to_numpy() > q75
            if high_mask_local.sum() < 20 or (~high_mask_local).sum() < 20:
                continue
            global_idx = sdf.index.to_numpy()
            high_idx = global_idx[high_mask_local]
            low_idx = global_idx[~high_mask_local]
            delta = np.asarray(x_log[high_idx].mean(axis=0)).ravel() - np.asarray(x_log[low_idx].mean(axis=0)).ravel()
            sample_deltas.append(delta)
        if not sample_deltas:
            continue
        mean_delta = np.vstack(sample_deltas).mean(axis=0)
        consistency = (np.vstack(sample_deltas) > 0).sum(axis=0)
        for i, gene in enumerate(symbols):
            rows.append(
                {
                    "gene": gene,
                    "region_signature": score_col.replace("_score", ""),
                    "region_high_minus_low_mean_log": mean_delta[i],
                    "region_positive_samples": int(consistency[i]),
                    "region_samples_tested": len(sample_deltas),
                }
            )
    return pd.DataFrame(rows)


def rank_candidates(
    sample_means: pd.DataFrame,
    sample_pct: pd.DataFrame,
    region_contrasts: pd.DataFrame,
    symbols: list[str],
) -> pd.DataFrame:
    symbol_counts = pd.Series(symbols).value_counts()
    unique_genes = set(symbol_counts[symbol_counts == 1].index)
    excluded_prefixes = ("MT-", "RPL", "RPS")

    pivot = sample_means.pivot_table(index="gene", columns="Title", values="mean_log_norm", aggfunc="mean")
    pct_pivot = sample_pct.pivot_table(index="gene", columns="Title", values="pct_detected", aggfunc="mean")
    sample_meta = pd.DataFrame(SAMPLES, columns=["GSM", "Title", "Group"])
    mm_titles = sample_meta.loc[sample_meta["Group"] == "MM", "Title"].tolist()
    ctrl_titles = sample_meta.loc[sample_meta["Group"] == "control", "Title"].tolist()

    region_best = (
        region_contrasts.sort_values(["gene", "region_high_minus_low_mean_log"], ascending=[True, False])
        .groupby("gene", as_index=False)
        .first()
    )
    region_best = region_best.set_index("gene")

    rows = []
    for gene in pivot.index:
        if gene not in unique_genes:
            continue
        gene_upper = gene.upper()
        if gene_upper.startswith(excluded_prefixes):
            continue
        if gene not in region_best.index:
            continue
        mm = pivot.loc[gene, mm_titles].to_numpy(dtype=float)
        ctrl = pivot.loc[gene, ctrl_titles].to_numpy(dtype=float)
        mm_pct = pct_pivot.loc[gene, mm_titles].to_numpy(dtype=float)
        ctrl_pct = pct_pivot.loc[gene, ctrl_titles].to_numpy(dtype=float)
        if np.nanmax(np.concatenate([mm_pct, ctrl_pct])) < 0.01:
            continue
        ctrl_median = float(np.nanmedian(ctrl))
        mm_above_ctrl_median = int(np.sum(mm > ctrl_median))
        mm_minus_ctrl = float(np.nanmean(mm) - np.nanmean(ctrl))
        d = cohen_d(mm, ctrl)
        p = safe_mannwhitney(mm, ctrl)
        region = region_best.loc[gene]
        region_delta = float(region["region_high_minus_low_mean_log"])
        region_consistency = int(region["region_positive_samples"])
        score = (
            max(mm_minus_ctrl, 0)
            * (mm_above_ctrl_median / max(len(mm_titles), 1))
            * (1 + max(region_delta, 0))
            * (0.5 + region_consistency / max(int(region["region_samples_tested"]), 1))
        )
        category = broad_category(gene, str(region["region_signature"]))
        if category == "canonical_plasma_support":
            priority = "supporting_marker"
        elif score >= 0.35 and mm_above_ctrl_median >= 4 and region_consistency >= 5:
            priority = "high"
        elif score >= 0.15 and mm_above_ctrl_median >= 3:
            priority = "medium"
        else:
            priority = "low"
        rows.append(
            {
                "gene": gene,
                "candidate_category": category,
                "validation_priority": priority,
                "mean_MM_sample_log_norm": float(np.nanmean(mm)),
                "mean_control_sample_log_norm": float(np.nanmean(ctrl)),
                "MM_minus_control_sample_log_norm": mm_minus_ctrl,
                "cohen_d_sample_level": d,
                "mannwhitney_p_sample_level": p,
                "MM_samples_above_control_median": mm_above_ctrl_median,
                "mean_MM_pct_detected": float(np.nanmean(mm_pct)),
                "mean_control_pct_detected": float(np.nanmean(ctrl_pct)),
                "best_spatial_region_signature": str(region["region_signature"]),
                "best_region_high_minus_low_mean_log": region_delta,
                "region_positive_samples": region_consistency,
                "region_samples_tested": int(region["region_samples_tested"]),
                "candidate_score": float(score),
            }
        )
    ranked = pd.DataFrame(rows)
    return ranked.sort_values(
        ["candidate_score", "MM_minus_control_sample_log_norm", "best_region_high_minus_low_mean_log"],
        ascending=False,
    )


def shortlist_role(row: pd.Series) -> str:
    gene = str(row["gene"]).upper()
    category = str(row["candidate_category"])
    if category == "canonical_plasma_support":
        return "canonical_plasma_anchor"
    if gene in PLASMA_PROGRAM_CANDIDATES:
        return "plasma_program_candidate"
    if gene in BROAD_EXPRESSION_REVIEW:
        return "broad_expression_review"
    if category in {
        "myeloid_inflammatory",
        "stromal_ecm",
        "t_nk_or_exhaustion",
        "endothelial_angiogenic",
        "erythroid_megak",
        "cycling_proliferation",
    }:
        return f"{category}_candidate"
    return "secondary_review"


def make_validation_shortlist(ranked: pd.DataFrame) -> pd.DataFrame:
    working = ranked.copy()
    working["shortlist_role"] = working.apply(shortlist_role, axis=1)
    keep_roles = {
        "canonical_plasma_anchor": 12,
        "plasma_program_candidate": 12,
        "myeloid_inflammatory_candidate": 8,
        "stromal_ecm_candidate": 8,
        "t_nk_or_exhaustion_candidate": 6,
        "endothelial_angiogenic_candidate": 5,
        "erythroid_megak_candidate": 5,
        "broad_expression_review": 8,
    }
    parts = []
    for role, n in keep_roles.items():
        sub = working[working["shortlist_role"] == role].head(n)
        if not sub.empty:
            parts.append(sub)
    if not parts:
        return working.head(50)
    shortlist = pd.concat(parts, ignore_index=True)
    return shortlist.sort_values(["shortlist_role", "candidate_score"], ascending=[True, False])


def sensitivity_signature_results(sample_scores: pd.DataFrame) -> pd.DataFrame:
    score_cols = [c for c in sample_scores.columns if c.endswith("_score")]
    subsets = {
        "all_samples": sample_scores,
        "exclude_hMM1_low_spot": sample_scores[sample_scores["Title"] != "hMM1"],
        "strong_depth_MM_hMM2_hMM3_plus_controls": sample_scores[
            sample_scores["Group"].eq("control") | sample_scores["Title"].isin(["hMM2", "hMM3"])
        ],
        "exclude_low_depth_hMM4_hMM5_hMM6_hMM1": sample_scores[
            sample_scores["Group"].eq("control") | sample_scores["Title"].isin(["hMM2", "hMM3"])
        ],
    }
    rows = []
    for subset_name, sdf in subsets.items():
        for score_col in score_cols:
            mm = sdf.loc[sdf["Group"] == "MM", score_col].to_numpy(float)
            ctrl = sdf.loc[sdf["Group"] == "control", score_col].to_numpy(float)
            if len(mm) == 0 or len(ctrl) == 0:
                continue
            rows.append(
                {
                    "subset": subset_name,
                    "signature": score_col.replace("_score", ""),
                    "n_MM": len(mm),
                    "n_control": len(ctrl),
                    "median_MM": float(np.nanmedian(mm)),
                    "median_control": float(np.nanmedian(ctrl)),
                    "MM_minus_control_median": float(np.nanmedian(mm) - np.nanmedian(ctrl)),
                    "cohen_d_sample_level": cohen_d(mm, ctrl),
                    "mannwhitney_p_sample_level": safe_mannwhitney(mm, ctrl),
                }
            )
    return pd.DataFrame(rows)


def plot_outputs(sample_scores: pd.DataFrame, sensitivity: pd.DataFrame, ranked: pd.DataFrame) -> None:
    score_cols = [c for c in sample_scores.columns if c.endswith("_score")]
    heat = sample_scores.set_index("Title")[score_cols]
    z = (heat - heat.mean(axis=0)) / heat.std(axis=0).replace(0, np.nan)
    z = z.fillna(0)
    row_colors = sample_scores.set_index("Title")["Group"].map({"control": "#4c78a8", "MM": "#f58518"})

    fig, ax = plt.subplots(figsize=(10, 4.8))
    im = ax.imshow(z.to_numpy(), aspect="auto", cmap="coolwarm", vmin=-2, vmax=2)
    ax.set_yticks(np.arange(z.shape[0]))
    ax.set_yticklabels(z.index)
    ax.set_xticks(np.arange(z.shape[1]))
    ax.set_xticklabels([c.replace("_score", "") for c in z.columns], rotation=40, ha="right")
    for i, color in enumerate(row_colors):
        ax.add_patch(plt.Rectangle((-0.65, i - 0.5), 0.15, 1, color=color, transform=ax.transData, clip_on=False))
    ax.set_title("Sample-level spatial signature scores")
    fig.colorbar(im, ax=ax, shrink=0.75, label="z-score")
    fig.tight_layout()
    fig.savefig(OUT / "sample_signature_score_heatmap.png", dpi=180)
    plt.close(fig)

    top = ranked.head(30).iloc[::-1]
    colors = top["candidate_category"].map(
        {
            "canonical_plasma_support": "#999999",
            "myeloid_inflammatory": "#e45756",
            "stromal_ecm": "#54a24b",
            "t_nk_or_exhaustion": "#4c78a8",
            "endothelial_angiogenic": "#72b7b2",
            "erythroid_megak": "#b279a2",
            "cycling_proliferation": "#f58518",
        }
    ).fillna("#bab0ac")
    fig, ax = plt.subplots(figsize=(9, 8))
    ax.barh(top["gene"], top["candidate_score"], color=colors)
    ax.set_xlabel("Candidate score")
    ax.set_title("Top sample-aware spatial candidate genes")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "top_candidate_genes_barplot.png", dpi=180)
    plt.close(fig)

    all_sens = sensitivity[sensitivity["subset"] == "all_samples"].sort_values("MM_minus_control_median")
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.barh(all_sens["signature"], all_sens["MM_minus_control_median"], color="#f58518")
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("MM minus control median score")
    ax.set_title("Sample-level signature effects")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "signature_effects_all_samples.png", dpi=180)
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
    clusters = pd.read_csv(PRELIM / "combined_spot_embedding_clusters.tsv.gz", sep="\t")
    meta = meta.merge(
        clusters[
            [
                "GSM",
                "Title",
                "Group",
                "barcode",
                "cluster",
                "total_counts",
                "n_genes",
                "pct_mt",
                "pxl_row_in_fullres",
                "pxl_col_in_fullres",
            ]
        ],
        on=["GSM", "Title", "Group", "barcode"],
        how="left",
    )
    if meta["cluster"].isna().any():
        raise ValueError("Missing cluster assignments after metadata merge")

    x_log = log_normalize(x_raw)
    scores, presence = module_scores(x_log, symbols, meta)
    presence.to_csv(OUT / "signature_gene_presence.tsv", sep="\t", index=False)
    scores.to_csv(OUT / "spot_signature_scores.tsv.gz", sep="\t", index=False, compression="gzip")

    score_cols = [c for c in scores.columns if c.endswith("_score")]
    sample_scores = scores.groupby(["GSM", "Title", "Group"], sort=False)[score_cols].median().reset_index()
    sample_scores.to_csv(OUT / "sample_signature_scores.tsv", sep="\t", index=False)

    cluster_scores = meta[["GSM", "Title", "Group", "barcode", "cluster"]].merge(
        scores[["GSM", "barcode", *score_cols]], on=["GSM", "barcode"], how="left"
    )
    cluster_scores.groupby(["cluster", "GSM", "Title", "Group"], sort=False)[score_cols].median().reset_index().to_csv(
        OUT / "sample_cluster_signature_scores.tsv", sep="\t", index=False
    )

    print("Computing sample-level gene means")
    sample_means, sample_pct = sample_gene_tables(x_log, x_raw, symbols, meta)
    sample_means.to_csv(OUT / "sample_gene_mean_log_norm.tsv.gz", sep="\t", index=False, compression="gzip")
    sample_pct.to_csv(OUT / "sample_gene_pct_detected.tsv.gz", sep="\t", index=False, compression="gzip")

    print("Computing spatial region contrasts")
    region_contrasts = spatial_region_contrasts(x_log, symbols, meta, scores)
    region_contrasts.to_csv(OUT / "gene_spatial_region_contrasts.tsv.gz", sep="\t", index=False, compression="gzip")

    print("Ranking candidates")
    ranked = rank_candidates(sample_means, sample_pct, region_contrasts, symbols)
    ranked.to_csv(OUT / "candidate_spatial_signature_table.tsv", sep="\t", index=False)
    ranked.head(100).to_csv(OUT / "candidate_spatial_signature_top100.tsv", sep="\t", index=False)
    make_validation_shortlist(ranked).to_csv(OUT / "candidate_validation_shortlist.tsv", sep="\t", index=False)

    sensitivity = sensitivity_signature_results(sample_scores)
    sensitivity.to_csv(OUT / "signature_sensitivity_results.tsv", sep="\t", index=False)

    plot_outputs(sample_scores, sensitivity, ranked)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
