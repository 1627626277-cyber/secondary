from __future__ import annotations

import re
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "reports" / "manuscript" / "MANUSCRIPT_BMC_MEDICAL_GENOMICS_TARGET_DRAFT.md"
OUT_MD = ROOT / "reports" / "manuscript" / "REFERENCE_LINK_AUDIT_2026-05-01.md"
OUT_TSV = ROOT / "reports" / "manuscript" / "REFERENCE_LINK_AUDIT_2026-05-01.tsv"


@dataclass
class LinkResult:
    reference: str
    link_type: str
    target: str
    status: str
    http_status: str
    final_url: str
    note: str


def extract_references(text: str) -> list[tuple[str, str]]:
    match = re.search(r"^## References\s*$\n(?P<body>.*)$", text, flags=re.S | re.M)
    if not match:
        return []
    refs = []
    current_num = None
    current_lines: list[str] = []
    for line in match.group("body").splitlines():
        m = re.match(r"^(\d+)\.\s+(.*)", line)
        if m:
            if current_num is not None:
                refs.append((current_num, " ".join(current_lines).strip()))
            current_num = m.group(1)
            current_lines = [m.group(2).strip()]
        elif current_num is not None and line.strip():
            current_lines.append(line.strip())
    if current_num is not None:
        refs.append((current_num, " ".join(current_lines).strip()))
    return refs


def extract_links(reference_text: str) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    for doi in re.findall(r"doi:\s*([^\s;]+)", reference_text, flags=re.I):
        clean = doi.rstrip(".")
        links.append(("doi", f"https://doi.org/{clean}"))
    for url in re.findall(r"https?://[^\s)]+", reference_text):
        clean = url.rstrip(".")
        if clean.startswith("https://doi.org/"):
            continue
        links.append(("url", clean))
    return links


def check_url(url: str) -> tuple[str, str, str, str]:
    context = ssl.create_default_context()
    headers = {
        "User-Agent": "Mozilla/5.0 reference-link-audit",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=20, context=context) as response:
            code = str(response.getcode())
            final = response.geturl()
            return "ok", code, final, ""
    except urllib.error.HTTPError as exc:
        final = getattr(exc, "url", url)
        if exc.code in {401, 403, 405, 429}:
            return "access_limited", str(exc.code), final, type(exc).__name__
        return "failed", str(exc.code), final, type(exc).__name__
    except Exception as exc:  # noqa: BLE001
        return "failed", "", url, f"{type(exc).__name__}: {exc}"


def main() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    refs = extract_references(text)
    results: list[LinkResult] = []
    for num, ref_text in refs:
        links = extract_links(ref_text)
        if not links:
            results.append(LinkResult(num, "none", "", "not_applicable", "", "", "No DOI or URL present in reference entry."))
            continue
        for link_type, target in links:
            status, code, final, note = check_url(target)
            results.append(LinkResult(num, link_type, target, status, code, final, note))

    lines = [
        "# Reference DOI/URL Live-Link Audit",
        "",
        "Date: 2026-05-01",
        "",
        "Scope:",
        "",
        "- Checked DOI and URL targets in the current Vancouver reference list.",
        "- `access_limited` means the target responded but blocked automated access, usually with 403, 405, 429, or authentication behavior.",
        "",
        "## Summary",
        "",
    ]
    total = len(results)
    for status in ["ok", "access_limited", "failed", "not_applicable"]:
        count = sum(1 for row in results if row.status == status)
        lines.append(f"- {status}: {count}")
    lines.extend(["", "## Results", "", "| Ref | Type | Status | HTTP | Target | Note |", "|---:|---|---|---|---|---|"])
    for row in results:
        note = row.note.replace("|", "/")
        target = row.target.replace("|", "%7C")
        lines.append(f"| {row.reference} | {row.link_type} | {row.status} | {row.http_status} | {target} | {note} |")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    tsv = ["reference\tlink_type\ttarget\tstatus\thttp_status\tfinal_url\tnote"]
    for row in results:
        tsv.append(
            "\t".join(
                [
                    row.reference,
                    row.link_type,
                    row.target,
                    row.status,
                    row.http_status,
                    row.final_url,
                    row.note.replace("\t", " "),
                ]
            )
        )
    OUT_TSV.write_text("\n".join(tsv) + "\n", encoding="utf-8")
    print(OUT_MD)
    print(OUT_TSV)


if __name__ == "__main__":
    main()
