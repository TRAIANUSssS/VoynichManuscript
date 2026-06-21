"""Baseline text statistics for exp-001.

This script parses one IVTFF interlinear transcription file and analyzes a
single transcriber code by default. It is intentionally conservative: it keeps
the raw input untouched and records the parsing choices in run_summary.json.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt


LINE_RE = re.compile(r"^<(?P<locator>[^>;]+;(?P<code>[A-Z]))>\s*(?P<text>.*)$")
COMMENT_RE = re.compile(r"\{[^}]*\}")
TOKEN_SPLIT_RE = re.compile(r"[.,\s]+")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_token(raw_token: str) -> str:
    """Return a baseline EVA token with uncertain/editorial marks removed."""
    return re.sub(r"[^A-Za-z]", "", raw_token).lower()


def parse_ivtff(path: Path, transcriber_code: str) -> tuple[list[str], dict[str, int]]:
    tokens: list[str] = []
    stats = Counter()

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            stats["input_lines"] += 1
            match = LINE_RE.match(line)
            if not match:
                continue

            stats["data_lines"] += 1
            if match.group("code") != transcriber_code:
                continue

            stats["selected_lines"] += 1
            text = COMMENT_RE.sub("", match.group("text"))
            for raw_token in TOKEN_SPLIT_RE.split(text):
                token = normalize_token(raw_token)
                if token:
                    tokens.append(token)
                elif raw_token:
                    stats["discarded_empty_tokens"] += 1

    return tokens, dict(stats)


def entropy(counter: Counter[str]) -> float:
    total = sum(counter.values())
    if total == 0:
        return 0.0
    return -sum((count / total) * math.log2(count / total) for count in counter.values())


def write_counter_csv(path: Path, field_name: str, counter: Counter[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([field_name, "count", "proportion"])
        total = sum(counter.values())
        for item, count in counter.most_common():
            writer.writerow([item, count, count / total if total else 0])


def write_top_csv(path: Path, field_name: str, items: list[tuple[str, int]], total: int) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([field_name, "count", "proportion"])
        for item, count in items:
            writer.writerow([item, count, count / total if total else 0])


def write_length_csv(path: Path, counter: Counter[int]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["word_length", "count", "proportion"])
        total = sum(counter.values())
        for length in sorted(counter):
            count = counter[length]
            writer.writerow([length, count, count / total if total else 0])


def bar_chart(path: Path, title: str, xlabel: str, ylabel: str, labels: list[str], counts: list[int]) -> None:
    fig_width = max(8, min(14, len(labels) * 0.45))
    plt.figure(figsize=(fig_width, 5))
    plt.bar(labels, counts, color="#3f6f8f")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def length_chart(path: Path, counter: Counter[int]) -> None:
    lengths = sorted(counter)
    counts = [counter[length] for length in lengths]
    plt.figure(figsize=(9, 5))
    plt.bar([str(length) for length in lengths], counts, color="#5f7f45")
    plt.title("Word Length Distribution")
    plt.xlabel("Normalized token length")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run exp-001 baseline Voynich transcription statistics.")
    parser.add_argument("--input", required=True, type=Path, help="Raw IVTFF transcription file.")
    parser.add_argument("--output", required=True, type=Path, help="Output artifact directory.")
    parser.add_argument("--transcriber-code", default="H", help="IVTFF transcriber code to analyze.")
    args = parser.parse_args()

    input_path = args.input
    output_dir = args.output
    output_dir.mkdir(parents=True, exist_ok=True)

    tokens, parse_stats = parse_ivtff(input_path, args.transcriber_code)
    token_counter = Counter(tokens)
    glyph_counter = Counter("".join(tokens))
    length_counter = Counter(len(token) for token in tokens)

    write_counter_csv(output_dir / "token_frequencies.csv", "token", token_counter)
    write_counter_csv(output_dir / "glyph_frequencies.csv", "glyph", glyph_counter)
    write_length_csv(output_dir / "word_length_distribution.csv", length_counter)
    top_tokens = token_counter.most_common(20)
    top_glyphs = glyph_counter.most_common(20)
    write_top_csv(output_dir / "top_tokens.csv", "token", top_tokens, sum(token_counter.values()))
    write_top_csv(output_dir / "top_glyphs.csv", "glyph", top_glyphs, sum(glyph_counter.values()))
    bar_chart(
        output_dir / "top_tokens.png",
        "Top 20 Normalized Tokens",
        "Token",
        "Count",
        [item for item, _ in top_tokens],
        [count for _, count in top_tokens],
    )
    bar_chart(
        output_dir / "glyph_frequencies.png",
        "Top 20 EVA Character Frequencies",
        "EVA character",
        "Count",
        [item for item, _ in top_glyphs],
        [count for _, count in top_glyphs],
    )
    length_chart(output_dir / "word_length_distribution.png", length_counter)

    run_summary = {
        "experiment": "exp-001_baseline-statistics",
        "run_date_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "script": "scripts/exp001_baseline_stats.py",
        "input": str(input_path.as_posix()),
        "input_sha256": file_sha256(input_path),
        "output": str(output_dir.as_posix()),
        "parameters": {
            "transcriber_code": args.transcriber_code,
            "token_separators": "period, comma, whitespace",
            "normalization": "lowercase; remove non-ASCII-letter uncertain/editorial marks",
            "glyph_counting": "single EVA transcription characters after token normalization",
        },
        "parse_stats": parse_stats,
        "metrics": {
            "token_count": len(tokens),
            "unique_token_count": len(token_counter),
            "type_token_ratio": len(token_counter) / len(tokens) if tokens else 0,
            "glyph_count": sum(glyph_counter.values()),
            "unique_glyph_count": len(glyph_counter),
            "glyph_entropy_bits": entropy(glyph_counter),
            "token_entropy_bits": entropy(token_counter),
            "mean_token_length": (
                sum(length * count for length, count in length_counter.items()) / len(tokens) if tokens else 0
            ),
        },
        "artifacts": [
            "token_frequencies.csv",
            "glyph_frequencies.csv",
            "word_length_distribution.csv",
            "top_tokens.csv",
            "top_glyphs.csv",
            "run_summary.json",
            "word_length_distribution.png",
            "top_tokens.png",
            "glyph_frequencies.png",
        ],
        "limitations": [
            "This run uses one IVTFF transcriber code only.",
            "EVA digraphs such as ch and sh are counted as separate characters in this baseline.",
            "Uncertain and editorial marks are stripped for counting rather than modeled.",
            "No comparison corpus, folio metadata, section metadata, or Currier-language split is used.",
        ],
    }

    with (output_dir / "run_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(run_summary, handle, indent=2)
        handle.write("\n")

    print(json.dumps(run_summary["metrics"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
