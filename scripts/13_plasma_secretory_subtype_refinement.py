from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


PROJECT = Path.cwd()
IN = PROJECT / "analysis" / "bulk_clinical_validation" / "bulk_clinical_sample_scores.tsv"
OUT = PROJECT / "analysis" / "plasma_secretory_subtype_refinement"
REPORTS = PROJECT / "reports" / "validation"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

CLINICAL_MODULE_GENES = ["POU2AF1", "XBP1", "JCHAIN"]
AXIS_VARIABLES = [
    "clinical_subtype_module_score_z",
    "plasma_secretory_score_z",
    "TXNDC5_z",
    "POU2AF1_z",
    "XBP1_z",
    "JCHAIN_z",
]


def zscore(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    std = values.std(skipna=True)
    if pd.isna(std) or std == 0:
        return pd.Series(np.nan, index=series.index)
    return (values - values.mean(skipna=True)) / std


def bh_fdr(values: pd.Series) -> pd.Series:
    p = pd.to_numeric(values, errors="coerce")
    out = pd.Series(np.nan, index=values.index, dtype=float)
    valid = p.dropna()
    if valid.empty:
        return out
    order = valid.sort_values().index
    ranked = valid.loc[order].to_numpy(float)
    n = len(ranked)
    adjusted = ranked * n / np.arange(1, n + 1)
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
    out.loc[order] = np.clip(adjusted, 0, 1)
    return out


def rank_auc(values: np.ndarray, y: np.ndarray) -> float:
    pos = y == 1
    neg = y == 0
    n_pos = int(pos.sum())
    n_neg = int(neg.sum())
    if n_pos == 0 or n_neg == 0:
        return np.nan
    ranks = stats.rankdata(values)
    u = ranks[pos].sum() - n_pos * (n_pos + 1) / 2
    return float(u / (n_pos * n_neg))


def binary_association(df: pd.DataFrame, dataset: str, variable: str, outcome: str, label: str) -> dict[str, object]:
    sub = df[[variable, outcome]].dropna()
    sub = sub[sub[outcome].isin([0, 1])]
    result: dict[str, object] = {
        "dataset": dataset,
        "variable": variable,
        "outcome": outcome,
        "outcome_label": label,
        "test_family": "binary",
        "n": int(len(sub)),
        "n_event": int((sub[outcome] == 1).sum()) if len(sub) else 0,
        "n_nonevent": int((sub[outcome] == 0).sum()) if len(sub) else 0,
    }
    if result["n_event"] == 0 or result["n_nonevent"] == 0:
        return result
    event_vals = sub.loc[sub[outcome] == 1, variable].to_numpy(float)
    nonevent_vals = sub.loc[sub[outcome] == 0, variable].to_numpy(float)
    cutoff = float(np.nanmedian(sub[variable]))
    high = sub[variable] >= cutoff
    table = pd.crosstab(high, sub[outcome])
    for idx in [False, True]:
        if idx not in table.index:
            table.loc[idx] = 0
    for col in [0, 1]:
        if col not in table.columns:
            table[col] = 0
    table = table.sort_index().sort_index(axis=1)
    fisher_table = [[int(table.loc[True, 1]), int(table.loc[True, 0])], [int(table.loc[False, 1]), int(table.loc[False, 0])]]
    fisher_or, fisher_p = stats.fisher_exact(fisher_table)
    result.update(
        {
            "median_event": float(np.nanmedian(event_vals)),
            "median_nonevent": float(np.nanmedian(nonevent_vals)),
            "delta_event_minus_nonevent": float(np.nanmedian(event_vals) - np.nanmedian(nonevent_vals)),
            "mannwhitney_p": float(stats.mannwhitneyu(event_vals, nonevent_vals, alternative="two-sided").pvalue),
            "auc_event": rank_auc(sub[variable].to_numpy(float), sub[outcome].to_numpy(float)),
            "median_split_or": float(fisher_or),
            "median_split_fisher_p": float(fisher_p),
            "high_event_count": int(fisher_table[0][0]),
            "high_nonevent_count": int(fisher_table[0][1]),
            "low_event_count": int(fisher_table[1][0]),
            "low_nonevent_count": int(fisher_table[1][1]),
        }
    )
    return result


def logrank_association(df: pd.DataFrame, dataset: str, variable: str, time_col: str, event_col: str, label: str) -> dict[str, object]:
    sub = df[[variable, time_col, event_col]].dropna()
    sub = sub[(sub[time_col] > 0) & sub[event_col].isin([0, 1])]
    result: dict[str, object] = {
        "dataset": dataset,
        "variable": variable,
        "outcome": f"{time_col}/{event_col}",
        "outcome_label": label,
        "test_family": "survival_logrank",
        "n": int(len(sub)),
        "n_event": int((sub[event_col] == 1).sum()) if len(sub) else 0,
    }
    if len(sub) < 10 or result["n_event"] == 0:
        return result
    cutoff = float(np.nanmedian(sub[variable]))
    high = (sub[variable] >= cutoff).to_numpy(bool)
    times = sub[time_col].to_numpy(float)
    events = sub[event_col].to_numpy(int)
    oe = 0.0
    var = 0.0
    for event_time in np.unique(times[events == 1]):
        risk = times >= event_time
        n_total = int(risk.sum())
        n_high = int((risk & high).sum())
        n_low = n_total - n_high
        d_total = int(((times == event_time) & (events == 1)).sum())
        d_high = int(((times == event_time) & (events == 1) & high).sum())
        if n_total <= 1 or d_total == 0:
            continue
        expected_high = d_total * (n_high / n_total)
        variance = n_high * n_low * d_total * (n_total - d_total) / (n_total**2 * (n_total - 1))
        oe += d_high - expected_high
        var += variance
    chi2 = (oe * oe / var) if var > 0 else np.nan
    result.update(
        {
            "high_n": int(high.sum()),
            "low_n": int((~high).sum()),
            "high_events": int((events[high] == 1).sum()),
            "low_events": int((events[~high] == 1).sum()),
            "high_median_time": float(np.nanmedian(times[high])) if high.any() else np.nan,
            "low_median_time": float(np.nanmedian(times[~high])) if (~high).any() else np.nan,
            "logrank_chi2": float(chi2) if not math.isnan(chi2) else np.nan,
            "logrank_p": float(stats.chi2.sf(chi2, df=1)) if not math.isnan(chi2) else np.nan,
        }
    )
    return result


def add_fdr(assoc: pd.DataFrame) -> pd.DataFrame:
    out = assoc.copy()
    for p_col in ["mannwhitney_p", "median_split_fisher_p", "logrank_p"]:
        if p_col not in out:
            continue
        fdr_col = p_col.replace("_p", "_fdr")
        out[fdr_col] = np.nan
        for (_, outcome, family), idx in out.groupby(["dataset", "outcome", "test_family"]).groups.items():
            out.loc[idx, fdr_col] = bh_fdr(out.loc[idx, p_col])
    p_cols = [col for col in ["mannwhitney_fdr", "median_split_fisher_fdr", "logrank_fdr"] if col in out]
    out["best_fdr"] = out[p_cols].min(axis=1, skipna=True)
    return out


def add_axis_scores(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for dataset, idx in out.groupby("dataset").groups.items():
        for gene in ["TXNDC5", *CLINICAL_MODULE_GENES]:
            out.loc[idx, f"{gene}_z"] = zscore(out.loc[idx, gene])
        module_cols = [f"{gene}_z" for gene in CLINICAL_MODULE_GENES]
        out.loc[idx, "clinical_subtype_module_score_z"] = out.loc[idx, module_cols].mean(axis=1, skipna=True)
        cutoff = out.loc[idx, "clinical_subtype_module_score_z"].median(skipna=True)
        out.loc[idx, "clinical_subtype_state"] = np.where(out.loc[idx, "clinical_subtype_module_score_z"] >= cutoff, "module_high", "module_low")
    return out


def km_curve(times: np.ndarray, events: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    order = np.argsort(times)
    times = times[order]
    events = events[order]
    unique_event_times = np.unique(times[events == 1])
    xs = [0.0]
    ys = [1.0]
    survival = 1.0
    for t in unique_event_times:
        at_risk = np.sum(times >= t)
        deaths = np.sum((times == t) & (events == 1))
        if at_risk > 0:
            survival *= 1 - deaths / at_risk
        xs.extend([float(t), float(t)])
        ys.extend([ys[-1], survival])
    if len(times):
        xs.append(float(np.max(times)))
        ys.append(ys[-1])
    return np.array(xs), np.array(ys)


def simple_boxplot(df: pd.DataFrame, value: str, group: str, title: str, ylabel: str, path: Path, labels: dict[object, str] | None = None) -> None:
    sub = df[[value, group]].dropna()
    groups = list(sorted(sub[group].unique()))
    data = [sub.loc[sub[group] == g, value].to_numpy(float) for g in groups]
    names = [labels.get(g, str(g)) if labels else str(g) for g in groups]
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    bp = ax.boxplot(data, patch_artist=True, widths=0.55, showfliers=False)
    colors = ["#d8e2dc", "#b56576", "#6d597a", "#355070"]
    for patch, color in zip(bp["boxes"], colors):
        patch.set(facecolor=color, alpha=0.78, edgecolor="#222222", linewidth=1.0)
    for i, vals in enumerate(data, start=1):
        jitter = np.linspace(-0.12, 0.12, len(vals)) if len(vals) else []
        if len(vals) > 80:
            rng = np.random.default_rng(13)
            jitter = rng.uniform(-0.14, 0.14, len(vals))
        ax.scatter(np.full(len(vals), i) + jitter, vals, s=12, alpha=0.45, color="#222222", linewidths=0)
    ax.set_xticklabels(names)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def association_barplot(assoc: pd.DataFrame, path: Path) -> None:
    sub = assoc.dropna(subset=["best_fdr"]).copy()
    sub = sub.sort_values("best_fdr").head(12)
    if sub.empty:
        return
    sub["label"] = sub["dataset"] + " | " + sub["outcome"] + " | " + sub["variable"]
    sub["neg_log10_fdr"] = -np.log10(sub["best_fdr"].clip(lower=1e-12))
    fig, ax = plt.subplots(figsize=(9, 5.5))
    colors = np.where(sub["best_fdr"] < 0.05, "#b56576", "#6d6875")
    ax.barh(np.arange(len(sub)), sub["neg_log10_fdr"], color=colors)
    ax.set_yticks(np.arange(len(sub)))
    ax.set_yticklabels(sub["label"], fontsize=8)
    ax.invert_yaxis()
    ax.axvline(-np.log10(0.05), color="#222222", linewidth=1, linestyle="--")
    ax.set_xlabel("-log10(FDR)")
    ax.set_title("Top clinical associations for plasma-secretory subtype axis")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def correlation_heatmap(df: pd.DataFrame, dataset: str, path: Path) -> None:
    cols = ["plasma_secretory_score_z", "TXNDC5_z", "clinical_subtype_module_score_z", "POU2AF1_z", "XBP1_z", "JCHAIN_z"]
    sub = df[df["dataset"] == dataset][cols].dropna()
    if sub.empty:
        return
    corr = sub.corr(method="spearman")
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    im = ax.imshow(corr, vmin=-1, vmax=1, cmap="RdBu_r")
    ax.set_xticks(np.arange(len(cols)))
    ax.set_yticks(np.arange(len(cols)))
    short = ["Plasma score", "TXNDC5", "Module", "POU2AF1", "XBP1", "JCHAIN"]
    ax.set_xticklabels(short, rotation=45, ha="right")
    ax.set_yticklabels(short)
    for i in range(corr.shape[0]):
        for j in range(corr.shape[1]):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Spearman r")
    ax.set_title(f"{dataset}: axis correlation")
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def km_plot(df: pd.DataFrame, variable: str, path: Path) -> None:
    sub = df[(df["dataset"] == "GSE2658")][[variable, "SURTIM", "SURIND"]].dropna()
    sub = sub[(sub["SURTIM"] > 0) & sub["SURIND"].isin([0, 1])]
    if sub.empty:
        return
    cutoff = sub[variable].median()
    groups = {
        "module low": sub[sub[variable] < cutoff],
        "module high": sub[sub[variable] >= cutoff],
    }
    fig, ax = plt.subplots(figsize=(5.8, 4.4))
    colors = {"module low": "#4a4e69", "module high": "#b56576"}
    for name, group in groups.items():
        xs, ys = km_curve(group["SURTIM"].to_numpy(float), group["SURIND"].to_numpy(int))
        ax.step(xs, ys, where="post", label=f"{name} (n={len(group)})", color=colors[name], linewidth=2)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("Follow-up time, months")
    ax.set_ylabel("Disease-related survival probability")
    ax.set_title("GSE2658: clinical subtype module survival split")
    ax.legend(frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def format_p(value: object) -> str:
    try:
        number = float(value)
    except Exception:
        return "NA"
    if math.isnan(number):
        return "NA"
    if number < 0.001:
        return f"{number:.2e}"
    return f"{number:.4f}"


def write_report(df: pd.DataFrame, assoc: pd.DataFrame) -> None:
    report = REPORTS / "PLASMA_SECRETORY_SUBTYPE_REFINEMENT_REPORT.md"
    lines: list[str] = []
    lines.append("# Plasma-Secretory Clinical Subtype Refinement Report")
    lines.append("")
    lines.append("Date: 2026-04-29")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append("- Refine the manuscript direction from a single-gene TXNDC5 prognostic claim to a plasma-secretory clinical-subtype axis.")
    lines.append("- Treat TXNDC5 as a spatial/single-cell localization candidate.")
    lines.append("- Treat POU2AF1, XBP1, and JCHAIN as the clinical subtype / risk-linking module.")
    lines.append("")
    lines.append("## Module Definition")
    lines.append("")
    lines.append("- Clinical subtype module: mean within-cohort z-score of `POU2AF1`, `XBP1`, and `JCHAIN`.")
    lines.append("- Module state: median split within each dataset into `module_high` and `module_low`.")
    lines.append("")
    lines.append("## Main Results")
    lines.append("")
    top = assoc.dropna(subset=["best_fdr"]).sort_values("best_fdr").head(10)
    if top.empty:
        lines.append("- No subtype-axis associations were available.")
    else:
        lines.append("| Dataset | Outcome | Variable | n | Events | Effect | Best FDR |")
        lines.append("|---|---|---|---:|---:|---:|---:|")
        for _, row in top.iterrows():
            effect = row.get("delta_event_minus_nonevent", np.nan)
            if pd.isna(effect):
                effect = row.get("logrank_chi2", np.nan)
            lines.append(
                f"| {row['dataset']} | {row['outcome']} | {row['variable']} | {int(row.get('n', 0))} | "
                f"{int(row.get('n_event', 0)) if pd.notna(row.get('n_event', np.nan)) else ''} | {format_p(effect)} | {format_p(row['best_fdr'])} |"
            )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("- The strongest FDR-stable signal remains the GSE2658 1q21 amplification association for POU2AF1/XBP1/JCHAIN-related expression.")
    lines.append("- The combined POU2AF1/XBP1/JCHAIN module is suitable as a clinical subtype axis, but its survival signal is exploratory and needs CoMMpass or another external clinical cohort.")
    lines.append("- TXNDC5 should remain in the manuscript as a spatial and single-cell-supported plasma-localization marker, not as the current main clinical-risk marker.")
    lines.append("")
    lines.append("## Outputs")
    lines.append("")
    for name in [
        "plasma_secretory_subtype_sample_scores.tsv",
        "plasma_secretory_subtype_associations.tsv",
        "plasma_secretory_subtype_fdr_ranked.tsv",
        "plasma_secretory_subtype_effect_summary.tsv",
        "subtype_top_associations_barplot.png",
        "gse2658_module_by_1q21.png",
        "gse24080_xbp1_by_os.png",
        "gse2658_module_survival_km.png",
        "gse24080_axis_correlation_heatmap.png",
        "gse2658_axis_correlation_heatmap.png",
    ]:
        if (OUT / name).exists():
            lines.append(f"- `{(OUT / name).relative_to(PROJECT)}`")
    lines.append("")
    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    df = pd.read_csv(IN, sep="\t")
    df = add_axis_scores(df)
    df.to_csv(OUT / "plasma_secretory_subtype_sample_scores.tsv", sep="\t", index=False)

    rows: list[dict[str, object]] = []
    gse24080 = df[df["dataset"] == "GSE24080"].copy()
    for outcome, label in [("efs_24mo_event", "24-month EFS event"), ("os_24mo_event", "24-month OS death")]:
        for variable in AXIS_VARIABLES:
            rows.append(binary_association(gse24080, "GSE24080", variable, outcome, label))
    gse2658 = df[df["dataset"] == "GSE2658"].copy()
    for variable in AXIS_VARIABLES:
        rows.append(binary_association(gse2658, "GSE2658", variable, "SURIND", "Disease-related death indicator"))
        rows.append(logrank_association(gse2658, "GSE2658", variable, "SURTIM", "SURIND", "Disease-related survival"))
        rows.append(binary_association(gse2658, "GSE2658", variable, "AMP_high_3plus", "FISH 1q21 amplification >=3 copies"))
    assoc = add_fdr(pd.DataFrame(rows))
    assoc.to_csv(OUT / "plasma_secretory_subtype_associations.tsv", sep="\t", index=False)
    assoc.dropna(subset=["best_fdr"]).sort_values("best_fdr").to_csv(OUT / "plasma_secretory_subtype_fdr_ranked.tsv", sep="\t", index=False)

    effect_cols = [
        "dataset",
        "variable",
        "outcome",
        "outcome_label",
        "n",
        "n_event",
        "delta_event_minus_nonevent",
        "auc_event",
        "median_split_or",
        "mannwhitney_p",
        "mannwhitney_fdr",
        "median_split_fisher_p",
        "median_split_fisher_fdr",
        "logrank_chi2",
        "logrank_p",
        "logrank_fdr",
        "best_fdr",
    ]
    assoc[[col for col in effect_cols if col in assoc.columns]].to_csv(OUT / "plasma_secretory_subtype_effect_summary.tsv", sep="\t", index=False)

    association_barplot(assoc, OUT / "subtype_top_associations_barplot.png")
    simple_boxplot(
        gse2658,
        "clinical_subtype_module_score_z",
        "AMP_high_3plus",
        "GSE2658: clinical subtype module by 1q21 amplification",
        "POU2AF1/XBP1/JCHAIN module score",
        OUT / "gse2658_module_by_1q21.png",
        labels={0.0: "2 copies", 1.0: "3+ copies"},
    )
    simple_boxplot(
        gse24080,
        "XBP1_z",
        "os_24mo_event",
        "GSE24080: XBP1 by 24-month OS outcome",
        "XBP1 z-score",
        OUT / "gse24080_xbp1_by_os.png",
        labels={0.0: "alive at 24 mo", 1.0: "death by 24 mo"},
    )
    km_plot(df, "clinical_subtype_module_score_z", OUT / "gse2658_module_survival_km.png")
    correlation_heatmap(df, "GSE24080", OUT / "gse24080_axis_correlation_heatmap.png")
    correlation_heatmap(df, "GSE2658", OUT / "gse2658_axis_correlation_heatmap.png")
    write_report(df, assoc)


if __name__ == "__main__":
    main()
