from __future__ import annotations

import math
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.duration.hazard_regression import PHReg
from statsmodels.stats.multitest import multipletests


PROJECT = Path.cwd()
INPUT = PROJECT / "analysis" / "skerget_ng2024_public_supplement" / "commppass_scores_with_ng2024_annotations.tsv"
OUT = PROJECT / "analysis" / "commppass_sensitivity_models"
REPORTS = PROJECT / "reports" / "validation"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

SCORES = [
    "plasma_secretory_score_z",
    "clinical_subtype_module_score_z",
]

LABELS = {
    "plasma_secretory_score_z": "Plasma-secretory score",
    "clinical_subtype_module_score_z": "POU2AF1/XBP1/JCHAIN module",
}


def zscore(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce")
    sd = x.std(skipna=True)
    if pd.isna(sd) or sd == 0:
        return pd.Series(np.nan, index=s.index)
    return (x - x.mean(skipna=True)) / sd


def bh_fdr(p: pd.Series) -> pd.Series:
    out = pd.Series(np.nan, index=p.index, dtype=float)
    valid = pd.to_numeric(p, errors="coerce").dropna()
    if valid.empty:
        return out
    _, q, _, _ = multipletests(valid.to_numpy(float), method="fdr_bh")
    out.loc[valid.index] = q
    return out


def c_index(time: np.ndarray, event: np.ndarray, risk: np.ndarray) -> float:
    concordant = 0.0
    comparable = 0
    n = len(time)
    for i in range(n):
        if event[i] != 1 or not np.isfinite(time[i]) or not np.isfinite(risk[i]):
            continue
        for j in range(n):
            if time[i] >= time[j] or not np.isfinite(time[j]) or not np.isfinite(risk[j]):
                continue
            comparable += 1
            if risk[i] > risk[j]:
                concordant += 1
            elif risk[i] == risk[j]:
                concordant += 0.5
    return concordant / comparable if comparable else np.nan


def load_data() -> pd.DataFrame:
    df = pd.read_csv(INPUT, sep="\t")
    df["age_z"] = zscore(df["age_at_index"].combine_first(df.get("Age", pd.Series(index=df.index))))
    gender = df.get("gender", pd.Series(index=df.index, dtype=object)).astype(str).str.lower()
    df["male"] = np.where(gender.eq("male"), 1.0, np.where(gender.eq("female"), 0.0, np.nan))
    df["iss_stage_num"] = pd.to_numeric(df["iss_stage_num"], errors="coerce")
    df["os_time_months"] = pd.to_numeric(df["os_time_months"], errors="coerce")
    df["os_event"] = pd.to_numeric(df["os_event"], errors="coerce")
    df["oneq21"] = pd.to_numeric(df.get("Cp_1q21_Call"), errors="coerce")
    df["del17p"] = pd.to_numeric(df.get("Cp_17p13_Call"), errors="coerce")
    df["high_risk_cyto"] = pd.to_numeric(df.get("Cytogenetic_High_Risk"), errors="coerce")
    df["pr_probability_z"] = zscore(df.get("PR", pd.Series(index=df.index)))
    df["proliferation_z"] = zscore(df.get("Proliferation_Index_Bergsagel", pd.Series(index=df.index)))
    df["low_purity_probability_z"] = zscore(df.get("Low purity", pd.Series(index=df.index)))
    cmmc = pd.to_numeric(df.get("CMMC_Value", pd.Series(index=df.index)), errors="coerce")
    df["log1p_cmmc_z"] = zscore(np.log1p(cmmc))
    return df


def model_specs() -> list[tuple[str, list[str], str]]:
    return [
        ("M1 age+sex+ISS+1q21", ["age_z", "male", "iss_stage_num", "oneq21"], "Base clinical/cytogenetic adjustment"),
        ("M2 M1+PR probability", ["age_z", "male", "iss_stage_num", "oneq21", "pr_probability_z"], "Tests whether the score adds information beyond PR-like subtype probability"),
        ("M3 M1+PR+proliferation", ["age_z", "male", "iss_stage_num", "oneq21", "pr_probability_z", "proliferation_z"], "Controls PR-like subtype and proliferation/cell-cycle context"),
        ("M4 M1+del17p+high-risk cytogenetics", ["age_z", "male", "iss_stage_num", "oneq21", "del17p", "high_risk_cyto"], "Adds public high-risk cytogenetic annotations"),
        ("M5 M1+low-purity probability", ["age_z", "male", "iss_stage_num", "oneq21", "low_purity_probability_z"], "Uses NG2024 low-purity probability as a public purity sensitivity covariate"),
        ("M6 M1+PR+proliferation+low-purity", ["age_z", "male", "iss_stage_num", "oneq21", "pr_probability_z", "proliferation_z", "low_purity_probability_z"], "Stringent public-annotation sensitivity model"),
        ("M7 M1+clinical tumor burden CMMC", ["age_z", "male", "iss_stage_num", "oneq21", "log1p_cmmc_z"], "Exploratory model using available CMMC tumor-burden field; many samples are missing"),
    ]


def fit_cox(df: pd.DataFrame, score: str, model_name: str, covariates: list[str], note: str) -> dict[str, object]:
    cols = [score] + covariates
    tmp = df[["os_time_months", "os_event"] + cols].copy()
    tmp = tmp.apply(pd.to_numeric, errors="coerce").dropna()
    tmp = tmp[(tmp["os_time_months"] > 0) & tmp["os_event"].isin([0, 1])]
    if len(tmp) < 80 or tmp["os_event"].sum() < 20:
        return {
            "model_name": model_name,
            "score": score,
            "score_label": LABELS.get(score, score),
            "n": int(len(tmp)),
            "events": int(tmp["os_event"].sum()) if len(tmp) else 0,
            "hr": np.nan,
            "ci_lower": np.nan,
            "ci_upper": np.nan,
            "coef": np.nan,
            "se": np.nan,
            "p_value": np.nan,
            "c_index": np.nan,
            "covariates": ",".join(covariates),
            "status": "insufficient_complete_data",
            "note": note,
        }
    used_cols = ["score"] + covariates
    design = tmp[[score] + covariates].copy()
    design.columns = used_cols
    try:
        fit = PHReg(tmp["os_time_months"], design[used_cols], status=tmp["os_event"]).fit(disp=False)
        coef = float(fit.params[0])
        se = float(fit.bse[0])
        p = float(fit.pvalues[0])
        risk = np.asarray(design[used_cols] @ fit.params, dtype=float)
        return {
            "model_name": model_name,
            "score": score,
            "score_label": LABELS.get(score, score),
            "n": int(len(tmp)),
            "events": int(tmp["os_event"].sum()),
            "hr": math.exp(coef),
            "ci_lower": math.exp(coef - 1.96 * se),
            "ci_upper": math.exp(coef + 1.96 * se),
            "coef": coef,
            "se": se,
            "p_value": p,
            "c_index": c_index(tmp["os_time_months"].to_numpy(float), tmp["os_event"].to_numpy(float), risk),
            "covariates": ",".join(covariates),
            "status": "ok",
            "note": note,
        }
    except Exception as exc:
        return {
            "model_name": model_name,
            "score": score,
            "score_label": LABELS.get(score, score),
            "n": int(len(tmp)),
            "events": int(tmp["os_event"].sum()),
            "hr": np.nan,
            "ci_lower": np.nan,
            "ci_upper": np.nan,
            "coef": np.nan,
            "se": np.nan,
            "p_value": np.nan,
            "c_index": np.nan,
            "covariates": ",".join(covariates),
            "status": "failed",
            "note": f"{note}; {type(exc).__name__}: {exc}",
        }


def fit_logit_1q21(df: pd.DataFrame, score: str) -> dict[str, object]:
    covariates = ["age_z", "male", "iss_stage_num", "pr_probability_z", "proliferation_z", "low_purity_probability_z"]
    tmp = df[["oneq21", score] + covariates].copy()
    tmp = tmp.apply(pd.to_numeric, errors="coerce").dropna()
    tmp = tmp[tmp["oneq21"].isin([0, 1])]
    if len(tmp) < 80 or tmp["oneq21"].sum() < 20:
        return {"score": score, "n": len(tmp), "cases": tmp["oneq21"].sum() if len(tmp) else 0, "status": "insufficient_complete_data"}
    design = sm.add_constant(tmp[[score] + covariates], has_constant="add")
    design = design.rename(columns={score: "score"})
    try:
        fit = sm.Logit(tmp["oneq21"], design).fit(disp=False, maxiter=200)
        coef = float(fit.params["score"])
        se = float(fit.bse["score"])
        return {
            "score": score,
            "score_label": LABELS.get(score, score),
            "n": int(len(tmp)),
            "cases": int(tmp["oneq21"].sum()),
            "odds_ratio": math.exp(coef),
            "ci_lower": math.exp(coef - 1.96 * se),
            "ci_upper": math.exp(coef + 1.96 * se),
            "coef": coef,
            "se": se,
            "p_value": float(fit.pvalues["score"]),
            "covariates": ",".join(covariates),
            "status": "ok",
            "note": "1q21 association adjusted for PR probability, proliferation, and low-purity probability",
        }
    except Exception as exc:
        return {"score": score, "n": int(len(tmp)), "cases": int(tmp["oneq21"].sum()), "status": "failed", "note": str(exc)}


def plot_sensitivity(results: pd.DataFrame) -> None:
    mpl.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none"})
    ok = results[results["status"].eq("ok") & results["score"].eq("plasma_secretory_score_z")].copy()
    ok = ok.sort_values("model_name")
    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    y = np.arange(len(ok))
    ax.errorbar(
        ok["hr"],
        y,
        xerr=[ok["hr"] - ok["ci_lower"], ok["ci_upper"] - ok["hr"]],
        fmt="o",
        color="#C44E52",
        ecolor="#444444",
        capsize=2,
    )
    ax.axvline(1, color="#222222", lw=0.8, ls="--")
    labels = [f"{r.model_name}\nN={int(r.n)}, events={int(r.events)}, FDR={r.fdr:.3g}" for r in ok.itertuples()]
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("OS hazard ratio per 1-SD plasma-secretory score")
    ax.set_title("Fig. 8 | CoMMpass OS sensitivity models")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    for suffix in [".png", ".pdf", ".svg"]:
        fig.savefig(OUT / f"commppass_os_sensitivity_forestplot{suffix}", dpi=350, bbox_inches="tight")
    plt.close(fig)


def write_report(cox: pd.DataFrame, logit: pd.DataFrame) -> None:
    plasma = cox[cox["score"].eq("plasma_secretory_score_z")].copy()
    plasma_ok = plasma[plasma["status"].eq("ok")]
    lines = [
        "# CoMMpass Sensitivity Models",
        "",
        "Purpose: address reviewer concerns that OS and 1q21 associations may be driven by PR subtype probability, proliferation, cytogenetic risk, or public purity/tumor-burden annotations.",
        "",
        "Cox OS models:",
        "",
        plasma_ok[["model_name", "n", "events", "hr", "ci_lower", "ci_upper", "p_value", "fdr", "c_index", "covariates"]].to_markdown(index=False),
        "",
        "1q21 logistic sensitivity models:",
        "",
        logit.to_markdown(index=False),
        "",
        "Interpretation boundary:",
        "",
        "- Models are retrospective association models, not prospective prediction models.",
        "- If PR/proliferation adjustment attenuates the score, this supports reframing the axis as a PR/proliferation/1q21 molecular-risk context rather than an independent clinical biomarker.",
        "- Low-purity probability and CMMC are public annotation proxies; they do not replace direct tumor purity or matched flow cytometry.",
    ]
    (REPORTS / "COMMPASS_SENSITIVITY_MODELS.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    df = load_data()
    rows = []
    for score in SCORES:
        for name, covars, note in model_specs():
            rows.append(fit_cox(df, score, name, covars, note))
    cox = pd.DataFrame(rows)
    cox["fdr"] = bh_fdr(cox["p_value"])
    cox.to_csv(OUT / "commppass_os_sensitivity_models.tsv", sep="\t", index=False)

    logit = pd.DataFrame([fit_logit_1q21(df, score) for score in SCORES])
    logit["fdr"] = bh_fdr(logit.get("p_value", pd.Series(index=logit.index)))
    logit.to_csv(OUT / "commppass_1q21_sensitivity_models.tsv", sep="\t", index=False)

    plot_sensitivity(cox)
    write_report(cox, logit)

    print(OUT / "commppass_os_sensitivity_models.tsv")
    print(OUT / "commppass_1q21_sensitivity_models.tsv")
    print(REPORTS / "COMMPASS_SENSITIVITY_MODELS.md")


if __name__ == "__main__":
    main()
