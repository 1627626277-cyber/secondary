from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests


PROJECT = Path.cwd()
DATA = PROJECT / "external_bulk" / "Skerget_NG2024_CoMMpass_public_supplement"
OUT = PROJECT / "analysis" / "skerget_ng2024_public_supplement"
REPORTS = PROJECT / "reports" / "validation"
SCORES = PROJECT / "analysis" / "commppass_gdc_validation" / "commppass_axis_clinical_scores.tsv"

TABLE1 = DATA / "41588_2024_1853_MOESM4_ESM.xlsx"
TABLE7 = DATA / "41588_2024_1853_MOESM10_ESM.xlsx"

SCORE_COLS = [
    "plasma_secretory_score_z",
    "clinical_subtype_module_score_z",
    "TXNDC5_z",
    "POU2AF1_z",
    "XBP1_z",
    "JCHAIN_z",
]

BINARY_FEATURES = [
    "Cytogenetic_High_Risk",
    "Cp_1q21_Call",
    "Cp_17p13_Call",
    "Cp_13q14_Call",
    "Hyperdiploid_Call",
    "CCND1_Tx_Call",
    "WHSC1_Tx_Call",
    "MAF_Tx_Call",
    "MYC_CN_FLAG",
    "MYC_STR_FLAG",
]

ORDINAL_FEATURES = [
    "ISS_Stage",
    "IMWG_Risk_Class",
    "TP53_Funct_Copies",
    "TP53_NS_Mut_Count",
    "Serum_Albumin",
    "Serum_B2M",
    "Serum_LDH",
]

CATEGORICAL_FEATURES = [
    "RNA_Subtype_Name",
    "CNA_Subtype_Name",
]

SUBTYPE_PROB_COLS = [
    "MAF",
    "CD1",
    "CD2a",
    "CD2b",
    "MS",
    "1q gain",
    "PR",
    "HRD, MYC, low NFkB",
    "Low purity",
    "HRD, low TP53",
    "HRD, ++15",
    "HRD, ++15, MYC",
]


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fdr_adjust(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    pvals = [float(row["p_value"]) for row in rows if np.isfinite(float(row["p_value"]))]
    if not pvals:
        return rows
    _, qvals, _, _ = multipletests(pvals, method="fdr_bh")
    q_iter = iter(qvals)
    for row in rows:
        if np.isfinite(float(row["p_value"])):
            row["fdr"] = next(q_iter)
        else:
            row["fdr"] = math.nan
    return rows


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    scores = pd.read_csv(SCORES, sep="\t")
    features = pd.read_excel(TABLE1, sheet_name="1A_Patient_features")
    subtype = pd.read_excel(TABLE7, sheet_name="7A_RNA_subtype_predictions")
    subtype = subtype[subtype["Reason_For_Collection"].astype(str).str.lower().eq("baseline")].copy()
    subtype = subtype.sort_values(["Patient_ID", "Visit_ID"]).drop_duplicates("Patient_ID", keep="first")
    return scores, features, subtype


def merge_annotations(scores: pd.DataFrame, features: pd.DataFrame, subtype: pd.DataFrame) -> pd.DataFrame:
    merged = scores.merge(
        features,
        left_on="case_submitter_id",
        right_on="Patient_ID",
        how="left",
        suffixes=("", "_ng2024_features"),
    )
    subtype_keep = ["Patient_ID", "RNA_Subtype_ID", "RNA_Subtype_Name"] + SUBTYPE_PROB_COLS
    subtype_renamed = subtype[subtype_keep].rename(
        columns={
            "Patient_ID": "Patient_ID_ng2024_subtype",
            "RNA_Subtype_ID": "RNA_Subtype_ID_ng2024",
            "RNA_Subtype_Name": "RNA_Subtype_Name_ng2024",
        }
    )
    merged = merged.merge(
        subtype_renamed,
        left_on="case_submitter_id",
        right_on="Patient_ID_ng2024_subtype",
        how="left",
    )
    OUT.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUT / "commppass_scores_with_ng2024_annotations.tsv", sep="\t", index=False)
    return merged


def binary_tests(df: pd.DataFrame) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for feature in BINARY_FEATURES:
        if feature not in df.columns:
            continue
        x = pd.to_numeric(df[feature], errors="coerce")
        for score in SCORE_COLS:
            y = pd.to_numeric(df[score], errors="coerce")
            tmp = pd.DataFrame({"x": x, "y": y}).dropna()
            groups = sorted(tmp["x"].unique().tolist())
            if set(groups) < {0, 1}:
                continue
            g0 = tmp.loc[tmp["x"] == 0, "y"]
            g1 = tmp.loc[tmp["x"] == 1, "y"]
            if len(g0) < 10 or len(g1) < 10:
                continue
            stat, p = stats.mannwhitneyu(g1, g0, alternative="two-sided")
            rows.append(
                {
                    "analysis_type": "binary_mannwhitney",
                    "feature": feature,
                    "score": score,
                    "n": len(tmp),
                    "n_feature_0": len(g0),
                    "n_feature_1": len(g1),
                    "effect": float(np.median(g1) - np.median(g0)),
                    "effect_label": "median_feature1_minus_feature0",
                    "statistic": float(stat),
                    "p_value": float(p),
                }
            )
    return rows


def ordinal_tests(df: pd.DataFrame) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for feature in ORDINAL_FEATURES:
        if feature not in df.columns:
            continue
        x = pd.to_numeric(df[feature], errors="coerce")
        for score in SCORE_COLS:
            y = pd.to_numeric(df[score], errors="coerce")
            tmp = pd.DataFrame({"x": x, "y": y}).dropna()
            if len(tmp) < 30 or tmp["x"].nunique() < 2:
                continue
            rho, p = stats.spearmanr(tmp["x"], tmp["y"])
            rows.append(
                {
                    "analysis_type": "ordinal_spearman",
                    "feature": feature,
                    "score": score,
                    "n": len(tmp),
                    "n_feature_0": "",
                    "n_feature_1": "",
                    "effect": float(rho),
                    "effect_label": "spearman_rho",
                    "statistic": float(rho),
                    "p_value": float(p),
                }
            )
    return rows


def categorical_tests(df: pd.DataFrame) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for feature in CATEGORICAL_FEATURES + ["RNA_Subtype_Name_ng2024"]:
        if feature not in df.columns:
            continue
        x = df[feature].astype("string")
        for score in SCORE_COLS:
            y = pd.to_numeric(df[score], errors="coerce")
            tmp = pd.DataFrame({"x": x, "y": y}).dropna()
            groups = [grp["y"].values for _, grp in tmp.groupby("x") if len(grp) >= 10]
            if len(groups) < 3:
                continue
            stat, p = stats.kruskal(*groups)
            medians = tmp.groupby("x")["y"].median().sort_values(ascending=False)
            rows.append(
                {
                    "analysis_type": "categorical_kruskal",
                    "feature": feature,
                    "score": score,
                    "n": len(tmp),
                    "n_feature_0": "",
                    "n_feature_1": "",
                    "effect": float(stat),
                    "effect_label": f"kruskal_H; top_median={medians.index[0]}",
                    "statistic": float(stat),
                    "p_value": float(p),
                }
            )
    return rows


def subtype_probability_tests(df: pd.DataFrame) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for feature in SUBTYPE_PROB_COLS:
        if feature not in df.columns:
            continue
        x = pd.to_numeric(df[feature], errors="coerce")
        for score in SCORE_COLS:
            y = pd.to_numeric(df[score], errors="coerce")
            tmp = pd.DataFrame({"x": x, "y": y}).dropna()
            if len(tmp) < 30:
                continue
            rho, p = stats.spearmanr(tmp["x"], tmp["y"])
            rows.append(
                {
                    "analysis_type": "subtype_probability_spearman",
                    "feature": feature,
                    "score": score,
                    "n": len(tmp),
                    "n_feature_0": "",
                    "n_feature_1": "",
                    "effect": float(rho),
                    "effect_label": "spearman_rho",
                    "statistic": float(rho),
                    "p_value": float(p),
                }
            )
    return rows


def plot_top_associations(rows: list[dict[str, object]], df: pd.DataFrame) -> None:
    ranked = pd.DataFrame(rows).sort_values("fdr").head(16)
    if ranked.empty:
        return
    ranked["neg_log10_fdr"] = -np.log10(ranked["fdr"].astype(float).clip(lower=1e-30))
    ranked["label"] = ranked["feature"].astype(str) + " | " + ranked["score"].astype(str)
    ranked = ranked.sort_values("neg_log10_fdr")
    type_colors = {
        "categorical_kruskal": "#4C78A8",
        "subtype_probability_spearman": "#59A14F",
        "binary_mannwhitney": "#C44E52",
        "ordinal_spearman": "#B07AA1",
    }
    colors = ranked["analysis_type"].map(type_colors).fillna("#6B7280")
    fig, ax = plt.subplots(figsize=(8.6, 6.3))
    y = np.arange(len(ranked))
    ax.barh(y, ranked["neg_log10_fdr"], color=colors, height=0.72)
    ax.axvline(-np.log10(0.05), color="#222222", linewidth=0.9, linestyle="--")
    ax.set_yticks(y)
    ax.set_yticklabels(ranked["label"], fontsize=7)
    ax.set_xlabel("-log10(FDR)")
    ax.set_title("Public CoMMpass NG2024 molecular-annotation associations")
    for i, row in enumerate(ranked.itertuples(index=False)):
        ax.text(
            row.neg_log10_fdr + 0.25,
            i,
            f"{row.analysis_type.replace('_', ' ')}; effect={float(row.effect):.2g}",
            va="center",
            fontsize=6.5,
        )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "ng2024_top_molecular_annotation_associations.png", dpi=300)
    fig.savefig(OUT / "ng2024_top_molecular_annotation_associations.pdf")
    plt.close(fig)


def plot_key_boxes(df: pd.DataFrame) -> None:
    panels = [
        ("Cp_1q21_Call", "plasma_secretory_score_z", "1q21 gain"),
        ("Cp_1q21_Call", "TXNDC5_z", "1q21 gain"),
        ("Cp_17p13_Call", "POU2AF1_z", "17p13 deletion"),
        ("Cytogenetic_High_Risk", "JCHAIN_z", "Cytogenetic high-risk"),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.2), sharey=False)
    for ax, (feature, score, title) in zip(axes, panels, strict=True):
        tmp = df[[feature, score]].copy()
        tmp[feature] = pd.to_numeric(tmp[feature], errors="coerce")
        tmp[score] = pd.to_numeric(tmp[score], errors="coerce")
        tmp = tmp.dropna()
        data = [tmp.loc[tmp[feature] == 0, score], tmp.loc[tmp[feature] == 1, score]]
        bp = ax.boxplot(data, tick_labels=["0", "1"], widths=0.55, showfliers=False, patch_artist=True)
        for patch, color in zip(bp["boxes"], ["#DAD7CD", "#A44A3F"], strict=False):
            patch.set_facecolor(color)
            patch.set_edgecolor("#222222")
            patch.set_linewidth(0.8)
        for element in ["whiskers", "caps", "medians"]:
            for obj in bp[element]:
                obj.set(color="#222222", linewidth=0.8)
        for i, arr in enumerate(data, start=1):
            values = pd.to_numeric(arr, errors="coerce").dropna().to_numpy()
            if len(values) == 0:
                continue
            rng = np.random.default_rng(700 + i)
            ax.scatter(
                np.full(len(values), i) + rng.normal(0, 0.045, len(values)),
                values,
                s=8,
                color="#222222",
                alpha=0.45,
                linewidths=0,
                zorder=3,
            )
            ax.text(i, np.nanmax(values), f"n={len(values)}", ha="center", va="bottom", fontsize=7)
        ax.set_title(title, fontsize=9)
        ax.set_xlabel(feature)
        ax.set_ylabel(score if ax is axes[0] else "")
        ax.tick_params(axis="both", labelsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "ng2024_key_molecular_annotation_boxplots.png", dpi=300)
    fig.savefig(OUT / "ng2024_key_molecular_annotation_boxplots.pdf")
    plt.close(fig)


def write_report(merged: pd.DataFrame, rows: list[dict[str, object]]) -> None:
    ranked = pd.DataFrame(rows).sort_values("fdr")
    top = ranked.head(12)
    clinical_features = {
        "Cytogenetic_High_Risk",
        "Cp_1q21_Call",
        "Cp_17p13_Call",
        "Cp_13q14_Call",
        "Hyperdiploid_Call",
        "IMWG_Risk_Class",
        "ISS_Stage",
    }
    clinical_top = ranked[ranked["feature"].isin(clinical_features)].head(12)
    lines = [
        "# Skerget NG2024 Molecular Annotation Validation",
        "",
        "Date: 2026-04-30",
        "",
        "## Data Join",
        "",
        f"- Current CoMMpass/GDC score table samples: {len(merged)}.",
        f"- Samples with NG2024 patient-feature annotations: {int(merged['Patient_ID'].notna().sum())}.",
        f"- Samples with NG2024 RNA subtype predictions: {int(merged['Patient_ID_ng2024_subtype'].notna().sum())}.",
        "",
        "## Analysis Scope",
        "",
        "- Tested plasma-secretory, clinical subtype module and marker z-scores against public CoMMpass molecular-risk annotations.",
        "- Tested binary calls, ordinal/lab variables, categorical molecular subtypes and RNA subtype probability scores.",
        "- PFS, treatment response and therapy-line claims remain out of scope.",
        "",
        "## Top Associations",
        "",
    ]
    if top.empty:
        lines.append("- No associations were generated.")
    else:
        for row in top.itertuples(index=False):
            lines.append(
                f"- {row.analysis_type}: `{row.feature}` vs `{row.score}`, "
                f"n={row.n}, effect={float(row.effect):.4g}, p={float(row.p_value):.3g}, FDR={float(row.fdr):.3g}."
            )
    lines.extend(["", "## Clinically Relevant Annotation Results", ""])
    if clinical_top.empty:
        lines.append("- No cytogenetic / ISS / IMWG risk associations passed the first-pass filter.")
    else:
        for row in clinical_top.itertuples(index=False):
            lines.append(
                f"- {row.analysis_type}: `{row.feature}` vs `{row.score}`, "
                f"n={row.n}, effect={float(row.effect):.4g}, p={float(row.p_value):.3g}, FDR={float(row.fdr):.3g}."
            )
    lines.extend(
        [
            "",
            "## Outputs",
            "",
            "- Merged annotation table: `analysis/skerget_ng2024_public_supplement/commppass_scores_with_ng2024_annotations.tsv`.",
            "- Association table: `analysis/skerget_ng2024_public_supplement/ng2024_molecular_annotation_associations.tsv`.",
            "- Ranked association table: `analysis/skerget_ng2024_public_supplement/ng2024_molecular_annotation_fdr_ranked.tsv`.",
            "- Top-association plot: `analysis/skerget_ng2024_public_supplement/ng2024_top_molecular_annotation_associations.png`.",
            "- Key boxplots: `analysis/skerget_ng2024_public_supplement/ng2024_key_molecular_annotation_boxplots.png`.",
            "",
            "## Interpretation",
            "",
            "- This public supplement can now be used as a molecular-risk annotation layer for the Q2 mainline.",
            "- The result should be framed as molecular annotation / subtype support, not as PFS or treatment-response validation.",
        ]
    )
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "SKERGET_NG2024_MOLECULAR_ANNOTATION_VALIDATION_REPORT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    scores, features, subtype = load_data()
    merged = merge_annotations(scores, features, subtype)
    rows = []
    rows.extend(binary_tests(merged))
    rows.extend(ordinal_tests(merged))
    rows.extend(categorical_tests(merged))
    rows.extend(subtype_probability_tests(merged))
    rows = fdr_adjust(rows)
    write_tsv(OUT / "ng2024_molecular_annotation_associations.tsv", rows)
    ranked = sorted(rows, key=lambda row: float(row.get("fdr", math.inf)))
    write_tsv(OUT / "ng2024_molecular_annotation_fdr_ranked.tsv", ranked)
    plot_top_associations(ranked, merged)
    plot_key_boxes(merged)
    write_report(merged, ranked)
    print(f"Merged samples: {len(merged)}")
    print(f"Feature annotation match: {int(merged['Patient_ID'].notna().sum())}")
    print(f"RNA subtype match: {int(merged['Patient_ID_ng2024_subtype'].notna().sum())}")
    print(f"Associations tested: {len(ranked)}")
    print(f"Report: {REPORTS / 'SKERGET_NG2024_MOLECULAR_ANNOTATION_VALIDATION_REPORT.md'}")


if __name__ == "__main__":
    main()
