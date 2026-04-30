from __future__ import annotations

import math
import shutil
import textwrap
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT = Path.cwd()
OUT = PROJECT / "analysis" / "manuscript_figures"
REPORTS = PROJECT / "reports" / "manuscript"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

SPATIAL = PROJECT / "analysis" / "spatial_candidate_signatures"
SCRNA = PROJECT / "analysis" / "scrna_gse271107_validation"
BULK = PROJECT / "analysis" / "plasma_secretory_subtype_refinement"
COMMPASS = PROJECT / "analysis" / "commppass_gdc_validation"
NG2024 = PROJECT / "analysis" / "skerget_ng2024_public_supplement"
ADJUSTED = PROJECT / "analysis" / "commppass_ng2024_adjusted_models"
GSE299193 = PROJECT / "analysis" / "gse299193_xenium_validation"

AXIS_GENES = ["TXNDC5", "POU2AF1", "XBP1", "JCHAIN"]
PLASMA_GENES = ["TXNDC5", "POU2AF1", "XBP1", "JCHAIN", "MZB1", "SDC1"]
SIGNATURE_LABELS = {
    "plasma_secretory": "Plasma-secretory",
    "myeloid_inflammatory": "Myeloid inflammatory",
    "t_nk_cytotoxic_exhaustion": "T/NK cytotoxic",
    "stromal_ecm": "Stromal ECM",
    "endothelial_angiogenic": "Endothelial angiogenic",
    "erythroid_megak": "Erythroid/megak",
    "cycling_proliferation": "Cycling",
}

PALETTE = {
    "control": "#4C78A8",
    "MM": "#C44E52",
    "HD": "#4C78A8",
    "MGUS": "#72B7B2",
    "SMM": "#F2CF5B",
    "I": "#7EA1C4",
    "II": "#B6B1D6",
    "III": "#C44E52",
    "low": "#4C78A8",
    "high": "#C44E52",
    "neutral": "#6B7280",
    "accent": "#C44E52",
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
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path, sep="\t")


def as_float(value: object) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def format_p(value: object) -> str:
    p = as_float(value)
    if math.isnan(p):
        return "NA"
    if p < 0.001:
        return f"{p:.2e}"
    return f"{p:.3g}"


def first_nonmissing(row: pd.Series, columns: list[str]) -> float:
    for col in columns:
        if col in row and not pd.isna(row[col]):
            return as_float(row[col])
    return float("nan")


def save_figure(fig: mpl.figure.Figure, stem: str) -> None:
    fig.tight_layout()
    for suffix in [".png", ".svg", ".pdf"]:
        fig.savefig(OUT / f"{stem}{suffix}", dpi=350, bbox_inches="tight")
    plt.close(fig)


def clean_axis(ax: mpl.axes.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#E5E7EB", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)


def panel_label(ax: mpl.axes.Axes, label: str) -> None:
    ax.text(-0.12, 1.06, label, transform=ax.transAxes, ha="left", va="bottom", fontsize=10, fontweight="bold")


def jitter(values: np.ndarray, seed: int, width: float = 0.08) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.normal(0, width, size=len(values))


def box_scatter(
    ax: mpl.axes.Axes,
    data: pd.DataFrame,
    group_col: str,
    value_col: str,
    order: list[str],
    colors: list[str],
    ylabel: str,
) -> None:
    vals = [pd.to_numeric(data.loc[data[group_col] == group, value_col], errors="coerce").dropna().to_numpy() for group in order]
    bp = ax.boxplot(vals, patch_artist=True, showfliers=False, widths=0.48)
    for patch, color in zip(bp["boxes"], colors):
        patch.set(facecolor=color, alpha=0.72, edgecolor="#222222", linewidth=0.8)
    for element in ["whiskers", "caps", "medians"]:
        for obj in bp[element]:
            obj.set(color="#222222", linewidth=0.8)
    for i, arr in enumerate(vals, start=1):
        if len(arr) == 0:
            continue
        ax.scatter(
            np.full(len(arr), i) + jitter(arr, seed=100 + i, width=0.045),
            arr,
            s=14,
            color="#222222",
            alpha=0.75,
            linewidths=0,
            zorder=3,
        )
        ax.text(i, np.nanmax(arr) + 0.04 * (np.nanmax(arr) - np.nanmin(arr) + 1), f"n={len(arr)}", ha="center", va="bottom", fontsize=7)
    ax.set_xticks(range(1, len(order) + 1))
    ax.set_xticklabels(order)
    ax.set_ylabel(ylabel)
    clean_axis(ax)


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


def load_core_tables() -> dict[str, pd.DataFrame]:
    tables = {
        "spatial_sensitivity": read_tsv(SPATIAL / "signature_sensitivity_results.tsv"),
        "spatial_sample_scores": read_tsv(SPATIAL / "sample_signature_scores.tsv"),
        "spatial_shortlist": read_tsv(SPATIAL / "candidate_validation_shortlist.tsv"),
        "scrna_celltype": read_tsv(SCRNA / "gse271107_signature_by_celltype.tsv"),
        "scrna_stage": read_tsv(SCRNA / "gse271107_signature_by_stage.tsv"),
        "scrna_gene_celltype": read_tsv(SCRNA / "gse271107_candidate_gene_by_sample_celltype.tsv"),
        "bulk_scores": read_tsv(BULK / "plasma_secretory_subtype_sample_scores.tsv"),
        "bulk_assoc": read_tsv(BULK / "plasma_secretory_subtype_fdr_ranked.tsv"),
        "comm_scores": read_tsv(COMMPASS / "commppass_axis_clinical_scores.tsv"),
        "comm_assoc": read_tsv(COMMPASS / "commppass_axis_fdr_ranked.tsv"),
    }
    optional_paths = {
        "ng2024_assoc": NG2024 / "ng2024_molecular_annotation_fdr_ranked.tsv",
        "ng2024_merged": NG2024 / "commppass_scores_with_ng2024_annotations.tsv",
        "adjusted_models": ADJUSTED / "commppass_ng2024_adjusted_model_fdr_ranked.tsv",
        "gse299193_assoc": GSE299193 / "gse299193_axis_group_associations.tsv",
        "gse299193_scores": GSE299193 / "gse299193_sample_axis_scores.tsv",
    }
    for key, path in optional_paths.items():
        if path.exists():
            tables[key] = read_tsv(path)
    return tables


def build_evidence_table(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    spatial = tables["spatial_sensitivity"]
    plasma = spatial[(spatial["subset"] == "all_samples") & (spatial["signature"] == "plasma_secretory")].iloc[0]
    rows.append(
        {
            "evidence_layer": "Spatial discovery",
            "cohort": "GSE269875",
            "data_type": "human bone marrow spatial transcriptomics",
            "sample_n": int(plasma["n_MM"] + plasma["n_control"]),
            "contrast_or_endpoint": "MM vs control",
            "primary_feature": "plasma_secretory signature",
            "effect_summary": f"MM-control median difference={as_float(plasma['MM_minus_control_median']):.3f}; Cohen d={as_float(plasma['cohen_d_sample_level']):.3f}",
            "p_value": as_float(plasma["mannwhitney_p_sample_level"]),
            "fdr_or_adjusted_p": np.nan,
            "claim_level": "Discovery",
            "interpretation": "Spatial plasma-secretory program is enriched in MM bone marrow.",
        }
    )

    if "gse299193_assoc" in tables:
        gse299193 = tables["gse299193_assoc"]
        for variable, feature_label, interpretation in [
            (
                "plasma_secretory_score_z",
                "plasma-secretory score",
                "The plasma-secretory program is independently higher in active MM/RM Xenium bone marrow samples than Ctrl/MGUS/SM samples.",
            ),
            (
                "clinical_module_score_z",
                "POU2AF1/XBP1 module",
                "The POU2AF1/XBP1-covered clinical module is independently higher in active MM/RM Xenium bone marrow samples.",
            ),
        ]:
            hit = gse299193[(gse299193["contrast"] == "MM_RM_vs_Ctrl_MGUS_SM") & (gse299193["variable"] == variable)]
            if hit.empty:
                continue
            row = hit.iloc[0]
            rows.append(
                {
                    "evidence_layer": "Second spatial validation",
                    "cohort": "GSE299193",
                    "data_type": "human bone marrow Xenium spatial transcriptomics",
                    "sample_n": int(row["n_high"] + row["n_low"]),
                    "contrast_or_endpoint": "MM/RM vs Ctrl/MGUS/SM",
                    "primary_feature": feature_label,
                    "effect_summary": f"median delta={as_float(row['delta_high_minus_low']):.3f}",
                    "p_value": as_float(row["mannwhitney_p"]),
                    "fdr_or_adjusted_p": as_float(row["mannwhitney_fdr"]),
                    "claim_level": "Independent spatial validation",
                    "interpretation": interpretation,
                }
            )

    gene_cell = tables["scrna_gene_celltype"]
    txn = gene_cell[(gene_cell["gene"] == "TXNDC5") & (gene_cell["marker_inferred_cell_type"] == "plasma_cell")].copy()
    rows.append(
        {
            "evidence_layer": "Single-cell localization",
            "cohort": "GSE271107",
            "data_type": "single-cell RNA-seq",
            "sample_n": int(txn["n_cells"].sum()),
            "contrast_or_endpoint": "marker-inferred plasma cells",
            "primary_feature": "TXNDC5",
            "effect_summary": f"mean log-normalized expression={txn['mean_log_norm'].mean():.3f}; detected={100 * txn['pct_detected'].mean():.2f}%",
            "p_value": np.nan,
            "fdr_or_adjusted_p": np.nan,
            "claim_level": "Localization validation",
            "interpretation": "TXNDC5 is consistently expressed in plasma-cell annotated single cells.",
        }
    )

    bulk = tables["bulk_assoc"]
    for dataset, variable, outcome in [
        ("GSE2658", "clinical_subtype_module_score_z", "AMP_high_3plus"),
        ("GSE24080", "XBP1_z", "os_24mo_event"),
    ]:
        row = bulk[(bulk["dataset"] == dataset) & (bulk["variable"] == variable) & (bulk["outcome"] == outcome)].iloc[0]
        rows.append(
            {
                "evidence_layer": "External bulk validation",
                "cohort": dataset,
                "data_type": "bulk expression microarray",
                "sample_n": int(row["n"]),
                "contrast_or_endpoint": row["outcome_label"],
                "primary_feature": variable,
                "effect_summary": f"delta={as_float(row.get('delta_event_minus_nonevent')):.3f}",
                "p_value": as_float(row.get("mannwhitney_p")),
                "fdr_or_adjusted_p": as_float(row.get("best_fdr")),
                "claim_level": "Clinical/subtype support",
                "interpretation": "Subtype module links the spatial axis to independent clinical or cytogenetic risk annotations.",
            }
        )

    comm = tables["comm_assoc"]
    for variable, outcome in [
        ("plasma_secretory_score_z", "os_event"),
        ("plasma_secretory_score_z", "iss_stage_num"),
        ("plasma_secretory_score_z", "os_time_months/os_event"),
    ]:
        row = comm[(comm["variable"] == variable) & (comm["outcome"] == outcome)].iloc[0]
        effect = row.get("delta_event_minus_nonevent")
        if pd.isna(effect):
            effect = row.get("spearman_rho")
        if pd.isna(effect):
            effect = row.get("logrank_chi2")
        p_value = first_nonmissing(row, ["mannwhitney_p", "spearman_p", "logrank_p", "median_split_fisher_p"])
        rows.append(
            {
                "evidence_layer": "Clinical bulk validation",
                "cohort": "MMRF-COMMPASS/GDC",
                "data_type": "baseline bone marrow CD138+ RNA-seq",
                "sample_n": int(row["n"]),
                "contrast_or_endpoint": row["outcome_label"],
                "primary_feature": variable,
                "effect_summary": f"effect={as_float(effect):.3f}",
                "p_value": p_value,
                "fdr_or_adjusted_p": as_float(row.get("best_fdr")),
                "claim_level": "Clinical validation",
                "interpretation": "The plasma-secretory axis is associated with OS event, ISS stage, and median-split OS in CoMMpass/GDC.",
            }
        )

    if "ng2024_assoc" in tables:
        ng = tables["ng2024_assoc"]
        for feature, score, label, interpretation in [
            (
                "PR",
                "plasma_secretory_score_z",
                "PR RNA-subtype probability",
                "The plasma-secretory score tracks the NG2024 proliferation-like RNA subtype probability.",
            ),
            (
                "Cp_1q21_Call",
                "plasma_secretory_score_z",
                "1q21 gain/amplification",
                "The plasma-secretory score is higher in samples with public NG2024 1q21 gain/amplification calls.",
            ),
            (
                "Cp_1q21_Call",
                "TXNDC5_z",
                "1q21 gain/amplification",
                "TXNDC5 expression is associated with public NG2024 1q21 gain/amplification calls.",
            ),
        ]:
            hit = ng[(ng["feature"] == feature) & (ng["score"] == score)]
            if hit.empty:
                continue
            row = hit.iloc[0]
            rows.append(
                {
                    "evidence_layer": "Public CoMMpass molecular annotation",
                    "cohort": "Skerget NG2024 / CoMMpass",
                    "data_type": "public CoMMpass molecular-risk annotation",
                    "sample_n": int(row["n"]),
                    "contrast_or_endpoint": label,
                    "primary_feature": score,
                    "effect_summary": f"{row['effect_label']}={as_float(row['effect']):.3f}",
                    "p_value": as_float(row["p_value"]),
                    "fdr_or_adjusted_p": as_float(row["fdr"]),
                    "claim_level": "Molecular annotation support",
                    "interpretation": interpretation,
                }
            )

    if "adjusted_models" in tables:
        adjusted = tables["adjusted_models"]
        for model_name, score, label in [
            ("OS adjusted for age, sex, ISS, 1q21", "plasma_secretory_score_z", "OS adjusted for age, sex, ISS and 1q21"),
            ("OS adjusted for age, sex, ISS, 1q21", "clinical_subtype_module_score_z", "OS adjusted for age, sex, ISS and 1q21"),
            ("1q21 gain/amplification adjusted for age, sex, ISS", "plasma_secretory_score_z", "1q21 adjusted for age, sex and ISS"),
        ]:
            hit = adjusted[(adjusted["model_name"] == model_name) & (adjusted["score"] == score)]
            if hit.empty:
                continue
            row = hit.iloc[0]
            ci = f"{as_float(row['ci_lower']):.3f}-{as_float(row['ci_upper']):.3f}"
            rows.append(
                {
                    "evidence_layer": "Adjusted clinical/molecular model",
                    "cohort": "CoMMpass/GDC + NG2024",
                    "data_type": "baseline CD138+ RNA-seq plus public molecular annotation",
                    "sample_n": int(row["n"]),
                    "contrast_or_endpoint": label,
                    "primary_feature": score,
                    "effect_summary": f"{row['effect_type']}={as_float(row['effect']):.3f}; 95% CI={ci}",
                    "p_value": as_float(row["p_value"]),
                    "fdr_or_adjusted_p": as_float(row["fdr"]),
                    "claim_level": "Covariate-adjusted association",
                    "interpretation": "The plasma-secretory axis retains association after basic adjustment; this is not a prospective clinical classifier claim.",
                }
            )

    table = pd.DataFrame(rows)
    table.to_csv(OUT / "cross_cohort_evidence_table.tsv", sep="\t", index=False)
    return table


def plot_fig1(evidence: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(10.2, 5.4))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)

    stages = [
        ("Spatial discovery", "GSE269875\nMM vs control\nplasma-secretory program", 0.6, 3.3, "#D7E6F5"),
        ("scRNA localization", "GSE271107\nplasma-cell localization\nTXNDC5 support", 3.1, 3.3, "#D8EFEA"),
        ("Bulk validation", "GSE24080 / GSE2658\nsubtype-risk support\nPOU2AF1/XBP1/JCHAIN", 5.6, 3.3, "#F7E7AD"),
        ("Clinical/molecular validation", "CoMMpass/GDC + NG2024\n762 baseline samples\nOS, ISS, 1q21, RNA subtype", 8.1, 3.3, "#F3D3D5"),
    ]
    for title, body, x, y, color in stages:
        ax.add_patch(mpl.patches.FancyBboxPatch((x, y), 1.8, 1.0, boxstyle="round,pad=0.03,rounding_size=0.05", facecolor=color, edgecolor="#1F2937", linewidth=0.9))
        ax.text(x + 0.9, y + 0.73, title, ha="center", va="center", fontsize=9, fontweight="bold")
        ax.text(x + 0.9, y + 0.35, body, ha="center", va="center", fontsize=7.3, linespacing=1.15)
    for x0 in [2.4, 4.9, 7.4]:
        ax.annotate("", xy=(x0 + 0.55, 3.8), xytext=(x0, 3.8), arrowprops=dict(arrowstyle="->", color="#111827", lw=1.1))

    claim = (
        "Defensible current claim\n"
        "MM bone marrow plasma_secretory spatial program is single-cell localized\n"
        "and associated with OS / ISS / public molecular-risk annotations in CoMMpass."
    )
    ax.add_patch(mpl.patches.Rectangle((1.2, 1.35), 7.6, 0.82, facecolor="#F9FAFB", edgecolor="#374151", linewidth=0.9))
    ax.text(5.0, 1.76, claim, ha="center", va="center", fontsize=9, linespacing=1.35)

    limits = (
        "Claim boundary: R-ISS, PFS and treatment-response validation\n"
        "require fuller MMRF/CoMMpass clinical files and are not claimed from the GDC open slice."
    )
    ax.text(5.0, 0.72, limits, ha="center", va="center", fontsize=7.5, color="#374151")
    ax.text(0.1, 4.75, "Fig. 1 | Cross-cohort study design and evidence chain", ha="left", va="top", fontsize=11, fontweight="bold")
    save_figure(fig, "fig1_study_design_evidence_chain")


def plot_fig2(tables: dict[str, pd.DataFrame]) -> None:
    sample = tables["spatial_sample_scores"]
    sens = tables["spatial_sensitivity"]
    shortlist = tables["spatial_shortlist"]

    fig = plt.figure(figsize=(11.2, 4.2))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.35, 1.35])
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])

    box_scatter(
        ax1,
        sample,
        "Group",
        "plasma_secretory_score",
        ["control", "MM"],
        [PALETTE["control"], PALETTE["MM"]],
        "Spatial plasma-secretory score",
    )
    plasma = sens[(sens["subset"] == "all_samples") & (sens["signature"] == "plasma_secretory")].iloc[0]
    ax1.set_title(f"MM enrichment\np={format_p(plasma['mannwhitney_p_sample_level'])}, d={as_float(plasma['cohen_d_sample_level']):.2f}")
    ax1.set_ylim(-0.06, 1.36)

    sub = sens[sens["subset"] == "all_samples"].copy()
    sub["label"] = sub["signature"].map(SIGNATURE_LABELS).fillna(sub["signature"])
    sub = sub.sort_values("cohen_d_sample_level")
    colors = ["#C44E52" if sig == "plasma_secretory" else "#9CA3AF" for sig in sub["signature"]]
    ax2.barh(sub["label"], sub["cohen_d_sample_level"], color=colors)
    ax2.axvline(0, color="#111827", lw=0.8)
    ax2.set_xlabel("Cohen d, MM vs control")
    ax2.set_title("Sample-level spatial programs")
    clean_axis(ax2)

    genes = shortlist[shortlist["gene"].isin(PLASMA_GENES)].copy()
    genes = genes.sort_values("cohen_d_sample_level")
    ax3.barh(genes["gene"], genes["cohen_d_sample_level"], color="#C44E52")
    ax3.axvline(0, color="#111827", lw=0.8)
    for y, (_, row) in enumerate(genes.iterrows()):
        ax3.text(row["cohen_d_sample_level"] + 0.04, y, f"p={format_p(row['mannwhitney_p_sample_level'])}", va="center", fontsize=6.5)
    ax3.set_xlabel("Cohen d, MM vs control")
    ax3.set_title("Spatial candidate genes")
    clean_axis(ax3)

    panel_label(ax1, "A")
    panel_label(ax2, "B")
    panel_label(ax3, "C")

    fig.suptitle("Fig. 2 | Spatial discovery of the plasma-secretory program", x=0.01, ha="left", fontweight="bold")
    save_figure(fig, "fig2_spatial_plasma_secretory_discovery")


def plot_fig3(tables: dict[str, pd.DataFrame]) -> None:
    cell = tables["scrna_celltype"]
    stage = tables["scrna_stage"]
    gene = tables["scrna_gene_celltype"]

    fig = plt.figure(figsize=(12.1, 4.9))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.65, 1.15, 1.1])
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])

    dot = (
        gene[gene["gene"].isin(AXIS_GENES)]
        .groupby(["marker_inferred_cell_type", "gene"], as_index=False)
        .agg(mean_log_norm=("mean_log_norm", "mean"), pct_detected=("pct_detected", "mean"))
    )
    cell_order = (
        cell.sort_values("plasma_secretory_score", ascending=False)["marker_inferred_cell_type"]
        .tolist()
    )
    gene_order = AXIS_GENES
    x_map = {c: i for i, c in enumerate(cell_order)}
    y_map = {g: i for i, g in enumerate(gene_order)}
    for _, row in dot.iterrows():
        if row["marker_inferred_cell_type"] not in x_map:
            continue
        ax1.scatter(
            x_map[row["marker_inferred_cell_type"]],
            y_map[row["gene"]],
            s=25 + 190 * as_float(row["pct_detected"]),
            c=[as_float(row["mean_log_norm"])],
            cmap="Reds",
            vmin=0,
            vmax=max(2.8, dot["mean_log_norm"].max()),
            edgecolor="#374151",
            linewidth=0.25,
        )
    ax1.set_xticks(range(len(cell_order)))
    ax1.set_xticklabels([c.replace("_", " ") for c in cell_order], rotation=45, ha="right")
    ax1.set_yticks(range(len(gene_order)))
    ax1.set_yticklabels(gene_order)
    ax1.set_title("Axis genes by inferred cell type")
    ax1.grid(False)
    for spine in ax1.spines.values():
        spine.set_visible(False)
    norm = mpl.colors.Normalize(vmin=0, vmax=max(2.8, dot["mean_log_norm"].max()))
    sm = mpl.cm.ScalarMappable(norm=norm, cmap="Reds")
    cbar = fig.colorbar(sm, ax=ax1, fraction=0.045, pad=0.02)
    cbar.set_label("Mean log-normalized expression")

    cell_plot = cell.sort_values("plasma_secretory_score")
    colors = ["#C44E52" if c == "plasma_cell" else "#9CA3AF" for c in cell_plot["marker_inferred_cell_type"]]
    ax2.barh(cell_plot["marker_inferred_cell_type"].str.replace("_", " "), cell_plot["plasma_secretory_score"], color=colors)
    ax2.set_xlabel("Mean plasma-secretory score")
    ax2.set_title("Program localization")
    clean_axis(ax2)

    stage_order = ["HD", "MGUS", "SMM", "MM"]
    stage_plot = stage.set_index("stage").loc[stage_order].reset_index()
    ax3.plot(stage_plot["stage"], stage_plot["plasma_secretory_score"], color="#C44E52", marker="o", lw=1.8)
    ax3.bar(stage_plot["stage"], stage_plot["plasma_secretory_score"], color="#F3D3D5", edgecolor="#C44E52", linewidth=0.7, zorder=0)
    ax3.set_ylabel("Mean plasma-secretory score")
    ax3.set_title("Disease-stage trend")
    clean_axis(ax3)

    panel_label(ax1, "A")
    panel_label(ax2, "B")
    panel_label(ax3, "C")

    fig.suptitle("Fig. 3 | Single-cell localization of the plasma-secretory axis", x=0.01, ha="left", fontweight="bold")
    save_figure(fig, "fig3_scrna_plasma_secretory_localization")


def plot_fig4(tables: dict[str, pd.DataFrame]) -> None:
    scores = tables["bulk_scores"]
    assoc = tables["bulk_assoc"].dropna(subset=["best_fdr"]).copy()
    assoc["neg_log10_fdr"] = -np.log10(assoc["best_fdr"].clip(lower=1e-12))

    fig = plt.figure(figsize=(11.5, 4.4))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.45, 1.1, 1.1])
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])

    top = assoc.sort_values("best_fdr").head(8).copy()
    top["label"] = top["dataset"] + " | " + top["outcome"].astype(str) + " | " + top["variable"].astype(str)
    top = top.sort_values("neg_log10_fdr")
    colors = ["#C44E52" if f < 0.05 else "#9CA3AF" for f in top["best_fdr"]]
    ax1.barh(top["label"], top["neg_log10_fdr"], color=colors)
    ax1.axvline(-math.log10(0.05), color="#111827", lw=0.8, ls="--")
    ax1.set_xlabel("-log10(FDR)")
    ax1.set_title("Independent GEO bulk associations")
    clean_axis(ax1)

    gse2658 = scores[(scores["dataset"] == "GSE2658") & (scores["AMP_high_3plus"].notna())].copy()
    gse2658["AMP_group"] = np.where(pd.to_numeric(gse2658["AMP_high_3plus"], errors="coerce") == 1, "1q21 >=3", "1q21 <3")
    box_scatter(
        ax2,
        gse2658,
        "AMP_group",
        "clinical_subtype_module_score_z",
        ["1q21 <3", "1q21 >=3"],
        [PALETTE["control"], PALETTE["MM"]],
        "Clinical subtype module z-score",
    )
    row = assoc[(assoc["dataset"] == "GSE2658") & (assoc["variable"] == "clinical_subtype_module_score_z") & (assoc["outcome"] == "AMP_high_3plus")].iloc[0]
    ax2.set_title(f"GSE2658 1q21 amplification\nFDR={format_p(row['best_fdr'])}")

    gse24080 = scores[(scores["dataset"] == "GSE24080") & (scores["os_24mo_event"].notna())].copy()
    gse24080["OS24"] = np.where(pd.to_numeric(gse24080["os_24mo_event"], errors="coerce") == 1, "death <24 mo", "alive >=24 mo")
    box_scatter(
        ax3,
        gse24080,
        "OS24",
        "XBP1_z",
        ["alive >=24 mo", "death <24 mo"],
        [PALETTE["control"], PALETTE["MM"]],
        "XBP1 z-score",
    )
    row = assoc[(assoc["dataset"] == "GSE24080") & (assoc["variable"] == "XBP1_z") & (assoc["outcome"] == "os_24mo_event")].iloc[0]
    ax3.set_title(f"GSE24080 OS milestone\nFDR={format_p(row['best_fdr'])}")

    panel_label(ax1, "A")
    panel_label(ax2, "B")
    panel_label(ax3, "C")

    fig.suptitle("Fig. 4 | External GEO bulk support for the clinical subtype axis", x=0.01, ha="left", fontweight="bold")
    save_figure(fig, "fig4_geo_bulk_clinical_support")


def plot_fig5(tables: dict[str, pd.DataFrame]) -> None:
    scores = tables["comm_scores"].copy()
    assoc = tables["comm_assoc"].dropna(subset=["best_fdr"]).copy()
    assoc["neg_log10_fdr"] = -np.log10(assoc["best_fdr"].clip(lower=1e-12))
    adjusted = tables.get("adjusted_models", pd.DataFrame())
    ng_assoc = tables.get("ng2024_assoc", pd.DataFrame())
    ng_merged = tables.get("ng2024_merged", pd.DataFrame())

    fig = plt.figure(figsize=(13.2, 8.2))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.0, 1.0], width_ratios=[1.1, 1.0, 1.12])
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    ax4 = fig.add_subplot(gs[1, 0])
    ax5 = fig.add_subplot(gs[1, 1])
    ax6 = fig.add_subplot(gs[1, 2])

    top = assoc.sort_values("best_fdr").head(10).copy()
    outcome_labels = {
        "os_event": "OS event",
        "iss_stage_num": "ISS ordinal",
        "iss_stage_III": "ISS III",
        "os_time_months/os_event": "Median-split OS",
    }
    variable_labels = {
        "plasma_secretory_score_z": "Plasma score",
        "clinical_subtype_module_score_z": "Module",
        "TXNDC5_z": "TXNDC5",
        "POU2AF1_z": "POU2AF1",
        "XBP1_z": "XBP1",
        "JCHAIN_z": "JCHAIN",
    }
    top["label"] = top["outcome"].map(outcome_labels).fillna(top["outcome"].astype(str)) + " | " + top["variable"].map(variable_labels).fillna(top["variable"].astype(str))
    top = top.sort_values("neg_log10_fdr")
    colors = ["#C44E52" if f < 0.05 else "#9CA3AF" for f in top["best_fdr"]]
    ax1.barh(top["label"], top["neg_log10_fdr"], color=colors)
    ax1.axvline(-math.log10(0.05), color="#111827", lw=0.8, ls="--")
    ax1.set_xlabel("-log10(FDR)")
    ax1.set_title("CoMMpass/GDC association ranking")
    clean_axis(ax1)

    scores["OS_event_group"] = np.where(pd.to_numeric(scores["os_event"], errors="coerce") == 1, "OS event", "No OS event")
    box_scatter(
        ax2,
        scores.dropna(subset=["os_event", "plasma_secretory_score_z"]),
        "OS_event_group",
        "plasma_secretory_score_z",
        ["No OS event", "OS event"],
        [PALETTE["control"], PALETTE["MM"]],
        "Plasma-secretory score z",
    )
    row = assoc[(assoc["variable"] == "plasma_secretory_score_z") & (assoc["outcome"] == "os_event")].iloc[0]
    ax2.set_title(f"Overall survival event\nFDR={format_p(row['best_fdr'])}")

    km = scores[["plasma_secretory_score_z", "os_time_months", "os_event"]].dropna()
    km = km[(km["os_time_months"] > 0) & (km["os_event"].isin([0, 1]))]
    cutoff = km["plasma_secretory_score_z"].median()
    low = km[km["plasma_secretory_score_z"] < cutoff]
    high = km[km["plasma_secretory_score_z"] >= cutoff]
    for label, data, color in [("Low", low, PALETTE["low"]), ("High", high, PALETTE["high"])]:
        xs, ys = km_curve(data["os_time_months"].to_numpy(float), data["os_event"].to_numpy(int))
        events = int(data["os_event"].sum())
        ax3.step(xs, ys, where="post", lw=1.8, color=color, label=f"{label} (n={len(data)}, events={events})")
    row = assoc[(assoc["variable"] == "plasma_secretory_score_z") & (assoc["outcome"] == "os_time_months/os_event")].iloc[0]
    ax3.set_ylim(0, 1.03)
    ax3.set_xlabel("OS time, months")
    ax3.set_ylabel("Overall survival probability")
    ax3.set_title(f"Median split OS\nlog-rank FDR={format_p(row['best_fdr'])}")
    ax3.legend(frameon=False)
    clean_axis(ax3)

    if not adjusted.empty:
        model_rows = []
        desired = [
            ("OS adjusted for age, sex, ISS, 1q21", "plasma_secretory_score_z"),
            ("OS adjusted for age, sex, ISS, 1q21", "clinical_subtype_module_score_z"),
            ("OS adjusted for age, sex, ISS, 1q21", "JCHAIN_z"),
            ("1q21 gain/amplification adjusted for age, sex, ISS", "plasma_secretory_score_z"),
            ("1q21 gain/amplification adjusted for age, sex, ISS", "TXNDC5_z"),
        ]
        for model_name, score in desired:
            hit = adjusted[(adjusted["model_name"] == model_name) & (adjusted["score"] == score)]
            if not hit.empty:
                model_rows.append(hit.iloc[0])
        forest = pd.DataFrame(model_rows)
        if not forest.empty:
            labels = []
            for _, row in forest.iterrows():
                score_label = str(row["score_label"]).replace("POU2AF1/XBP1/JCHAIN module", "Module")
                if str(row["model_name"]).startswith("OS adjusted"):
                    labels.append(f"OS + age/sex/ISS/1q21\n{score_label}")
                else:
                    labels.append(f"1q21 + age/sex/ISS\n{score_label}")
            y = np.arange(len(forest))
            for i, (_, row) in enumerate(forest.iterrows()):
                color = "#C44E52" if as_float(row["fdr"]) < 0.05 else "#9CA3AF"
                ax4.errorbar(
                    as_float(row["effect"]),
                    i,
                    xerr=[[as_float(row["effect"]) - as_float(row["ci_lower"])], [as_float(row["ci_upper"]) - as_float(row["effect"])]],
                    fmt="none",
                    ecolor=color,
                    elinewidth=1.4,
                    capsize=2,
                )
                ax4.scatter(as_float(row["effect"]), i, c=color, s=28, zorder=3)
                ax4.text(as_float(row["ci_upper"]) + 0.05, i, f"FDR={format_p(row['fdr'])}", va="center", fontsize=6.4)
            ax4.set_yticks(y)
            ax4.set_yticklabels(labels, fontsize=6.6)
            ax4.invert_yaxis()
            ax4.axvline(1.0, color="#111827", lw=0.8, ls="--")
            xmax = max(2.45, float(forest["ci_upper"].max()) + 0.4)
            ax4.set_xlim(0.55, xmax)
            ax4.set_xlabel("Adjusted HR / OR per 1 SD")
            ax4.set_title("Adjusted CoMMpass/NG2024 models")
            clean_axis(ax4)
    else:
        ax4.axis("off")

    if not ng_merged.empty and {"Cp_1q21_Call", "plasma_secretory_score_z"}.issubset(ng_merged.columns):
        tmp = ng_merged[["Cp_1q21_Call", "plasma_secretory_score_z"]].copy()
        tmp["Cp_1q21_Call"] = pd.to_numeric(tmp["Cp_1q21_Call"], errors="coerce")
        tmp["group"] = np.where(tmp["Cp_1q21_Call"] == 1, "1q21 gain", "No 1q21 gain")
        tmp = tmp[tmp["Cp_1q21_Call"].isin([0, 1])].dropna(subset=["plasma_secretory_score_z"])
        box_scatter(
            ax5,
            tmp,
            "group",
            "plasma_secretory_score_z",
            ["No 1q21 gain", "1q21 gain"],
            [PALETTE["control"], PALETTE["MM"]],
            "Plasma-secretory score z",
        )
        if not ng_assoc.empty:
            hit = ng_assoc[(ng_assoc["feature"] == "Cp_1q21_Call") & (ng_assoc["score"] == "plasma_secretory_score_z")]
            if not hit.empty:
                row = hit.iloc[0]
                ax5.set_title(f"NG2024 1q21 annotation\nmedian delta={as_float(row['effect']):.2f}, FDR={format_p(row['fdr'])}")
    else:
        ax5.axis("off")

    if not ng_assoc.empty:
        keep = ng_assoc[
            (
                ((ng_assoc["feature"] == "PR") & (ng_assoc["score"] == "plasma_secretory_score_z"))
                | ((ng_assoc["feature"] == "RNA_Subtype_Name") & (ng_assoc["score"] == "plasma_secretory_score_z"))
                | ((ng_assoc["feature"] == "Cp_1q21_Call") & (ng_assoc["score"] == "plasma_secretory_score_z"))
                | ((ng_assoc["feature"] == "Cp_1q21_Call") & (ng_assoc["score"] == "TXNDC5_z"))
                | ((ng_assoc["feature"] == "Cp_17p13_Call") & (ng_assoc["score"] == "POU2AF1_z"))
            )
        ].copy()
        keep = keep.sort_values("fdr")
        feature_labels = {
            "PR": "PR probability",
            "RNA_Subtype_Name": "RNA subtype",
            "Cp_1q21_Call": "1q21",
            "Cp_17p13_Call": "17p13",
        }
        keep["label"] = keep["feature"].map(feature_labels).fillna(keep["feature"].astype(str)) + " | " + keep["score"].map(variable_labels).fillna(keep["score"].astype(str))
        keep["neg_log10_fdr"] = -np.log10(keep["fdr"].astype(float).clip(lower=1e-30))
        keep = keep.sort_values("neg_log10_fdr")
        colors = ["#C44E52" if f < 0.05 else "#9CA3AF" for f in keep["fdr"]]
        ax6.barh(keep["label"], keep["neg_log10_fdr"], color=colors)
        ax6.axvline(-np.log10(0.05), color="#111827", lw=0.8, ls="--")
        ax6.set_xlabel("-log10(FDR)")
        ax6.set_title("Public NG2024 molecular annotations")
        clean_axis(ax6)
    else:
        ax6.axis("off")

    panel_label(ax1, "A")
    panel_label(ax2, "B")
    panel_label(ax3, "C")
    panel_label(ax4, "D")
    panel_label(ax5, "E")
    panel_label(ax6, "F")

    fig.suptitle("Fig. 5 | CoMMpass/GDC and NG2024 validation of the plasma-secretory axis", x=0.01, ha="left", fontweight="bold")
    save_figure(fig, "fig5_commppass_os_iss_validation")


def plot_fig6() -> None:
    source_stem = GSE299193 / "gse299193_xenium_axis_validation"
    target_stem = OUT / "fig6_gse299193_xenium_spatial_validation"
    for suffix in [".png", ".svg", ".pdf"]:
        source = source_stem.with_suffix(suffix)
        if source.exists():
            shutil.copyfile(source, target_stem.with_suffix(suffix))


def write_figure_legends(evidence: pd.DataFrame) -> None:
    lines = [
        "# Draft Figure Legends",
        "",
        "## Figure 1",
        "",
        "Cross-cohort study design and evidence chain. The workflow starts from spatial discovery in GSE269875, adds second spatial validation in GSE299193 Xenium, proceeds through single-cell localization in GSE271107, external GEO bulk validation in GSE24080/GSE2658, and clinical/molecular validation in MMRF-COMMPASS/GDC plus NG2024 public annotations.",
        "",
        "## Figure 2",
        "",
        "Spatial discovery of the plasma-secretory program. Sample-level MM versus control differences are shown for the plasma-secretory score, followed by effect-size ranking across spatial programs and selected axis-associated candidate genes.",
        "",
        "## Figure 3",
        "",
        "Single-cell localization of the plasma-secretory axis. Dot size indicates detection fraction and color indicates mean log-normalized expression across marker-inferred cell types. The plasma-cell compartment shows the strongest plasma-secretory program localization, with TXNDC5 retained as a localization candidate.",
        "",
        "## Figure 4",
        "",
        "External GEO bulk support for the clinical subtype axis. Ranked association statistics summarize subtype and risk links in GSE24080 and GSE2658. Boxplots show representative associations with 1q21 amplification and 24-month OS milestone status.",
        "",
        "## Figure 5",
        "",
        "CoMMpass/GDC and public NG2024 validation. The plasma-secretory score and related subtype module show association with OS event, ISS stage, median-split overall survival, public NG2024 RNA subtype probability, and 1q21 copy-number annotation. Adjusted Cox/logistic models summarize associations after age, sex, ISS and 1q21 or molecular-risk covariate adjustment where applicable.",
        "",
        "## Figure 6",
        "",
        "Independent GSE299193 Xenium spatial validation. Sample-level Xenium matrices show higher plasma-secretory and POU2AF1/XBP1 module scores in active MM/RM samples compared with Ctrl/MGUS/SM samples. The heatmap displays axis genes covered by the Xenium panel. TXNDC5, JCHAIN and SDC1 are absent from this Xenium panel and are therefore not claimed as directly validated in this cohort.",
        "",
    ]
    (REPORTS / "FIGURE_LEGENDS_DRAFT.md").write_text("\n".join(lines), encoding="utf-8")


def write_results_skeleton(evidence: pd.DataFrame) -> None:
    spatial = evidence[evidence["evidence_layer"] == "Spatial discovery"].iloc[0]
    second_spatial = evidence[
        (evidence["evidence_layer"] == "Second spatial validation")
        & (evidence["primary_feature"] == "plasma-secretory score")
    ].iloc[0]
    scrna = evidence[evidence["evidence_layer"] == "Single-cell localization"].iloc[0]
    comp_os = evidence[(evidence["cohort"] == "MMRF-COMMPASS/GDC") & (evidence["contrast_or_endpoint"] == "Overall survival event")].iloc[0]
    comp_iss = evidence[(evidence["cohort"] == "MMRF-COMMPASS/GDC") & (evidence["contrast_or_endpoint"] == "ISS ordinal stage")].iloc[0]
    comp_km = evidence[(evidence["cohort"] == "MMRF-COMMPASS/GDC") & (evidence["contrast_or_endpoint"] == "Overall survival")].iloc[0]
    adj_os = evidence[
        (evidence["evidence_layer"] == "Adjusted clinical/molecular model")
        & (evidence["primary_feature"] == "plasma_secretory_score_z")
        & (evidence["contrast_or_endpoint"] == "OS adjusted for age, sex, ISS and 1q21")
    ].iloc[0]
    ng_1q = evidence[
        (evidence["evidence_layer"] == "Public CoMMpass molecular annotation")
        & (evidence["primary_feature"] == "plasma_secretory_score_z")
        & (evidence["contrast_or_endpoint"] == "1q21 gain/amplification")
    ].iloc[0]

    lines = [
        "# Manuscript Results Skeleton",
        "",
        "## Result 1. Spatial transcriptomics identifies a plasma-secretory program enriched in MM bone marrow",
        "",
        f"- In GSE269875, the plasma-secretory score was higher in MM than control bone marrow samples ({spatial['effect_summary']}; Mann-Whitney p={format_p(spatial['p_value'])}).",
        "- This establishes the spatial discovery layer and motivates downstream single-cell and bulk clinical validation.",
        "- Claim boundary: this is a spatial program-level finding, not a standalone single-gene biomarker claim.",
        f"- In the independent GSE299193 Xenium cohort, the same plasma-secretory program was higher in MM/RM than Ctrl/MGUS/SM samples ({second_spatial['effect_summary']}; FDR={format_p(second_spatial['fdr_or_adjusted_p'])}).",
        "- GSE299193 validates the program-level spatial signal, but its Xenium panel does not contain TXNDC5, JCHAIN, or SDC1, so it should not be used as direct TXNDC5 validation.",
        "",
        "## Result 2. Single-cell validation localizes the axis to plasma-cell annotated compartments",
        "",
        f"- In GSE271107, TXNDC5 showed plasma-cell expression support ({scrna['effect_summary']}).",
        "- The plasma-secretory program was highest in marker-inferred plasma cells compared with other broad cell-type bins.",
        "- TXNDC5 should be presented as a spatial/single-cell localization candidate within the broader axis.",
        "",
        "## Result 3. External GEO bulk cohorts support a clinical subtype/risk-linked module",
        "",
        "- In GSE2658, the POU2AF1/XBP1/JCHAIN clinical subtype module was associated with 1q21 amplification.",
        "- In GSE24080, XBP1 showed FDR-supported association with 24-month OS death.",
        "- These results justify shifting the clinical framing from a single TXNDC5 marker to a broader plasma-secretory subtype axis.",
        "",
        "## Result 4. CoMMpass/GDC validates OS and ISS association of the plasma-secretory axis",
        "",
        f"- In 762 baseline MMRF-COMMPASS/GDC bone marrow CD138+ RNA-seq samples, the plasma-secretory score was associated with OS event ({comp_os['effect_summary']}; FDR={format_p(comp_os['fdr_or_adjusted_p'])}).",
        f"- The same score was associated with ISS ordinal stage ({comp_iss['effect_summary']}; FDR={format_p(comp_iss['fdr_or_adjusted_p'])}).",
        f"- Median-split OS analysis remained significant ({comp_km['effect_summary']}; log-rank FDR={format_p(comp_km['fdr_or_adjusted_p'])}).",
        f"- In public NG2024 CoMMpass molecular annotations, the plasma-secretory score was associated with 1q21 gain/amplification ({ng_1q['effect_summary']}; FDR={format_p(ng_1q['fdr_or_adjusted_p'])}).",
        f"- In the requested adjusted Cox model, the plasma-secretory score remained associated with OS after age, sex, ISS and 1q21 adjustment ({adj_os['effect_summary']}; FDR={format_p(adj_os['fdr_or_adjusted_p'])}).",
        "",
        "## Current Claim Boundary",
        "",
        "- The current manuscript can claim spatial discovery, independent second spatial validation, single-cell localization, OS/ISS association in CoMMpass/GDC, and public NG2024 molecular-annotation support including 1q21 and RNA-subtype probability.",
        "- It should not claim completed R-ISS, PFS, detailed cytogenetic high-risk, or treatment-response validation.",
        "- Those endpoints require fuller MMRF/CoMMpass clinical files outside the currently used GDC open clinical slice.",
        "",
        "## Draft One-Sentence Result Claim",
        "",
        "An MM bone marrow plasma-secretory spatial program is reproduced in a second Xenium spatial cohort, localized to plasma-cell compartments, and associated with overall survival, ISS, public CoMMpass 1q21/RNA-subtype annotations, and adjusted OS models, with TXNDC5 acting as a spatial/single-cell localization candidate and POU2AF1/XBP1 forming the clinically stronger panel-validated subtype module.",
        "",
    ]
    (REPORTS / "MANUSCRIPT_RESULTS_SKELETON.md").write_text("\n".join(lines), encoding="utf-8")


def write_design_reference_note() -> None:
    lines = [
        "# Figure Design Reference Note",
        "",
        "The manuscript figures were designed as reproducible multi-panel translational genomics figures using conventions common in high-impact primary research: cohort flow diagrams, effect-size ranked summaries, dot plots for single-cell localization, box/scatter overlays for clinical contrasts, and Kaplan-Meier survival panels.",
        "",
        "Reference class used for design only:",
        "",
        "- CoMMpass multi-omics cohort structure: Nature Genetics, `Comprehensive molecular profiling of multiple myeloma identifies refined copy number and expression subtypes`, https://www.nature.com/articles/s41588-024-01853-0",
        "- CoMMpass-linked single-cell outcome analysis style: Nature Cancer, `A single-cell atlas characterizes dysregulation of the bone marrow immune microenvironment associated with outcomes in multiple myeloma`, https://www.nature.com/articles/s43018-025-01072-4",
        "- MM spatial transcriptomics context: Communications Biology, `Characterization of the bone marrow architecture of multiple myeloma using spatial transcriptomics`, https://www.nature.com/articles/s42003-025-08975-z",
        "- MM genomic cohort figure conventions: Nature Communications, `Genomic landscape and chronological reconstruction of driver events in multiple myeloma`, https://www.nature.com/articles/s41467-019-11680-1",
        "",
        "Excluded reference classes:",
        "",
        "- textbooks;",
        "- encyclopedia pages;",
        "- blogs;",
        "- non-peer-reviewed tutorial examples;",
        "- low-quality or non-primary papers.",
        "",
        "Design rules applied:",
        "",
        "- Every figure panel is directly generated from local project data or local analysis outputs.",
        "- Figures emphasize cohort, sample size, effect direction, FDR/p-value, and claim boundary.",
        "- No decorative gradients, stock images, or non-data graphics were used.",
        "- Output formats include PNG for review plus SVG/PDF for manuscript assembly.",
        "",
    ]
    (REPORTS / "FIGURE_DESIGN_REFERENCE_NOTE.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    configure_style()
    tables = load_core_tables()
    evidence = build_evidence_table(tables)
    plot_fig1(evidence)
    plot_fig2(tables)
    plot_fig3(tables)
    plot_fig4(tables)
    plot_fig5(tables)
    plot_fig6()
    write_figure_legends(evidence)
    write_results_skeleton(evidence)
    write_design_reference_note()
    print(f"Wrote manuscript figures and tables to: {OUT}")
    print(f"Wrote manuscript report drafts to: {REPORTS}")


if __name__ == "__main__":
    main()
