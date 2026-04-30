from __future__ import annotations

import json
import re
import subprocess
import time
from pathlib import Path

import pandas as pd


PROJECT = Path.cwd()
OUT = PROJECT / "references"
PDF_DIR = OUT / "pdf"
META_DIR = OUT / "metadata"

PMID_REFS = [
    ("skerget_ng2024", "39160255", "CoMMpass NG2024 molecular annotation and public supplementary data"),
    ("yip_blood_2025_spatial", "40643106", "Related publication for GSE299193 spatial architecture dataset"),
    ("pdia4_scrna_gse271107", "41121130", "Single-cell MM progression dataset publication linked to GSE271107"),
    ("rustad_natcomm_2019", "31444325", "MM genomic landscape and driver-event context"),
    ("palumbo_riss_2015", "26240224", "R-ISS clinical-risk framework"),
    ("rajkumar_imwg_2014", "25439696", "IMWG diagnostic criteria and MM clinical context"),
    ("mcshane_remark_2005", "16106022", "REMARK reporting standard for marker studies"),
    ("wolf_scanpy_2018", "29409532", "Scanpy single-cell analysis software citation"),
    ("chapman_nature_2011", "21430775", "Initial MM genome sequencing reference"),
    ("maqc_ii_2010", "20676074", "MAQC-II microarray validation context for GSE24080"),
    ("shi_plosone_2009_maqc", "20011240", "MAQC-II multiple myeloma microarray modeling context"),
    ("rajkumar_2022_update", "35560063", "Modern MM diagnosis and management review"),
    ("greipp_iss_2005", "15809451", "ISS clinical staging framework"),
    ("zhan_blood_2006_molecular_classification", "16728703", "Molecular classification of MM by expression"),
    ("hanamura_blood_2006_1q21", "16705089", "1q21 gain/amplification in plasma-cell dyscrasias"),
    ("barrett_geo_2013", "23193258", "NCBI GEO database citation"),
    ("gdc_uniform_analysis_2021", "33619257", "NCI Genomic Data Commons citation"),
]

MANUAL_REFS = [
    {
        "key": "geo_gse269875",
        "citation": "National Center for Biotechnology Information. GEO Series GSE269875: Spatial transcriptomics unveils novel potential disease mechanisms associated with the microenvironment in multiple myeloma. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269875. Accessed 1 May 2026.",
        "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269875",
        "reason": "Primary dataset accession for spatial discovery",
    },
    {
        "key": "geo_gse299193",
        "citation": "National Center for Biotechnology Information. GEO Series GSE299193: Profiling the spatial architecture of multiple myeloma in human bone marrow trephines with spatial transcriptomics. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299193. Accessed 1 May 2026.",
        "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299193",
        "reason": "Primary dataset accession for second spatial validation",
    },
    {
        "key": "geo_gse271107",
        "citation": "National Center for Biotechnology Information. GEO Series GSE271107: Single-cell RNA sequencing of bone marrow aspirate samples from multiple myeloma and its precursor conditions. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE271107. Accessed 1 May 2026.",
        "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE271107",
        "reason": "Primary dataset accession for single-cell validation",
    },
    {
        "key": "geo_gse24080",
        "citation": "National Center for Biotechnology Information. GEO Series GSE24080: MAQC-II Project: Multiple myeloma data set. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE24080. Accessed 1 May 2026.",
        "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE24080",
        "reason": "Primary dataset accession for external bulk validation",
    },
    {
        "key": "geo_gse2658",
        "citation": "National Center for Biotechnology Information. GEO Series GSE2658: Gene expression profiles of multiple myeloma. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE2658. Accessed 1 May 2026.",
        "url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE2658",
        "reason": "Primary dataset accession for external bulk validation",
    },
    {
        "key": "gdc_mmrf_commppass",
        "citation": "National Cancer Institute Genomic Data Commons. Multiple Myeloma Research Foundation CoMMpass Study. https://gdc.cancer.gov/about-gdc/contributed-genomic-data-cancer-research/foundation-medicine/multiple-myeloma-research-foundation-mmrf. Accessed 1 May 2026.",
        "url": "https://gdc.cancer.gov/about-gdc/contributed-genomic-data-cancer-research/foundation-medicine/multiple-myeloma-research-foundation-mmrf",
        "reason": "Primary open CoMMpass/GDC resource citation",
    },
    {
        "key": "cox_1972",
        "citation": "Cox DR. Regression models and life-tables. J R Stat Soc Series B Stat Methodol. 1972;34:187-220.",
        "url": "https://doi.org/10.1111/j.2517-6161.1972.tb00899.x",
        "reason": "Cox proportional hazards model",
    },
    {
        "key": "benjamini_hochberg_1995",
        "citation": "Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J R Stat Soc Series B Stat Methodol. 1995;57:289-300. doi:10.1111/j.2517-6161.1995.tb02031.x.",
        "url": "https://doi.org/10.1111/j.2517-6161.1995.tb02031.x",
        "reason": "Benjamini-Hochberg FDR correction",
    },
    {
        "key": "statsmodels",
        "citation": "Seabold S, Perktold J. Statsmodels: econometric and statistical modeling with Python. Proceedings of the 9th Python in Science Conference. 2010;92-96. https://www.statsmodels.org/. Accessed 1 May 2026.",
        "url": "https://www.statsmodels.org/",
        "reason": "Statsmodels PHReg, logistic, and linear model implementation",
    },
]


def run_curl(url: str, output: Path | None = None) -> str:
    cmd = ["curl.exe", "-4", "-s", "-L", "-A", "Mozilla/5.0", url]
    if output is not None:
        cmd.extend(["-o", str(output)])
    result = subprocess.run(cmd, text=True, capture_output=True, timeout=90)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"curl failed: {url}")
    return result.stdout


def ncbi_json(url: str) -> dict:
    return json.loads(run_curl(url))


def clean_filename(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("_")
    return text[:120]


def author_string(authors: list[dict[str, str]]) -> str:
    names = [a.get("name", "") for a in authors if a.get("name")]
    if not names:
        return ""
    if len(names) > 6:
        return ", ".join(names[:6]) + ", et al"
    return ", ".join(names)


def pubmed_citation(item: dict) -> str:
    authors = author_string(item.get("authors", []))
    title = item.get("title", "").rstrip(".")
    source = item.get("source") or item.get("fulljournalname") or ""
    pubdate = item.get("pubdate", "")
    year = re.search(r"\d{4}", pubdate)
    year_text = year.group(0) if year else pubdate
    volume = item.get("volume", "")
    issue = item.get("issue", "")
    pages = item.get("pages", "")
    doi = ""
    for article_id in item.get("articleids", []):
        if article_id.get("idtype") == "doi":
            doi = article_id.get("value", "")
    vol_issue = volume
    if issue:
        vol_issue += f"({issue})"
    details = f"{source}. {year_text}"
    if vol_issue:
        details += f";{vol_issue}"
    if pages:
        details += f":{pages}"
    details += "."
    if doi:
        details += f" doi:{doi}."
    citation = f"{authors}. {title}. {details}"
    citation = citation.replace("Blad鑼?J", "Blade J")
    citation = citation.replace("BladèŒ… J", "Blade J")
    citation = citation.replace("data sets--update", "data sets - update")
    return citation


def get_pubmed_metadata(pmids: list[str]) -> dict[str, dict]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=" + ",".join(pmids)
    data = ncbi_json(url)
    return {pmid: data["result"][pmid] for pmid in pmids if pmid in data["result"]}


def get_idconv(pmids: list[str]) -> dict[str, dict]:
    url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?format=json&ids=" + ",".join(pmids)
    data = ncbi_json(url)
    return {str(record.get("pmid")): record for record in data.get("records", []) if record.get("pmid")}


def download_pmc_pdf(key: str, pmcid: str) -> tuple[str, int, str]:
    target = PDF_DIR / f"{clean_filename(key)}_{pmcid}.pdf"
    if target.exists() and target.stat().st_size > 1000 and target.read_bytes()[:5] == b"%PDF-":
        return str(target), target.stat().st_size, "exists"
    url = f"https://europepmc.org/articles/{pmcid}?pdf=render"
    try:
        run_curl(url, target)
        header = target.read_bytes()[:5] if target.exists() else b""
        if header != b"%PDF-":
            size = target.stat().st_size if target.exists() else 0
            target.unlink(missing_ok=True)
            return "", size, "pdf_not_available_from_europepmc"
        return str(target), target.stat().st_size, "downloaded"
    except Exception as exc:
        return "", 0, f"failed: {type(exc).__name__}: {exc}"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    META_DIR.mkdir(parents=True, exist_ok=True)

    pmids = [pmid for _, pmid, _ in PMID_REFS]
    metadata = get_pubmed_metadata(pmids)
    idconv = get_idconv(pmids)

    rows = []
    numbered_lines = ["# Formal Reference Draft", "", "Target style: Vancouver / numbered biomedical style.", ""]
    download_rows = []

    number = 1
    for key, pmid, reason in PMID_REFS:
        item = metadata.get(pmid, {})
        conv = idconv.get(pmid, {})
        pmcid = conv.get("pmcid", "")
        doi = conv.get("doi", "")
        citation = pubmed_citation(item) if item else f"PMID {pmid}"
        pdf_path, pdf_bytes, pdf_status = ("", 0, "no_pmcid")
        if pmcid:
            pdf_path, pdf_bytes, pdf_status = download_pmc_pdf(key, pmcid)
        rows.append(
            {
                "number": number,
                "key": key,
                "type": "journal_article",
                "pmid": pmid,
                "pmcid": pmcid,
                "doi": doi,
                "title": item.get("title", ""),
                "journal": item.get("fulljournalname", ""),
                "pubdate": item.get("pubdate", ""),
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "local_pdf": pdf_path,
                "pdf_status": pdf_status,
                "reason": reason,
                "citation": citation,
            }
        )
        download_rows.append(
            {
                "key": key,
                "pmid": pmid,
                "pmcid": pmcid,
                "pdf_path": pdf_path,
                "bytes": pdf_bytes,
                "status": pdf_status,
            }
        )
        numbered_lines.append(f"{number}. {citation}")
        number += 1
        time.sleep(0.25)

    for ref in MANUAL_REFS:
        rows.append(
            {
                "number": number,
                "key": ref["key"],
                "type": "dataset_or_method",
                "pmid": "",
                "pmcid": "",
                "doi": "",
                "title": "",
                "journal": "",
                "pubdate": "",
                "url": ref["url"],
                "local_pdf": "",
                "pdf_status": "not_applicable",
                "reason": ref["reason"],
                "citation": ref["citation"],
            }
        )
        numbered_lines.append(f"{number}. {ref['citation']}")
        number += 1

    pd.DataFrame(rows).to_csv(OUT / "REFERENCE_LIBRARY.tsv", sep="\t", index=False)
    pd.DataFrame(download_rows).to_csv(OUT / "downloaded_pdfs_manifest.tsv", sep="\t", index=False)
    (OUT / "REFERENCES_VANCOUVER_NUMBERED_DRAFT.md").write_text("\n".join(numbered_lines) + "\n", encoding="utf-8")
    (META_DIR / "pubmed_esummary.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (META_DIR / "pmc_idconv.json").write_text(json.dumps(idconv, indent=2), encoding="utf-8")
    print(f"Wrote reference library to: {OUT}")


if __name__ == "__main__":
    main()
