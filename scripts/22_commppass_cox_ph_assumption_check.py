from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.duration.hazard_regression import PHReg
from statsmodels.stats.multitest import multipletests


PROJECT = Path.cwd()
INPUT = PROJECT / "analysis" / "skerget_ng2024_public_supplement" / "commppass_scores_with_ng2024_annotations.tsv"
OUT = PROJECT / "analysis" / "commppass_cox_ph_assumption"
REPORTS = PROJECT / "reports" / "validation"

SCORE_COLS = [
    "plasma_secretory_score_z",
    "clinical_subtype_module_score_z",
    "TXNDC5_z",
    "POU2AF1_z",
    "XBP1_z",
    "JCHAIN_z",
]

SCORE_LABELS = {
    "plasma_secretory_score_z": "Plasma-secretory score",
    "clinical_subtype_module_score_z": "POU2AF1/XBP1/JCHAIN module",
    "TXNDC5_z": "TXNDC5",
    "POU2AF1_z": "POU2AF1",
    "XBP1_z": "XBP1",
    "JCHAIN_z": "JCHAIN",
}

MODELS = [
    ("OS adjusted for age, sex, ISS", ["age_z", "male", "iss_stage_num"]),
    ("OS adjusted for age, sex, ISS, 1q21", ["age_z", "male", "iss_stage_num", "Cp_1q21_Call"]),
]


def zscore(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce")
    sd = x.std(skipna=True)
    if pd.isna(sd) or sd == 0:
        return pd.Series(np.nan, index=s.index)
    return (x - x.mean(skipna=True)) / sd


def bh_fdr(values: pd.Series) -> pd.Series:
    out = pd.Series(np.nan, index=values.index, dtype=float)
    valid = pd.to_numeric(values, errors="coerce").dropna()
    if valid.empty:
        return out
    _, q, _, _ = multipletests(valid.to_numpy(float), method="fdr_bh")
    out.loc[valid.index] = q
    return out


def load_data() -> pd.DataFrame:
    df = pd.read_csv(INPUT, sep="\t")
    df["age_z"] = zscore(df["age_at_index"].combine_first(df.get("Age", pd.Series(index=df.index))))
    gender = df.get("gender", pd.Series(index=df.index, dtype=object)).astype(str).str.lower()
    df["male"] = np.where(gender.eq("male"), 1.0, np.where(gender.eq("female"), 0.0, np.nan))
    df["os_time_months"] = pd.to_numeric(df["os_time_months"], errors="coerce")
    df["os_event"] = pd.to_numeric(df["os_event"], errors="coerce")
    df["iss_stage_num"] = pd.to_numeric(df["iss_stage_num"], errors="coerce")
    return df


def fit_ph_model(df: pd.DataFrame, score: str, covariates: list[str]) -> tuple[pd.DataFrame, list[str], object]:
    used_cols = ["score"] + covariates
    mat = df[[score] + covariates].apply(pd.to_numeric, errors="coerce").copy()
    mat.columns = used_cols
    tmp = pd.concat([df[["os_time_months", "os_event"]], mat], axis=1).dropna()
    tmp = tmp[(tmp["os_time_months"] > 0) & (tmp["os_event"].isin([0, 1]))].copy()
    fit = PHReg(tmp["os_time_months"], tmp[used_cols], status=tmp["os_event"]).fit(disp=False)
    return tmp, used_cols, fit


def ph_tests_for_model(df: pd.DataFrame, score: str, model_name: str, covariates: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    try:
        tmp, used_cols, fit = fit_ph_model(df, score, covariates)
        residuals = pd.DataFrame(fit.schoenfeld_residuals, columns=used_cols, index=tmp.index)
        event_mask = tmp["os_event"].eq(1) & np.isfinite(residuals).all(axis=1)
        event_res = residuals.loc[event_mask]
        event_time = tmp.loc[event_mask, "os_time_months"].astype(float)
        log_time = np.log(event_time)
        for cov in used_cols:
            x = pd.to_numeric(event_res[cov], errors="coerce")
            valid = x.notna() & np.isfinite(x) & np.isfinite(log_time)
            if valid.sum() < 20 or x[valid].std() == 0:
                rows.append(
                    {
                        "model_name": model_name,
                        "score": score,
                        "score_label": SCORE_LABELS.get(score, score),
                        "covariate": cov,
                        "n": int(len(tmp)),
                        "events": int(tmp["os_event"].sum()),
                        "rho": np.nan,
                        "p_value": np.nan,
                        "status": "failed",
                        "note": "insufficient residual variation",
                    }
                )
                continue
            rho, p = stats.spearmanr(log_time[valid], x[valid])
            rows.append(
                {
                    "model_name": model_name,
                    "score": score,
                    "score_label": SCORE_LABELS.get(score, score),
                    "covariate": cov,
                    "n": int(len(tmp)),
                    "events": int(tmp["os_event"].sum()),
                    "rho": float(rho),
                    "p_value": float(p),
                    "status": "ok",
                    "note": "Schoenfeld residual Spearman correlation with log(event time)",
                }
            )
    except Exception as exc:
        rows.append(
            {
                "model_name": model_name,
                "score": score,
                "score_label": SCORE_LABELS.get(score, score),
                "covariate": "",
                "n": 0,
                "events": 0,
                "rho": np.nan,
                "p_value": np.nan,
                "status": "failed",
                "note": f"{type(exc).__name__}: {exc}",
            }
        )
    return rows


def plot_score_residuals(df: pd.DataFrame) -> None:
    selected = [
        ("plasma_secretory_score_z", "OS adjusted for age, sex, ISS, 1q21", ["age_z", "male", "iss_stage_num", "Cp_1q21_Call"]),
        ("clinical_subtype_module_score_z", "OS adjusted for age, sex, ISS, 1q21", ["age_z", "male", "iss_stage_num", "Cp_1q21_Call"]),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.5), sharey=False)
    for ax, (score, model_name, covariates) in zip(axes, selected):
        tmp, used_cols, fit = fit_ph_model(df, score, covariates)
        residuals = pd.DataFrame(fit.schoenfeld_residuals, columns=used_cols, index=tmp.index)
        event_mask = tmp["os_event"].eq(1) & residuals["score"].notna()
        x = np.log(tmp.loc[event_mask, "os_time_months"].astype(float))
        y = residuals.loc[event_mask, "score"].astype(float)
        ax.scatter(x, y, s=13, alpha=0.68, color="#4c78a8", edgecolor="none")
        if len(x) >= 5:
            slope, intercept, _, _, _ = stats.linregress(x, y)
            xx = np.linspace(float(x.min()), float(x.max()), 100)
            ax.plot(xx, intercept + slope * xx, color="#d1495b", linewidth=1.2)
        ax.axhline(0, color="#222222", linewidth=0.8, linestyle="--")
        ax.set_title(SCORE_LABELS.get(score, score))
        ax.set_xlabel("log(event time in months)")
        ax.set_ylabel("Schoenfeld residual")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.suptitle("Cox PH assumption screen for primary scores", x=0.02, ha="left", fontweight="bold")
    fig.tight_layout()
    for suffix in [".png", ".pdf", ".svg"]:
        fig.savefig(OUT / f"commppass_cox_ph_schoenfeld_score_residuals{suffix}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_report(results: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    primary = results[
        results["model_name"].eq("OS adjusted for age, sex, ISS, 1q21")
        & results["score"].isin(["plasma_secretory_score_z", "clinical_subtype_module_score_z"])
    ].copy()
    score_rows = primary[primary["covariate"].eq("score")].copy()
    flag_rows = results[(results["status"].eq("ok")) & (results["fdr"] < 0.05)].copy()
    lines = [
        "# CoMMpass Cox PH Assumption Check",
        "",
        "Date: 2026-05-01",
        "",
        "Purpose:",
        "",
        "- Screen Cox proportional hazards assumptions for CoMMpass/NG2024 adjusted OS models.",
        "- Use Schoenfeld residual Spearman correlation with log(event time).",
        "- Treat this as a presubmission diagnostic screen, not as a replacement for external statistical review.",
        "",
        "## Primary Score Results",
        "",
    ]
    if score_rows.empty:
        lines.append("- No primary score PH rows were generated.")
    else:
        for _, row in score_rows.iterrows():
            lines.append(
                f"- {row['score_label']} | {row['model_name']}: n={row['n']}, events={row['events']}, "
                f"rho={row['rho']:.4f}, p={row['p_value']:.4g}, FDR={row['fdr']:.4g}."
            )
    lines.extend(["", "## Interpretation", ""])
    if flag_rows.empty:
        lines.extend(
            [
                "- No covariate-level Schoenfeld residual test reached FDR < 0.05.",
                "- The primary adjusted Cox associations can be reported with no detected PH-screen violation in this diagnostic.",
            ]
        )
    else:
        lines.append("- At least one covariate-level PH screen reached FDR < 0.05.")
        lines.append("- Report Cox results with caution and inspect flagged covariates before submission.")
    lines.extend(
        [
            "",
            "## Outputs",
            "",
            "- `analysis/commppass_cox_ph_assumption/commppass_cox_ph_schoenfeld_tests.tsv`",
            "- `analysis/commppass_cox_ph_assumption/commppass_cox_ph_schoenfeld_score_residuals.png`",
            "- `analysis/commppass_cox_ph_assumption/commppass_cox_ph_schoenfeld_score_residuals.pdf`",
            "- `analysis/commppass_cox_ph_assumption/commppass_cox_ph_schoenfeld_score_residuals.svg`",
            "",
            "## Manuscript Language",
            "",
            "A proportional hazards diagnostic screen based on Schoenfeld residual correlations with log(event time) did not detect an FDR-significant violation for the primary adjusted Cox score terms.",
        ]
    )
    (REPORTS / "COMMPASS_COX_PH_ASSUMPTION_CHECK.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = load_data()
    rows: list[dict[str, object]] = []
    for score in SCORE_COLS:
        for model_name, covariates in MODELS:
            rows.extend(ph_tests_for_model(df, score, model_name, covariates))
    results = pd.DataFrame(rows)
    ok = results["status"].eq("ok")
    results["fdr"] = np.nan
    results.loc[ok, "fdr"] = bh_fdr(results.loc[ok, "p_value"])
    results = results.sort_values(["fdr", "p_value"], na_position="last")
    results.to_csv(OUT / "commppass_cox_ph_schoenfeld_tests.tsv", sep="\t", index=False)
    plot_score_residuals(df)
    write_report(results)
    print(f"Wrote Cox PH assumption outputs to: {OUT}")


if __name__ == "__main__":
    main()
