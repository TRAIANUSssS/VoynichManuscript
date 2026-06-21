"""Section frequency comparison for exp-003.

This script derives or reads folio-to-section metadata from IVTFF page headers,
then compares cleaned token-frequency profiles across sections.
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
from statistics import median

import matplotlib.pyplot as plt


LINE_RE = re.compile(r"^<(?P<locator>[^>;]+;(?P<code>[A-Z]))>\s*(?P<text>.*)$")
PAGE_HEADER_RE = re.compile(r"^<(?P<folio>f[^.>]+)>\s+<!\s*(?P<vars>[^>]*)>")
VAR_RE = re.compile(r"\$(?P<key>[A-Z])=(?P<value>[^ $\t>]+)")
COMMENT_RE = re.compile(r"\{[^}]*\}")
ANGLE_TAG_RE = re.compile(r"<[^>]*>")
TOKEN_SPLIT_RE = re.compile(r"[.,\s]+")

SECTION_CODE_MAP = {
    "T": "text",
    "H": "herbal",
    "A": "astronomical",
    "Z": "zodiac",
    "B": "biological",
    "C": "cosmological",
    "P": "pharmaceutical",
    "S": "stars",
}


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


def clean_text(text: str, stats: Counter[str]) -> str:
    without_comments = COMMENT_RE.sub("", text)
    tags = ANGLE_TAG_RE.findall(without_comments)
    if tags:
        stats["lines_with_angle_tags"] += 1
        stats["angle_tags_removed"] += len(tags)
        for tag in tags:
            stats[f"angle_tag::{tag}"] += 1
    return ANGLE_TAG_RE.sub(".", without_comments)


def tokenize_clean_line(text: str, stats: Counter[str]) -> list[str]:
    cleaned = clean_text(text, stats)
    tokens: list[str] = []
    for raw_token in TOKEN_SPLIT_RE.split(cleaned):
        token = normalize_token(raw_token)
        if token:
            tokens.append(token)
        elif raw_token:
            stats["discarded_empty_tokens"] += 1
    return tokens


def extract_folio_from_locator(locator: str) -> str:
    return locator.split(";", 1)[0].split(".", 1)[0]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def derive_metadata(input_path: Path, metadata_path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with input_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            match = PAGE_HEADER_RE.match(line)
            if not match:
                continue
            variables = {item.group("key"): item.group("value") for item in VAR_RE.finditer(match.group("vars"))}
            illustration_code = variables.get("I", "")
            section = SECTION_CODE_MAP.get(illustration_code, "unknown")
            rows.append(
                {
                    "folio_id": match.group("folio"),
                    "section": section,
                    "illustration_code": illustration_code,
                    "quire": variables.get("Q", ""),
                    "page_in_quire": variables.get("P", ""),
                    "currier_language": variables.get("L", ""),
                    "currier_hand": variables.get("H", ""),
                    "source": "data/raw/LSI_ivtff_0d.txt page header parsable information; source documentation https://www.voynich.nu/transcr.html",
                    "note": "Derived from IVTFF page header $I illustration type. Code meanings are documented in the IVTFF file comments.",
                }
            )

    write_csv(
        metadata_path,
        rows,
        [
            "folio_id",
            "section",
            "illustration_code",
            "quire",
            "page_in_quire",
            "currier_language",
            "currier_hand",
            "source",
            "note",
        ],
    )
    return rows


def load_or_create_metadata(input_path: Path, metadata_path: Path) -> tuple[dict[str, dict[str, str]], bool]:
    if metadata_path.exists():
        created = False
        with metadata_path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
    else:
        created = True
        rows = derive_metadata(input_path, metadata_path)
    return {row["folio_id"]: row for row in rows}, created


def parse_selected_lines(
    input_path: Path,
    transcriber_code: str,
    metadata: dict[str, dict[str, str]],
) -> tuple[list[dict[str, object]], list[dict[str, str]], dict[str, int]]:
    parsed_rows: list[dict[str, object]] = []
    unmapped_rows: list[dict[str, str]] = []
    stats: Counter[str] = Counter()

    with input_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            stats["input_lines"] += 1
            match = LINE_RE.match(line)
            if not match:
                continue
            stats["data_lines"] += 1
            if match.group("code") != transcriber_code:
                continue

            stats["selected_lines"] += 1
            locator = match.group("locator")
            folio_id = extract_folio_from_locator(locator)
            tokens = tokenize_clean_line(match.group("text"), stats)
            if tokens:
                stats["non_empty_selected_lines"] += 1
            else:
                stats["empty_selected_lines"] += 1

            metadata_row = metadata.get(folio_id)
            if not metadata_row:
                stats["unmapped_selected_lines"] += 1
                unmapped_rows.append({"locator": locator, "folio_id": folio_id, "reason": "folio_id not present in metadata"})
                continue

            stats["mapped_selected_lines"] += 1
            if tokens:
                parsed_rows.append(
                    {
                        "locator": locator,
                        "folio_id": folio_id,
                        "section": metadata_row["section"],
                        "tokens": tokens,
                    }
                )

    public_stats = {key: value for key, value in stats.items() if not key.startswith("angle_tag::")}
    public_stats["unique_angle_tag_forms_removed"] = sum(1 for key in stats if key.startswith("angle_tag::"))
    return parsed_rows, unmapped_rows, public_stats


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


def section_summary(parsed_rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], dict[str, Counter[str]]]:
    section_tokens: dict[str, list[str]] = defaultdict(list)
    section_lines: Counter[str] = Counter()
    for row in parsed_rows:
        section = str(row["section"])
        section_lines[section] += 1
        section_tokens[section].extend(row["tokens"])

    counters = {section: Counter(tokens) for section, tokens in section_tokens.items()}
    rows: list[dict[str, object]] = []
    for section in sorted(counters):
        tokens = section_tokens[section]
        token_counter = counters[section]
        glyph_counter = Counter("".join(tokens))
        lengths = [len(token) for token in tokens]
        rows.append(
            {
                "section": section,
                "line_count": section_lines[section],
                "token_count": len(tokens),
                "unique_token_count": len(token_counter),
                "type_token_ratio": len(token_counter) / len(tokens) if tokens else 0,
                "glyph_count": sum(glyph_counter.values()),
                "unique_glyph_count": len(glyph_counter),
                "glyph_entropy_bits": entropy(glyph_counter),
                "token_entropy_bits": entropy(token_counter),
                "mean_token_length": sum(lengths) / len(lengths) if lengths else 0,
                "median_token_length": median(lengths) if lengths else 0,
            }
        )
    return rows, counters


def write_token_section_outputs(
    output_dir: Path,
    section_counters: dict[str, Counter[str]],
    min_count: int,
    top_n: int,
) -> None:
    overall_counter: Counter[str] = Counter()
    for counter in section_counters.values():
        overall_counter.update(counter)
    overall_total = sum(overall_counter.values())
    section_totals = {section: sum(counter.values()) for section, counter in section_counters.items()}

    count_rows = []
    share_rows = []
    over_rows = []
    top_rows = []
    for section in sorted(section_counters):
        counter = section_counters[section]
        section_total = section_totals[section]
        for token, count in sorted(counter.items()):
            overall_count = overall_counter[token]
            section_share = count / section_total if section_total else 0
            overall_share = overall_count / overall_total if overall_total else 0
            count_rows.append(
                {
                    "section": section,
                    "token": token,
                    "section_count": count,
                    "overall_count": overall_count,
                }
            )
            share_rows.append(
                {
                    "section": section,
                    "token": token,
                    "section_share": section_share,
                    "overall_share": overall_share,
                }
            )
            if count >= min_count and overall_share > 0:
                over_rows.append(
                    {
                        "section": section,
                        "token": token,
                        "section_count": count,
                        "overall_count": overall_count,
                        "section_share": section_share,
                        "overall_share": overall_share,
                        "overrepresentation_ratio": section_share / overall_share,
                    }
                )
        for rank, (token, count) in enumerate(counter.most_common(top_n), start=1):
            top_rows.append(
                {
                    "section": section,
                    "rank": rank,
                    "token": token,
                    "count": count,
                    "share": count / section_total if section_total else 0,
                }
            )

    over_rows.sort(key=lambda row: (str(row["section"]), -float(row["overrepresentation_ratio"]), -int(row["section_count"])))
    write_csv(output_dir / "section_token_counts.csv", count_rows, ["section", "token", "section_count", "overall_count"])
    write_csv(output_dir / "section_token_shares.csv", share_rows, ["section", "token", "section_share", "overall_share"])
    write_csv(
        output_dir / "section_token_overrepresentation.csv",
        over_rows,
        ["section", "token", "section_count", "overall_count", "section_share", "overall_share", "overrepresentation_ratio"],
    )
    write_csv(output_dir / "top_tokens_by_section.csv", top_rows, ["section", "rank", "token", "count", "share"])


def pairwise_distances(section_counters: dict[str, Counter[str]]) -> list[dict[str, object]]:
    rows = []
    sections = sorted(section_counters)
    for index, left in enumerate(sections):
        for right in sections[index + 1 :]:
            rows.append(
                {
                    "section_a": left,
                    "section_b": right,
                    "jensen_shannon_divergence_bits": jensen_shannon_divergence(section_counters[left], section_counters[right]),
                }
            )
    return rows


def compare_with_position_distances(section_rows: list[dict[str, object]], position_path: Path) -> tuple[list[dict[str, object]], dict[str, object] | None]:
    if not position_path.exists():
        return [], None
    with position_path.open("r", encoding="utf-8") as handle:
        position_distances = json.load(handle)
    section_values = [float(row["jensen_shannon_divergence_bits"]) for row in section_rows]
    position_values = [float(item["jensen_shannon_divergence_bits"]) for item in position_distances.values()]
    comparison_rows = []
    for row in section_rows:
        section_distance = float(row["jensen_shannon_divergence_bits"])
        comparison_rows.append(
            {
                "section_pair": f"{row['section_a']} vs {row['section_b']}",
                "section_jsd_bits": section_distance,
                "exp002b_position_min_jsd_bits": min(position_values) if position_values else "",
                "exp002b_position_mean_jsd_bits": sum(position_values) / len(position_values) if position_values else "",
                "exp002b_position_max_jsd_bits": max(position_values) if position_values else "",
            }
        )
    summary = {
        "section_min_jsd_bits": min(section_values) if section_values else None,
        "section_mean_jsd_bits": sum(section_values) / len(section_values) if section_values else None,
        "section_max_jsd_bits": max(section_values) if section_values else None,
        "exp002b_position_distances": position_distances,
        "exp002b_position_min_jsd_bits": min(position_values) if position_values else None,
        "exp002b_position_mean_jsd_bits": sum(position_values) / len(position_values) if position_values else None,
        "exp002b_position_max_jsd_bits": max(position_values) if position_values else None,
    }
    return comparison_rows, summary


def plot_section_token_counts(output_dir: Path, rows: list[dict[str, object]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    sections = [str(row["section"]) for row in rows]
    counts = [int(row["token_count"]) for row in rows]
    plt.figure(figsize=(10, 5))
    plt.bar(sections, counts, color="#4f6f8f")
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("Token count")
    plt.title("Cleaned Tokens By Section")
    plt.tight_layout()
    plt.savefig(output_dir / "section_token_counts.png", dpi=150)
    plt.close()


def plot_ttr_entropy(output_dir: Path, rows: list[dict[str, object]]) -> None:
    sections = [str(row["section"]) for row in rows]
    x_positions = list(range(len(sections)))
    width = 0.35
    plt.figure(figsize=(10, 5))
    plt.bar([x - width / 2 for x in x_positions], [float(row["type_token_ratio"]) for row in rows], width=width, label="TTR")
    plt.bar(
        [x + width / 2 for x in x_positions],
        [float(row["token_entropy_bits"]) / 12 for row in rows],
        width=width,
        label="Token entropy / 12",
    )
    plt.xticks(x_positions, sections, rotation=35, ha="right")
    plt.title("Section TTR And Scaled Token Entropy")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "section_ttr_entropy.png", dpi=150)
    plt.close()


def plot_distance_heatmap(output_dir: Path, distance_rows: list[dict[str, object]], sections: list[str]) -> None:
    index = {section: idx for idx, section in enumerate(sections)}
    matrix = [[0.0 for _ in sections] for _ in sections]
    for row in distance_rows:
        i = index[str(row["section_a"])]
        j = index[str(row["section_b"])]
        value = float(row["jensen_shannon_divergence_bits"])
        matrix[i][j] = value
        matrix[j][i] = value
    plt.figure(figsize=(8, 7))
    plt.imshow(matrix, cmap="viridis")
    plt.colorbar(label="JSD bits")
    plt.xticks(range(len(sections)), sections, rotation=45, ha="right")
    plt.yticks(range(len(sections)), sections)
    plt.title("Pairwise Section Distances")
    plt.tight_layout()
    plt.savefig(output_dir / "pairwise_section_distances_heatmap.png", dpi=150)
    plt.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run exp-003 section frequency comparison.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--transcriber-code", default="H")
    parser.add_argument("--min-count", type=int, default=10)
    parser.add_argument("--top-n", type=int, default=30)
    parser.add_argument(
        "--position-distances",
        type=Path,
        default=Path("artifacts/exp002b/position_clean/distribution_distances.json"),
    )
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    metadata, metadata_created = load_or_create_metadata(args.input, args.metadata)
    parsed_rows, unmapped_rows, parse_stats = parse_selected_lines(args.input, args.transcriber_code, metadata)

    summary_rows, section_counters = section_summary(parsed_rows)
    write_csv(
        args.output / "section_summary.csv",
        summary_rows,
        [
            "section",
            "line_count",
            "token_count",
            "unique_token_count",
            "type_token_ratio",
            "glyph_count",
            "unique_glyph_count",
            "glyph_entropy_bits",
            "token_entropy_bits",
            "mean_token_length",
            "median_token_length",
        ],
    )
    with (args.output / "section_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary_rows, handle, indent=2)
        handle.write("\n")

    write_token_section_outputs(args.output, section_counters, args.min_count, args.top_n)
    distance_rows = pairwise_distances(section_counters)
    write_csv(args.output / "pairwise_section_distances.csv", distance_rows, ["section_a", "section_b", "jensen_shannon_divergence_bits"])
    with (args.output / "pairwise_section_distances.json").open("w", encoding="utf-8") as handle:
        json.dump(distance_rows, handle, indent=2)
        handle.write("\n")

    write_csv(args.output / "unmapped_lines.csv", unmapped_rows, ["locator", "folio_id", "reason"])
    with (args.output / "parser_audit.json").open("w", encoding="utf-8") as handle:
        json.dump(parse_stats, handle, indent=2)
        handle.write("\n")

    comparison_rows, comparison_summary = compare_with_position_distances(distance_rows, args.position_distances)
    if comparison_rows and comparison_summary:
        write_csv(
            args.output / "section_vs_position_distance_comparison.csv",
            comparison_rows,
            [
                "section_pair",
                "section_jsd_bits",
                "exp002b_position_min_jsd_bits",
                "exp002b_position_mean_jsd_bits",
                "exp002b_position_max_jsd_bits",
            ],
        )
        with (args.output / "section_vs_position_distance_comparison.json").open("w", encoding="utf-8") as handle:
            json.dump(comparison_summary, handle, indent=2)
            handle.write("\n")

    plots_dir = args.output / "plots"
    plot_section_token_counts(plots_dir, summary_rows)
    plot_ttr_entropy(plots_dir, summary_rows)
    plot_distance_heatmap(plots_dir, distance_rows, sorted(section_counters))

    run_summary = {
        "experiment": "exp-003_section-frequency-comparison",
        "run_date_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "script": "scripts/exp003_section_frequency_comparison.py",
        "input": str(args.input.as_posix()),
        "input_sha256": file_sha256(args.input),
        "metadata": str(args.metadata.as_posix()),
        "metadata_created_by_script": metadata_created,
        "metadata_source": "IVTFF page header parsable information in data/raw/LSI_ivtff_0d.txt; code meanings documented in the raw file comments and https://www.voynich.nu/transcr.html",
        "output": str(args.output.as_posix()),
        "parameters": {
            "transcriber_code": args.transcriber_code,
            "min_count": args.min_count,
            "top_n": args.top_n,
            "parser_policy": "cleaned exp-002b policy: remove comments, replace inline <...> markup with token boundaries, split on periods/commas/whitespace, lowercase and strip non-ASCII letters",
        },
        "parse_stats": parse_stats,
        "section_count": len(section_counters),
        "sections": sorted(section_counters),
        "section_summary": summary_rows,
        "pairwise_section_distances": distance_rows,
        "section_vs_position_distance_summary": comparison_summary,
        "artifacts": [
            "run_summary.json",
            "parser_audit.json",
            "section_summary.csv",
            "section_summary.json",
            "section_token_counts.csv",
            "section_token_shares.csv",
            "section_token_overrepresentation.csv",
            "top_tokens_by_section.csv",
            "pairwise_section_distances.csv",
            "pairwise_section_distances.json",
            "unmapped_lines.csv",
            "section_vs_position_distance_comparison.csv",
            "section_vs_position_distance_comparison.json",
            "plots/section_token_counts.png",
            "plots/section_ttr_entropy.png",
            "plots/pairwise_section_distances_heatmap.png",
        ],
    }
    with (args.output / "run_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(run_summary, handle, indent=2)
        handle.write("\n")

    print(json.dumps({"parse_stats": parse_stats, "section_count": len(section_counters)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
