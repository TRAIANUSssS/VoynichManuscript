"""Clean IVTFF parser rerun for exp-002b.

This experiment audits inline IVTFF angle-tag markup and reruns the exp-001
baseline statistics and exp-002 line-position statistics with a parser that
keeps such markup out of normalized manuscript tokens.
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
ANGLE_TAG_RE = re.compile(r"<[^>]*>")
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


def entropy(counter: Counter[str]) -> float:
    total = sum(counter.values())
    if total == 0:
        return 0.0
    return -sum((count / total) * math.log2(count / total) for count in counter.values())


def normalize_token(raw_token: str) -> str:
    return re.sub(r"[^A-Za-z]", "", raw_token).lower()


def clean_text(text: str, stats: Counter[str], examples: list[dict[str, str]], locator: str) -> str:
    without_comments = COMMENT_RE.sub("", text)
    tags = ANGLE_TAG_RE.findall(without_comments)
    if tags:
        stats["lines_with_angle_tags"] += 1
        stats["angle_tags_removed"] += len(tags)
        for tag in tags:
            stats[f"angle_tag::{tag}"] += 1
        if len(examples) < 50:
            examples.append({"locator": locator, "raw_text": without_comments.strip(), "tags": " ".join(tags)})
    return ANGLE_TAG_RE.sub(".", without_comments)


def tokenize_clean_line(text: str, stats: Counter[str], examples: list[dict[str, str]], locator: str) -> list[str]:
    cleaned = clean_text(text, stats, examples, locator)
    tokens: list[str] = []
    for raw_token in TOKEN_SPLIT_RE.split(cleaned):
        token = normalize_token(raw_token)
        if token:
            tokens.append(token)
        elif raw_token:
            stats["discarded_empty_tokens"] += 1
    return tokens


def parse_selected_lines(path: Path, transcriber_code: str) -> tuple[list[tuple[str, list[str]]], dict[str, int], list[dict[str, str]]]:
    stats: Counter[str] = Counter()
    examples: list[dict[str, str]] = []
    selected_lines: list[tuple[str, list[str]]] = []

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            stats["input_lines"] += 1
            match = LINE_RE.match(line)
            if not match:
                continue
            stats["data_lines"] += 1
            if match.group("code") != transcriber_code:
                continue

            locator = match.group("locator")
            stats["selected_lines"] += 1
            tokens = tokenize_clean_line(match.group("text"), stats, examples, locator)
            if tokens:
                stats["non_empty_selected_lines"] += 1
                selected_lines.append((locator, tokens))
            else:
                stats["empty_selected_lines"] += 1

    public_stats = {key: value for key, value in stats.items() if not key.startswith("angle_tag::")}
    public_stats["unique_angle_tag_forms_removed"] = sum(1 for key in stats if key.startswith("angle_tag::"))
    return selected_lines, public_stats, examples


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
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_counter_csv(path: Path, field_name: str, counter: Counter[str]) -> None:
    total = sum(counter.values())
    rows = [
        {field_name: item, "count": count, "proportion": count / total if total else 0}
        for item, count in counter.most_common()
    ]
    write_csv(path, rows, [field_name, "count", "proportion"])


def write_top_csv(path: Path, field_name: str, items: list[tuple[str, int]], total: int) -> None:
    rows = [{field_name: item, "count": count, "proportion": count / total if total else 0} for item, count in items]
    write_csv(path, rows, [field_name, "count", "proportion"])


def write_length_csv(path: Path, counter: Counter[int]) -> None:
    total = sum(counter.values())
    rows = [
        {"word_length": length, "count": counter[length], "proportion": counter[length] / total if total else 0}
        for length in sorted(counter)
    ]
    write_csv(path, rows, ["word_length", "count", "proportion"])


def bar_chart(path: Path, title: str, xlabel: str, ylabel: str, labels: list[str], counts: list[int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
    plt.title("Cleaned Word Length Distribution")
    plt.xlabel("Normalized token length")
    plt.ylabel("Count")
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
    plt.title("Cleaned Position Distribution Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def run_clean_baseline(
    selected_lines: list[tuple[str, list[str]]],
    output_dir: Path,
    input_path: Path,
    transcriber_code: str,
    parse_stats: dict[str, int],
) -> dict[str, object]:
    tokens = [token for _locator, line_tokens in selected_lines for token in line_tokens]
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
        "Cleaned Top 20 Normalized Tokens",
        "Token",
        "Count",
        [item for item, _count in top_tokens],
        [count for _item, count in top_tokens],
    )
    bar_chart(
        output_dir / "glyph_frequencies.png",
        "Cleaned Top 20 EVA Character Frequencies",
        "EVA character",
        "Count",
        [item for item, _count in top_glyphs],
        [count for _item, count in top_glyphs],
    )
    length_chart(output_dir / "word_length_distribution.png", length_counter)

    summary: dict[str, object] = {
        "experiment": "exp-002b_clean-ivtff-parser-rerun",
        "rerun_scope": "cleaned exp-001 baseline statistics",
        "run_date_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "script": "scripts/exp002b_clean_ivtff_parser_rerun.py",
        "input": str(input_path.as_posix()),
        "input_sha256": file_sha256(input_path),
        "output": str(output_dir.as_posix()),
        "parameters": {
            "transcriber_code": transcriber_code,
            "token_separators": "period, comma, whitespace",
            "normalization": "lowercase; remove non-ASCII-letter uncertain/editorial marks after IVTFF markup removal",
            "inline_angle_tag_policy": "replace inline <...> markup in selected text with token boundaries before tokenization",
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
        "top_tokens": [{"token": token, "count": count} for token, count in top_tokens],
        "top_glyphs": [{"glyph": glyph, "count": count} for glyph, count in top_glyphs],
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
    }
    with (output_dir / "run_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")
    return summary


def run_clean_positions(
    selected_lines: list[tuple[str, list[str]]],
    output_dir: Path,
    input_path: Path,
    transcriber_code: str,
    parse_stats: dict[str, int],
    min_count: int,
    top_n: int,
) -> dict[str, object]:
    position_counters: dict[str, Counter[str]] = {position: Counter() for position in POSITION_CLASSES}
    overall_counter: Counter[str] = Counter()
    line_stats: Counter[str] = Counter()

    for _locator, tokens in selected_lines:
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
    for token in sorted(overall_counter):
        overall_count = overall_counter[token]
        overall_share = overall_count / overall_total if overall_total else 0
        count_row = {"token": token, "overall_count": overall_count}
        share_row = {"token": token, "overall_share": overall_share}
        for position_class in POSITION_CLASSES:
            position_count = position_counters[position_class][token]
            position_share = position_count / position_totals[position_class] if position_totals[position_class] else 0
            count_row[f"{position_class}_count"] = position_count
            share_row[f"{position_class}_share"] = position_share
            if position_count >= min_count and overall_share > 0:
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

    for name, position_class in (
        ("top_initial_tokens.csv", "line_initial"),
        ("top_medial_tokens.csv", "line_medial"),
        ("top_final_tokens.csv", "line_final"),
    ):
        total = sum(position_counters[position_class].values())
        rows = [
            {"token": token, "count": count, "share": count / total if total else 0}
            for token, count in position_counters[position_class].most_common(top_n)
        ]
        write_csv(output_dir / name, rows, ["token", "count", "share"])

    distances = {
        f"{left}_vs_{right}": {
            "jensen_shannon_divergence_bits": jensen_shannon_divergence(position_counters[left], position_counters[right])
        }
        for left, right in PAIRWISE_COMPARISONS
    }
    with (output_dir / "distribution_distances.json").open("w", encoding="utf-8") as handle:
        json.dump(distances, handle, indent=2)
        handle.write("\n")

    top_initial = position_counters["line_initial"].most_common(top_n)
    top_final = position_counters["line_final"].most_common(top_n)
    bar_chart(
        output_dir / "plots" / "top_initial_tokens.png",
        "Cleaned Top Line-Initial Tokens",
        "Token",
        "Count",
        [token for token, _count in top_initial],
        [count for _token, count in top_initial],
    )
    bar_chart(
        output_dir / "plots" / "top_final_tokens.png",
        "Cleaned Top Line-Final Tokens",
        "Token",
        "Count",
        [token for token, _count in top_final],
        [count for _token, count in top_final],
    )
    comparison_tokens = [token for token, _count in overall_counter.most_common(15)]
    grouped_position_chart(output_dir / "plots" / "position_distribution_comparison.png", position_counters, comparison_tokens)

    summary: dict[str, object] = {
        "experiment": "exp-002b_clean-ivtff-parser-rerun",
        "rerun_scope": "cleaned exp-002 word-position statistics",
        "run_date_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "script": "scripts/exp002b_clean_ivtff_parser_rerun.py",
        "input": str(input_path.as_posix()),
        "input_sha256": file_sha256(input_path),
        "output": str(output_dir.as_posix()),
        "parameters": {
            "transcriber_code": transcriber_code,
            "min_count": min_count,
            "top_n": top_n,
            "token_separators": "period, comma, whitespace",
            "normalization": "lowercase; remove non-ASCII-letter uncertain/editorial marks after IVTFF markup removal",
            "inline_angle_tag_policy": "replace inline <...> markup in selected text with token boundaries before tokenization",
            "position_classes": list(POSITION_CLASSES),
            "distance_metric": "Jensen-Shannon divergence in bits",
        },
        "parse_stats": parse_stats,
        "line_stats": dict(line_stats),
        "position_summary": position_summary_rows,
        "distribution_distances": distances,
        "top_initial_tokens": [
            {"token": token, "count": count} for token, count in position_counters["line_initial"].most_common(top_n)
        ],
        "top_medial_tokens": [
            {"token": token, "count": count} for token, count in position_counters["line_medial"].most_common(top_n)
        ],
        "top_final_tokens": [
            {"token": token, "count": count} for token, count in position_counters["line_final"].most_common(top_n)
        ],
    }
    with (output_dir / "position_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")
    return summary


def load_json(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_top_token_csv(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append({"token": row["token"], "count": int(row["count"])})
    return rows


def write_comparisons(
    output_dir: Path,
    old_exp001: dict[str, object],
    old_exp002: dict[str, object],
    old_exp001_top_tokens: list[dict[str, object]],
    clean_baseline: dict[str, object],
    clean_positions: dict[str, object],
) -> dict[str, object]:
    old_metrics = old_exp001["metrics"]
    clean_metrics = clean_baseline["metrics"]
    metric_rows = []
    for metric in (
        "token_count",
        "unique_token_count",
        "type_token_ratio",
        "glyph_count",
        "unique_glyph_count",
        "glyph_entropy_bits",
        "token_entropy_bits",
        "mean_token_length",
    ):
        old_value = old_metrics[metric]
        clean_value = clean_metrics[metric]
        metric_rows.append(
            {
                "metric": metric,
                "old_value": old_value,
                "cleaned_value": clean_value,
                "delta": clean_value - old_value,
            }
        )
    write_csv(output_dir / "comparison_metrics.csv", metric_rows, ["metric", "old_value", "cleaned_value", "delta"])

    old_top_tokens = old_exp001_top_tokens
    clean_top_tokens = clean_baseline.get("top_tokens", [])
    top_rows = []
    for rank in range(20):
        old_item = old_top_tokens[rank] if rank < len(old_top_tokens) else {}
        clean_item = clean_top_tokens[rank] if rank < len(clean_top_tokens) else {}
        top_rows.append(
            {
                "rank": rank + 1,
                "old_token": old_item.get("token", ""),
                "old_count": old_item.get("count", ""),
                "cleaned_token": clean_item.get("token", ""),
                "cleaned_count": clean_item.get("count", ""),
            }
        )
    write_csv(output_dir / "comparison_top_tokens.csv", top_rows, ["rank", "old_token", "old_count", "cleaned_token", "cleaned_count"])

    old_position_by_class = {row["position_class"]: row for row in old_exp002["position_summary"]}
    clean_position_by_class = {row["position_class"]: row for row in clean_positions["position_summary"]}
    position_rows = []
    for position_class in POSITION_CLASSES:
        old_row = old_position_by_class[position_class]
        clean_row = clean_position_by_class[position_class]
        position_rows.append(
            {
                "position_class": position_class,
                "old_token_count": old_row["token_count"],
                "cleaned_token_count": clean_row["token_count"],
                "token_count_delta": clean_row["token_count"] - old_row["token_count"],
                "old_unique_token_count": old_row["unique_token_count"],
                "cleaned_unique_token_count": clean_row["unique_token_count"],
                "unique_token_count_delta": clean_row["unique_token_count"] - old_row["unique_token_count"],
            }
        )
    write_csv(
        output_dir / "comparison_position_summary.csv",
        position_rows,
        [
            "position_class",
            "old_token_count",
            "cleaned_token_count",
            "token_count_delta",
            "old_unique_token_count",
            "cleaned_unique_token_count",
            "unique_token_count_delta",
        ],
    )

    old_distances = old_exp002["distribution_distances"]
    clean_distances = clean_positions["distribution_distances"]
    distance_rows = []
    for comparison in old_distances:
        old_value = old_distances[comparison]["jensen_shannon_divergence_bits"]
        clean_value = clean_distances[comparison]["jensen_shannon_divergence_bits"]
        distance_rows.append(
            {
                "comparison": comparison,
                "old_jsd_bits": old_value,
                "cleaned_jsd_bits": clean_value,
                "delta": clean_value - old_value,
            }
        )
    write_csv(output_dir / "comparison_distribution_distances.csv", distance_rows, ["comparison", "old_jsd_bits", "cleaned_jsd_bits", "delta"])

    comparison_summary = {
        "experiment": "exp-002b_clean-ivtff-parser-rerun",
        "old_exp001_summary": "artifacts/exp001/run_summary.json",
        "old_exp001_top_tokens": "artifacts/exp001/top_tokens.csv",
        "old_exp002_summary": "artifacts/exp002/position_summary.json",
        "cleaned_baseline_summary": "artifacts/exp002b/baseline_clean/run_summary.json",
        "cleaned_position_summary": "artifacts/exp002b/position_clean/position_summary.json",
        "metric_comparison": metric_rows,
        "position_comparison": position_rows,
        "distribution_distance_comparison": distance_rows,
    }
    with (output_dir / "comparison_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(comparison_summary, handle, indent=2)
        handle.write("\n")
    return comparison_summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run cleaned IVTFF parser reruns for exp-001 and exp-002 comparisons.")
    parser.add_argument("--input", required=True, type=Path, help="Raw IVTFF transcription file.")
    parser.add_argument("--output", required=True, type=Path, help="Output artifact directory.")
    parser.add_argument("--transcriber-code", default="H", help="IVTFF transcriber code to analyze.")
    parser.add_argument("--min-count", type=int, default=10, help="Minimum token count for overrepresentation ranking.")
    parser.add_argument("--top-n", type=int, default=30, help="Number of top position tokens to export.")
    parser.add_argument("--old-exp001-summary", default=Path("artifacts/exp001/run_summary.json"), type=Path)
    parser.add_argument("--old-exp001-top-tokens", default=Path("artifacts/exp001/top_tokens.csv"), type=Path)
    parser.add_argument("--old-exp002-summary", default=Path("artifacts/exp002/position_summary.json"), type=Path)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    baseline_dir = args.output / "baseline_clean"
    position_dir = args.output / "position_clean"
    comparison_dir = args.output / "comparisons"
    audit_dir = args.output / "parser_audit"
    for directory in (baseline_dir, position_dir, comparison_dir, audit_dir):
        directory.mkdir(parents=True, exist_ok=True)

    selected_lines, parse_stats, examples = parse_selected_lines(args.input, args.transcriber_code)
    write_csv(audit_dir / "angle_tag_examples.csv", examples, ["locator", "raw_text", "tags"])

    clean_baseline = run_clean_baseline(selected_lines, baseline_dir, args.input, args.transcriber_code, parse_stats)
    clean_positions = run_clean_positions(
        selected_lines,
        position_dir,
        args.input,
        args.transcriber_code,
        parse_stats,
        args.min_count,
        args.top_n,
    )
    comparison_summary = write_comparisons(
        comparison_dir,
        load_json(args.old_exp001_summary),
        load_json(args.old_exp002_summary),
        load_top_token_csv(args.old_exp001_top_tokens),
        clean_baseline,
        clean_positions,
    )

    summary = {
        "cleaned_baseline_metrics": clean_baseline["metrics"],
        "cleaned_position_line_stats": clean_positions["line_stats"],
        "comparison_metric_deltas": comparison_summary["metric_comparison"],
        "comparison_distribution_distance_deltas": comparison_summary["distribution_distance_comparison"],
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
