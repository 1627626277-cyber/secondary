from __future__ import annotations

import gzip
import re
from pathlib import Path

import pandas as pd


PROJECT = Path.cwd()
BASE = PROJECT / "external_spatial" / "GSE299193"
META = BASE / "metadata"
RAW = BASE / "raw"
ANALYSIS = PROJECT / "analysis" / "gse299193_xenium_validation"
REPORTS = PROJECT / "reports" / "validation"

SOFT = META / "GSE299193_family.soft.gz"
RAW_TAR = RAW / "GSE299193_RAW.tar"
EXPECTED_BYTES = 82_255_360_000
URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE299nnn/GSE299193/suppl/GSE299193_RAW.tar"


def parse_soft() -> pd.DataFrame:
    if not SOFT.exists():
        raise FileNotFoundError(f"Missing SOFT metadata: {SOFT}")
    text = gzip.open(SOFT, "rt", encoding="utf-8", errors="replace").read()
    rows: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in text.splitlines():
        if line.startswith("^SAMPLE = "):
            if current:
                rows.append(current)
            current = {"geo_accession": line.split("=", 1)[1].strip()}
        elif current is not None and line.startswith("!Sample_title = "):
            current["title"] = line.split("=", 1)[1].strip()
        elif current is not None and line.startswith("!Sample_source_name_ch1 = "):
            current["source"] = line.split("=", 1)[1].strip()
        elif current is not None and line.startswith("!Sample_characteristics_ch1 = condition:"):
            current["condition"] = line.split("condition:", 1)[1].strip()
        elif current is not None and line.startswith("!Sample_characteristics_ch1 = Sex:"):
            current["sex"] = line.split("Sex:", 1)[1].strip()
    if current:
        rows.append(current)
    df = pd.DataFrame(rows)
    if not df.empty:
        order = ["Ctrl", "MGUS", "SM", "MM", "RM"]
        df["condition_order"] = df["condition"].map({v: i for i, v in enumerate(order)}).fillna(99).astype(int)
        df = df.sort_values(["condition_order", "geo_accession"]).drop(columns=["condition_order"])
    return df


def write_outputs() -> None:
    META.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    ANALYSIS.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    manifest = parse_soft()
    manifest.to_csv(META / "gse299193_sample_manifest.tsv", sep="\t", index=False)
    summary = (
        manifest.groupby("condition", as_index=False)
        .agg(n_samples=("geo_accession", "count"), n_male=("sex", lambda s: int((s == "Male").sum())), n_female=("sex", lambda s: int((s == "Female").sum())))
        .sort_values("condition")
    )
    summary.to_csv(ANALYSIS / "gse299193_sample_group_summary.tsv", sep="\t", index=False)

    current = RAW_TAR.stat().st_size if RAW_TAR.exists() else 0
    pct = current / EXPECTED_BYTES * 100
    remaining = max(EXPECTED_BYTES - current, 0)
    status = pd.DataFrame(
        [
            {
                "dataset": "GSE299193",
                "raw_url": URL,
                "raw_tar": str(RAW_TAR.relative_to(PROJECT)),
                "expected_bytes": EXPECTED_BYTES,
                "current_bytes": current,
                "current_gib": round(current / 1024**3, 3),
                "remaining_gib": round(remaining / 1024**3, 3),
                "percent_complete": round(pct, 4),
                "is_complete_size": current == EXPECTED_BYTES,
            }
        ]
    )
    status.to_csv(ANALYSIS / "gse299193_download_status.tsv", sep="\t", index=False)

    lines = [
        "# GSE299193 Xenium Download and Validation Status",
        "",
        "Dataset:",
        "",
        "- GEO accession: `GSE299193`.",
        "- Title: Profiling the spatial architecture of multiple myeloma in human bone marrow trephines with spatial transcriptomics [human].",
        "- Platform: Xenium In Situ Analyzer, Homo sapiens.",
        "- RAW file: `GSE299193_RAW.tar`.",
        f"- Expected RAW size: {EXPECTED_BYTES:,} bytes / {EXPECTED_BYTES / 1024**3:.2f} GiB.",
        "",
        "Sample groups from SOFT metadata:",
        "",
    ]
    for _, row in summary.iterrows():
        lines.append(f"- {row['condition']}: {int(row['n_samples'])} sample(s), male={int(row['n_male'])}, female={int(row['n_female'])}.")
    lines.extend(
        [
            "",
            "Current download status:",
            "",
            f"- Current size: {current:,} bytes / {current / 1024**3:.2f} GiB.",
            f"- Percent complete: {pct:.4f}%.",
            f"- Remaining: {remaining / 1024**3:.2f} GiB.",
            "",
            "Planned validation after download:",
            "",
            "- List tar contents and identify Xenium cell-feature matrices.",
            "- Extract only matrix/metadata files required for expression scoring first.",
            "- Compute `plasma_secretory`, `clinical_subtype_module`, and marker-level TXNDC5/POU2AF1/XBP1/JCHAIN signals.",
            "- Compare disease groups: Ctrl/MGUS/SM vs MM/RM where sample counts allow.",
            "- Add Fig. 6 or supplemental validation figure if the signal is usable.",
            "",
        ]
    )
    (REPORTS / "GSE299193_XENIUM_DOWNLOAD_STATUS.md").write_text("\n".join(lines), encoding="utf-8")
    print(status.to_string(index=False))
    print(f"Wrote manifest: {META / 'gse299193_sample_manifest.tsv'}")
    print(f"Wrote report: {REPORTS / 'GSE299193_XENIUM_DOWNLOAD_STATUS.md'}")


if __name__ == "__main__":
    write_outputs()
