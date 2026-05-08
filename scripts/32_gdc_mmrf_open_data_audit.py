from __future__ import annotations

import collections
import csv
import io
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
GDC_API = "https://api.gdc.cancer.gov"
GDC_PROJECT = "MMRF-COMMPASS"

OUT = PROJECT / "analysis" / "mmrf_open_data_audit"
RAW = PROJECT / "external_bulk" / "CoMMpass_GDC"
REPORTS = PROJECT / "reports" / "validation"

OUT.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)


ENDPOINT_PATTERNS = {
    "R-ISS": [r"\br[\s_-]?iss\b", r"revised.*international.*staging", r"riss"],
    "PFS": [r"\bpfs\b", r"progression.*free", r"progression", r"relapse", r"recurrence"],
    "treatment_response": [
        r"treat",
        r"therapy",
        r"regimen",
        r"response",
        r"best.*response",
        r"\bcr\b",
        r"\bvgpr\b",
        r"\bpr\b",
        r"refractory",
    ],
    "cytogenetic_fish": [
        r"fish",
        r"cyto",
        r"del17p",
        r"17p",
        r"t\(4;14\)",
        r"t_4_14",
        r"t\(14;16\)",
        r"t_14_16",
        r"1q",
        r"gain",
        r"amp",
    ],
    "baseline_labs": [r"ldh", r"albumin", r"microglobulin", r"b2m", r"beta", r"calcium", r"creatinine", r"hemoglobin"],
}


def curl_get(path_or_url: str, params: dict[str, str] | None = None) -> str:
    url = path_or_url if path_or_url.startswith("http") else f"{GDC_API}/{path_or_url.lstrip('/')}"
    cmd = [
        "curl.exe",
        "-sS",
        "-L",
        "--ssl-no-revoke",
        "--connect-timeout",
        "30",
        "--max-time",
        "180",
    ]
    if params:
        cmd.extend(["-G", url])
        for key, value in params.items():
            cmd.extend(["--data-urlencode", f"{key}={value}"])
    else:
        cmd.append(url)

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    if result.returncode != 0:
        raise RuntimeError(f"curl failed for {url}: {result.stderr.strip()}")
    return result.stdout


def curl_json(path_or_url: str, params: dict[str, str] | None = None) -> dict:
    text = curl_get(path_or_url, params)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Expected JSON but received: {text[:500]}") from exc


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def flatten_case_projects(hit: dict) -> str:
    projects: list[str] = []
    for case in hit.get("cases", []) or []:
        project = case.get("project", {}) or {}
        project_id = project.get("project_id")
        if project_id:
            projects.append(str(project_id))
    return "|".join(sorted(set(projects)))


def audit_files() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    filters = {
        "op": "and",
        "content": [
            {"op": "in", "content": {"field": "cases.project.project_id", "value": [GDC_PROJECT]}},
            {"op": "in", "content": {"field": "files.access", "value": ["open"]}},
        ],
    }
    fields = ",".join(
        [
            "file_id",
            "file_name",
            "data_category",
            "data_type",
            "data_format",
            "experimental_strategy",
            "access",
            "cases.project.project_id",
        ]
    )
    data = curl_json(
        "files",
        {
            "filters": json.dumps(filters),
            "format": "json",
            "size": "5000",
            "fields": fields,
        },
    )
    hits = data.get("data", {}).get("hits", [])
    rows: list[dict[str, object]] = []
    for hit in hits:
        rows.append(
            {
                "file_id": hit.get("file_id") or hit.get("id") or "",
                "file_name": hit.get("file_name") or "",
                "data_category": hit.get("data_category") or "",
                "data_type": hit.get("data_type") or "",
                "data_format": hit.get("data_format") or "",
                "experimental_strategy": hit.get("experimental_strategy") or "",
                "access": hit.get("access") or "",
                "case_projects": flatten_case_projects(hit),
            }
        )

    write_tsv(
        OUT / "gdc_open_file_inventory.tsv",
        rows,
        ["file_id", "file_name", "data_category", "data_type", "data_format", "experimental_strategy", "access", "case_projects"],
    )

    counter = collections.Counter(
        (
            row["data_category"],
            row["data_type"],
            row["experimental_strategy"],
            row["data_format"],
        )
        for row in rows
    )
    count_rows = [
        {
            "n_files": count,
            "data_category": key[0],
            "data_type": key[1],
            "experimental_strategy": key[2],
            "data_format": key[3],
        }
        for key, count in counter.most_common()
    ]
    write_tsv(
        OUT / "gdc_open_file_type_counts.tsv",
        count_rows,
        ["n_files", "data_category", "data_type", "experimental_strategy", "data_format"],
    )
    return rows, count_rows


def audit_clinical() -> tuple[Path, list[str], list[dict[str, str]], dict[str, object]]:
    fields = ",".join(
        [
            "case_id",
            "submitter_id",
            "demographic.age_at_index",
            "demographic.days_to_death",
            "demographic.ethnicity",
            "demographic.gender",
            "demographic.race",
            "demographic.vital_status",
            "diagnoses.days_to_last_follow_up",
            "diagnoses.days_to_last_known_disease_status",
            "diagnoses.iss_stage",
            "diagnoses.last_known_disease_status",
            "diagnoses.primary_diagnosis",
            "diagnoses.progression_or_recurrence",
            "diagnoses.site_of_resection_or_biopsy",
            "diagnoses.tissue_or_organ_of_origin",
            "diagnoses.treatments.treatment_type",
            "diagnoses.treatments.treatment_or_therapy",
            "diagnoses.treatments.therapeutic_agents",
            "diagnoses.treatments.treatment_outcome",
            "diagnoses.treatments.days_to_treatment_start",
            "diagnoses.treatments.days_to_treatment_end",
        ]
    )
    filters = {"op": "in", "content": {"field": "project.project_id", "value": [GDC_PROJECT]}}
    text = curl_get(
        "cases",
        {
            "filters": json.dumps(filters),
            "format": "TSV",
            "size": "2000",
            "fields": fields,
        },
    )
    clinical_path = RAW / "gdc_mmrfcases_clinical_current_20260502.tsv"
    clinical_path.write_text(text, encoding="utf-8")
    first_line = text.splitlines()[0] if text.splitlines() else ""
    columns = first_line.split("\t") if first_line else []

    candidates: list[dict[str, str]] = []
    for endpoint, patterns in ENDPOINT_PATTERNS.items():
        for col in columns:
            if any(re.search(pattern, col, flags=re.IGNORECASE) for pattern in patterns):
                candidates.append({"endpoint": endpoint, "candidate_column": col})

    write_tsv(OUT / "gdc_open_clinical_endpoint_candidate_columns.tsv", candidates, ["endpoint", "candidate_column"])
    (OUT / "gdc_open_clinical_columns.txt").write_text("\n".join(columns) + "\n", encoding="utf-8")
    summary = summarize_clinical_values(text)
    return clinical_path, columns, candidates, summary


def summarize_clinical_values(text: str) -> dict[str, object]:
    reader = csv.DictReader(io.StringIO(text), delimiter="\t")
    rows = list(reader)
    columns = reader.fieldnames or []

    def nonempty_count(pattern: str) -> int:
        cols = [col for col in columns if pattern in col]
        return sum(1 for row in rows for col in cols if str(row.get(col, "")).strip())

    def value_counts(pattern: str, limit: int = 12) -> list[tuple[str, int]]:
        cols = [col for col in columns if pattern in col]
        counter: collections.Counter[str] = collections.Counter()
        for row in rows:
            for col in cols:
                value = str(row.get(col, "")).strip()
                if value:
                    counter[value] += 1
        return counter.most_common(limit)

    return {
        "n_rows": len(rows),
        "n_columns": len(columns),
        "progression_or_recurrence_values": value_counts("progression_or_recurrence"),
        "treatment_outcome_nonempty": nonempty_count("treatment_outcome"),
        "treatment_type_values": value_counts("treatment_type"),
        "therapeutic_agents_values": value_counts("therapeutic_agents"),
        "treatment_or_therapy_values": value_counts("treatment_or_therapy"),
        "days_to_treatment_start_nonempty": nonempty_count("days_to_treatment_start"),
        "days_to_treatment_end_nonempty": nonempty_count("days_to_treatment_end"),
    }


def build_report(
    status: dict,
    file_rows: list[dict[str, object]],
    count_rows: list[dict[str, object]],
    clinical_path: Path,
    clinical_columns: list[str],
    clinical_candidates: list[dict[str, str]],
    clinical_summary: dict[str, object],
) -> None:
    category_lines = [
        f"- {row['n_files']} file(s): {row['data_category']} / {row['data_type']} / {row['experimental_strategy']} / {row['data_format']}"
        for row in count_rows
    ]
    candidate_by_endpoint: dict[str, list[str]] = collections.defaultdict(list)
    for row in clinical_candidates:
        candidate_by_endpoint[row["endpoint"]].append(row["candidate_column"])

    clinical_like_file_rows = [
        row
        for row in file_rows
        if re.search(
            r"clinical|biospecimen|treatment|therapy|response|pfs|fish|cyto|relapse|progression",
            " ".join(str(row.get(k, "")) for k in ["data_category", "data_type", "file_name"]),
            flags=re.IGNORECASE,
        )
    ]

    lines = [
        "# GDC Open MMRF-COMMPASS Data Audit",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "Purpose:",
        "",
        "- Verify what the open GDC MMRF-COMMPASS API can provide for the current manuscript.",
        "- Distinguish already available open GDC data from fuller MMRF Researcher Gateway clinical files.",
        "",
        "GDC status:",
        "",
        f"- API status: {status.get('status', 'unknown')}",
        f"- Data release: {status.get('data_release', 'unknown')}",
        "",
        "Open file inventory:",
        "",
        f"- Total open files found: {len(file_rows)}",
        *category_lines,
        "",
        "Clinical-like files in the GDC files endpoint:",
        "",
    ]
    if clinical_like_file_rows:
        for row in clinical_like_file_rows:
            lines.append(
                f"- {row['data_category']} / {row['data_type']} / {row['data_format']}: {row['file_name']}"
            )
    else:
        lines.append("- None found in the open GDC files endpoint.")

    lines.extend(
        [
            "",
            "Clinical endpoint:",
            "",
            f"- Current clinical TSV saved to `{clinical_path.relative_to(PROJECT)}`.",
            f"- Current cases returned: {clinical_summary.get('n_rows', 'unknown')}.",
            f"- Number of columns in current GDC cases/clinical TSV: {len(clinical_columns)}.",
            "",
            "Endpoint candidate columns detected by keyword scan:",
            "",
        ]
    )
    for endpoint in ENDPOINT_PATTERNS:
        cols = candidate_by_endpoint.get(endpoint, [])
        if cols:
            preview = ", ".join(cols[:12])
            suffix = "" if len(cols) <= 12 else f" ... ({len(cols)} columns total)"
            lines.append(f"- {endpoint}: {preview}{suffix}")
        else:
            lines.append(f"- {endpoint}: none detected")

    lines.extend(
        [
            "",
            "Usability checks for key open clinical fields:",
            "",
            f"- `diagnoses.progression_or_recurrence` values: {clinical_summary.get('progression_or_recurrence_values')}",
            f"- treatment outcome non-empty cells: {clinical_summary.get('treatment_outcome_nonempty')}",
            f"- treatment type values: {clinical_summary.get('treatment_type_values')}",
            f"- therapeutic agent values: {clinical_summary.get('therapeutic_agents_values')}",
            f"- treatment-or-therapy values: {clinical_summary.get('treatment_or_therapy_values')}",
            f"- treatment start-date non-empty cells: {clinical_summary.get('days_to_treatment_start_nonempty')}",
            f"- treatment end-date non-empty cells: {clinical_summary.get('days_to_treatment_end_nonempty')}",
            "",
            "Interpretation for the manuscript:",
            "",
            "- Open GDC remains useful for RNA-seq expression, masked somatic mutation MAF, copy-number segment files, limited OS/ISS clinical fields, and treatment-exposure/therapeutic-agent metadata.",
            "- The current open GDC cases/clinical TSV still does not provide usable PFS, R-ISS, treatment-response outcome, baseline laboratory, or FISH/cytogenetic fields needed for the optional fuller-clinical extension.",
            "- Therefore open GDC cannot replace authorized MMRF Researcher Gateway / Virtual Lab fuller clinical tables for R-ISS, PFS, treatment response, and detailed cytogenetic validation.",
            "",
            "Outputs:",
            "",
            f"- `{(OUT / 'gdc_open_file_inventory.tsv').relative_to(PROJECT)}`",
            f"- `{(OUT / 'gdc_open_file_type_counts.tsv').relative_to(PROJECT)}`",
            f"- `{(OUT / 'gdc_open_clinical_endpoint_candidate_columns.tsv').relative_to(PROJECT)}`",
            f"- `{(OUT / 'gdc_open_clinical_columns.txt').relative_to(PROJECT)}`",
            "",
        ]
    )
    (REPORTS / "GDC_OPEN_MMRF_COMMPASS_DATA_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    status = curl_json("status")
    file_rows, count_rows = audit_files()
    clinical_path, clinical_columns, clinical_candidates, clinical_summary = audit_clinical()
    build_report(status, file_rows, count_rows, clinical_path, clinical_columns, clinical_candidates, clinical_summary)
    print(f"Open file inventory: {OUT / 'gdc_open_file_inventory.tsv'}")
    print(f"Clinical TSV: {clinical_path}")
    print(f"Report: {REPORTS / 'GDC_OPEN_MMRF_COMMPASS_DATA_AUDIT.md'}")


if __name__ == "__main__":
    main()
