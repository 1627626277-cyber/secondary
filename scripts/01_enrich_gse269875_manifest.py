import argparse
import gzip
import re
from pathlib import Path

import pandas as pd


def first_match(pattern: str, text: str, default: str = "NA") -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def parse_characteristics(block: str) -> dict:
    values = {}
    for raw in re.findall(r"^!Sample_characteristics_ch1 = (.+)$", block, flags=re.MULTILINE):
        if ":" in raw:
            key, value = raw.split(":", 1)
            values[key.strip().lower().replace(" ", "_")] = value.strip()
    return values


def classify(title: str, organism: str, platform: str, tumor: str) -> tuple[str, str, str]:
    include = organism == "Homo sapiens" and platform == "GPL30173"
    if include and title.startswith("hMM"):
        return "Yes", "human_mm_mainline", "pilot_first" if title == "hMM1" else "mainline"
    if include and title.startswith("hHBM"):
        return "Yes", "human_control_mainline", "control"
    if organism == "Mus musculus":
        return "No", "mouse_isolated_supplement", "do_not_mix"
    return "No", "ambiguous_or_excluded", "review_required"


def parse_soft(soft_path: Path) -> pd.DataFrame:
    with gzip.open(soft_path, "rt", encoding="utf-8", errors="replace") as fh:
        text = fh.read()

    sample_blocks = [
        block
        for block in re.split(r"(?=^\^SAMPLE = )", text, flags=re.MULTILINE)
        if block.startswith("^SAMPLE = ")
    ]

    rows = []
    for block in sample_blocks:
        ch = parse_characteristics(block)
        title = first_match(r"^!Sample_title = (.+)$", block)
        organism = first_match(r"^!Sample_organism_ch1 = (.+)$", block)
        platform = first_match(r"^!Sample_platform_id = (.+)$", block)
        tumor = ch.get("tumor", "NA")
        include, role, pilot_status = classify(title, organism, platform, tumor)

        rows.append(
            {
                "GSE": "GSE269875",
                "GSM": first_match(r"^\^SAMPLE = (GSM\d+)$", block),
                "sample_title": title,
                "organism_geo": organism,
                "taxid": first_match(r"^!Sample_taxid_ch1 = (.+)$", block),
                "platform_id": platform,
                "instrument_model": first_match(r"^!Sample_instrument_model = (.+)$", block),
                "tissue": ch.get("tissue", first_match(r"^!Sample_source_name_ch1 = (.+)$", block)),
                "gender": ch.get("gender", "NA"),
                "tumor": tumor,
                "technique": ch.get("technique", "NA"),
                "biological_replicates": ch.get("biological_replicates", "NA"),
                "biosample": first_match(r"^!Sample_relation = BioSample: .*/(SAMN\d+)$", block),
                "srx": first_match(r"^!Sample_relation = SRA: .*term=(SRX\d+)$", block),
                "include_mainline": include,
                "analysis_role": role,
                "pilot_status": pilot_status,
                "species_seq_qc": "pending",
                "seq_qc_method": "pending",
                "notes": "Use sequence-level QC before any human mainline analysis.",
            }
        )

    df = pd.DataFrame(rows)
    return df.sort_values(["include_mainline", "sample_title"], ascending=[False, True])


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an enriched manifest for GSE269875.")
    parser.add_argument(
        "--project",
        default=r"D:\二区",
        help="Project directory containing GSE269875_family.soft.gz.",
    )
    parser.add_argument(
        "--out",
        default="gse269875_manifest_enriched.tsv",
        help="Output TSV path.",
    )
    args = parser.parse_args()

    soft_path = Path(args.project) / "GSE269875_family.soft.gz"
    if not soft_path.exists():
        raise FileNotFoundError(f"Cannot find {soft_path}")

    df = parse_soft(soft_path)
    out_path = Path(args.out)
    df.to_csv(out_path, sep="\t", index=False, encoding="utf-8")

    human = df[df["include_mainline"] == "Yes"]
    print(f"Wrote: {out_path.resolve()}")
    print(f"Human mainline: {len(human)}")
    print(f"Mouse/isolated or excluded: {len(df) - len(human)}")
    print("Recommended first pilot: GSM8329293 / hMM1 / SRX24927515")


if __name__ == "__main__":
    main()
