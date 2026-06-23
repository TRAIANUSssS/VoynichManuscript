"""Currier-section interaction control for exp-006.

This script reuses the cleaned IVTFF parser policy from exp-002b and the
folio-to-section mapping used by exp-003/exp-004/exp-005. It tests whether
section-level token-frequency differences remain visible after grouping by
Currier language labels from documented IVTFF page-header metadata.
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

UNKNOWN_CURRIER_LABELS = {"", "?", "-"}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(json_ready(value), handle, indent=2)
        handle.write("\n")


def json_ready(value: object) -> object:
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    return value


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


def parse_page_headers(input_path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with input_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            match = PAGE_HEADER_RE.match(line)
            if not match:
                continue
            variables = {item.group("key"): item.group("value") for item in VAR_RE.finditer(match.group("vars"))}
            illustration_code = variables.get("I", "")
            rows.append(
                {
                    "folio_id": match.group("folio"),
                    "section": SECTION_CODE_MAP.get(illustration_code, "unknown"),
                    "illustration_code": illustration_code,
                    "quire": variables.get("Q", ""),
                    "page_in_quire": variables.get("P", ""),
                    "currier_language": variables.get("L", ""),
                    "currier_hand": variables.get("H", ""),
                    "source": "data/raw/LSI_ivtff_0d.txt page header parsable information; source documentation https://www.voynich.nu/transcr.html",
                    "note": "Derived from IVTFF page header metadata. $I supplies illustration type; $L supplies Currier language.",
                }
            )
    return rows


def derive_section_metadata(input_path: Path, metadata_path: Path) -> list[dict[str, str]]:
    rows = parse_page_headers(input_path)
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


def derive_currier_metadata(input_path: Path, metadata_path: Path) -> list[dict[str, str]]:
    rows = [
        {
            "folio_id": row["folio_id"],
            "currier_language": row["currier_language"],
            "source": row["source"],
            "note": "Derived from IVTFF page-header $L Currier language metadata. Blank, ? and - labels are treated as unmapped for Currier-controlled comparisons.",
        }
        for row in parse_page_headers(input_path)
    ]
    write_csv(metadata_path, rows, ["folio_id", "currier_language", "source", "note"])
    return rows


def load_section_metadata(input_path: Path, metadata_path: Path) -> tuple[dict[str, dict[str, str]], bool]:
    if metadata_path.exists():
        with metadata_path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return {row["folio_id"]: row for row in rows}, False
    rows = derive_section_metadata(input_path, metadata_path)
    return {row["folio_id"]: row for row in rows}, True


def load_currier_metadata(input_path: Path, metadata_path: Path) -> tuple[dict[str, dict[str, str]], bool]:
    if metadata_path.exists():
        with metadata_path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return {row["folio_id"]: row for row in rows}, False
    rows = derive_currier_metadata(input_path, metadata_path)
    return {row["folio_id"]: row for row in rows}, True


def is_valid_currier_label(label: str) -> bool:
    return label.strip() not in UNKNOWN_CURRIER_LABELS


def parse_selected_lines(
    input_path: Path,
    transcriber_code: str,
    section_metadata: dict[str, dict[str, str]],
    currier_metadata: dict[str, dict[str, str]],
) -> tuple[list[dict[str, object]], list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    line_rows: list[dict[str, object]] = []
    unmapped_section_rows: list[dict[str, str]] = []
    unmapped_currier_rows: list[dict[str, str]] = []
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

            section_row = section_metadata.get(folio_id)
            currier_row = currier_metadata.get(folio_id)
            section = section_row.get("section", "") if section_row else ""
            raw_currier = currier_row.get("currier_language", "") if currier_row else ""
            valid_section = bool(section_row and section and section != "unknown")
            valid_currier = bool(currier_row and is_valid_currier_label(raw_currier))

            if valid_section:
                stats["section_mapped_selected_lines"] += 1
            else:
                stats["unmapped_section_selected_lines"] += 1
                unmapped_section_rows.append(
                    {
                        "locator": locator,
                        "folio_id": folio_id,
                        "reason": "folio_id missing from section metadata or section is unknown",
                    }
                )

            if valid_currier:
                stats["currier_mapped_selected_lines"] += 1
            else:
                stats["unmapped_currier_selected_lines"] += 1
                reason = "folio_id missing from Currier metadata"
                if currier_row and raw_currier in UNKNOWN_CURRIER_LABELS:
                    reason = f"Currier label is {raw_currier or 'blank'}"
                unmapped_currier_rows.append({"locator": locator, "folio_id": folio_id, "currier_language": raw_currier, "reason": reason})

            if valid_section and valid_currier:
                stats["both_mapped_selected_lines"] += 1

            line_rows.append(
                {
                    "locator": locator,
                    "folio_id": folio_id,
                    "section": section,
                    "currier_language": raw_currier if valid_currier else "",
                    "raw_currier_language": raw_currier,
                    "tokens": tokens,
                    "section_mapped": valid_section,
                    "currier_mapped": valid_currier,
                    "both_mapped": valid_section and valid_currier,
                }
            )

    public_stats = {key: value for key, value in stats.items() if not key.startswith("angle_tag::")}
    public_stats["unique_angle_tag_forms_removed"] = sum(1 for key in stats if key.startswith("angle_tag::"))
    return line_rows, unmapped_section_rows, unmapped_currier_rows, public_stats


def entropy(counter: Counter[str]) -> float:
    total = sum(counter.values())
    if total == 0:
        return 0.0
    return -sum((count / total) * math.log2(count / total) for count in counter.values())


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


def pairwise_names(names: list[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for index, left in enumerate(names):
        for right in names[index + 1 :]:
            pairs.append((left, right))
    return pairs


def group_tokens(line_rows: list[dict[str, object]], key: str, require_section: bool = False, require_currier: bool = False) -> tuple[dict[str, list[str]], Counter[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    line_counts: Counter[str] = Counter()
    for row in line_rows:
        if require_section and not row["section_mapped"]:
            continue
        if require_currier and not row["currier_mapped"]:
            continue
        label = str(row[key])
        if not label:
            continue
        tokens = list(row["tokens"])
        if not tokens:
            continue
        line_counts[label] += 1
        grouped[label].extend(tokens)
    return dict(grouped), line_counts


def summary_rows_for_groups(grouped_tokens: dict[str, list[str]], line_counts: Counter[str], label_name: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for label in sorted(grouped_tokens):
        tokens = grouped_tokens[label]
        counter = Counter(tokens)
        lengths = [len(token) for token in tokens]
        rows.append(
            {
                label_name: label,
                "line_count": line_counts[label],
                "token_count": len(tokens),
                "unique_token_count": len(counter),
                "type_token_ratio": len(counter) / len(tokens) if tokens else 0,
                "token_entropy_bits": entropy(counter),
                "mean_token_length": sum(lengths) / len(lengths) if lengths else 0,
                "median_token_length": median(lengths) if lengths else 0,
            }
        )
    return rows


def token_frequency_rows(grouped_tokens: dict[str, list[str]], group_name: str) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    count_rows: list[dict[str, object]] = []
    share_rows: list[dict[str, object]] = []
    top_rows: list[dict[str, object]] = []
    for group in sorted(grouped_tokens):
        counter = Counter(grouped_tokens[group])
        total = sum(counter.values())
        for token, count in sorted(counter.items()):
            count_rows.append({group_name: group, "token": token, "count": count})
            share_rows.append({group_name: group, "token": token, "share": count / total if total else 0})
        for rank, (token, count) in enumerate(counter.most_common(), start=1):
            top_rows.append({group_name: group, "rank": rank, "token": token, "count": count, "share": count / total if total else 0})
    return count_rows, share_rows, top_rows


def pairwise_distance_rows(grouped_tokens: dict[str, list[str]], label_name: str, output_a: str, output_b: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    counters = {name: Counter(tokens) for name, tokens in grouped_tokens.items()}
    for left, right in pairwise_names(sorted(counters)):
        rows.append(
            {
                output_a: left,
                output_b: right,
                "token_count_a": len(grouped_tokens[left]),
                "token_count_b": len(grouped_tokens[right]),
                "jensen_shannon_divergence_bits": jensen_shannon_divergence(counters[left], counters[right]),
            }
        )
    return rows


def section_currier_contingency(line_rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    line_counts: Counter[tuple[str, str]] = Counter()
    token_counts: Counter[tuple[str, str]] = Counter()
    section_token_totals: Counter[str] = Counter()
    currier_token_totals: Counter[str] = Counter()

    for row in line_rows:
        if not row["both_mapped"]:
            continue
        section = str(row["section"])
        currier = str(row["currier_language"])
        tokens = list(row["tokens"])
        line_counts[(section, currier)] += 1
        token_counts[(section, currier)] += len(tokens)
        section_token_totals[section] += len(tokens)
        currier_token_totals[currier] += len(tokens)

    sections = sorted({section for section, _ in set(line_counts) | set(token_counts)})
    curriers = sorted({currier for _, currier in set(line_counts) | set(token_counts)})

    line_rows_out = [
        {"section": section, "currier_language": currier, "line_count": line_counts[(section, currier)]}
        for section in sections
        for currier in curriers
    ]
    token_rows_out = [
        {"section": section, "currier_language": currier, "token_count": token_counts[(section, currier)]}
        for section in sections
        for currier in curriers
    ]
    percentage_rows = []
    for section in sections:
        for currier in curriers:
            token_count = token_counts[(section, currier)]
            percentage_rows.append(
                {
                    "section": section,
                    "currier_language": currier,
                    "token_count": token_count,
                    "share_of_section_tokens": token_count / section_token_totals[section] if section_token_totals[section] else 0,
                    "share_of_currier_tokens": token_count / currier_token_totals[currier] if currier_token_totals[currier] else 0,
                }
            )
    return line_rows_out, token_rows_out, percentage_rows


def section_within_currier_distances(
    line_rows: list[dict[str, object]],
    min_tokens_per_group: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    group_rows: list[dict[str, object]] = []
    curriers = sorted({str(row["currier_language"]) for row in line_rows if row["both_mapped"] and row["currier_language"]})
    for currier in curriers:
        section_tokens: dict[str, list[str]] = defaultdict(list)
        section_lines: Counter[str] = Counter()
        for row in line_rows:
            if not row["both_mapped"] or row["currier_language"] != currier:
                continue
            tokens = list(row["tokens"])
            if not tokens:
                continue
            section = str(row["section"])
            section_lines[section] += 1
            section_tokens[section].extend(tokens)
        valid = {section: tokens for section, tokens in section_tokens.items() if len(tokens) >= min_tokens_per_group}
        for section in sorted(section_tokens):
            group_rows.append(
                {
                    "currier_language": currier,
                    "section": section,
                    "line_count": section_lines[section],
                    "token_count": len(section_tokens[section]),
                    "meets_min_tokens": len(section_tokens[section]) >= min_tokens_per_group,
                }
            )
        counters = {section: Counter(tokens) for section, tokens in valid.items()}
        for left, right in pairwise_names(sorted(counters)):
            rows.append(
                {
                    "currier_language": currier,
                    "section_a": left,
                    "section_b": right,
                    "token_count_a": len(valid[left]),
                    "token_count_b": len(valid[right]),
                    "jensen_shannon_divergence_bits": jensen_shannon_divergence(counters[left], counters[right]),
                }
            )
    return rows, group_rows


def currier_within_section_distances(
    line_rows: list[dict[str, object]],
    min_tokens_per_group: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    group_rows: list[dict[str, object]] = []
    sections = sorted({str(row["section"]) for row in line_rows if row["both_mapped"] and row["section"]})
    for section in sections:
        currier_tokens: dict[str, list[str]] = defaultdict(list)
        currier_lines: Counter[str] = Counter()
        for row in line_rows:
            if not row["both_mapped"] or row["section"] != section:
                continue
            tokens = list(row["tokens"])
            if not tokens:
                continue
            currier = str(row["currier_language"])
            currier_lines[currier] += 1
            currier_tokens[currier].extend(tokens)
        valid = {currier: tokens for currier, tokens in currier_tokens.items() if len(tokens) >= min_tokens_per_group}
        for currier in sorted(currier_tokens):
            group_rows.append(
                {
                    "section": section,
                    "currier_language": currier,
                    "line_count": currier_lines[currier],
                    "token_count": len(currier_tokens[currier]),
                    "meets_min_tokens": len(currier_tokens[currier]) >= min_tokens_per_group,
                }
            )
        counters = {currier: Counter(tokens) for currier, tokens in valid.items()}
        for left, right in pairwise_names(sorted(counters)):
            rows.append(
                {
                    "section": section,
                    "currier_a": left,
                    "currier_b": right,
                    "token_count_a": len(valid[left]),
                    "token_count_b": len(valid[right]),
                    "jensen_shannon_divergence_bits": jensen_shannon_divergence(counters[left], counters[right]),
                }
            )
    return rows, group_rows


def mean_distance(rows: list[dict[str, object]]) -> float | None:
    values = [float(row["jensen_shannon_divergence_bits"]) for row in rows]
    return sum(values) / len(values) if values else None


def signal_label(full_section_mean: float | None, within_currier_mean: float | None, valid_within_pairs: int, dominant_section_count: int, section_count: int) -> str:
    if full_section_mean is None or within_currier_mean is None or valid_within_pairs == 0:
        return "insufficient_data"
    if section_count and dominant_section_count / section_count >= 0.5 and valid_within_pairs < 28:
        return "section_currier_strongly_confounded"
    ratio = within_currier_mean / full_section_mean if full_section_mean else 0
    if ratio >= 0.8:
        return "section_signal_preserved_within_currier"
    return "section_signal_reduced_within_currier"


def signal_attribution_summary(
    section_distance_rows: list[dict[str, object]],
    currier_distance_rows: list[dict[str, object]],
    section_within_rows: list[dict[str, object]],
    currier_within_rows: list[dict[str, object]],
    section_currier_percentages: list[dict[str, object]],
    total_tokens: int,
    both_mapped_tokens: int,
) -> list[dict[str, object]]:
    full_section_mean = mean_distance(section_distance_rows)
    currier_mean = mean_distance(currier_distance_rows)
    section_within_mean = mean_distance(section_within_rows)
    currier_within_mean = mean_distance(currier_within_rows)
    sections = sorted({str(row["section"]) for row in section_currier_percentages})
    dominant_section_count = 0
    for section in sections:
        shares = [float(row["share_of_section_tokens"]) for row in section_currier_percentages if row["section"] == section]
        if shares and max(shares) >= 0.9:
            dominant_section_count += 1
    label = signal_label(full_section_mean, section_within_mean, len(section_within_rows), dominant_section_count, len(sections))
    return [
        {
            "comparison_level": "section_only_recomputed",
            "mean_jsd_bits": full_section_mean if full_section_mean is not None else "",
            "valid_comparison_count": len(section_distance_rows),
            "token_coverage": total_tokens,
            "summary_label": "reference",
        },
        {
            "comparison_level": "currier_only",
            "mean_jsd_bits": currier_mean if currier_mean is not None else "",
            "valid_comparison_count": len(currier_distance_rows),
            "token_coverage": both_mapped_tokens,
            "summary_label": "currier_reference",
        },
        {
            "comparison_level": "section_within_currier",
            "mean_jsd_bits": section_within_mean if section_within_mean is not None else "",
            "valid_comparison_count": len(section_within_rows),
            "token_coverage": both_mapped_tokens,
            "summary_label": label,
        },
        {
            "comparison_level": "currier_within_section",
            "mean_jsd_bits": currier_within_mean if currier_within_mean is not None else "",
            "valid_comparison_count": len(currier_within_rows),
            "token_coverage": both_mapped_tokens,
            "summary_label": "within_section_currier_reference" if currier_within_rows else "insufficient_data",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run exp-006 Currier-section interaction control.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--section-metadata", default=Path("data/metadata/folio_sections.csv"), type=Path)
    parser.add_argument("--currier-metadata", default=Path("data/metadata/folio_currier.csv"), type=Path)
    parser.add_argument("--metadata", dest="section_metadata_alias", type=Path, help="Alias for --section-metadata.")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--transcriber-code", default="H")
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--min-tokens-per-group", type=int, default=100)
    parser.add_argument("--min-count", type=int, default=10)
    parser.add_argument("--top-n", type=int, default=30)
    parser.add_argument("--exp003-observed", default=Path("artifacts/exp003/pairwise_section_distances.json"), type=Path)
    args = parser.parse_args()

    if args.section_metadata_alias is not None:
        args.section_metadata = args.section_metadata_alias

    args.output.mkdir(parents=True, exist_ok=True)
    section_metadata, section_metadata_created = load_section_metadata(args.input, args.section_metadata)
    currier_metadata, currier_metadata_created = load_currier_metadata(args.input, args.currier_metadata)
    line_rows, unmapped_section_rows, unmapped_currier_rows, parse_stats = parse_selected_lines(
        args.input,
        args.transcriber_code,
        section_metadata,
        currier_metadata,
    )

    section_tokens, section_lines = group_tokens(line_rows, "section", require_section=True)
    currier_tokens, currier_lines = group_tokens(line_rows, "currier_language", require_currier=True)
    both_mapped_token_count = sum(len(row["tokens"]) for row in line_rows if row["both_mapped"])
    total_section_token_count = sum(len(tokens) for tokens in section_tokens.values())

    line_contingency, token_contingency, percentage_rows = section_currier_contingency(line_rows)
    currier_summary = summary_rows_for_groups(currier_tokens, currier_lines, "currier_language")
    section_summary = summary_rows_for_groups(section_tokens, section_lines, "section")
    currier_count_rows, currier_share_rows, top_tokens = token_frequency_rows(currier_tokens, "currier_language")
    top_tokens = [row for row in top_tokens if int(row["rank"]) <= args.top_n]
    currier_distances = pairwise_distance_rows(currier_tokens, "currier_language", "currier_a", "currier_b")
    section_distances = pairwise_distance_rows(section_tokens, "section", "section_a", "section_b")
    section_within_rows, section_within_group_rows = section_within_currier_distances(line_rows, args.min_tokens_per_group)
    currier_within_rows, currier_within_group_rows = currier_within_section_distances(line_rows, args.min_tokens_per_group)
    signal_summary = signal_attribution_summary(
        section_distances,
        currier_distances,
        section_within_rows,
        currier_within_rows,
        percentage_rows,
        total_section_token_count,
        both_mapped_token_count,
    )

    metadata_coverage = {
        "selected_line_count": parse_stats.get("selected_lines", 0),
        "non_empty_selected_line_count": parse_stats.get("non_empty_selected_lines", 0),
        "section_mapped_line_count": parse_stats.get("section_mapped_selected_lines", 0),
        "unmapped_section_line_count": parse_stats.get("unmapped_section_selected_lines", 0),
        "currier_mapped_line_count": parse_stats.get("currier_mapped_selected_lines", 0),
        "unmapped_currier_line_count": parse_stats.get("unmapped_currier_selected_lines", 0),
        "both_mapped_line_count": parse_stats.get("both_mapped_selected_lines", 0),
        "section_names": sorted(section_tokens),
        "currier_categories": sorted(currier_tokens),
        "section_count": len(section_tokens),
        "currier_category_count": len(currier_tokens),
        "unknown_currier_labels_treated_as_unmapped": sorted(UNKNOWN_CURRIER_LABELS),
    }

    write_json(args.output / "metadata_coverage.json", metadata_coverage)
    write_csv(args.output / "section_currier_contingency_lines.csv", line_contingency, ["section", "currier_language", "line_count"])
    write_csv(args.output / "section_currier_contingency_tokens.csv", token_contingency, ["section", "currier_language", "token_count"])
    write_csv(
        args.output / "section_currier_percentages.csv",
        percentage_rows,
        ["section", "currier_language", "token_count", "share_of_section_tokens", "share_of_currier_tokens"],
    )
    write_csv(
        args.output / "currier_summary.csv",
        currier_summary,
        [
            "currier_language",
            "line_count",
            "token_count",
            "unique_token_count",
            "type_token_ratio",
            "token_entropy_bits",
            "mean_token_length",
            "median_token_length",
        ],
    )
    write_csv(args.output / "currier_token_counts.csv", currier_count_rows, ["currier_language", "token", "count"])
    write_csv(args.output / "currier_token_shares.csv", currier_share_rows, ["currier_language", "token", "share"])
    write_csv(args.output / "top_tokens_by_currier.csv", top_tokens, ["currier_language", "rank", "token", "count", "share"])
    write_csv(args.output / "pairwise_currier_distances.csv", currier_distances, ["currier_a", "currier_b", "token_count_a", "token_count_b", "jensen_shannon_divergence_bits"])
    write_csv(args.output / "section_only_recomputed_distances.csv", section_distances, ["section_a", "section_b", "token_count_a", "token_count_b", "jensen_shannon_divergence_bits"])
    write_csv(
        args.output / "section_within_currier_groups.csv",
        section_within_group_rows,
        ["currier_language", "section", "line_count", "token_count", "meets_min_tokens"],
    )
    write_csv(
        args.output / "section_within_currier_distances.csv",
        section_within_rows,
        ["currier_language", "section_a", "section_b", "token_count_a", "token_count_b", "jensen_shannon_divergence_bits"],
    )
    write_csv(
        args.output / "currier_within_section_groups.csv",
        currier_within_group_rows,
        ["section", "currier_language", "line_count", "token_count", "meets_min_tokens"],
    )
    write_csv(
        args.output / "currier_within_section_distances.csv",
        currier_within_rows,
        ["section", "currier_a", "currier_b", "token_count_a", "token_count_b", "jensen_shannon_divergence_bits"],
    )
    write_csv(
        args.output / "signal_attribution_summary.csv",
        signal_summary,
        ["comparison_level", "mean_jsd_bits", "valid_comparison_count", "token_coverage", "summary_label"],
    )
    write_csv(args.output / "unmapped_section_lines.csv", unmapped_section_rows, ["locator", "folio_id", "reason"])
    write_csv(args.output / "unmapped_currier_lines.csv", unmapped_currier_rows, ["locator", "folio_id", "currier_language", "reason"])
    write_csv(
        args.output / "section_summary_recomputed.csv",
        section_summary,
        [
            "section",
            "line_count",
            "token_count",
            "unique_token_count",
            "type_token_ratio",
            "token_entropy_bits",
            "mean_token_length",
            "median_token_length",
        ],
    )

    historical_exp003_mean = None
    if args.exp003_observed.exists():
        with args.exp003_observed.open("r", encoding="utf-8") as handle:
            exp003_rows = json.load(handle)
        exp003_values = [float(row["jensen_shannon_divergence_bits"]) for row in exp003_rows]
        historical_exp003_mean = sum(exp003_values) / len(exp003_values) if exp003_values else None

    run_summary = {
        "experiment": "exp-006_currier-section-interaction-control",
        "run_date_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "script": "scripts/exp006_currier_section_interaction_control.py",
        "input": args.input,
        "input_sha256": file_sha256(args.input),
        "section_metadata": args.section_metadata,
        "section_metadata_created_by_script": section_metadata_created,
        "currier_metadata": args.currier_metadata,
        "currier_metadata_created_by_script": currier_metadata_created,
        "metadata_source": "IVTFF page-header metadata in data/raw/LSI_ivtff_0d.txt; $I for section labels and $L for Currier language; source documentation https://www.voynich.nu/transcr.html",
        "output": args.output,
        "parameters": {
            "transcriber_code": args.transcriber_code,
            "iterations": args.iterations,
            "seed": args.seed,
            "min_tokens_per_group": args.min_tokens_per_group,
            "min_count": args.min_count,
            "top_n": args.top_n,
            "parser_policy": "cleaned exp-002b policy: remove comments, replace inline <...> markup with token boundaries, split on periods/commas/whitespace, lowercase and strip non-ASCII letters",
            "currier_mapping_policy": "Use documented IVTFF page-header $L labels; treat blank, ? and - as unmapped for Currier-controlled comparisons.",
            "optional_controls": "Matched-size within-Currier resampling and nested null controls were not implemented in this run.",
        },
        "parse_stats": parse_stats,
        "metadata_coverage": metadata_coverage,
        "section_summary_recomputed": section_summary,
        "currier_summary": currier_summary,
        "historical_exp003_mean_pairwise_section_jsd_bits": historical_exp003_mean,
        "recomputed_section_mean_pairwise_jsd_bits": mean_distance(section_distances),
        "currier_only_mean_pairwise_jsd_bits": mean_distance(currier_distances),
        "section_within_currier_mean_pairwise_jsd_bits": mean_distance(section_within_rows),
        "currier_within_section_mean_pairwise_jsd_bits": mean_distance(currier_within_rows),
        "signal_attribution_summary": signal_summary,
        "artifacts": [
            "run_summary.json",
            "metadata_coverage.json",
            "section_currier_contingency_lines.csv",
            "section_currier_contingency_tokens.csv",
            "section_currier_percentages.csv",
            "currier_summary.csv",
            "currier_token_counts.csv",
            "currier_token_shares.csv",
            "top_tokens_by_currier.csv",
            "pairwise_currier_distances.csv",
            "section_only_recomputed_distances.csv",
            "section_within_currier_groups.csv",
            "section_within_currier_distances.csv",
            "currier_within_section_groups.csv",
            "currier_within_section_distances.csv",
            "signal_attribution_summary.csv",
            "unmapped_section_lines.csv",
            "unmapped_currier_lines.csv",
            "section_summary_recomputed.csv",
        ],
    }
    write_json(args.output / "run_summary.json", run_summary)

    print(
        json.dumps(
            {
                "selected_lines": parse_stats.get("selected_lines", 0),
                "both_mapped_lines": parse_stats.get("both_mapped_selected_lines", 0),
                "sections": sorted(section_tokens),
                "currier_categories": sorted(currier_tokens),
                "recomputed_section_mean_jsd_bits": mean_distance(section_distances),
                "currier_only_mean_jsd_bits": mean_distance(currier_distances),
                "section_within_currier_mean_jsd_bits": mean_distance(section_within_rows),
                "signal_label": next(row["summary_label"] for row in signal_summary if row["comparison_level"] == "section_within_currier"),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
