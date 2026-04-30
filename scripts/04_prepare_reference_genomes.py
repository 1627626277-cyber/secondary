import gzip
import os
import shutil
import subprocess
import sys
from pathlib import Path

import requests

PROJECT = Path(r"D:\二区")
REFS = {
    "hg38": "https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz",
    "mm10": "https://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/mm10.fa.gz",
}


def download(url: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".part")
    headers = {}
    mode = "wb"
    existing = tmp.stat().st_size if tmp.exists() else 0
    if existing:
        headers["Range"] = f"bytes={existing}-"
        mode = "ab"
        print(f"Resuming {out.name} from {existing:,} bytes")
    else:
        print(f"Downloading {out.name}")

    with requests.get(url, stream=True, timeout=120, headers=headers) as r:
        if r.status_code not in (200, 206):
            raise RuntimeError(f"Download failed: HTTP {r.status_code} for {url}")
        total = r.headers.get("Content-Length")
        total = int(total) + existing if total and mode == "ab" else int(total) if total else None
        done = existing
        with open(tmp, mode) as fh:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue
                fh.write(chunk)
                done += len(chunk)
                if total:
                    pct = done * 100 / total
                    print(f"  {out.name}: {done/1e9:.2f}/{total/1e9:.2f} GB ({pct:.1f}%)", end="\r")
        print()
    tmp.replace(out)
    print(f"Saved {out}")


def decompress(gz_path: Path, fa_path: Path) -> None:
    if fa_path.exists() and fa_path.stat().st_size > 0:
        print(f"Exists: {fa_path}")
        return
    print(f"Decompressing {gz_path.name} -> {fa_path.name}")
    with gzip.open(gz_path, "rb") as src, open(fa_path, "wb") as dst:
        shutil.copyfileobj(src, dst, length=1024 * 1024 * 8)
    print(f"Saved {fa_path}")


def find_makeblastdb() -> Path:
    candidates = [
        PROJECT / "tools" / "ncbi-magicblast-1.7.2" / "bin" / "makeblastdb.exe",
        Path("makeblastdb.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return Path("makeblastdb")


def build_db(name: str, fa_path: Path) -> None:
    db_dir = PROJECT / "blastdb"
    db_dir.mkdir(exist_ok=True)
    out_prefix = db_dir / name
    marker = Path(str(out_prefix) + ".nsq")
    if marker.exists():
        print(f"BLAST DB exists: {out_prefix}")
        return
    makeblastdb = find_makeblastdb()
    print(f"Building BLAST DB for {name}")
    subprocess.run([
        str(makeblastdb),
        "-in", str(fa_path),
        "-dbtype", "nucl",
        "-parse_seqids",
        "-blastdb_version", "4",
        "-out", str(out_prefix),
        "-title", name,
    ], check=True)


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    ref_dir = PROJECT / "references"
    ref_dir.mkdir(exist_ok=True)

    for name, url in REFS.items():
        gz_path = ref_dir / f"{name}.fa.gz"
        fa_path = PROJECT / f"{name}.fa"
        if mode in ("all", "download") and not gz_path.exists():
            download(url, gz_path)
        if mode in ("all", "decompress"):
            if not gz_path.exists():
                raise FileNotFoundError(gz_path)
            decompress(gz_path, fa_path)
        if mode in ("all", "builddb"):
            if not fa_path.exists():
                raise FileNotFoundError(fa_path)
            build_db(name, fa_path)

    print("Reference preparation complete.")


if __name__ == "__main__":
    main()

