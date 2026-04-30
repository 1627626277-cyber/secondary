from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


PROJECT = Path.cwd()
DATA = PROJECT / "external_bulk" / "CoMMpass_full_clinical"
OUT = PROJECT / "analysis" / "commppass_full_clinical_validation"
REPORTS = PROJECT / "reports" / "validation"
DATA.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

ENDPOINT_PATTERNS = {
    "R-ISS": [
        r"\br[\s_-]?iss\b",
        r"revised.*international.*staging",
        r"riss",
    ],
    "PFS": [
        r"\bpfs\b",
        r"progression.*free",
        r"progression",
        r"event.*free",
        r"\befs\b",
        r"relapse",
        r"recurrence",
    ],
    "cytogenetic_high_risk": [
        r"cyto",
        r"high.*risk",
        r"del17p",
        r"17p",
        r"t\(4;14\)",
        r"t_4_14",
        r"t\(14;16\)",
        r"t_14_16",
        r"1q",
        r"amp",
        r"gain",
        r"canonical.*variant",
    ],
    "treatment_response": [
        r"treat",
        r"therapy",
        r"regimen",
        r"induction",
        r"response",
        r"best.*response",
        r"\bcr\b",
        r"\bvgpr\b",
        r"\bpr\b",
        r"refractory",
    ],
}


def discover_tables() -> list[Path]:
    patterns = ["*.tsv", "*.txt", "*.csv", "*.xlsx", "*.xls"]
    files: list[Path] = []
    for pattern in patterns:
        files.extend(DATA.rglob(pattern))
    return sorted(set(files))


def read_columns(path: Path) -> tuple[int | None, list[str], str | None]:
    try:
        if path.suffix.lower() in [".xlsx", ".xls"]:
            df = pd.read_excel(path, nrows=5)
        elif path.suffix.lower() == ".csv":
            df = pd.read_csv(path, nrows=5)
        else:
            df = pd.read_csv(path, sep="\t", nrows=5)
        return len(df), list(map(str, df.columns)), None
    except Exception as exc:  # noqa: BLE001
        return None, [], str(exc)


def classify_columns(file: Path, columns: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for endpoint, patterns in ENDPOINT_PATTERNS.items():
        for col in columns:
            haystack = col.lower()
            if any(re.search(pattern, haystack, flags=re.IGNORECASE) for pattern in patterns):
                rows.append({"file": str(file.relative_to(PROJECT)), "endpoint": endpoint, "candidate_column": col})
    return rows


def write_report(inventory: pd.DataFrame, candidates: pd.DataFrame) -> None:
    lines = [
        "# CoMMpass Fuller Clinical Data Readiness Report",
        "",
        "Purpose:",
        "",
        "- Scan local fuller MMRF/CoMMpass clinical files for R-ISS, PFS, cytogenetic high-risk, and treatment-response fields.",
        "- This script does not claim validation by itself; it only checks whether the necessary local files and columns are present.",
        "",
        f"Input folder: `{DATA.relative_to(PROJECT)}`",
        "",
    ]
    if inventory.empty:
        lines.extend(
            [
                "Status: no fuller clinical files were found.",
                "",
                "Action required:",
                "",
                "- Obtain authorized MMRF Virtual Lab / Researcher Gateway clinical files.",
                "- Place CSV/TSV/XLSX files under `external_bulk/CoMMpass_full_clinical`.",
                "- Rerun `python scripts/16_commppass_full_clinical_validation.py`.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                f"Files scanned: {len(inventory)}",
                "",
                "Endpoint candidate columns found:",
                "",
            ]
        )
        if candidates.empty:
            lines.append("- None found by keyword scan. Manual inspection is required.")
        else:
            for endpoint, sub in candidates.groupby("endpoint"):
                lines.append(f"- {endpoint}: {len(sub)} candidate column(s)")
        lines.append("")
        lines.append("Next step if columns are confirmed:")
        lines.append("")
        lines.append("- Harmonize patient IDs to the existing CoMMpass/GDC expression score table.")
        lines.append("- Add R-ISS, PFS, high-risk cytogenetics, treatment class, and response endpoints.")
        lines.append("- Perform FDR-controlled association tests and survival models.")
        lines.append("")

    (REPORTS / "COMMPASS_FULL_CLINICAL_READINESS_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows: list[dict[str, object]] = []
    candidate_rows: list[dict[str, str]] = []
    for path in discover_tables():
        n_preview, columns, error = read_columns(path)
        rows.append(
            {
                "file": str(path.relative_to(PROJECT)),
                "suffix": path.suffix.lower(),
                "preview_rows_read": n_preview,
                "n_columns": len(columns),
                "read_error": error or "",
                "columns": "|".join(columns),
            }
        )
        if columns:
            candidate_rows.extend(classify_columns(path, columns))

    inventory = pd.DataFrame(rows)
    candidates = pd.DataFrame(candidate_rows, columns=["file", "endpoint", "candidate_column"])
    inventory.to_csv(OUT / "full_clinical_inventory.tsv", sep="\t", index=False)
    candidates.to_csv(OUT / "endpoint_candidate_columns.tsv", sep="\t", index=False)
    write_report(inventory, candidates)
    print(f"Scanned fuller clinical files under: {DATA}")
    print(f"Inventory written to: {OUT / 'full_clinical_inventory.tsv'}")
    print(f"Candidate endpoint columns written to: {OUT / 'endpoint_candidate_columns.tsv'}")
    print(f"Readiness report written to: {REPORTS / 'COMMPASS_FULL_CLINICAL_READINESS_REPORT.md'}")


if __name__ == "__main__":
    main()
