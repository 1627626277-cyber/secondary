from __future__ import annotations

import csv
import gzip
import math
import re
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


PROJECT = Path.cwd()
BULK = PROJECT / "external_bulk"
OUT = PROJECT / "analysis" / "bulk_clinical_validation"
REPORTS = PROJECT / "reports" / "validation"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

GPL570 = BULK / "GPL570" / "GPL570.annot.gz"
DATASETS = {
    "GSE24080": BULK / "GSE24080" / "GSE24080_series_matrix.txt.gz",
    "GSE2658": BULK / "GSE2658" / "GSE2658_series_matrix.txt.gz",
}

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
    "stromal_ecm": ["COL1A1", "COL1A2", "COL3A1", "DCN", "LUM", "CXCL12", "VCAM1", "FN1", "SPARC", "POSTN"],
}

KEY_GENES = [
    "TXNDC5",
    "PIM2",
    "TENT5C",
    "POU2AF1",
    "ITM2C",
    "UBE2J1",
    "SEC11C",
    "CD79A",
    "MZB1",
    "XBP1",
    "JCHAIN",
    "SDC1",
    "TNFRSF17",
    "IRF4",
    "PRDM1",
    "SLAMF7",
]

TARGET_GENES = sorted({gene for genes in SIGNATURES.values() for gene in genes} | set(KEY_GENES))


def split_geo_line(line: str) -> list[str]:
    return next(csv.reader([line.rstrip("\n\r")], delimiter="\t"))


def parse_numeric(value: object) -> float:
    if value is None:
        return np.nan
    text = str(value).strip()
    if not text or text.lower() in {"na", "nan", "none"}:
        return np.nan
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(match.group(0)) if match else np.nan


def parse_gpl570_target_probes(path: Path, target_genes: list[str]) -> tuple[dict[str, list[str]], pd.DataFrame]:
    if not path.exists():
        raise FileNotFoundError(path)
    target_set = {gene.upper() for gene in target_genes}
    gene_to_probes: dict[str, list[str]] = defaultdict(list)
    rows: list[dict[str, str]] = []
    in_table = False
    header: list[str] | None = None
    with gzip.open(path, "rt", encoding="utf-8", errors="replace", newline="") as handle:
        for line in handle:
            if line.startswith("!platform_table_begin"):
                in_table = True
                continue
            if line.startswith("!platform_table_end"):
                break
            if not in_table:
                continue
            fields = split_geo_line(line)
            if header is None:
                header = fields
                continue
            if not header or len(fields) < len(header):
                continue
            row = dict(zip(header, fields))
            probe = row.get("ID", "").strip()
            symbol_field = row.get("Gene symbol", "")
            symbols = [part.strip().upper() for part in symbol_field.split("///") if part.strip()]
            for symbol in symbols:
                if symbol in target_set and probe:
                    gene_to_probes[symbol].append(probe)
                    rows.append(
                        {
                            "gene": symbol,
                            "probe": probe,
                            "gene_title": row.get("Gene title", ""),
                            "gene_id": row.get("Gene ID", ""),
                        }
                    )
    return {gene: sorted(set(probes)) for gene, probes in gene_to_probes.items()}, pd.DataFrame(rows).drop_duplicates()


def parse_series_matrix_metadata(path: Path) -> tuple[pd.DataFrame, list[str]]:
    sample_ids: list[str] = []
    meta_cols: dict[str, list[str]] = {}
    characteristics: list[list[str]] = []
    with gzip.open(path, "rt", encoding="utf-8", errors="replace", newline="") as handle:
        for line in handle:
            if line.startswith("!series_matrix_table_begin"):
                break
            if not line.startswith("!Sample_"):
                continue
            fields = split_geo_line(line)
            key = fields[0].replace("!Sample_", "", 1)
            values = fields[1:]
            if key == "geo_accession":
                sample_ids = values
                characteristics = [[] for _ in sample_ids]
                meta_cols[key] = values
            elif key == "characteristics_ch1" and sample_ids:
                for idx, value in enumerate(values[: len(sample_ids)]):
                    if value:
                        characteristics[idx].append(value)
            else:
                meta_cols[key] = values
    if not sample_ids:
        raise ValueError(f"No sample accessions found in {path}")
    meta = pd.DataFrame({"sample_id": sample_ids})
    for key, values in meta_cols.items():
        if key == "geo_accession":
            continue
        if len(values) == len(sample_ids):
            meta[key] = values
    meta["characteristics_ch1_all"] = [" | ".join(items) for items in characteristics]
    return meta, sample_ids


def enrich_gse24080_metadata(meta: pd.DataFrame) -> pd.DataFrame:
    out = meta.copy()
    for idx, text in out["characteristics_ch1_all"].items():
        chunks = [chunk.strip() for chunk in str(text).split(" | ") if chunk.strip()]
        parsed: dict[str, str] = {}
        for chunk in chunks:
            low = chunk.lower()
            if "efs milestone outcome" in low:
                parsed["efs_24mo_event"] = chunk.rsplit(":", 1)[-1].strip()
            elif "os milestone outcome" in low:
                parsed["os_24mo_event"] = chunk.rsplit(":", 1)[-1].strip()
            elif chunk.lower().startswith("age:"):
                parsed["age"] = chunk.split(":", 1)[1].strip()
            elif chunk.lower().startswith("sex:"):
                parsed["sex"] = chunk.split(":", 1)[1].strip().lower()
            elif chunk.lower().startswith("maqc_distribution_status:"):
                parsed["maqc_distribution_status"] = chunk.split(":", 1)[1].strip()
            elif chunk.lower().startswith("randomly assigned class label:"):
                parsed["random_class_label"] = chunk.split(":", 1)[1].strip()
        for key, value in parsed.items():
            out.loc[idx, key] = value
    for col in ["age", "efs_24mo_event", "os_24mo_event", "random_class_label"]:
        if col in out:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def enrich_gse2658_metadata(meta: pd.DataFrame) -> pd.DataFrame:
    out = meta.copy()
    pattern = re.compile(r"\[([A-Za-z0-9_]+)=([^\]\(]+)")
    for idx, text in out["characteristics_ch1_all"].items():
        values: dict[str, str] = {}
        for key, value in pattern.findall(str(text)):
            clean_value = value.strip()
            if key == "Subgrp7" and "Subgrp7" in values and clean_value == "MY":
                values["Subgrp7_secondary"] = clean_value
            elif key not in values or values[key] in {"", "na"}:
                values[key] = clean_value
        for key, value in values.items():
            out.loc[idx, key] = value
    for col in ["SURIND", "SURTIM", "CONTAMIND"]:
        if col in out:
            out[col] = out[col].map(parse_numeric)
    if "AMPIND" in out:
        out["AMP_copies"] = out["AMPIND"].map(parse_numeric)
        out["AMP_high_3plus"] = np.where(out["AMP_copies"].notna(), (out["AMP_copies"] >= 3).astype(int), np.nan)
    return out


def read_target_probe_expression(path: Path, target_probes: set[str]) -> pd.DataFrame:
    rows: list[list[str]] = []
    header: list[str] | None = None
    in_table = False
    with gzip.open(path, "rt", encoding="utf-8", errors="replace", newline="") as handle:
        for line in handle:
            if line.startswith("!series_matrix_table_begin"):
                in_table = True
                continue
            if line.startswith("!series_matrix_table_end"):
                break
            if not in_table:
                continue
            fields = split_geo_line(line)
            if header is None:
                header = fields
                continue
            if fields and fields[0] in target_probes:
                rows.append(fields)
    if header is None:
        raise ValueError(f"No expression table found in {path}")
    if not rows:
        raise ValueError(f"No target probes found in {path}")
    expr = pd.DataFrame(rows, columns=header).set_index("ID_REF")
    return expr.apply(pd.to_numeric, errors="coerce")


def collapse_to_gene_expression(
    dataset: str,
    probe_expr: pd.DataFrame,
    gene_to_probes: dict[str, list[str]],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    gene_expr: dict[str, pd.Series] = {}
    mapping_rows: list[dict[str, object]] = []
    for gene in TARGET_GENES:
        probes = [probe for probe in gene_to_probes.get(gene.upper(), []) if probe in probe_expr.index]
        if not probes:
            mapping_rows.append({"dataset": dataset, "gene": gene, "n_probes": 0, "selected_probe": "", "selected_probe_variance": np.nan})
            continue
        sub = probe_expr.loc[probes]
        variances = sub.var(axis=1, skipna=True)
        selected = str(variances.idxmax())
        gene_expr[gene.upper()] = sub.loc[selected]
        mapping_rows.append(
            {
                "dataset": dataset,
                "gene": gene.upper(),
                "n_probes": len(probes),
                "selected_probe": selected,
                "selected_probe_variance": float(variances.loc[selected]),
            }
        )
    gene_df = pd.DataFrame(gene_expr)
    gene_df.index.name = "sample_id"
    return gene_df, pd.DataFrame(mapping_rows)


def zscore_frame(df: pd.DataFrame) -> pd.DataFrame:
    means = df.mean(axis=0, skipna=True)
    stds = df.std(axis=0, skipna=True).replace(0, np.nan)
    return (df - means) / stds


def add_signature_scores(gene_df: pd.DataFrame) -> pd.DataFrame:
    score_df = pd.DataFrame(index=gene_df.index)
    for signature, genes in SIGNATURES.items():
        present = [gene for gene in genes if gene in gene_df.columns]
        if not present:
            score_df[f"{signature}_score_z"] = np.nan
            score_df[f"{signature}_n_genes"] = 0
            continue
        score_df[f"{signature}_score_z"] = zscore_frame(gene_df[present]).mean(axis=1, skipna=True)
        score_df[f"{signature}_n_genes"] = len(present)
    return score_df


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
    adjusted = np.clip(adjusted, 0, 1)
    out.loc[order] = adjusted
    return out


def add_fdr_columns(assoc: pd.DataFrame) -> pd.DataFrame:
    out = assoc.copy()
    for p_col in ["mannwhitney_p", "median_split_fisher_p", "logrank_p"]:
        if p_col not in out.columns:
            continue
        fdr_col = p_col.replace("_p", "_fdr")
        out[fdr_col] = np.nan
        for (_, outcome), idx in out.groupby(["dataset", "outcome"]).groups.items():
            out.loc[idx, fdr_col] = bh_fdr(out.loc[idx, p_col])
    return out


def binary_association(df: pd.DataFrame, dataset: str, variable: str, outcome: str, label: str) -> dict[str, object]:
    sub = df[[variable, outcome]].dropna()
    sub = sub[sub[outcome].isin([0, 1])]
    result: dict[str, object] = {
        "dataset": dataset,
        "variable": variable,
        "outcome": outcome,
        "outcome_label": label,
        "n": int(len(sub)),
        "n_event": int((sub[outcome] == 1).sum()) if len(sub) else 0,
        "n_nonevent": int((sub[outcome] == 0).sum()) if len(sub) else 0,
    }
    if result["n_event"] == 0 or result["n_nonevent"] == 0:
        result.update({"median_event": np.nan, "median_nonevent": np.nan, "delta_event_minus_nonevent": np.nan, "mannwhitney_p": np.nan, "auc_event": np.nan, "median_split_or": np.nan, "median_split_fisher_p": np.nan})
        return result
    event_vals = sub.loc[sub[outcome] == 1, variable].to_numpy(float)
    nonevent_vals = sub.loc[sub[outcome] == 0, variable].to_numpy(float)
    median_cut = float(np.nanmedian(sub[variable]))
    high = sub[variable] >= median_cut
    table = pd.crosstab(high, sub[outcome])
    for state in [False, True]:
        if state not in table.index:
            table.loc[state] = 0
    for state in [0, 1]:
        if state not in table.columns:
            table[state] = 0
    table = table.sort_index().sort_index(axis=1)
    fisher_table = [[int(table.loc[True, 1]), int(table.loc[True, 0])], [int(table.loc[False, 1]), int(table.loc[False, 0])]]
    try:
        fisher_or, fisher_p = stats.fisher_exact(fisher_table)
    except Exception:
        fisher_or, fisher_p = np.nan, np.nan
    result.update(
        {
            "median_event": float(np.nanmedian(event_vals)),
            "median_nonevent": float(np.nanmedian(nonevent_vals)),
            "delta_event_minus_nonevent": float(np.nanmedian(event_vals) - np.nanmedian(nonevent_vals)),
            "mannwhitney_p": float(stats.mannwhitneyu(event_vals, nonevent_vals, alternative="two-sided").pvalue),
            "auc_event": rank_auc(sub[variable].to_numpy(float), sub[outcome].to_numpy(float)),
            "median_split_or": float(fisher_or) if fisher_or is not None else np.nan,
            "median_split_fisher_p": float(fisher_p) if fisher_p is not None else np.nan,
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
        "n": int(len(sub)),
        "n_event": int((sub[event_col] == 1).sum()) if len(sub) else 0,
    }
    if len(sub) < 10 or result["n_event"] == 0:
        result.update({"high_n": np.nan, "low_n": np.nan, "high_events": np.nan, "low_events": np.nan, "logrank_chi2": np.nan, "logrank_p": np.nan})
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
    p_value = float(stats.chi2.sf(chi2, df=1)) if not math.isnan(chi2) else np.nan
    result.update(
        {
            "high_n": int(high.sum()),
            "low_n": int((~high).sum()),
            "high_events": int((events[high] == 1).sum()),
            "low_events": int((events[~high] == 1).sum()),
            "high_median_time": float(np.nanmedian(times[high])) if high.any() else np.nan,
            "low_median_time": float(np.nanmedian(times[~high])) if (~high).any() else np.nan,
            "logrank_chi2": float(chi2) if not math.isnan(chi2) else np.nan,
            "logrank_p": p_value,
        }
    )
    return result


def plot_box(df: pd.DataFrame, dataset: str, variables: list[str], outcome: str, outcome_label: str, path: Path) -> None:
    rows = []
    for variable in variables:
        if variable not in df.columns:
            continue
        sub = df[[variable, outcome]].dropna()
        sub = sub[sub[outcome].isin([0, 1])]
        for _, row in sub.iterrows():
            rows.append({"variable": variable, "value": row[variable], "outcome": f"{int(row[outcome])}"})
    if not rows:
        return
    plot_df = pd.DataFrame(rows)
    width = max(7.0, 1.5 * len(plot_df["variable"].unique()))
    plt.figure(figsize=(width, 4.8))
    ax = plt.gca()
    plot_df.boxplot(column="value", by=["variable", "outcome"], ax=ax, grid=False, rot=45)
    plt.suptitle("")
    ax.set_title(f"{dataset}: {outcome_label}")
    ax.set_xlabel("Variable / outcome group")
    ax.set_ylabel("Expression or score")
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def process_dataset(dataset: str, path: Path, gene_to_probes: dict[str, list[str]]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    meta, _ = parse_series_matrix_metadata(path)
    if dataset == "GSE24080":
        meta = enrich_gse24080_metadata(meta)
    elif dataset == "GSE2658":
        meta = enrich_gse2658_metadata(meta)
    target_probes = {probe for probes in gene_to_probes.values() for probe in probes}
    probe_expr = read_target_probe_expression(path, target_probes)
    gene_expr, probe_map = collapse_to_gene_expression(dataset, probe_expr, gene_to_probes)
    score_df = add_signature_scores(gene_expr)
    sample_df = meta.merge(gene_expr.reset_index(), on="sample_id", how="left").merge(score_df.reset_index(), on="sample_id", how="left")
    sample_df.insert(0, "dataset", dataset)
    return sample_df, gene_expr, score_df, probe_map


def main() -> None:
    gene_to_probes, annotation_rows = parse_gpl570_target_probes(GPL570, TARGET_GENES)
    annotation_rows.to_csv(OUT / "bulk_target_probe_annotation.tsv", sep="\t", index=False)
    all_samples: list[pd.DataFrame] = []
    all_gene_expr: list[pd.DataFrame] = []
    all_scores: list[pd.DataFrame] = []
    all_probe_maps: list[pd.DataFrame] = []
    for dataset, path in DATASETS.items():
        sample_df, gene_expr, score_df, probe_map = process_dataset(dataset, path, gene_to_probes)
        sample_df.to_csv(OUT / f"{dataset}_bulk_sample_scores.tsv", sep="\t", index=False)
        gene_expr.reset_index().to_csv(OUT / f"{dataset}_target_gene_expression.tsv", sep="\t", index=False)
        score_df.reset_index().to_csv(OUT / f"{dataset}_signature_scores.tsv", sep="\t", index=False)
        all_samples.append(sample_df)
        all_gene_expr.append(gene_expr.assign(dataset=dataset).reset_index())
        all_scores.append(score_df.assign(dataset=dataset).reset_index())
        all_probe_maps.append(probe_map)

    sample_scores = pd.concat(all_samples, ignore_index=True)
    gene_expr_all = pd.concat(all_gene_expr, ignore_index=True)
    signature_scores_all = pd.concat(all_scores, ignore_index=True)
    probe_map_all = pd.concat(all_probe_maps, ignore_index=True)
    sample_scores.to_csv(OUT / "bulk_clinical_sample_scores.tsv", sep="\t", index=False)
    gene_expr_all.to_csv(OUT / "bulk_target_gene_expression.tsv", sep="\t", index=False)
    signature_scores_all.to_csv(OUT / "bulk_signature_scores.tsv", sep="\t", index=False)
    probe_map_all.to_csv(OUT / "bulk_target_probe_mapping.tsv", sep="\t", index=False)

    variables = ["plasma_secretory_score_z", "TXNDC5", "PIM2", "TENT5C", "POU2AF1", "MZB1", "XBP1", "JCHAIN"]
    results: list[dict[str, object]] = []
    gse24080 = sample_scores[sample_scores["dataset"] == "GSE24080"].copy()
    for outcome, label in [("efs_24mo_event", "24-month EFS event"), ("os_24mo_event", "24-month OS death")]:
        if outcome in gse24080.columns:
            for variable in variables:
                if variable in gse24080.columns:
                    results.append(binary_association(gse24080, "GSE24080", variable, outcome, label))
            plot_box(gse24080, "GSE24080", variables[:5], outcome, label, OUT / f"GSE24080_{outcome}_boxplots.png")

    gse2658 = sample_scores[sample_scores["dataset"] == "GSE2658"].copy()
    if "SURIND" in gse2658.columns:
        for variable in variables:
            if variable in gse2658.columns:
                results.append(binary_association(gse2658, "GSE2658", variable, "SURIND", "Disease-related death indicator"))
                if "SURTIM" in gse2658.columns:
                    results.append(logrank_association(gse2658, "GSE2658", variable, "SURTIM", "SURIND", "Disease-related survival"))
        plot_box(gse2658, "GSE2658", variables[:5], "SURIND", "Disease-related death indicator", OUT / "GSE2658_SURIND_boxplots.png")
    if "AMP_high_3plus" in gse2658.columns:
        for variable in variables:
            if variable in gse2658.columns:
                results.append(binary_association(gse2658, "GSE2658", variable, "AMP_high_3plus", "FISH 1q21 amplification >=3 copies"))
        plot_box(gse2658, "GSE2658", variables[:5], "AMP_high_3plus", "FISH 1q21 amplification >=3 copies", OUT / "GSE2658_AMP_high_3plus_boxplots.png")

    assoc = pd.DataFrame(results)
    assoc = add_fdr_columns(assoc)
    assoc.to_csv(OUT / "bulk_outcome_association_results.tsv", sep="\t", index=False)

    summary_rows = []
    for dataset, df in sample_scores.groupby("dataset"):
        summary_rows.append(
            {
                "dataset": dataset,
                "n_samples": int(len(df)),
                "n_plasma_signature_scored": int(df["plasma_secretory_score_z"].notna().sum()) if "plasma_secretory_score_z" in df else 0,
                "n_txndc5_scored": int(df["TXNDC5"].notna().sum()) if "TXNDC5" in df else 0,
            }
        )
    pd.DataFrame(summary_rows).to_csv(OUT / "bulk_validation_dataset_summary.tsv", sep="\t", index=False)

    write_report(sample_scores, assoc, probe_map_all)


def p_text(value: object) -> str:
    try:
        number = float(value)
    except Exception:
        return "NA"
    if math.isnan(number):
        return "NA"
    if number < 0.001:
        return f"{number:.2e}"
    return f"{number:.4f}"


def best_rows(assoc: pd.DataFrame, dataset: str, outcome: str, top_n: int = 8) -> pd.DataFrame:
    sub = assoc[(assoc["dataset"] == dataset) & (assoc["outcome"] == outcome)].copy()
    p_cols = [col for col in ["mannwhitney_p", "median_split_fisher_p", "logrank_p"] if col in sub.columns]
    if not p_cols or sub.empty:
        return sub
    sub["best_p"] = sub[p_cols].min(axis=1, skipna=True)
    return sub.sort_values("best_p").head(top_n)


def write_report(sample_scores: pd.DataFrame, assoc: pd.DataFrame, probe_map: pd.DataFrame) -> None:
    report_path = REPORTS / "BULK_CLINICAL_VALIDATION_REPORT.md"
    lines: list[str] = []
    lines.append("# Bulk / Clinical Transcriptomic Validation Report")
    lines.append("")
    lines.append("Date: 2026-04-29")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append("- Validate the spatially discovered plasma-secretory / TXNDC5 axis in independent MM bulk transcriptomic cohorts.")
    lines.append("- Test whether candidate genes or signature scores associate with clinical outcome variables available in GEO metadata.")
    lines.append("- Strengthen the pure public-data translational route without requiring wet-lab experiments.")
    lines.append("")
    lines.append("## Datasets")
    lines.append("")
    for dataset, df in sample_scores.groupby("dataset"):
        lines.append(f"- {dataset}: {len(df)} samples scored from GPL570 processed series matrix.")
    lines.append("")
    lines.append("## Method Summary")
    lines.append("")
    lines.append("- Parsed GPL570 annotation and mapped target genes to available Affymetrix probes.")
    lines.append("- Collapsed each target gene to the highest-variance mapped probe within each dataset.")
    lines.append("- Calculated z-scored plasma-secretory, myeloid-inflammatory, and stromal/ECM signatures within each cohort.")
    lines.append("- Tested GSE24080 24-month EFS and OS milestone outcomes with Mann-Whitney and median-split Fisher tests.")
    lines.append("- Tested GSE2658 disease-related death and follow-up time using binary association and a simple median-split log-rank test.")
    lines.append("")
    lines.append("## Data Coverage")
    lines.append("")
    lines.append("| Dataset | Samples | Plasma signature scored | TXNDC5 scored |")
    lines.append("|---|---:|---:|---:|")
    for dataset, df in sample_scores.groupby("dataset"):
        n_sig = int(df["plasma_secretory_score_z"].notna().sum()) if "plasma_secretory_score_z" in df else 0
        n_txn = int(df["TXNDC5"].notna().sum()) if "TXNDC5" in df else 0
        lines.append(f"| {dataset} | {len(df)} | {n_sig} | {n_txn} |")
    lines.append("")
    lines.append("## Key Association Results")
    lines.append("")
    if assoc.empty:
        lines.append("- No association results were generated.")
    else:
        for dataset, outcome in [
            ("GSE24080", "efs_24mo_event"),
            ("GSE24080", "os_24mo_event"),
            ("GSE2658", "SURIND"),
            ("GSE2658", "SURTIM/SURIND"),
            ("GSE2658", "AMP_high_3plus"),
        ]:
            sub = best_rows(assoc, dataset, outcome, top_n=5)
            if sub.empty:
                continue
            label = str(sub["outcome_label"].iloc[0])
            lines.append(f"### {dataset}: {label}")
            lines.append("")
            lines.append("| Variable | n | Events | Delta/effect | MW p/FDR | Fisher p/FDR | Log-rank p/FDR | AUC/event |")
            lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
            for _, row in sub.iterrows():
                delta = row.get("delta_event_minus_nonevent", np.nan)
                if pd.isna(delta):
                    delta = row.get("logrank_chi2", np.nan)
                lines.append(
                    f"| {row.get('variable', '')} | {int(row.get('n', 0))} | {int(row.get('n_event', 0)) if pd.notna(row.get('n_event', np.nan)) else ''} | "
                    f"{p_text(delta)} | {p_text(row.get('mannwhitney_p', np.nan))}/{p_text(row.get('mannwhitney_fdr', np.nan))} | "
                    f"{p_text(row.get('median_split_fisher_p', np.nan))}/{p_text(row.get('median_split_fisher_fdr', np.nan))} | "
                    f"{p_text(row.get('logrank_p', np.nan))}/{p_text(row.get('logrank_fdr', np.nan))} | {p_text(row.get('auc_event', np.nan))} |"
                )
            lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("- This step converts the project from spatial plus scRNA validation into a translational validation workflow.")
    lines.append("- Direct clinical-outcome support for TXNDC5 is weak in this first-pass analysis, so TXNDC5 should not yet be framed as an independent prognostic marker.")
    lines.append("- The most FDR-stable signals are XBP1 for GSE24080 24-month OS death and POU2AF1/XBP1/JCHAIN for GSE2658 1q21 amplification status.")
    lines.append("- The manuscript route should therefore broaden from a single-gene TXNDC5 claim to a plasma-secretory clinical-subtype axis, then seek CoMMpass or another clinically annotated MM cohort for stronger validation.")
    lines.append("")
    lines.append("## Outputs")
    lines.append("")
    for name in [
        "bulk_clinical_sample_scores.tsv",
        "bulk_target_gene_expression.tsv",
        "bulk_signature_scores.tsv",
        "bulk_target_probe_mapping.tsv",
        "bulk_outcome_association_results.tsv",
        "bulk_validation_dataset_summary.tsv",
        "GSE24080_efs_24mo_event_boxplots.png",
        "GSE24080_os_24mo_event_boxplots.png",
        "GSE2658_SURIND_boxplots.png",
        "GSE2658_AMP_high_3plus_boxplots.png",
    ]:
        path = OUT / name
        if path.exists():
            lines.append(f"- `{path.relative_to(PROJECT)}`")
    lines.append("")
    lines.append("## Probe Mapping Note")
    lines.append("")
    mapped = probe_map[probe_map["n_probes"] > 0]["gene"].nunique()
    lines.append(f"- Target genes with at least one GPL570 probe selected: {mapped}.")
    lines.append("- Multi-probe genes were represented by the highest-variance probe within each dataset; this is appropriate for exploratory validation and should be described in Methods.")
    lines.append("- FDR values were calculated within each dataset/outcome family for each statistical test type.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
