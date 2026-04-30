import argparse
from pathlib import Path


def sample_fastq(in_path: Path, out_path: Path, read_pairs: int) -> None:
    lines_needed = read_pairs * 4
    with open(in_path, "rb") as src, open(out_path, "wb") as dst:
        for i, line in enumerate(src):
            if i >= lines_needed:
                break
            dst.write(line)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sample paired FASTQ files by read-pair count.")
    parser.add_argument("--r1", required=True)
    parser.add_argument("--r2", required=True)
    parser.add_argument("--out-r1", required=True)
    parser.add_argument("--out-r2", required=True)
    parser.add_argument("--read-pairs", type=int, default=1_000_000)
    args = parser.parse_args()

    r1 = Path(args.r1)
    r2 = Path(args.r2)
    out_r1 = Path(args.out_r1)
    out_r2 = Path(args.out_r2)
    out_r1.parent.mkdir(parents=True, exist_ok=True)
    out_r2.parent.mkdir(parents=True, exist_ok=True)

    sample_fastq(r1, out_r1, args.read_pairs)
    sample_fastq(r2, out_r2, args.read_pairs)
    print(f"Wrote sampled FASTQ: {out_r1}")
    print(f"Wrote sampled FASTQ: {out_r2}")


if __name__ == "__main__":
    main()
