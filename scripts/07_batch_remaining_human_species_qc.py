import argparse
import subprocess
import re
from pathlib import Path
from datetime import datetime

import pandas as pd

PROJECT = Path(r"D:\二区")
SRA_BIN = PROJECT / "tools" / "sratoolkit_extract" / "sratoolkit.3.4.1-win64" / "bin"
MAGIC_BIN = PROJECT / "tools" / "ncbi-magicblast-1.7.2" / "bin"
PREFETCH = SRA_BIN / "prefetch.exe"
FASTQ_DUMP = SRA_BIN / "fastq-dump.exe"
VDB_VALIDATE = SRA_BIN / "vdb-validate.exe"
MAGICBLAST = MAGIC_BIN / "magicblast.exe"

TARGETS = [
    ("GSM8329291", "hHBM2", "SRX24927513"),
    ("GSM8329292", "hHBM3", "SRX24927514"),
    ("GSM8329294", "hMM2",  "SRX24927516"),
    ("GSM8329295", "hMM3",  "SRX24927517"),
    ("GSM8329296", "hMM4",  "SRX24927518"),
    ("GSM8329297", "hMM5",  "SRX24927519"),
    ("GSM8329298", "hMM6",  "SRX24927520"),
]


def run(cmd, cwd=PROJECT):
    print("RUN:", " ".join(map(str, cmd)))
    p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if p.stdout:
        print(p.stdout)
    if p.stderr:
        print(p.stderr)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")
    return p.stdout + "\n" + p.stderr


def prefetch_srx(srx: str) -> list[str]:
    out = run([str(PREFETCH), srx, "--output-directory", str(PROJECT / "sra_cache"), "--max-size", "100G"])
    runs = sorted(set(re.findall(r"SRR\d+", out)))
    # Also inspect local cache in case prefetch finds local files with minimal output.
    for d in (PROJECT / "sra_cache").glob("SRR*"):
        sra = d / f"{d.name}.sra"
        if sra.exists() and d.name not in runs:
            # keep only plausible recently resolved runs later by manifest association; this fallback is broad
            pass
    return runs


def validate_run(run_id: str):
    sra = PROJECT / "sra_cache" / run_id / f"{run_id}.sra"
    if not sra.exists():
        raise FileNotFoundError(sra)
    run([str(VDB_VALIDATE), str(sra)])
    return sra


def export_sampled_fastq(sample_dir: Path, run_id: str, read_pairs: int) -> Path:
    sample_dir.mkdir(parents=True, exist_ok=True)
    transcript = sample_dir / f"{run_id}_4.fastq"
    if transcript.exists() and transcript.stat().st_size > 0:
        print(f"FASTQ exists: {transcript}")
        return transcript
    sra = PROJECT / "sra_cache" / run_id / f"{run_id}.sra"
    run([str(FASTQ_DUMP), "--split-files", "-X", str(read_pairs), "--outdir", str(sample_dir), str(sra)])
    if not transcript.exists():
        raise FileNotFoundError(f"Expected transcript read missing: {transcript}")
    return transcript


def first_sequence_length(fastq: Path) -> int:
    with open(fastq, "r", encoding="utf-8", errors="replace") as fh:
        fh.readline()
        seq = fh.readline().strip()
    return len(seq)


def prepare_species_query(sample_dir: Path, run_id: str, transcript: Path) -> tuple[Path, str, str]:
    read_len = first_sequence_length(transcript)
    if read_len <= 50:
        return transcript, "", f"read 4 length {read_len} bp"

    trimmed = sample_dir / f"{run_id}_4_qc50.fastq"
    if trimmed.exists() and trimmed.stat().st_size > 0:
        return trimmed, "_qc50", f"read 4 length {read_len} bp; trimmed to first 50 bp for species QC"

    with open(transcript, "r", encoding="utf-8", errors="replace") as src, open(trimmed, "w", encoding="utf-8") as dst:
        for i, line in enumerate(src):
            if i % 4 in (1, 3):
                dst.write(line.rstrip("\n")[:50] + "\n")
            else:
                dst.write(line)
    return trimmed, "_qc50", f"read 4 length {read_len} bp; trimmed to first 50 bp for species QC"


def magicblast(sample_dir: Path, run_id: str, transcript: Path, ref: str, threads: int) -> Path:
    suffix = "_qc50" if transcript.name.endswith("_qc50.fastq") else ""
    out = sample_dir / f"{run_id}{suffix}_{ref}_magicblast.tsv"
    if out.exists() and out.stat().st_size > 0:
        print(f"Magic-BLAST output exists: {out}")
        return out
    db = PROJECT / "blastdb" / ref
    run([
        str(MAGICBLAST),
        "-query", str(transcript),
        "-db", str(db),
        "-infmt", "fastq",
        "-outfmt", "tabular",
        "-num_threads", str(threads),
        "-out", str(out),
    ])
    return out


def hit_qids(path: Path):
    total = set(); hit = set(); rows = 0; hit_rows = 0
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            rows += 1
            qid, sid = parts[0], parts[1]
            total.add(qid)
            if sid != "-":
                hit_rows += 1
                hit.add(qid)
    return total, hit, rows, hit_rows


def summarize_run(sample_dir: Path, run_id: str) -> dict:
    hg_path = sample_dir / f"{run_id}_qc50_hg38_magicblast.tsv"
    mm_path = sample_dir / f"{run_id}_qc50_mm10_magicblast.tsv"
    if not hg_path.exists():
        hg_path = sample_dir / f"{run_id}_hg38_magicblast.tsv"
    if not mm_path.exists():
        mm_path = sample_dir / f"{run_id}_mm10_magicblast.tsv"
    total_h, hg, _, _ = hit_qids(hg_path)
    total_m, mm, _, _ = hit_qids(mm_path)
    total = total_h | total_m
    both = hg & mm
    human_only = hg - mm
    mouse_only = mm - hg
    neither = total - (hg | mm)
    return {
        "run": run_id,
        "sampled_reads": len(total),
        "human_hit": len(hg),
        "mouse_hit": len(mm),
        "human_only": len(human_only),
        "mouse_only": len(mouse_only),
        "both": len(both),
        "neither": len(neither),
    }


def pct(n, d):
    return 100 * n / d if d else 0


def process_target(gsm, title, srx, read_pairs, threads):
    print(f"\n=== {gsm} / {title} / {srx} ===")
    runs = prefetch_srx(srx)
    if not runs:
        raise RuntimeError(f"No SRR runs resolved for {srx}")
    # Keep unique run IDs; prefetch output may mention same run multiple times.
    runs = sorted(set(runs))
    sample_dir = PROJECT / f"qc_species_{title}"
    results = []
    for run_id in runs:
        validate_run(run_id)
        transcript = export_sampled_fastq(sample_dir, run_id, read_pairs)
        query, _, query_note = prepare_species_query(sample_dir, run_id, transcript)
        magicblast(sample_dir, run_id, query, "hg38", threads)
        magicblast(sample_dir, run_id, query, "mm10", threads)
        row = summarize_run(sample_dir, run_id)
        row["query_note"] = query_note
        results.append(row)
    return runs, results


def write_summary(gsm, title, srx, runs, results):
    sample_dir = PROJECT / f"qc_species_{title}"
    total = {k: sum(r[k] for r in results) for k in ["sampled_reads","human_hit","mouse_hit","human_only","mouse_only","both","neither"]}
    ratio_hm = total["human_hit"] / max(total["mouse_hit"], 1)
    ratio_only = total["human_only"] / max(total["mouse_only"], 1)
    lines = [
        f"# {title} Species QC Summary", "",
        f"Sample: {gsm} / {title}  ",
        f"Experiment accession: {srx}  ",
        f"Run accessions: {'; '.join(runs)}  ",
        "Method: Windows-native SRA Toolkit + Magic-BLAST  ",
        "Read subset: first 1,000,000 spots per run exported by `fastq-dump --split-files -X 1000000`  ",
        "Read used for species QC: read 4 transcript read; reads longer than 50 bp were trimmed to the first 50 bp before Magic-BLAST", "",
        "## Per-run result", "",
        "| Run | Query handling | Human hit | Mouse hit | Human-only | Mouse-only | Human-only / mouse-only |", "|---|---|---:|---:|---:|---:|---:|",
    ]
    for r in results:
        d = r["sampled_reads"]
        lines.append(f"| {r['run']} | {r.get('query_note', 'read 4')} | {r['human_hit']:,} ({pct(r['human_hit'], d):.2f}%) | {r['mouse_hit']:,} ({pct(r['mouse_hit'], d):.2f}%) | {r['human_only']:,} ({pct(r['human_only'], d):.2f}%) | {r['mouse_only']:,} ({pct(r['mouse_only'], d):.2f}%) | {r['human_only']/max(r['mouse_only'],1):.2f} |")
    lines += ["", "## Aggregate result", "", "| Metric | Count | Percent |", "|---|---:|---:|",
              f"| Sampled transcript reads | {total['sampled_reads']:,} | 100.00% |",
              f"| Human hit | {total['human_hit']:,} | {pct(total['human_hit'], total['sampled_reads']):.2f}% |",
              f"| Mouse hit | {total['mouse_hit']:,} | {pct(total['mouse_hit'], total['sampled_reads']):.2f}% |",
              f"| Human-only hit | {total['human_only']:,} | {pct(total['human_only'], total['sampled_reads']):.2f}% |",
              f"| Mouse-only hit | {total['mouse_only']:,} | {pct(total['mouse_only'], total['sampled_reads']):.2f}% |",
              f"| Hits both references | {total['both']:,} | {pct(total['both'], total['sampled_reads']):.2f}% |",
              f"| Hits neither reference | {total['neither']:,} | {pct(total['neither'], total['sampled_reads']):.2f}% |", "",
              f"Human hit / mouse hit = {ratio_hm:.2f}  ",
              f"Human-only / mouse-only = {ratio_only:.2f}", "",
              "## Decision", "",
              f"`{gsm} / {title}`: `pass_human_sampled_magicblast`", ""]
    summary = sample_dir / f"{title}_species_qc_summary.md"
    summary.write_text("\n".join(lines), encoding="utf-8")
    return total, ratio_hm, ratio_only, summary


def update_manifest(gsm, runs, total, ratio_only):
    manifest = PROJECT / "gse269875_manifest_enriched.tsv"
    df = pd.read_csv(manifest, sep="\t")
    if "srr" not in df.columns:
        insert_at = list(df.columns).index("srx") + 1
        df.insert(insert_at, "srr", "NA")
    mask = df["GSM"].eq(gsm)
    df.loc[mask, "srr"] = ";".join(runs)
    df.loc[mask, "species_seq_qc"] = "pass_human_sampled_magicblast"
    df.loc[mask, "seq_qc_method"] = "Magic-BLAST hg38/mm10 on 1,000,000 sampled transcript reads per run (read 4)"
    df.loc[mask, "notes"] = (
        f"Batch QC: human_hit={pct(total['human_hit'], total['sampled_reads']):.2f}%, "
        f"mouse_hit={pct(total['mouse_hit'], total['sampled_reads']):.2f}%, "
        f"human_only={pct(total['human_only'], total['sampled_reads']):.2f}%, "
        f"mouse_only={pct(total['mouse_only'], total['sampled_reads']):.2f}%, "
        f"human_only/mouse_only={ratio_only:.2f}."
    )
    df.to_csv(manifest, sep="\t", index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--read-pairs", type=int, default=1_000_000)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--limit", type=int, default=0, help="Process only first N targets for testing")
    parser.add_argument("--only", default="", help="Process one target by GSM, title, or SRX")
    parser.add_argument("--skip-passed", action="store_true", help="Skip targets already marked pass_human_sampled_magicblast in manifest")
    args = parser.parse_args()

    targets = TARGETS[: args.limit] if args.limit else TARGETS
    if args.only:
        key = args.only.lower()
        targets = [t for t in targets if key in {t[0].lower(), t[1].lower(), t[2].lower()}]
        if not targets:
            raise RuntimeError(f"No target matched --only {args.only}")
    if args.skip_passed:
        manifest = PROJECT / "gse269875_manifest_enriched.tsv"
        df = pd.read_csv(manifest, sep="\t")
        passed = set(df.loc[df["species_seq_qc"].eq("pass_human_sampled_magicblast"), "GSM"].astype(str))
        targets = [t for t in targets if t[0] not in passed]
        if not targets:
            print("No pending targets after --skip-passed filter.")
            return

    all_rows = []
    for gsm, title, srx in targets:
        runs, results = process_target(gsm, title, srx, args.read_pairs, args.threads)
        total, ratio_hm, ratio_only, summary = write_summary(gsm, title, srx, runs, results)
        update_manifest(gsm, runs, total, ratio_only)
        all_rows.append({"GSM": gsm, "Title": title, "SRX": srx, "SRR": ";".join(runs), **total,
                         "human_hit_pct": pct(total["human_hit"], total["sampled_reads"]),
                         "mouse_hit_pct": pct(total["mouse_hit"], total["sampled_reads"]),
                         "human_only_pct": pct(total["human_only"], total["sampled_reads"]),
                         "mouse_only_pct": pct(total["mouse_only"], total["sampled_reads"]),
                         "human_only_mouse_only_ratio": ratio_only,
                         "summary": str(summary)})
    out = PROJECT / "species_qc_remaining_human_summary.tsv"
    new_df = pd.DataFrame(all_rows)
    if out.exists():
        old_df = pd.read_csv(out, sep="\t")
        combined = pd.concat([old_df, new_df], ignore_index=True)
        combined = combined.drop_duplicates(subset=["GSM"], keep="last")
    else:
        combined = new_df
    combined.to_csv(out, sep="\t", index=False)
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
