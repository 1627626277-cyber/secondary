from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.duration.hazard_regression import PHReg
from statsmodels.stats.multitest import multipletests


PROJECT = Path.cwd()
INPUT = PROJECT / "analysis" / "skerget_ng2024_public_supplement" / "commppass_scores_with_ng2024_annotations.tsv"
OUT = PROJECT / "analysis" / "commppass_ng2024_adjusted_models"
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


def bh_fdr(p_values: pd.Series) -> pd.Series:
    out = pd.Series(np.nan, index=p_values.index, dtype=float)
    valid = pd.to_numeric(p_values, errors="coerce").dropna()
    if valid.empty:
        return out
    _, q, _, _ = multipletests(valid.to_numpy(float), method="fdr_bh")
    out.loc[valid.index] = q
    return out


def zscore(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce")
    sd = x.std(skipna=True)
    if pd.isna(sd) or sd == 0:
        return pd.Series(np.nan, index=s.index)
    return (x - x.mean(skipna=True)) / sd


def load_data() -> pd.DataFrame:
    if not INPUT.exists():
        raise FileNotFoundError(f"Missing input: {INPUT}")
    df = pd.read_csv(INPUT, sep="\t")
    df["age_z"] = zscore(df["age_at_index"].combine_first(df.get("Age", pd.Series(index=df.index))))
    gender = df.get("gender", pd.Series(index=df.index, dtype=object)).astype(str).str.lower()
    df["male"] = np.where(gender.eq("male"), 1.0, np.where(gender.eq("female"), 0.0, np.nan))
    df["imwg_risk_nonstandard"] = np.where(
        pd.to_numeric(df.get("IMWG_Risk_Class"), errors="coerce") > 0,
        1.0,
        np.where(pd.to_numeric(df.get("IMWG_Risk_Class"), errors="coerce").eq(0), 0.0, np.nan),
    )
    df["os_time_months"] = pd.to_numeric(df["os_time_months"], errors="coerce")
    df["os_event"] = pd.to_numeric(df["os_event"], errors="coerce")
    df["iss_stage_num"] = pd.to_numeric(df["iss_stage_num"], errors="coerce")
    df["iss_stage_III"] = pd.to_numeric(df["iss_stage_III"], errors="coerce")
    return df


def design_matrix(df: pd.DataFrame, score: str, covariates: list[str], add_const: bool) -> tuple[pd.DataFrame, list[str]]:
    cols = [score] + covariates
    mat = df[cols].apply(pd.to_numeric, errors="coerce").copy()
    mat.columns = ["score"] + covariates
    used_cols = mat.columns.tolist()
    if add_const:
        mat = sm.add_constant(mat, has_constant="add")
        used_cols = mat.columns.tolist()
    return mat, used_cols


def cox_model(df: pd.DataFrame, score: str, model_name: str, covariates: list[str]) -> dict[str, object]:
    mat, used_cols = design_matrix(df, score, covariates, add_const=False)
    tmp = pd.concat(
        [
            df[["os_time_months", "os_event"]].apply(pd.to_numeric, errors="coerce"),
            mat,
        ],
        axis=1,
    ).dropna()
    tmp = tmp[(tmp["os_time_months"] > 0) & (tmp["os_event"].isin([0, 1]))]
    if len(tmp) < 80 or tmp["os_event"].sum() < 20:
        return failed_row("cox_ph", model_name, score, len(tmp), "insufficient complete OS data")
    try:
        fit = PHReg(tmp["os_time_months"], tmp[used_cols], status=tmp["os_event"]).fit(disp=False)
        idx = used_cols.index("score")
        coef = float(fit.params[idx])
        se = float(fit.bse[idx])
        p = float(fit.pvalues[idx])
        hr = math.exp(coef)
        ci_low = math.exp(coef - 1.96 * se)
        ci_high = math.exp(coef + 1.96 * se)
        return {
            "model_type": "cox_ph",
            "model_name": model_name,
            "endpoint": "overall_survival",
            "score": score,
            "score_label": SCORE_LABELS.get(score, score),
            "n": int(len(tmp)),
            "events_or_cases": int(tmp["os_event"].sum()),
            "effect_type": "hazard_ratio_per_1sd_score",
            "effect": hr,
            "ci_lower": ci_low,
            "ci_upper": ci_high,
            "coef": coef,
            "se": se,
            "p_value": p,
            "covariates": ",".join(covariates),
            "status": "ok",
            "note": "",
        }
    except Exception as exc:
        return failed_row("cox_ph", model_name, score, len(tmp), f"{type(exc).__name__}: {exc}")


def logit_model(
    df: pd.DataFrame,
    score: str,
    endpoint: str,
    model_name: str,
    covariates: list[str],
) -> dict[str, object]:
    y = pd.to_numeric(df[endpoint], errors="coerce")
    mat, used_cols = design_matrix(df, score, covariates, add_const=True)
    tmp = pd.concat([y.rename("endpoint"), mat], axis=1).dropna()
    tmp = tmp[tmp["endpoint"].isin([0, 1])]
    cases = int(tmp["endpoint"].sum()) if not tmp.empty else 0
    controls = int(len(tmp) - cases)
    if len(tmp) < 80 or cases < 20 or controls < 20:
        return failed_row("logit", model_name, score, len(tmp), f"insufficient cases/controls: {cases}/{controls}", endpoint)
    try:
        fit = sm.Logit(tmp["endpoint"], tmp[used_cols]).fit(disp=False, maxiter=200)
        coef = float(fit.params["score"])
        se = float(fit.bse["score"])
        p = float(fit.pvalues["score"])
        odds = math.exp(coef)
        ci_low = math.exp(coef - 1.96 * se)
        ci_high = math.exp(coef + 1.96 * se)
        return {
            "model_type": "logit",
            "model_name": model_name,
            "endpoint": endpoint,
            "score": score,
            "score_label": SCORE_LABELS.get(score, score),
            "n": int(len(tmp)),
            "events_or_cases": cases,
            "effect_type": "odds_ratio_per_1sd_score",
            "effect": odds,
            "ci_lower": ci_low,
            "ci_upper": ci_high,
            "coef": coef,
            "se": se,
            "p_value": p,
            "covariates": ",".join(covariates),
            "status": "ok",
            "note": "",
        }
    except Exception as exc:
        return failed_row("logit", model_name, score, len(tmp), f"{type(exc).__name__}: {exc}", endpoint)


def ols_model(
    df: pd.DataFrame,
    score: str,
    endpoint: str,
    model_name: str,
    covariates: list[str],
) -> dict[str, object]:
    y = pd.to_numeric(df[endpoint], errors="coerce")
    mat, used_cols = design_matrix(df, score, covariates, add_const=True)
    tmp = pd.concat([y.rename("endpoint"), mat], axis=1).dropna()
    if len(tmp) < 80:
        return failed_row("ols", model_name, score, len(tmp), "insufficient complete data", endpoint)
    try:
        fit = sm.OLS(tmp["endpoint"], tmp[used_cols]).fit()
        coef = float(fit.params["score"])
        se = float(fit.bse["score"])
        p = float(fit.pvalues["score"])
        return {
            "model_type": "ols",
            "model_name": model_name,
            "endpoint": endpoint,
            "score": score,
            "score_label": SCORE_LABELS.get(score, score),
            "n": int(len(tmp)),
            "events_or_cases": "",
            "effect_type": "beta_per_1sd_score",
            "effect": coef,
            "ci_lower": coef - 1.96 * se,
            "ci_upper": coef + 1.96 * se,
            "coef": coef,
            "se": se,
            "p_value": p,
            "covariates": ",".join(covariates),
            "status": "ok",
            "note": "",
        }
    except Exception as exc:
        return failed_row("ols", model_name, score, len(tmp), f"{type(exc).__name__}: {exc}", endpoint)


def failed_row(
    model_type: str,
    model_name: str,
    score: str,
    n: int,
    note: str,
    endpoint: str = "",
) -> dict[str, object]:
    return {
        "model_type": model_type,
        "model_name": model_name,
        "endpoint": endpoint,
        "score": score,
        "score_label": SCORE_LABELS.get(score, score),
        "n": int(n),
        "events_or_cases": "",
        "effect_type": "",
        "effect": np.nan,
        "ci_lower": np.nan,
        "ci_upper": np.nan,
        "coef": np.nan,
        "se": np.nan,
        "p_value": np.nan,
        "covariates": "",
        "status": "failed",
        "note": note,
    }


def run_models(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for score in SCORE_COLS:
        rows.append(cox_model(df, score, "OS adjusted for age, sex, ISS", ["age_z", "male", "iss_stage_num"]))
        rows.append(
            cox_model(
                df,
                score,
                "OS adjusted for age, sex, ISS, cytogenetic high risk",
                ["age_z", "male", "iss_stage_num", "Cytogenetic_High_Risk"],
            )
        )
        rows.append(
            cox_model(
                df,
                score,
                "OS adjusted for age, sex, ISS, 1q21",
                ["age_z", "male", "iss_stage_num", "Cp_1q21_Call"],
            )
        )
        rows.append(logit_model(df, score, "iss_stage_III", "ISS III adjusted for age and sex", ["age_z", "male"]))
        rows.append(
            logit_model(
                df,
                score,
                "imwg_risk_nonstandard",
                "IMWG non-standard risk adjusted for age, sex, ISS",
                ["age_z", "male", "iss_stage_num"],
            )
        )
        rows.append(
            logit_model(
                df,
                score,
                "Cytogenetic_High_Risk",
                "Cytogenetic high risk adjusted for age, sex, ISS",
                ["age_z", "male", "iss_stage_num"],
            )
        )
        rows.append(
            logit_model(
                df,
                score,
                "Cp_1q21_Call",
                "1q21 gain/amplification adjusted for age, sex, ISS",
                ["age_z", "male", "iss_stage_num"],
            )
        )
        rows.append(
            logit_model(
                df,
                score,
                "Cp_17p13_Call",
                "17p13 deletion adjusted for age, sex, ISS",
                ["age_z", "male", "iss_stage_num"],
            )
        )
        rows.append(ols_model(df, score, "PR", "PR RNA-subtype probability adjusted for age, sex, ISS", ["age_z", "male", "iss_stage_num"]))
    results = pd.DataFrame(rows)
    ok = results["status"].eq("ok")
    results["fdr"] = np.nan
    results.loc[ok, "fdr"] = bh_fdr(results.loc[ok, "p_value"])
    results = results.sort_values(["fdr", "p_value"], na_position="last")
    return results


def plot_forest(results: pd.DataFrame) -> None:
    selected_models = [
        "OS adjusted for age, sex, ISS",
        "OS adjusted for age, sex, ISS, 1q21",
        "ISS III adjusted for age and sex",
        "1q21 gain/amplification adjusted for age, sex, ISS",
    ]
    sub = results[
        results["status"].eq("ok")
        & results["model_name"].isin(selected_models)
        & results["score"].isin(["plasma_secretory_score_z", "clinical_subtype_module_score_z", "TXNDC5_z", "JCHAIN_z"])
        & results["effect_type"].isin(["hazard_ratio_per_1sd_score", "odds_ratio_per_1sd_score"])
    ].copy()
    if sub.empty:
        return
    sub["label"] = sub["model_name"] + " | " + sub["score_label"]
    sub = sub.sort_values(["model_name", "fdr"], ascending=[True, True]).head(24)
    y = np.arange(len(sub))
    fig_h = max(5, 0.32 * len(sub) + 1.2)
    fig, ax = plt.subplots(figsize=(9.5, fig_h))
    colors = np.where(sub["fdr"] < 0.05, "#b56576", "#6d6875")
    for i, (_, row) in enumerate(sub.iterrows()):
        color = colors[i]
        ax.errorbar(
            row["effect"],
            i,
            xerr=[[row["effect"] - row["ci_lower"]], [row["ci_upper"] - row["effect"]]],
            fmt="none",
            ecolor=color,
            elinewidth=1.4,
            capsize=2,
        )
        ax.scatter(row["effect"], i, c=color, s=32, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(sub["label"], fontsize=7)
    ax.invert_yaxis()
    ax.axvline(1.0, color="#222222", linestyle="--", linewidth=0.9)
    ax.set_xscale("log")
    ax.set_xlabel("Adjusted HR / OR per 1 SD score")
    ax.set_title("Adjusted CoMMpass / NG2024 models")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "commppass_ng2024_adjusted_model_forestplot.png", dpi=240)
    fig.savefig(OUT / "commppass_ng2024_adjusted_model_forestplot.pdf")
    plt.close(fig)


def fmt(x: object) -> str:
    try:
        value = float(x)
    except Exception:
        return "NA"
    if math.isnan(value):
        return "NA"
    if abs(value) < 0.001:
        return f"{value:.2e}"
    return f"{value:.4f}"


def write_report(df: pd.DataFrame, results: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    path = REPORTS / "COMMPASS_NG2024_ADJUSTED_MODEL_REPORT.md"
    ok = results[results["status"].eq("ok")].copy()
    top = ok.sort_values("fdr").head(16)
    sig = ok[ok["fdr"] < 0.05]
    lines = [
        "# CoMMpass / NG2024 Adjusted Model Report",
        "",
        "Date: 2026-04-30",
        "",
        "## Purpose",
        "",
        "- Strengthen the project beyond univariate associations by testing whether the plasma-secretory axis remains associated with OS, ISS and public molecular-risk annotations after basic covariate adjustment.",
        "- This analysis uses public GDC CoMMpass OS/ISS fields plus public Skerget et al. Nature Genetics 2024 CoMMpass molecular annotations.",
        "- It does not add PFS, R-ISS or treatment-response endpoints because those fields are not available in the current public/open tables.",
        "",
        "## Input",
        "",
        f"- Input table: `{INPUT.relative_to(PROJECT)}`.",
        f"- Samples in merged table: {len(df)}.",
        f"- OS events: {int(pd.to_numeric(df['os_event'], errors='coerce').sum())}.",
        f"- ISS available: {int(pd.to_numeric(df['iss_stage_num'], errors='coerce').notna().sum())}.",
        f"- Cytogenetic high-risk available: {int(pd.to_numeric(df['Cytogenetic_High_Risk'], errors='coerce').notna().sum())}.",
        f"- 1q21 call available: {int(pd.to_numeric(df['Cp_1q21_Call'], errors='coerce').notna().sum())}.",
        "",
        "## Models",
        "",
        "- Cox proportional hazards: OS ~ score + age + sex + ISS.",
        "- Cox proportional hazards: OS ~ score + age + sex + ISS + 1q21.",
        "- Cox proportional hazards: OS ~ score + age + sex + ISS + cytogenetic high-risk.",
        "- Logistic regression: ISS III ~ score + age + sex.",
        "- Logistic regression: IMWG non-standard risk / cytogenetic high-risk / 1q21 / 17p13 ~ score + age + sex + ISS.",
        "- Linear model: PR RNA-subtype probability ~ score + age + sex + ISS.",
        "",
        "## Top Adjusted Results",
        "",
    ]
    if top.empty:
        lines.append("- No adjusted models completed.")
    else:
        lines.append("| Model | Endpoint | Score | n | Events/cases | Effect | 95% CI | FDR |")
        lines.append("|---|---|---|---:|---:|---:|---:|---:|")
        for _, row in top.iterrows():
            ci = f"{fmt(row['ci_lower'])}-{fmt(row['ci_upper'])}"
            lines.append(
                f"| {row['model_name']} | {row['endpoint']} | {row['score_label']} | {int(row['n'])} | "
                f"{row['events_or_cases']} | {fmt(row['effect'])} | {ci} | {fmt(row['fdr'])} |"
            )
    lines += [
        "",
        "## Interpretation",
        "",
        f"- Completed adjusted models: {len(ok)}.",
        f"- FDR < 0.05 adjusted findings: {len(sig)}.",
        "- These results can support the manuscript as covariate-adjusted association evidence, but they should not be written as causal mechanism or wet-lab validation.",
        "- Because public/open CoMMpass still lacks PFS, R-ISS and treatment-response fields, those endpoints remain future MMRF-dependent enhancements.",
        "",
        "## Outputs",
        "",
        f"- `{(OUT / 'commppass_ng2024_adjusted_model_results.tsv').relative_to(PROJECT)}`",
        f"- `{(OUT / 'commppass_ng2024_adjusted_model_fdr_ranked.tsv').relative_to(PROJECT)}`",
        f"- `{(OUT / 'commppass_ng2024_adjusted_model_forestplot.png').relative_to(PROJECT)}`",
        f"- `{(OUT / 'commppass_ng2024_adjusted_model_forestplot.pdf').relative_to(PROJECT)}`",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = load_data()
    results = run_models(df)
    results.to_csv(OUT / "commppass_ng2024_adjusted_model_results.tsv", sep="\t", index=False)
    results[results["status"].eq("ok")].sort_values("fdr").to_csv(
        OUT / "commppass_ng2024_adjusted_model_fdr_ranked.tsv", sep="\t", index=False
    )
    plot_forest(results)
    write_report(df, results)
    print(results[results["status"].eq("ok")].head(12).to_string(index=False))
    print(f"Wrote: {OUT / 'commppass_ng2024_adjusted_model_results.tsv'}")
    print(f"Wrote: {REPORTS / 'COMMPASS_NG2024_ADJUSTED_MODEL_REPORT.md'}")


if __name__ == "__main__":
    main()
