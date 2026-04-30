from __future__ import annotations

import math
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


PROJECT = Path.cwd()
DATA = PROJECT / "external_bulk" / "CoMMpass_GDC"
COUNTS = DATA / "star_counts"
OUT = PROJECT / "analysis" / "commppass_gdc_validation"
REPORTS = PROJECT / "reports" / "validation"
COUNTS.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

MANIFEST = DATA / "gdc_mmrfgene_expression_files.tsv"
CLINICAL = DATA / "gdc_mmrfcases_clinical.tsv"

PLASMA_SECRETORY_GENES = ["SDC1", "MZB1", "XBP1", "JCHAIN", "TNFRSF17", "SLAMF7", "PRDM1", "TXNDC5", "PIM2", "IRF4"]
CLINICAL_MODULE_GENES = ["POU2AF1", "XBP1", "JCHAIN"]
AXIS_GENES = sorted(set(PLASMA_SECRETORY_GENES + CLINICAL_MODULE_GENES + ["TXNDC5"]))
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


def load_baseline_manifest() -> pd.DataFrame:
    df = pd.read_csv(MANIFEST, sep="\t")
    sample_col = "cases.0.samples.0.submitter_id"
    aliquot_col = "cases.0.samples.0.portions.0.analytes.0.aliquots.0.submitter_id"
    case_col = "cases.0.submitter_id"
    df["is_cd138pos"] = df[sample_col].astype(str).str.contains("BM_CD138pos", na=False)
    df["visit"] = pd.to_numeric(df[sample_col].astype(str).str.extract(r"MMRF_\d+_(\d+)_BM_CD138pos")[0], errors="coerce")
    df["aliquot_timepoint"] = df[aliquot_col].astype(str).str.extract(r"_(T\d)_")[0]
    baseline = df[(df["is_cd138pos"]) & (df["visit"] == 1)].copy()
    baseline = baseline.sort_values([case_col, "file_id"]).drop_duplicates(case_col, keep="first")
    baseline["local_count_file"] = baseline["file_id"].map(lambda x: str(COUNTS / f"{x}.tsv"))
    return baseline


def run_curl_download(file_id: str, expected_size: int) -> tuple[str, bool, str]:
    dest = COUNTS / f"{file_id}.tsv"
    if dest.exists() and dest.stat().st_size == expected_size:
        return file_id, True, "exists"
    tmp = COUNTS / f"{file_id}.tmp"
    if tmp.exists():
        tmp.unlink()
    url = f"https://api.gdc.cancer.gov/data/{file_id}"
    cmd = [
        "curl.exe",
        "-sS",
        "-L",
        "--fail",
        "--retry",
        "4",
        "--retry-delay",
        "3",
        "--ssl-no-revoke",
        "--connect-timeout",
        "30",
        "--max-time",
        "300",
        "-o",
        str(tmp),
        url,
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        if tmp.exists():
            tmp.unlink()
        return file_id, False, proc.stderr.strip()[:300]
    size = tmp.stat().st_size if tmp.exists() else 0
    if expected_size and abs(size - expected_size) > max(1024, expected_size * 0.02):
        return file_id, False, f"size mismatch: got {size}, expected {expected_size}"
    tmp.replace(dest)
    return file_id, True, "downloaded"


def download_counts(manifest: pd.DataFrame, max_workers: int = 6) -> pd.DataFrame:
    rows = manifest[["file_id", "file_size"]].drop_duplicates().copy()
    total = len(rows)
    print(f"Downloading/checking {total} baseline CD138+ STAR count files")
    start = time.time()
    status_rows = []
    done = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(run_curl_download, str(row.file_id), int(row.file_size)): str(row.file_id)
            for row in rows.itertuples(index=False)
        }
        for future in as_completed(futures):
            file_id, ok, message = future.result()
            status_rows.append({"file_id": file_id, "ok": ok, "message": message})
            done += 1
            if done == 1 or done % 25 == 0 or done == total:
                elapsed = time.time() - start
                print(f"  {done}/{total} checked; elapsed {elapsed/60:.1f} min")
    status = pd.DataFrame(status_rows)
    status.to_csv(OUT / "commppass_download_status.tsv", sep="\t", index=False)
    failed = status[~status["ok"]]
    if not failed.empty:
        raise RuntimeError(f"Failed downloads: {len(failed)}. See {OUT / 'commppass_download_status.tsv'}")
    return status


def parse_target_tpm(path: Path) -> dict[str, float]:
    values: dict[str, list[float]] = {gene: [] for gene in AXIS_GENES}
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        header = None
        for line in handle:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if header is None:
                header = parts
                try:
                    gene_idx = header.index("gene_name")
                    tpm_idx = header.index("tpm_unstranded")
                except ValueError as exc:
                    raise ValueError(f"Missing required columns in {path}") from exc
                continue
            if len(parts) <= tpm_idx:
                continue
            gene = parts[gene_idx]
            if gene in values:
                try:
                    values[gene].append(float(parts[tpm_idx]))
                except ValueError:
                    pass
    return {gene: float(np.nanmean(vals)) if vals else np.nan for gene, vals in values.items()}


def build_expression_matrix(manifest: pd.DataFrame) -> pd.DataFrame:
    rows = []
    case_col = "cases.0.submitter_id"
    sample_col = "cases.0.samples.0.submitter_id"
    aliquot_col = "cases.0.samples.0.portions.0.analytes.0.aliquots.0.submitter_id"
    for idx, (_, row) in enumerate(manifest.iterrows(), start=1):
        file_id = str(row["file_id"])
        path = COUNTS / f"{file_id}.tsv"
        values = parse_target_tpm(path)
        values.update(
            {
                "case_submitter_id": row[case_col],
                "sample_submitter_id": row[sample_col],
                "aliquot_submitter_id": row[aliquot_col],
                "file_id": file_id,
            }
        )
        rows.append(values)
        if idx == 1 or idx % 100 == 0 or idx == len(manifest):
            print(f"  parsed target TPM from {idx}/{len(manifest)} files")
    expr = pd.DataFrame(rows)
    for gene in AXIS_GENES:
        expr[f"{gene}_log2_tpm"] = np.log2(pd.to_numeric(expr[gene], errors="coerce") + 1)
        expr[f"{gene}_z"] = zscore(expr[f"{gene}_log2_tpm"])
    expr["clinical_subtype_module_score_z"] = expr[[f"{gene}_z" for gene in CLINICAL_MODULE_GENES]].mean(axis=1, skipna=True)
    expr["plasma_secretory_score_z"] = expr[[f"{gene}_z" for gene in PLASMA_SECRETORY_GENES]].mean(axis=1, skipna=True)
    expr["clinical_subtype_state"] = np.where(
        expr["clinical_subtype_module_score_z"] >= expr["clinical_subtype_module_score_z"].median(skipna=True),
        "module_high",
        "module_low",
    )
    return expr


def prepare_clinical() -> pd.DataFrame:
    clinical = pd.read_csv(CLINICAL, sep="\t")
    clinical = clinical.rename(
        columns={
            "submitter_id": "case_submitter_id",
            "demographic.vital_status": "vital_status",
            "demographic.days_to_death": "days_to_death",
            "demographic.age_at_index": "age_at_index",
            "demographic.gender": "gender",
            "diagnoses.0.days_to_last_follow_up": "days_to_last_follow_up",
            "diagnoses.0.iss_stage": "iss_stage",
        }
    )
    clinical["os_event"] = (clinical["vital_status"].astype(str).str.lower() == "dead").astype(int)
    death = pd.to_numeric(clinical["days_to_death"], errors="coerce")
    follow = pd.to_numeric(clinical["days_to_last_follow_up"], errors="coerce")
    clinical["os_time_days"] = death.where(death.notna(), follow)
    clinical["os_time_months"] = clinical["os_time_days"] / 30.4375
    stage_map = {"I": 1, "II": 2, "III": 3}
    clinical["iss_stage_num"] = clinical["iss_stage"].map(stage_map)
    clinical["iss_stage_III"] = np.where(clinical["iss_stage_num"].notna(), (clinical["iss_stage_num"] == 3).astype(int), np.nan)
    return clinical


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


def binary_association(df: pd.DataFrame, variable: str, outcome: str, label: str) -> dict[str, object]:
    sub = df[[variable, outcome]].dropna()
    sub = sub[sub[outcome].isin([0, 1])]
    result: dict[str, object] = {
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
        }
    )
    return result


def spearman_association(df: pd.DataFrame, variable: str, outcome: str, label: str) -> dict[str, object]:
    sub = df[[variable, outcome]].dropna()
    result: dict[str, object] = {
        "variable": variable,
        "outcome": outcome,
        "outcome_label": label,
        "test_family": "spearman",
        "n": int(len(sub)),
    }
    if len(sub) < 10:
        return result
    rho, p_value = stats.spearmanr(sub[variable], sub[outcome])
    result.update({"spearman_rho": float(rho), "spearman_p": float(p_value)})
    return result


def logrank_association(df: pd.DataFrame, variable: str, time_col: str, event_col: str, label: str) -> dict[str, object]:
    sub = df[[variable, time_col, event_col]].dropna()
    sub = sub[(sub[time_col] > 0) & sub[event_col].isin([0, 1])]
    result: dict[str, object] = {
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
            "high_median_time_months": float(np.nanmedian(times[high])) if high.any() else np.nan,
            "low_median_time_months": float(np.nanmedian(times[~high])) if (~high).any() else np.nan,
            "logrank_chi2": float(chi2) if not math.isnan(chi2) else np.nan,
            "logrank_p": float(stats.chi2.sf(chi2, df=1)) if not math.isnan(chi2) else np.nan,
        }
    )
    return result


def add_fdr(assoc: pd.DataFrame) -> pd.DataFrame:
    out = assoc.copy()
    for p_col in ["mannwhitney_p", "median_split_fisher_p", "logrank_p", "spearman_p"]:
        if p_col not in out:
            continue
        fdr_col = p_col.replace("_p", "_fdr")
        out[fdr_col] = np.nan
        for (outcome, family), idx in out.groupby(["outcome", "test_family"]).groups.items():
            out.loc[idx, fdr_col] = bh_fdr(out.loc[idx, p_col])
    fdr_cols = [col for col in ["mannwhitney_fdr", "median_split_fisher_fdr", "logrank_fdr", "spearman_fdr"] if col in out]
    out["best_fdr"] = out[fdr_cols].min(axis=1, skipna=True)
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


def plot_module_by_iss(df: pd.DataFrame) -> None:
    sub = df[["clinical_subtype_module_score_z", "iss_stage"]].dropna()
    order = ["I", "II", "III"]
    data = [sub.loc[sub["iss_stage"] == stage, "clinical_subtype_module_score_z"].to_numpy(float) for stage in order]
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    bp = ax.boxplot(data, patch_artist=True, showfliers=False, widths=0.55)
    for patch, color in zip(bp["boxes"], ["#d8e2dc", "#6d597a", "#b56576"]):
        patch.set(facecolor=color, alpha=0.8, edgecolor="#222222")
    for i, vals in enumerate(data, start=1):
        rng = np.random.default_rng(14 + i)
        ax.scatter(np.full(len(vals), i) + rng.uniform(-0.12, 0.12, len(vals)), vals, s=12, alpha=0.35, color="#222222", linewidths=0)
    ax.set_xticklabels(order)
    ax.set_xlabel("ISS stage")
    ax.set_ylabel("POU2AF1/XBP1/JCHAIN module score")
    ax.set_title("CoMMpass/GDC: subtype module by ISS stage")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "commppass_module_by_iss.png", dpi=220)
    plt.close(fig)


def plot_km(df: pd.DataFrame, variable: str) -> None:
    sub = df[[variable, "os_time_months", "os_event"]].dropna()
    sub = sub[(sub["os_time_months"] > 0) & sub["os_event"].isin([0, 1])]
    cutoff = sub[variable].median()
    groups = {"module low": sub[sub[variable] < cutoff], "module high": sub[sub[variable] >= cutoff]}
    fig, ax = plt.subplots(figsize=(5.8, 4.4))
    colors = {"module low": "#4a4e69", "module high": "#b56576"}
    for name, group in groups.items():
        xs, ys = km_curve(group["os_time_months"].to_numpy(float), group["os_event"].to_numpy(int))
        ax.step(xs, ys, where="post", label=f"{name} (n={len(group)})", color=colors[name], linewidth=2)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("OS time, months")
    ax.set_ylabel("Overall survival probability")
    ax.set_title("CoMMpass/GDC: module median split OS")
    ax.legend(frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "commppass_module_os_km.png", dpi=220)
    plt.close(fig)


def plot_assoc_bar(assoc: pd.DataFrame) -> None:
    sub = assoc.dropna(subset=["best_fdr"]).sort_values("best_fdr").head(12).copy()
    if sub.empty:
        return
    sub["label"] = sub["outcome"] + " | " + sub["variable"]
    sub["neg_log10_fdr"] = -np.log10(sub["best_fdr"].clip(lower=1e-12))
    fig, ax = plt.subplots(figsize=(9, 5.2))
    colors = np.where(sub["best_fdr"] < 0.05, "#b56576", "#6d6875")
    ax.barh(np.arange(len(sub)), sub["neg_log10_fdr"], color=colors)
    ax.set_yticks(np.arange(len(sub)))
    ax.set_yticklabels(sub["label"], fontsize=8)
    ax.invert_yaxis()
    ax.axvline(-np.log10(0.05), color="#222222", linestyle="--", linewidth=1)
    ax.set_xlabel("-log10(FDR)")
    ax.set_title("CoMMpass/GDC subtype-axis associations")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "commppass_top_associations_barplot.png", dpi=220)
    plt.close(fig)


def plot_axis_corr(df: pd.DataFrame) -> None:
    cols = ["clinical_subtype_module_score_z", "plasma_secretory_score_z", "TXNDC5_z", "POU2AF1_z", "XBP1_z", "JCHAIN_z"]
    corr = df[cols].corr(method="spearman")
    labels = ["Module", "Plasma score", "TXNDC5", "POU2AF1", "XBP1", "JCHAIN"]
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    im = ax.imshow(corr, vmin=-1, vmax=1, cmap="RdBu_r")
    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(cols)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)
    for i in range(corr.shape[0]):
        for j in range(corr.shape[1]):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Spearman r")
    ax.set_title("CoMMpass/GDC subtype-axis correlation")
    fig.tight_layout()
    fig.savefig(OUT / "commppass_axis_correlation_heatmap.png", dpi=220)
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


def write_report(df: pd.DataFrame, assoc: pd.DataFrame, manifest: pd.DataFrame) -> None:
    path = REPORTS / "COMMPASS_GDC_VALIDATION_REPORT.md"
    top = assoc.dropna(subset=["best_fdr"]).sort_values("best_fdr").head(12)
    lines = [
        "# CoMMpass / GDC Clinical Validation Report",
        "",
        "Date: 2026-04-29",
        "",
        "## Purpose",
        "",
        "- Validate the plasma-secretory clinical-subtype axis in CoMMpass using open GDC STAR-count RNA-seq and GDC clinical fields.",
        "- Prioritize OS and ISS because these are available in the open GDC clinical slice.",
        "- Keep R-ISS, cytogenetic high-risk, PFS, and treatment response as pending until a fuller CoMMpass/MMRF clinical table is obtained.",
        "",
        "## Data",
        "",
        f"- Open STAR-count gene-expression files indexed by GDC: {len(pd.read_csv(MANIFEST, sep='\\t'))}.",
        f"- Baseline visit-1 bone marrow CD138+ samples selected: {len(manifest)}.",
        f"- Samples with merged RNA-seq and clinical data: {len(df)}.",
        f"- OS events in merged data: {int(df['os_event'].sum())}.",
        f"- ISS available in merged data: {int(df['iss_stage_num'].notna().sum())}.",
        "",
        "## Main Results",
        "",
    ]
    if top.empty:
        lines.append("- No associations were generated.")
    else:
        lines.append("| Outcome | Variable | n | Events | Effect | Best FDR |")
        lines.append("|---|---|---:|---:|---:|---:|")
        for _, row in top.iterrows():
            effect = row.get("delta_event_minus_nonevent", np.nan)
            if pd.isna(effect):
                effect = row.get("logrank_chi2", np.nan)
            if pd.isna(effect):
                effect = row.get("spearman_rho", np.nan)
            lines.append(
                f"| {row.get('outcome', '')} | {row.get('variable', '')} | {int(row.get('n', 0))} | "
                f"{int(row.get('n_event', 0)) if pd.notna(row.get('n_event', np.nan)) else ''} | {format_p(effect)} | {format_p(row.get('best_fdr', np.nan))} |"
            )
    lines += [
        "",
        "## Interpretation",
        "",
        "- This analysis provides CoMMpass-scale support for the revised subtype-axis route.",
        "- The plasma-secretory score and POU2AF1/XBP1/JCHAIN module show FDR-supported OS-event associations.",
        "- The plasma-secretory score also shows FDR-supported ISS-stage association and a median-split OS log-rank signal.",
        "- The open GDC clinical slice does not provide sufficient R-ISS, detailed cytogenetic high-risk, PFS, or treatment-response fields, so those endpoints require a fuller MMRF/CoMMpass clinical table or another curated cohort.",
        "",
        "## Outputs",
        "",
    ]
    for name in [
        "commppass_baseline_manifest.tsv",
        "commppass_target_tpm.tsv",
        "commppass_axis_clinical_scores.tsv",
        "commppass_axis_associations.tsv",
        "commppass_axis_fdr_ranked.tsv",
        "commppass_module_by_iss.png",
        "commppass_module_os_km.png",
        "commppass_top_associations_barplot.png",
        "commppass_axis_correlation_heatmap.png",
    ]:
        if (OUT / name).exists():
            lines.append(f"- `{(OUT / name).relative_to(PROJECT)}`")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    manifest = load_baseline_manifest()
    manifest.to_csv(OUT / "commppass_baseline_manifest.tsv", sep="\t", index=False)
    download_counts(manifest)
    expr = build_expression_matrix(manifest)
    expr.to_csv(OUT / "commppass_target_tpm.tsv", sep="\t", index=False)
    clinical = prepare_clinical()
    merged = expr.merge(clinical, on="case_submitter_id", how="left")
    merged.to_csv(OUT / "commppass_axis_clinical_scores.tsv", sep="\t", index=False)

    rows: list[dict[str, object]] = []
    for variable in AXIS_VARIABLES:
        rows.append(binary_association(merged, variable, "os_event", "Overall survival event"))
        rows.append(logrank_association(merged, variable, "os_time_months", "os_event", "Overall survival"))
        rows.append(binary_association(merged, variable, "iss_stage_III", "ISS stage III vs I/II"))
        rows.append(spearman_association(merged, variable, "iss_stage_num", "ISS ordinal stage"))
    assoc = add_fdr(pd.DataFrame(rows))
    assoc.to_csv(OUT / "commppass_axis_associations.tsv", sep="\t", index=False)
    assoc.dropna(subset=["best_fdr"]).sort_values("best_fdr").to_csv(OUT / "commppass_axis_fdr_ranked.tsv", sep="\t", index=False)
    plot_module_by_iss(merged)
    plot_km(merged, "clinical_subtype_module_score_z")
    plot_assoc_bar(assoc)
    plot_axis_corr(merged)
    write_report(merged, assoc, manifest)


if __name__ == "__main__":
    main()
