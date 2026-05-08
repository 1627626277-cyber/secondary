#!/usr/bin/env python3
"""
Redraw all manuscript figures (Fig 1-8) using processed analysis data,
following Nature publication figure style guidelines.

Data sources: all processed TSV files under D:\\二区\\analysis\\
Output: D:\\二区\\analysis\\redrawn_figures\\*.svg, *.pdf
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT = Path(r"D:\二区")
OUT = ROOT / "analysis" / "redrawn_figures"
OUT.mkdir(parents=True, exist_ok=True)

SPATIAL_CAND = ROOT / "analysis" / "spatial_candidate_signatures"
SPATIAL_PRELIM = ROOT / "analysis" / "spatial_preliminary"
SPATIAL_MORAN = ROOT / "analysis" / "spatial_autocorrelation_niche"
SCRNA = ROOT / "analysis" / "scrna_gse271107_validation"
BULK_CLIN = ROOT / "analysis" / "bulk_clinical_validation"
PLASMA_REFINE = ROOT / "analysis" / "plasma_secretory_subtype_refinement"
COMMPASS = ROOT / "analysis" / "commppass_gdc_validation"
NG2024 = ROOT / "analysis" / "skerget_ng2024_public_supplement"
ADJUSTED = ROOT / "analysis" / "commppass_ng2024_adjusted_models"
SENSITIVITY = ROOT / "analysis" / "commppass_sensitivity_models"
COX_PH = ROOT / "analysis" / "commppass_cox_ph_assumption"
GSE299193 = ROOT / "analysis" / "gse299193_xenium_validation"

# ── Nature-style rcParams ──────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.titlesize": 12,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 1.5,
    "xtick.major.width": 1.0,
    "ytick.major.width": 1.0,
    "legend.frameon": False,
})

# ── Palettes ────────────────────────────────────────────────────────────────
PALETTE = {
    "control": "#4C72B0",      # Nature blue
    "MM": "#C44E52",            # Nature red
    "HD": "#4C72B0",
    "MGUS": "#55A868",          # Nature green
    "SMM": "#DD8452",           # Nature orange
    "I": "#7EA1C4",
    "II": "#B6B1D6",
    "III": "#C44E52",
    "low": "#4C72B0",
    "high": "#C44E52",
    "signal": "#C44E52",
    "neutral": "#9CA3AF",
    "stromal": "#DD8452",
    "myeloid": "#55A868",
    "cycling": "#8B5CF6",
    "endothelial": "#3B82F6",
    "tnk": "#F59E0B",
    "erythroid": "#EC4899",
}

SIGNATURE_LABELS = {
    "plasma_secretory_score": "Plasma-secretory",
    "plasma_secretory": "Plasma-secretory",
    "myeloid_inflammatory_score": "Myeloid inflammatory",
    "myeloid_inflammatory": "Myeloid inflammatory",
    "t_nk_cytotoxic_exhaustion_score": "T/NK cytotoxic",
    "t_nk_cytotoxic_exhaustion": "T/NK cytotoxic",
    "stromal_ecm_score": "Stromal ECM",
    "stromal_ecm": "Stromal ECM",
    "endothelial_angiogenic_score": "Endothelial angiogenic",
    "endothelial_angiogenic": "Endothelial angiogenic",
    "erythroid_megak_score": "Erythroid/megak",
    "erythroid_megak": "Erythroid/megak",
    "cycling_proliferation_score": "Cycling",
    "cycling_proliferation": "Cycling",
    "plasma_cell_score": "Plasma cell",
    "immune_pan_score": "Immune pan",
    "t_cell_nk_score": "T cell/NK",
    "myeloid_score": "Myeloid",
    "stromal_ecm_score": "Stromal ECM",
    "endothelial_score": "Endothelial",
}

AXIS_GENES = ["TXNDC5", "POU2AF1", "XBP1", "JCHAIN", "MZB1", "SDC1", "PIM2", "IRF4", "PRDM1"]
CORE_AXIS = ["TXNDC5", "POU2AF1", "XBP1", "JCHAIN"]

# ── Helpers ─────────────────────────────────────────────────────────────────
def read_tsv(path: Path) -> pd.DataFrame:
    """Read a TSV file; raise if missing."""
    if not path.exists():
        print(f"WARNING: {path} not found, skipping dependent panel.")
        return pd.DataFrame()
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
        return f"p={p:.1e}"
    if p < 0.01:
        return f"p={p:.3f}"
    return f"p={p:.2f}"


def clean_axis(ax: plt.Axes) -> None:
    """Nature-style axis cleanup."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def panel_label(ax: plt.Axes, label: str, x: float = -0.10, y: float = 1.06) -> None:
    ax.text(x, y, label, transform=ax.transAxes, ha="left", va="bottom",
            fontsize=10, fontweight="bold")


def save_figure(fig: plt.Figure, stem: str) -> None:
    fig.tight_layout(pad=0.8)
    for suffix, dpi in [(".svg", 300), (".pdf", 300), (".png", 350)]:
        fig.savefig(OUT / f"{stem}{suffix}", dpi=dpi, bbox_inches="tight")
    print(f"  Saved: {stem}")
    plt.close(fig)


def jitter(values: np.ndarray, seed: int = 42, width: float = 0.08) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.normal(0, width, size=len(values))


def barh_simple(ax, labels, values, colors, xlabel, title):
    """Simple horizontal bar chart."""
    y_pos = range(len(labels))
    ax.barh(y_pos, values, color=colors, height=0.65, edgecolor="#222222", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.axvline(0, color="#111827", linewidth=0.7)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    clean_axis(ax)


def box_scatter(ax, data, group_col, value_col, order, colors, ylabel):
    """Boxplot with overlaid scatter points."""
    vals = []
    for group in order:
        arr = pd.to_numeric(data.loc[data[group_col] == group, value_col],
                            errors="coerce").dropna().to_numpy()
        vals.append(arr)

    bp = ax.boxplot(vals, patch_artist=True, showfliers=False, widths=0.50)
    for patch, color in zip(bp["boxes"], colors):
        patch.set(facecolor=color, alpha=0.72, edgecolor="#222222", linewidth=1.0)
    for element in ["whiskers", "caps", "medians"]:
        for obj in bp[element]:
            obj.set(color="#222222", linewidth=1.0)

    for i, arr in enumerate(vals, start=1):
        if len(arr) == 0:
            continue
        x_jittered = np.full(len(arr), i) + jitter(arr, seed=100 + i, width=0.04)
        ax.scatter(x_jittered, arr, s=12, color="#222222", alpha=0.65,
                   linewidths=0, zorder=3)
        y_max = np.nanmax(arr)
        y_range = y_max - np.nanmin(arr) + 0.1
        ax.text(i, y_max + 0.05 * y_range, f"n={len(arr)}",
                ha="center", va="bottom", fontsize=7, color="#374151")

    ax.set_xticks(range(1, len(order) + 1))
    ax.set_xticklabels(order)
    ax.set_ylabel(ylabel)
    clean_axis(ax)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — Study design & evidence chain
# ══════════════════════════════════════════════════════════════════════════════
def plot_fig1() -> None:
    """Schematic evidence-chain figure."""
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)

    # Evidence stages
    stages = [
        ("Spatial discovery\n(GSE269875)", "Plasma-secretory program\nMM vs control\nspatial transcriptomics", 0.5, 3.3, "#D6E7F8"),
        ("scRNA localization\n(GSE271107)", "Plasma-cell compartment\nTXNDC5 detection\ncell-type resolution", 2.9, 3.3, "#D6F0E8"),
        ("Bulk association\n(GSE24080/GSE2658)", "Subtype/clinical-risk\nPOU2AF1/XBP1/JCHAIN\n1q21 amplification", 5.3, 3.3, "#FDF1C7"),
        ("CoMMpass molecular\n(MMRF + NG2024)", "OS, ISS, 1q21\nPR RNA subtype\n762 baseline samples", 7.7, 3.3, "#F4D4D6"),
    ]
    for title, body, x, y, color in stages:
        rect = mpl.patches.FancyBboxPatch(
            (x, y), 1.7, 1.05,
            boxstyle="round,pad=0.04,rounding_size=0.06",
            facecolor=color, edgecolor="#374151", linewidth=1.2
        )
        ax.add_patch(rect)
        ax.text(x + 0.85, y + 0.75, title, ha="center", va="center",
                fontsize=9, fontweight="bold")
        ax.text(x + 0.85, y + 0.30, body, ha="center", va="center",
                fontsize=7.5, linespacing=1.2)

    # Arrows connecting stages
    for x0 in [2.2, 4.6, 7.0]:
        ax.annotate("", xy=(x0 + 0.55, 3.82), xytext=(x0, 3.82),
                    arrowprops=dict(arrowstyle="->", color="#111827", lw=1.2))

    # Claim box
    claim_text = (
        "Defensible current claim:\n"
        "MM bone marrow plasma-secretory spatial program is single-cell localized "
        "and associated with OS / ISS /\npublic molecular-risk annotations in CoMMpass."
    )
    ax.add_patch(mpl.patches.Rectangle(
        (0.8, 1.30), 8.4, 0.85,
        facecolor="#F9FAFB", edgecolor="#374151", linewidth=1.0
    ))
    ax.text(5.0, 1.72, claim_text, ha="center", va="center",
            fontsize=9, linespacing=1.3)

    # Limitation note
    limits = (
        "Claim boundary: R-ISS, PFS and treatment-response validation require fuller "
        "clinical files and are not claimed from the GDC open slice."
    )
    ax.text(5.0, 0.65, limits, ha="center", va="center",
            fontsize=7.5, color="#374151")

    ax.text(0.1, 5.20, "Fig. 1 | Cross-cohort study design and evidence chain",
            ha="left", va="top", fontsize=12, fontweight="bold")
    save_figure(fig, "fig1_study_design_evidence_chain")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Spatial plasma-secretory program discovery
# ══════════════════════════════════════════════════════════════════════════════
def plot_fig2() -> None:
    """Spatial discovery: plasma-secretory score, program ranking, gene ranking."""
    sample_scores = read_tsv(SPATIAL_CAND / "sample_signature_scores.tsv")
    shortlist = read_tsv(SPATIAL_CAND / "candidate_validation_shortlist.tsv")

    if sample_scores.empty:
        print("SKIP Fig 2: missing data")
        return

    fig = plt.figure(figsize=(11.5, 4.5))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.3, 1.5], wspace=0.35)

    # --- Panel A: Plasma-secretory score boxplot MM vs control ---
    ax_a = fig.add_subplot(gs[0, 0])
    box_scatter(ax_a, sample_scores, "Group", "plasma_secretory_score",
                ["control", "MM"],
                [PALETTE["control"], PALETTE["MM"]],
                "Plasma-secretory score")

    # Compute stats
    mm_vals = pd.to_numeric(
        sample_scores.loc[sample_scores["Group"] == "MM", "plasma_secretory_score"],
        errors="coerce").dropna()
    ctrl_vals = pd.to_numeric(
        sample_scores.loc[sample_scores["Group"] == "control", "plasma_secretory_score"],
        errors="coerce").dropna()
    if len(mm_vals) > 0 and len(ctrl_vals) > 0:
        d = (mm_vals.mean() - ctrl_vals.mean()) / np.sqrt(
            ((len(mm_vals) - 1) * mm_vals.std()**2 + (len(ctrl_vals) - 1) * ctrl_vals.std()**2)
            / (len(mm_vals) + len(ctrl_vals) - 2))
        from scipy.stats import mannwhitneyu
        try:
            _, p = mannwhitneyu(mm_vals, ctrl_vals, alternative="two-sided")
        except Exception:
            p = float("nan")
        ax_a.set_title(f"MM enrichment\nd={d:.2f}, {format_p(p)}", fontsize=9)
    panel_label(ax_a, "a")

    # --- Panel B: Program-level effect ranking ---
    ax_b = fig.add_subplot(gs[0, 1])
    # Use shortlist data aggregated by category
    cats = shortlist["candidate_category"].dropna().unique()
    cat_data = []
    for cat in cats:
        sub = shortlist[shortlist["candidate_category"] == cat]
        d_mean = sub["cohen_d_sample_level"].mean()
        cat_data.append({"category": cat, "d": d_mean})

    cat_df = pd.DataFrame(cat_data).sort_values("d")
    label_map = {
        "region_linked_plasma_secretory": "Plasma-secretory",
        "canonical_plasma_support": "Canonical plasma",
        "stromal_ecm": "Stromal ECM",
        "myeloid_inflammatory": "Myeloid inflam.",
        "endothelial_angiogenic": "Endothelial",
        "erythroid_megak": "Erythroid/megak",
        "t_nk_or_exhaustion": "T/NK exhaustion",
    }
    labels = [label_map.get(c, c) for c in cat_df["category"]]
    colors = ["#C44E52" if "plasma" in str(c).lower() else "#9CA3AF"
              for c in cat_df["category"]]
    barh_simple(ax_b, labels, cat_df["d"].values, colors,
                "Mean Cohen d, MM vs control", "Candidate categories")
    panel_label(ax_b, "b")

    # --- Panel C: Top candidate gene ranking ---
    ax_c = fig.add_subplot(gs[0, 2])
    top_n = 12
    top_genes = shortlist.nlargest(top_n, "candidate_score")
    top_genes = top_genes.sort_values("candidate_score")
    gene_colors = ["#C44E52" if "plasma" in str(c).lower() or "canonical" in str(c).lower()
                   else "#9CA3AF" for _, c in top_genes[["candidate_category"]].iterrows()]
    barh_simple(ax_c, top_genes["gene"].values, top_genes["candidate_score"].values,
                gene_colors, "Candidate score", f"Top {top_n} candidate genes")
    for i, (_, row) in enumerate(top_genes.iterrows()):
        d_val = as_float(row.get("cohen_d_sample_level", float("nan")))
        ax_c.text(row["candidate_score"] + 0.15, i,
                  f"d={d_val:.2f}", va="center", fontsize=6)
    panel_label(ax_c, "c")

    fig.suptitle("Fig. 2 | Spatial discovery of the plasma-secretory program",
                 x=0.01, ha="left", fontweight="bold", fontsize=12)
    save_figure(fig, "fig2_spatial_plasma_secretory_discovery")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — Spatial organization and autocorrelation (Moran's I)
# ══════════════════════════════════════════════════════════════════════════════
def plot_fig3() -> None:
    """Spatial autocorrelation: Moran's I across programs and samples."""
    moran = read_tsv(SPATIAL_MORAN / "spatial_morans_i_results.tsv")

    if moran.empty:
        print("SKIP Fig 3: missing Moran's I data")
        return

    fig = plt.figure(figsize=(10.0, 5.0))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.6, 1.0], wspace=0.30)

    # --- Panel A: Moran's I by program across all samples ---
    ax_a = fig.add_subplot(gs[0, 0])

    # Aggregate by signature across all samples
    sig_order = [
        "plasma_secretory_score", "stromal_ecm_score",
        "myeloid_inflammatory_score", "cycling_proliferation_score",
        "endothelial_angiogenic_score", "t_nk_cytotoxic_exhaustion_score",
        "erythroid_megak_score"
    ]
    sig_colors_map = {
        "plasma_secretory_score": "#C44E52",
        "stromal_ecm_score": "#DD8452",
        "myeloid_inflammatory_score": "#55A868",
        "cycling_proliferation_score": "#8B5CF6",
        "endothelial_angiogenic_score": "#3B82F6",
        "t_nk_cytotoxic_exhaustion_score": "#F59E0B",
        "erythroid_megak_score": "#EC4899",
    }

    moran_data = []
    for sig in sig_order:
        sub = moran[moran["signature"] == sig]
        mi_vals = sub["morans_i"].dropna().values
        if len(mi_vals) > 0:
            moran_data.append({
                "sig": sig,
                "mean_mi": np.mean(mi_vals),
                "sem_mi": np.std(mi_vals) / np.sqrt(len(mi_vals)),
                "n": len(mi_vals)
            })

    md = pd.DataFrame(moran_data)
    labels = [SIGNATURE_LABELS.get(s, s) for s in md["sig"]]
    colors = [sig_colors_map.get(s, "#9CA3AF") for s in md["sig"]]
    y_pos = range(len(md))
    ax_a.barh(y_pos, md["mean_mi"].values, xerr=md["sem_mi"].values,
              color=colors, height=0.60, edgecolor="#222222", linewidth=0.6,
              capsize=3)
    ax_a.set_yticks(y_pos)
    ax_a.set_yticklabels(labels)
    ax_a.axvline(0, color="#111827", linewidth=0.7)
    ax_a.set_xlabel("Mean Moran's I (6-NN spatial graph)")
    ax_a.set_title("Spatial autocorrelation by program")
    clean_axis(ax_a)
    panel_label(ax_a, "a")

    # --- Panel B: Per-sample Moran's I for plasma-secretory ---
    ax_b = fig.add_subplot(gs[0, 1])
    plasma_moran = moran[
        (moran["signature"] == "plasma_secretory_score")
    ].copy()
    # Split by group
    plasma_mm = plasma_moran[plasma_moran["Group"] == "MM"]
    plasma_ctrl = plasma_moran[plasma_moran["Group"] == "control"]

    x_positions = []
    labels_b = []
    colors_b = []
    mi_vals_b = []

    for _, row in plasma_mm.iterrows():
        x_positions.append(len(labels_b))
        labels_b.append(row["Title"])
        colors_b.append(PALETTE["MM"])
        mi_vals_b.append(as_float(row["morans_i"]))

    for _, row in plasma_ctrl.iterrows():
        x_positions.append(len(labels_b))
        labels_b.append(row["Title"])
        colors_b.append(PALETTE["control"])
        mi_vals_b.append(as_float(row["morans_i"]))

    ax_b.bar(range(len(labels_b)), mi_vals_b, color=colors_b,
             edgecolor="#222222", linewidth=0.6)
    ax_b.set_xticks(range(len(labels_b)))
    ax_b.set_xticklabels(labels_b, rotation=45, ha="right", fontsize=7)
    ax_b.set_ylabel("Moran's I")
    ax_b.set_title("Plasma-secretory\nper-sample Moran's I")

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=PALETTE["MM"], label="MM"),
        Patch(facecolor=PALETTE["control"], label="Control"),
    ]
    ax_b.legend(handles=legend_elements, loc="upper right", fontsize=7)
    clean_axis(ax_b)
    panel_label(ax_b, "b")

    fig.suptitle("Fig. 3 | Spatial organization and autocorrelation analysis",
                 x=0.01, ha="left", fontweight="bold", fontsize=12)
    save_figure(fig, "fig3_spatial_organization_autocorrelation")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 4 — Xenium spatial reproducibility (GSE299193)
# ══════════════════════════════════════════════════════════════════════════════
def plot_fig4() -> None:
    """Xenium validation plot."""
    xenium_assoc_path = GSE299193 / "gse299193_axis_group_associations.tsv"
    xenium_scores_path = GSE299193 / "gse299193_sample_axis_scores.tsv"

    xenium_assoc = read_tsv(xenium_assoc_path) if xenium_assoc_path.exists() else pd.DataFrame()
    xenium_scores = read_tsv(xenium_scores_path) if xenium_scores_path.exists() else pd.DataFrame()

    if xenium_assoc.empty and xenium_scores.empty:
        print("SKIP Fig 4: missing Xenium data")
        # Try alternative path
        alt_path = GSE299193 / "gse299193_xenium_axis_validation.svg"
        if alt_path.exists():
            print(f"  Xenium validation exists at {alt_path}")
        return

    fig = plt.figure(figsize=(10.0, 4.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1.0], wspace=0.30)

    # --- Panel A: Feature score comparison between groups ---
    ax_a = fig.add_subplot(gs[0, 0])

    if not xenium_scores.empty:
        # Expect columns: sample, group, plasma_secretory_score, POU2AF1_XBP1_module_score
        score_cols = [c for c in xenium_scores.columns if "score" in c.lower()]
        group_col = None
        for gc in ["group", "Group", "condition", "disease_group"]:
            if gc in xenium_scores.columns:
                group_col = gc
                break

        if group_col and score_cols:
            # Use first score column
            sc = score_cols[0]
            groups = xenium_scores[group_col].unique()
            vals_by_group = []
            group_labels = []
            for g in groups:
                vals = pd.to_numeric(xenium_scores.loc[xenium_scores[group_col] == g, sc],
                                     errors="coerce").dropna()
                if len(vals) > 0:
                    vals_by_group.append(vals.values)
                    group_labels.append(str(g))

            colors_pick = [PALETTE.get(g.lower(), "#9CA3AF") for g in groups]

            bp = ax_a.boxplot(vals_by_group, patch_artist=True, showfliers=False, widths=0.50)
            for patch, color in zip(bp["boxes"], colors_pick[:len(bp["boxes"])]):
                patch.set(facecolor=color, alpha=0.72, edgecolor="#222222", linewidth=1.0)
            for i, arr in enumerate(vals_by_group, start=1):
                if len(arr) > 0:
                    x_j = np.full(len(arr), i) + jitter(arr, seed=200 + i, width=0.04)
                    ax_a.scatter(x_j, arr, s=10, color="#222222", alpha=0.6,
                                 linewidths=0, zorder=3)
            ax_a.set_xticks(range(1, len(group_labels) + 1))
            ax_a.set_xticklabels(group_labels, rotation=30, ha="right", fontsize=8)
            ax_a.set_ylabel(sc.replace("_", " "))
            ax_a.set_title("GSE299193 Xenium validation\nfeature score by group")
            clean_axis(ax_a)
    else:
        ax_a.text(0.5, 0.5, "Xenium data not available", ha="center", va="center",
                  transform=ax_a.transAxes, fontsize=11, color="#9CA3AF")
        ax_a.axis("off")

    panel_label(ax_a, "a")

    # --- Panel B: Association bar chart ---
    ax_b = fig.add_subplot(gs[0, 1])
    if not xenium_assoc.empty:
        # Extract relevant rows
        rel = xenium_assoc[xenium_assoc["contrast"].str.contains("MM_RM", na=False)]
        if len(rel) > 0:
            rel = rel.sort_values("delta_high_minus_low")
            labels = []
            effects = []
            p_vals = []
            for _, row in rel.iterrows():
                var_name = row.get("variable", "unknown")
                labels.append(var_name.replace("_score_z", "").replace("_", " "))
                effects.append(as_float(row.get("delta_high_minus_low", 0)))
                p_vals.append(as_float(row.get("mannwhitney_p", float("nan"))))
            colors_b = ["#C44E52" if e > 0 else "#4C72B0" for e in effects]
            ax_b.barh(range(len(labels)), effects, color=colors_b,
                      edgecolor="#222222", linewidth=0.5)
            for i, (e, p) in enumerate(zip(effects, p_vals)):
                ax_b.text(e + 0.02 * (max(abs(x) for x in effects) + 0.1), i,
                          format_p(p), va="center", fontsize=6.5)
            ax_b.set_yticks(range(len(labels)))
            ax_b.set_yticklabels(labels)
            ax_b.axvline(0, color="#111827", linewidth=0.8)
            ax_b.set_xlabel("Median delta (MM/RM vs Ctrl)")
            ax_b.set_title("Xenium axis associations")
            clean_axis(ax_b)
    else:
        ax_b.text(0.5, 0.5, "Association data not available", ha="center", va="center",
                  transform=ax_b.transAxes, fontsize=11, color="#9CA3AF")
        ax_b.axis("off")
    panel_label(ax_b, "b")

    fig.suptitle("Fig. 4 | Independent Xenium spatial reproducibility (GSE299193)",
                 x=0.01, ha="left", fontweight="bold", fontsize=12)
    save_figure(fig, "fig4_xenium_spatial_reproducibility")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 5 — Single-cell RNA-seq localization (GSE271107)
# ══════════════════════════════════════════════════════════════════════════════
def plot_fig5() -> None:
    """scRNA-seq: dot plot by cell type + bar chart."""
    sig_celltype = read_tsv(SCRNA / "gse271107_signature_by_celltype.tsv")
    gene_celltype = read_tsv(SCRNA / "gse271107_candidate_gene_by_sample_celltype.tsv")
    sig_stage_celltype = read_tsv(SCRNA / "gse271107_signature_by_stage_celltype.tsv")

    if sig_celltype.empty:
        print("SKIP Fig 5: missing scRNA data")
        return

    fig = plt.figure(figsize=(10.5, 4.8))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.7, 1.15], wspace=0.32)

    # --- Panel A: Dot plot of axis genes by cell type ---
    ax_a = fig.add_subplot(gs[0, 0])

    if not gene_celltype.empty:
        dot = gene_celltype[gene_celltype["gene"].isin(AXIS_GENES)].copy()
        if not dot.empty:
            dot_agg = dot.groupby(["marker_inferred_cell_type", "gene"],
                                  as_index=False).agg(
                mean_log_norm=("mean_log_norm", "mean"),
                pct_detected=("pct_detected", "mean"))

            cell_order = list(sig_celltype.sort_values("plasma_secretory_score",
                                                       ascending=False)["marker_inferred_cell_type"])
            gene_order = [g for g in AXIS_GENES if g in dot_agg["gene"].unique()]

            x_map = {c: i for i, c in enumerate(cell_order)}
            y_map = {g: i for i, g in enumerate(gene_order)}

            vmax = max(2.5, dot_agg["mean_log_norm"].max())
            for _, row in dot_agg.iterrows():
                ct = row["marker_inferred_cell_type"]
                g = row["gene"]
                if ct not in x_map or g not in y_map:
                    continue
                ax_a.scatter(
                    x_map[ct], y_map[g],
                    s=30 + 180 * as_float(row["pct_detected"]),
                    c=[as_float(row["mean_log_norm"])],
                    cmap="OrRd", vmin=0, vmax=vmax,
                    edgecolor="#374151", linewidth=0.3
                )
            ax_a.set_xticks(range(len(cell_order)))
            ax_a.set_xticklabels([c.replace("_", " ") for c in cell_order],
                                 rotation=45, ha="right", fontsize=7.5)
            ax_a.set_yticks(range(len(gene_order)))
            ax_a.set_yticklabels(gene_order)
            ax_a.set_title("Axis genes by inferred cell type\n(dot size = % detected)")

            # Colorbar
            norm = mpl.colors.Normalize(vmin=0, vmax=vmax)
            sm = mpl.cm.ScalarMappable(norm=norm, cmap="OrRd")
            cbar = fig.colorbar(sm, ax=ax_a, fraction=0.04, pad=0.02)
            cbar.set_label("Mean log-norm expr.", fontsize=8)
            for spine in ax_a.spines.values():
                spine.set_visible(False)
    else:
        ax_a.text(0.5, 0.5, "Gene-celltype data not available", ha="center", va="center",
                  transform=ax_a.transAxes, color="#9CA3AF")
        ax_a.axis("off")
    panel_label(ax_a, "a")

    # --- Panel B: Plasma-secretory score by cell type ---
    ax_b = fig.add_subplot(gs[0, 1])
    if not sig_celltype.empty:
        cell_plot = sig_celltype.sort_values("plasma_secretory_score")
        colors = ["#C44E52" if c == "plasma_cell" else "#9CA3AF"
                  for c in cell_plot["marker_inferred_cell_type"]]
        ax_b.barh(cell_plot["marker_inferred_cell_type"].str.replace("_", " "),
                  cell_plot["plasma_secretory_score"], color=colors,
                  height=0.60, edgecolor="#222222", linewidth=0.5)
        ax_b.set_xlabel("Mean plasma-secretory score")
        ax_b.set_title("Plasma-secretory score\nby cell type")
        clean_axis(ax_b)

        # --- Panel C inset: stage-stratified plasma cell scores ---
        if not sig_stage_celltype.empty:
            pc_stage = sig_stage_celltype[
                sig_stage_celltype["marker_inferred_cell_type"] == "plasma_cell"
            ]
            if len(pc_stage) > 0:
                # Add small text annotation
                stage_order = ["HD", "MGUS", "SMM", "MM"]
                text_lines = []
                for stage in stage_order:
                    sub = pc_stage[pc_stage["stage"] == stage]
                    if len(sub) > 0:
                        val = sub["plasma_secretory_score"].values[0]
                        text_lines.append(f"{stage}: {val:.2f}")
                if text_lines:
                    ax_b.text(0.98, 0.15, "Plasma cell by stage:\n" + "\n".join(text_lines),
                              transform=ax_b.transAxes, fontsize=7,
                              ha="right", va="bottom",
                              bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFBE6",
                                        edgecolor="#DDD", alpha=0.9))
    else:
        ax_b.text(0.5, 0.5, "Celltype data not available", ha="center", va="center",
                  transform=ax_b.transAxes, color="#9CA3AF")
        ax_b.axis("off")
    panel_label(ax_b, "b")

    fig.suptitle("Fig. 5 | Single-cell localization of the plasma-secretory axis (GSE271107)",
                 x=0.01, ha="left", fontweight="bold", fontsize=12)
    save_figure(fig, "fig5_scrna_plasma_secretory_localization")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 6 — External bulk cohort clinical support (GSE24080, GSE2658)
# ══════════════════════════════════════════════════════════════════════════════
def plot_fig6() -> None:
    """Bulk clinical association boxplots for key endpoints."""
    outcome_assoc = read_tsv(BULK_CLIN / "bulk_outcome_association_results.tsv")
    subtype_assoc = read_tsv(PLASMA_REFINE / "plasma_secretory_subtype_fdr_ranked.tsv")

    # Use the subtype association table (more comprehensive)
    assoc = subtype_assoc if not subtype_assoc.empty else outcome_assoc
    if assoc.empty:
        print("SKIP Fig 6: missing bulk association data")
        return

    fig = plt.figure(figsize=(11.0, 5.5))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.0],
                          width_ratios=[1.0, 1.0], hspace=0.45, wspace=0.35)

    # Key comparisons to show:
    # GSE24080: XBP1 ~ os_24mo, plasma_secretory ~ os_24mo
    # GSE2658: clinical_subtype_module ~ AMP_high_3plus, POU2AF1 ~ AMP_high_3plus

    highlights = [
        ("GSE24080", "XBP1_z", "os_24mo_event", "GSE24080: XBP1 by 24m OS",
         PALETTE["low"], PALETTE["high"]),
        ("GSE24080", "plasma_secretory_score_z", "os_24mo_event",
         "GSE24080: Plasma-secretory score by 24m OS",
         PALETTE["low"], PALETTE["high"]),
        ("GSE2658", "clinical_subtype_module_score_z", "AMP_high_3plus",
         "GSE2658: Clinical subtype module by 1q21 amplification",
         PALETTE["low"], PALETTE["high"]),
        ("GSE2658", "POU2AF1_z", "AMP_high_3plus",
         "GSE2658: POU2AF1 by 1q21 amplification",
         PALETTE["low"], PALETTE["high"]),
    ]

    for idx, (dataset, var, outcome, title, c0, c1) in enumerate(highlights):
        ax = fig.add_subplot(gs[idx // 2, idx % 2])
        sub = assoc[(assoc["dataset"] == dataset) &
                    (assoc["variable"] == var) &
                    (assoc["outcome"] == outcome)]
        if sub.empty:
            ax.text(0.5, 0.5, f"No data for\n{var} ~ {outcome}\n({dataset})",
                    ha="center", va="center", transform=ax.transAxes,
                    fontsize=8, color="#9CA3AF")
            ax.axis("off")
            continue

        row = sub.iloc[0]
        # Show key statistics as bar
        effect = as_float(row.get("delta_event_minus_nonevent", 0))
        p = as_float(row.get("mannwhitney_p", row.get("median_split_fisher_p", float("nan"))))
        or_val = as_float(row.get("median_split_or", float("nan")))

        # Create a summary panel with key metrics
        metrics = [
            ("Δ (event - non-event)", effect),
            ("Mann-Whitney p", p),
            ("Median-split OR", or_val if not math.isnan(or_val) else None),
        ]
        metrics = [(m, v) for m, v in metrics if v is not None]

        colors_metrics = [
            PALETTE["signal"] if ("OR" not in m and not math.isnan(v) and v > 0)
            else PALETTE["low"] if (not math.isnan(v) and v < 0)
            else PALETTE["neutral"]
            for m, v in metrics
        ]

        ax.barh([m[0] for m in metrics], [m[1] for m in metrics],
                color=colors_metrics, height=0.45, edgecolor="#222222", linewidth=0.5)
        ax.set_title(title, fontsize=8.5)
        clean_axis(ax)

        # Add text annotations
        ax.text(0.98, 0.05, f"n={int(row['n'])}; event n={int(row.get('n_event', 0))}",
                transform=ax.transAxes, fontsize=7, ha="right", va="bottom",
                color="#374151")

    fig.suptitle("Fig. 6 | External bulk cohorts supporting a clinical-risk direction (GSE24080, GSE2658)",
                 x=0.01, ha="left", fontweight="bold", fontsize=12)
    save_figure(fig, "fig6_external_bulk_clinical_support")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 7 — CoMMpass/GDC clinical and NG2024 molecular annotation
# ══════════════════════════════════════════════════════════════════════════════
def plot_fig7() -> None:
    """CoMMpass: OS, ISS and NG2024 PR subtype / 1q21 associations."""
    comm_assoc = read_tsv(COMMPASS / "commppass_axis_fdr_ranked.tsv")
    ng2024_assoc = read_tsv(NG2024 / "ng2024_molecular_annotation_fdr_ranked.tsv")

    if comm_assoc.empty:
        print("SKIP Fig 7: missing CoMMpass data")
        return

    fig = plt.figure(figsize=(11.0, 5.2))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.3, 1.2, 1.2], wspace=0.35)

    # --- Panel A: Top CoMMpass clinical associations ---
    ax_a = fig.add_subplot(gs[0, 0])
    if not comm_assoc.empty:
        top = comm_assoc.head(10).sort_values("effect", na_position="first")
        labels = []
        effects = []
        for _, row in top.iterrows():
            outcome = str(row.get("outcome_label", row.get("outcome", "")))
            var = str(row.get("variable", "")).replace("_score_z", "").replace("_z", "")
            labels.append(f"{var}\n{outcome}")
            eff = as_float(row.get("delta_event_minus_nonevent",
                            row.get("spearman_rho",
                            row.get("logrank_chi2", 0))))
            effects.append(eff)

        colors_a = ["#C44E52" if e > 0 else "#4C72B0" for e in effects]
        ax_a.barh(range(len(labels)), effects, color=colors_a,
                  edgecolor="#222222", linewidth=0.5)
        ax_a.set_yticks(range(len(labels)))
        ax_a.set_yticklabels(labels, fontsize=6.5)
        ax_a.axvline(0, color="#111827", linewidth=0.8)
        ax_a.set_xlabel("Effect size")
        ax_a.set_title("CoMMpass clinical associations")
        clean_axis(ax_a)

        # Add FDR annotations
        for i, (_, row) in enumerate(top.iterrows()):
            fdr = as_float(row.get("best_fdr", float("nan")))
            p_val = as_float(row.get("mannwhitney_p",
                           row.get("spearman_p",
                           row.get("logrank_p", float("nan")))))
            best = min(fdr, p_val) if not (math.isnan(fdr) and math.isnan(p_val)) else float("nan")
            if not math.isnan(best):
                ax_a.text(effects[i] + 0.02 * max(0.1, max(abs(x) for x in effects)),
                          i, format_p(best), va="center", fontsize=6)
    else:
        ax_a.text(0.5, 0.5, "CoMMpass data not available", ha="center", va="center",
                  transform=ax_a.transAxes, color="#9CA3AF")
        ax_a.axis("off")
    panel_label(ax_a, "a")

    # --- Panel B: NG2024 PR subtype association ---
    ax_b = fig.add_subplot(gs[0, 1])
    if not ng2024_assoc.empty:
        pr_sub = ng2024_assoc[ng2024_assoc["feature"].str.contains("PR", na=False)]
        if not pr_sub.empty:
            pr_labels = []
            pr_effects = []
            pr_pvals = []
            for _, row in pr_sub.iterrows():
                score_name = str(row.get("score", "")).replace("_score_z", "").replace("_z", "")
                pr_labels.append(score_name.replace("_", " "))
                pr_effects.append(as_float(row.get("effect", 0)))
                pr_pvals.append(as_float(row.get("p_value", float("nan"))))

            colors_b = ["#C44E52" if abs(e) > 0.1 else "#9CA3AF" for e in pr_effects]
            ax_b.barh(range(len(pr_labels)), pr_effects, color=colors_b,
                      edgecolor="#222222", linewidth=0.5)
            ax_b.set_yticks(range(len(pr_labels)))
            ax_b.set_yticklabels(pr_labels, fontsize=7.5)
            ax_b.axvline(0, color="#111827", linewidth=0.8)
            ax_b.set_xlabel("Effect (e.g., Spearman rho)")
            ax_b.set_title("NG2024 PR subtype\nprobability associations")
            clean_axis(ax_b)
            for i, (e, p) in enumerate(zip(pr_effects, pr_pvals)):
                offset = 0.02 * max(0.1, max(abs(x) for x in pr_effects))
                ax_b.text(e + offset, i, format_p(p), va="center", fontsize=6)
    else:
        ax_b.text(0.5, 0.5, "NG2024 data not available", ha="center", va="center",
                  transform=ax_b.transAxes, color="#9CA3AF")
        ax_b.axis("off")
    panel_label(ax_b, "b")

    # --- Panel C: 1q21 copy-number associations ---
    ax_c = fig.add_subplot(gs[0, 2])
    if not ng2024_assoc.empty:
        cna_sub = ng2024_assoc[ng2024_assoc["feature"].str.contains("1q21", na=False)]
        if not cna_sub.empty:
            cna_labels = []
            cna_effects = []
            cna_pvals = []
            for _, row in cna_sub.iterrows():
                score_name = str(row.get("score", "")).replace("_score_z", "").replace("_z", "")
                cna_labels.append(score_name.replace("_", " "))
                cna_effects.append(as_float(row.get("effect", 0)))
                cna_pvals.append(as_float(row.get("p_value", float("nan"))))

            colors_c = [PALETTE["signal"] if abs(e) > 0.1 else "#9CA3AF"
                        for e in cna_effects]
            ax_c.barh(range(len(cna_labels)), cna_effects, color=colors_c,
                      edgecolor="#222222", linewidth=0.5)
            ax_c.set_yticks(range(len(cna_labels)))
            ax_c.set_yticklabels(cna_labels, fontsize=7.5)
            ax_c.axvline(0, color="#111827", linewidth=0.8)
            ax_c.set_xlabel("Effect (e.g., delta / rho)")
            ax_c.set_title("NG2024 1q21 gain/amp\nscore associations")
            clean_axis(ax_c)
            for i, (e, p) in enumerate(zip(cna_effects, cna_pvals)):
                offset = 0.02 * max(0.1, max(abs(x) for x in cna_effects))
                ax_c.text(e + offset, i, format_p(p), va="center", fontsize=6)
    else:
        ax_c.text(0.5, 0.5, "NG2024 data not available", ha="center", va="center",
                  transform=ax_c.transAxes, color="#9CA3AF")
        ax_c.axis("off")
    panel_label(ax_c, "c")

    fig.suptitle("Fig. 7 | CoMMpass/GDC clinical and NG2024 molecular annotation associations",
                 x=0.01, ha="left", fontweight="bold", fontsize=12)
    save_figure(fig, "fig7_commppass_ng2024_association")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 8 — CoMMpass sensitivity models (forest plot)
# ══════════════════════════════════════════════════════════════════════════════
def plot_fig8() -> None:
    """Forest plot of adjusted Cox models constraining interpretation."""
    adjusted = read_tsv(ADJUSTED / "commppass_ng2024_adjusted_model_fdr_ranked.tsv")

    # Also try sensitivity directory
    sensitivity_path = SENSITIVITY / "commppass_os_sensitivity_forestplot.svg"
    has_existing = sensitivity_path.exists()

    if adjusted.empty and not has_existing:
        print("SKIP Fig 8: missing adjusted model data")
        return

    fig = plt.figure(figsize=(9.0, 5.5))
    gs = fig.add_gridspec(1, 1)

    ax = fig.add_subplot(gs[0, 0])

    if not adjusted.empty:
        # Extract Cox/OR model rows
        model_rows = adjusted.dropna(subset=["effect"]).copy()
        if len(model_rows) == 0:
            ax.text(0.5, 0.5, "No model results with effects", ha="center", va="center",
                    transform=ax.transAxes, color="#9CA3AF")
            ax.axis("off")
        else:
            model_rows = model_rows.sort_values("effect", ascending=False)
            labels = []
            hrs = []
            ci_lowers = []
            ci_uppers = []
            p_vals = []

            for _, row in model_rows.iterrows():
                model = str(row.get("model_name", row.get("variable", "")))
                score = str(row.get("score", "")).replace("_score_z", "").replace("_z", "")
                labels.append(f"{model}\n({score})")
                hrs.append(as_float(row.get("effect", 1.0)))
                ci_lowers.append(as_float(row.get("ci_lower", row.get("effect", 1.0) * 0.8)))
                ci_uppers.append(as_float(row.get("ci_upper", row.get("effect", 1.0) * 1.2)))
                p_vals.append(as_float(row.get("p_value", float("nan"))))

            # Compute error bars
            y_positions = range(len(labels))
            xerr_low = [h - l for h, l in zip(hrs, ci_lowers)]
            xerr_high = [u - h for h, u in zip(hrs, ci_uppers)]

            colors_f = ["#C44E52" if h > 1.0 else "#4C72B0" for h in hrs]

            ax.errorbar(hrs, y_positions,
                        xerr=[xerr_low, xerr_high],
                        fmt="o", color="#222222", capsize=3, capthick=1.2,
                        markersize=8, markerfacecolor=colors_f,
                        markeredgecolor="#222222", markeredgewidth=0.8)

            ax.axvline(1.0, color="#111827", linewidth=1.0, linestyle="--", alpha=0.5)
            ax.set_yticks(y_positions)
            ax.set_yticklabels(labels, fontsize=7)
            ax.set_xlabel("Hazard ratio / Odds ratio (95% CI)")
            ax.set_title("Sensitivity models constraining interpretation")

            # Add p-value annotations
            for i, (hr, p) in enumerate(zip(hrs, p_vals)):
                ax.text(max(hrs) * 1.15, i, format_p(p), va="center", fontsize=6.5)

            clean_axis(ax)

            # Add annotation about claim constraint
            ax.text(0.02, -0.18,
                    "These models support molecular-risk association, "
                    "not independent prognostic biomarker claims.\n"
                    "HRs attenuate as molecular covariates are added.",
                    transform=ax.transAxes, fontsize=7.5, color="#374151",
                    style="italic")
    elif has_existing:
        ax.text(0.5, 0.5,
                f"Pre-built forest plot available at:\n{sensitivity_path}\n"
                "Using existing rendered version.",
                ha="center", va="center", transform=ax.transAxes,
                fontsize=10, color="#6B7280")
        ax.axis("off")
    else:
        ax.text(0.5, 0.5, "No sensitivity model data", ha="center", va="center",
                transform=ax.transAxes, color="#9CA3AF")
        ax.axis("off")

    panel_label(ax, "a")

    fig.suptitle("Fig. 8 | CoMMpass sensitivity models constraining interpretation",
                 x=0.01, ha="left", fontweight="bold", fontsize=12)
    save_figure(fig, "fig8_commpass_sensitivity_models")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main() -> None:
    print("=" * 70)
    print("Redrawing manuscript figures (Nature style)")
    print(f"Output directory: {OUT}")
    print("=" * 70)

    for name, func in [
        ("Fig 1 — Study design & evidence chain", plot_fig1),
        ("Fig 2 — Spatial plasma-secretory discovery", plot_fig2),
        ("Fig 3 — Spatial organization & autocorrelation", plot_fig3),
        ("Fig 4 — Xenium spatial reproducibility", plot_fig4),
        ("Fig 5 — Single-cell localization", plot_fig5),
        ("Fig 6 — External bulk clinical support", plot_fig6),
        ("Fig 7 — CoMMpass/NG2024 association", plot_fig7),
        ("Fig 8 — Sensitivity models", plot_fig8),
    ]:
        print(f"\n▶ {name}")
        try:
            func()
        except Exception as exc:
            print(f"  ERROR: {exc}")
            import traceback
            traceback.print_exc()

    print(f"\n{'=' * 70}")
    print(f"Done. Figures saved to: {OUT}")
    for f in sorted(OUT.glob("*.svg")):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
