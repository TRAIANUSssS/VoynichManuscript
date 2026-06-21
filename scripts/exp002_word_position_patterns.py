"""Word position pattern analysis for exp-002.

This script uses the same baseline IVTFF token normalization assumptions as
exp-001, then compares token distributions by position inside selected lines.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt


LINE_RE = re.compile(r"^<(?P<locator>[^>;]+;(?P<code>[A-Z]))>\s*(?P<text>.*)$")
COMMENT_RE = re.compile(r"\{[^}]*\}")
TOKEN_SPLIT_RE = re.compile(r"[.,\s]+")
POSITION_CLASSES = ("line_initial", "line_medial", "line_final", "single_token_line")
PAIRWISE_COMPARISONS = (
    ("line_initial", "line_medial"),
    ("line_final", "line_medial"),
    ("line_initial", "line_final"),
)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_token(raw_token: str) -> str:
    return re.sub(r"[^A-Za-z]", "", raw_token).lower()


def tokenize_line(text: str) -> list[str]:
    text = COMMENT_RE.sub("", text)
    return [token for raw in TOKEN_SPLIT_RE.split(text) if (token := normalize_token(raw))]


def iter_selected_lines(path: Path, transcriber_code: str):
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
            tokens = tokenize_line(match.group("text"))
            if tokens:
                stats["non_empty_selected_lines"] += 1
                yield match.group("locator"), tokens, stats
            else:
                stats["empty_selected_lines"] += 1
    yield None, None, stats


def classify_positions(tokens: list[str]) -> list[tuple[str, str]]:
    if len(tokens) == 1:
        return [(tokens[0], "single_token_line")]

    classified = [(tokens[0], "line_initial")]
    classified.extend((token, "line_medial") for token in tokens[1:-1])
    classified.append((tokens[-1], "line_final"))
    return classified


def distribution(counter: Counter[str], vocabulary: set[str]) -> list[float]:
    total = sum(counter.values())
    if total == 0:
        return [0.0 for _ in vocabulary]
    return [counter[token] / total for token in vocabulary]


def kl_divergence(p_dist: list[float], q_dist: list[float]) -> float:
    return sum(p * math.log2(p / q) for p, q in zip(p_dist, q_dist) if p > 0 and q > 0)


def jensen_shannon_divergence(counter_a: Counter[str], counter_b: Counter[str]) -> float:
    vocabulary = set(counter_a) | set(counter_b)
    p_dist = distribution(counter_a, vocabulary)
    q_dist = distribution(counter_b, vocabulary)
    midpoint = [(p + q) / 2 for p, q in zip(p_dist, q_dist)]
    return 0.5 * kl_divergence(p_dist, midpoint) + 0.5 * kl_divergence(q_dist, midpoint)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_top_tokens(path: Path, counter: Counter[str], top_n: int) -> None:
    total = sum(counter.values())
    rows = [
        {"token": token, "count": count, "share": count / total if total else 0}
        for token, count in counter.most_common(top_n)
    ]
    write_csv(path, rows, ["token", "count", "share"])


def bar_chart(path: Path, title: str, labels: list[str], counts: list[int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig_width = max(8, min(14, len(labels) * 0.45))
    plt.figure(figsize=(fig_width, 5))
    plt.bar(labels, counts, color="#4f6f8f")
    plt.title(title)
    plt.xlabel("Token")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def grouped_position_chart(path: Path, counters: dict[str, Counter[str]], tokens: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    x_positions = list(range(len(tokens)))
    width = 0.25
    plt.figure(figsize=(12, 6))
    for offset, position_class in enumerate(("line_initial", "line_medial", "line_final")):
        total = sum(counters[position_class].values())
        shares = [counters[position_class][token] / total if total else 0 for token in tokens]
        shifted = [x + (offset - 1) * width for x in x_positions]
        plt.bar(shifted, shares, width=width, label=position_class)
    plt.xticks(x_positions, tokens, rotation=45, ha="right")
    plt.ylabel("Share within position class")
    plt.title("Position Distribution Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run exp-002 word position pattern analysis.")
    parser.add_argument("--input", required=True, type=Path, help="Raw IVTFF transcription file.")
    parser.add_argument("--output", required=True, type=Path, help="Output artifact directory.")
    parser.add_argument("--transcriber-code", default="H", help="IVTFF transcriber code to analyze.")
    parser.add_argument("--min-count", type=int, default=10, help="Minimum token count for overrepresentation ranking.")
    parser.add_argument("--top-n", type=int, default=30, help="Number of top tokens to export per position class.")
    args = parser.parse_args()

    output_dir = args.output
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "plots").mkdir(parents=True, exist_ok=True)

    position_counters: dict[str, Counter[str]] = {position: Counter() for position in POSITION_CLASSES}
    overall_counter: Counter[str] = Counter()
    line_stats = Counter()
    parse_stats: dict[str, int] = {}

    for _locator, tokens, stats in iter_selected_lines(args.input, args.transcriber_code):
        if tokens is None:
            parse_stats = dict(stats)
            break

        line_stats["total_normalized_tokens"] += len(tokens)
        if len(tokens) == 1:
            line_stats["single_token_lines"] += 1
        else:
            line_stats["multi_token_lines"] += 1

        for token, position_class in classify_positions(tokens):
            overall_counter[token] += 1
            position_counters[position_class][token] += 1

    overall_total = sum(overall_counter.values())
    position_summary_rows = []
    for position_class in POSITION_CLASSES:
        position_total = sum(position_counters[position_class].values())
        position_summary_rows.append(
            {
                "position_class": position_class,
                "token_count": position_total,
                "token_share": position_total / overall_total if overall_total else 0,
                "unique_token_count": len(position_counters[position_class]),
            }
        )
    write_csv(
        output_dir / "position_summary.csv",
        position_summary_rows,
        ["position_class", "token_count", "token_share", "unique_token_count"],
    )

    count_rows = []
    share_rows = []
    overrepresentation_rows = []
    position_totals = {position: sum(counter.values()) for position, counter in position_counters.items()}
    tokens_sorted = sorted(overall_counter)

    for token in tokens_sorted:
        overall_count = overall_counter[token]
        overall_share = overall_count / overall_total if overall_total else 0
        count_row = {"token": token, "overall_count": overall_count}
        share_row = {"token": token, "overall_share": overall_share}
        for position_class in POSITION_CLASSES:
            position_count = position_counters[position_class][token]
            position_share = position_count / position_totals[position_class] if position_totals[position_class] else 0
            count_row[f"{position_class}_count"] = position_count
            share_row[f"{position_class}_share"] = position_share
            if position_count >= args.min_count and overall_share > 0:
                overrepresentation_rows.append(
                    {
                        "token": token,
                        "position_class": position_class,
                        "position_count": position_count,
                        "overall_count": overall_count,
                        "position_share": position_share,
                        "overall_share": overall_share,
                        "overrepresentation_ratio": position_share / overall_share,
                    }
                )
        count_rows.append(count_row)
        share_rows.append(share_row)

    write_csv(
        output_dir / "token_position_counts.csv",
        count_rows,
        [
            "token",
            "overall_count",
            "line_initial_count",
            "line_medial_count",
            "line_final_count",
            "single_token_line_count",
        ],
    )
    write_csv(
        output_dir / "token_position_shares.csv",
        share_rows,
        [
            "token",
            "overall_share",
            "line_initial_share",
            "line_medial_share",
            "line_final_share",
            "single_token_line_share",
        ],
    )

    overrepresentation_rows.sort(
        key=lambda row: (str(row["position_class"]), -float(row["overrepresentation_ratio"]), -int(row["position_count"]))
    )
    write_csv(
        output_dir / "token_position_overrepresentation.csv",
        overrepresentation_rows,
        [
            "token",
            "position_class",
            "position_count",
            "overall_count",
            "position_share",
            "overall_share",
            "overrepresentation_ratio",
        ],
    )

    write_top_tokens(output_dir / "top_initial_tokens.csv", position_counters["line_initial"], args.top_n)
    write_top_tokens(output_dir / "top_medial_tokens.csv", position_counters["line_medial"], args.top_n)
    write_top_tokens(output_dir / "top_final_tokens.csv", position_counters["line_final"], args.top_n)

    distances = {
        f"{left}_vs_{right}": {
            "jensen_shannon_divergence_bits": jensen_shannon_divergence(position_counters[left], position_counters[right])
        }
        for left, right in PAIRWISE_COMPARISONS
    }
    with (output_dir / "distribution_distances.json").open("w", encoding="utf-8") as handle:
        json.dump(distances, handle, indent=2)
        handle.write("\n")

    summary = {
        "experiment": "exp-002_word-position-patterns",
        "run_date_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "script": "scripts/exp002_word_position_patterns.py",
        "input": str(args.input.as_posix()),
        "input_sha256": file_sha256(args.input),
        "output": str(output_dir.as_posix()),
        "parameters": {
            "transcriber_code": args.transcriber_code,
            "min_count": args.min_count,
            "top_n": args.top_n,
            "token_separators": "period, comma, whitespace",
            "normalization": "lowercase; remove non-ASCII-letter uncertain/editorial marks",
            "position_classes": list(POSITION_CLASSES),
            "distance_metric": "Jensen-Shannon divergence in bits",
        },
        "parse_stats": parse_stats,
        "line_stats": dict(line_stats),
        "position_summary": position_summary_rows,
        "distribution_distances": distances,
        "artifacts": [
            "position_summary.json",
            "position_summary.csv",
            "token_position_counts.csv",
            "token_position_shares.csv",
            "token_position_overrepresentation.csv",
            "top_initial_tokens.csv",
            "top_medial_tokens.csv",
            "top_final_tokens.csv",
            "distribution_distances.json",
            "plots/top_initial_tokens.png",
            "plots/top_final_tokens.png",
            "plots/position_distribution_comparison.png",
        ],
        "limitations": [
            "Uses the same baseline token normalization as exp-001.",
            "Analyzes position inside transcription lines, not manuscript layout geometry.",
            "Does not use folio, section, scribe/hand, Currier-language, or control-corpus metadata.",
            "Jensen-Shannon divergence measures distribution distance but does not identify a cause.",
            "Overrepresentation rankings use a count threshold and are descriptive.",
        ],
    }
    with (output_dir / "position_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")

    top_initial = position_counters["line_initial"].most_common(args.top_n)
    top_final = position_counters["line_final"].most_common(args.top_n)
    bar_chart(
        output_dir / "plots" / "top_initial_tokens.png",
        "Top Line-Initial Tokens",
        [token for token, _ in top_initial],
        [count for _, count in top_initial],
    )
    bar_chart(
        output_dir / "plots" / "top_final_tokens.png",
        "Top Line-Final Tokens",
        [token for token, _ in top_final],
        [count for _, count in top_final],
    )
    comparison_tokens = [token for token, _ in overall_counter.most_common(15)]
    grouped_position_chart(output_dir / "plots" / "position_distribution_comparison.png", position_counters, comparison_tokens)

    print(json.dumps({"line_stats": dict(line_stats), "distribution_distances": distances}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
