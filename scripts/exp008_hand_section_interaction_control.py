"""Hand-section interaction controls for exp-008.

This script reuses the cleaned IVTFF parser policy from exp-002b and the
section mapping pattern used by exp-003 through exp-007. It uses documented
IVTFF page-header $H labels as hand metadata and reports unmapped hand labels
instead of inferring them from section or Currier categories.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
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

UNKNOWN_HAND_LABELS = {"", "?", "-"}
UNKNOWN_CURRIER_LABELS = {"", "?", "-"}
EXP003_REFERENCE_MEAN_JSD = 0.5554700431523788


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: object) -> object:
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    return value


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(json_ready(value), handle, indent=2)
        handle.write("\n")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


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
                    "note": "Derived from IVTFF page header metadata. $I supplies illustration type, $L supplies Currier language, and $H supplies Currier hand.",
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


def derive_hand_metadata(input_path: Path, metadata_path: Path) -> list[dict[str, str]]:
    rows = [
        {
            "folio_id": row["folio_id"],
            "hand": row["currier_hand"],
            "source": row["source"],
            "note": "Derived from IVTFF page-header $H Currier hand metadata. Blank, ? and - labels are treated as unmapped for hand-controlled comparisons.",
        }
        for row in parse_page_headers(input_path)
    ]
    write_csv(metadata_path, rows, ["folio_id", "hand", "source", "note"])
    return rows


def load_csv_by_key(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


def load_section_metadata(input_path: Path, metadata_path: Path) -> tuple[dict[str, dict[str, str]], bool]:
    if metadata_path.exists():
        return load_csv_by_key(metadata_path, "folio_id"), False
    rows = derive_section_metadata(input_path, metadata_path)
    return {row["folio_id"]: row for row in rows}, True


def load_hand_metadata(input_path: Path, metadata_path: Path) -> tuple[dict[str, dict[str, str]], bool]:
    if metadata_path.exists():
        return load_csv_by_key(metadata_path, "folio_id"), False
    rows = derive_hand_metadata(input_path, metadata_path)
    return {row["folio_id"]: row for row in rows}, True


def load_optional_currier_metadata(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    return load_csv_by_key(path, "folio_id")


def valid_label(label: str, unknowns: set[str]) -> bool:
    return label.strip() not in unknowns


def parse_selected_lines(
    input_path: Path,
    transcriber_code: str,
    section_metadata: dict[str, dict[str, str]],
    hand_metadata: dict[str, dict[str, str]],
    currier_metadata: dict[str, dict[str, str]],
) -> tuple[list[dict[str, object]], list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    line_rows: list[dict[str, object]] = []
    unmapped_section_rows: list[dict[str, str]] = []
    unmapped_hand_rows: list[dict[str, str]] = []
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
            hand_row = hand_metadata.get(folio_id)
            currier_row = currier_metadata.get(folio_id, {})
            section = section_row.get("section", "") if section_row else ""
            raw_hand = hand_row.get("hand", "") if hand_row else ""
            raw_currier = currier_row.get("currier_language", "") if currier_row else section_row.get("currier_language", "") if section_row else ""
            valid_section = bool(section_row and section and section != "unknown")
            valid_hand = bool(hand_row and valid_label(raw_hand, UNKNOWN_HAND_LABELS))
            valid_currier = bool(valid_label(raw_currier, UNKNOWN_CURRIER_LABELS))

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

            if valid_hand:
                stats["hand_mapped_selected_lines"] += 1
            else:
                stats["unmapped_hand_selected_lines"] += 1
                reason = "folio_id missing from hand metadata"
                if hand_row and raw_hand in UNKNOWN_HAND_LABELS:
                    reason = f"hand label is {raw_hand or 'blank'}"
                unmapped_hand_rows.append({"locator": locator, "folio_id": folio_id, "hand": raw_hand, "reason": reason})

            if valid_section and valid_hand:
                stats["both_mapped_selected_lines"] += 1

            line_rows.append(
                {
                    "locator": locator,
                    "folio_id": folio_id,
                    "section": section,
                    "hand": raw_hand if valid_hand else "",
                    "raw_hand": raw_hand,
                    "currier_language": raw_currier if valid_currier else "",
                    "raw_currier_language": raw_currier,
                    "tokens": tokens,
                    "section_mapped": valid_section,
                    "hand_mapped": valid_hand,
                    "currier_mapped": valid_currier,
                    "both_mapped": valid_section and valid_hand,
                }
            )

    public_stats = {key: value for key, value in stats.items() if not key.startswith("angle_tag::")}
    public_stats["unique_angle_tag_forms_removed"] = sum(1 for key in stats if key.startswith("angle_tag::"))
    return line_rows, unmapped_section_rows, unmapped_hand_rows, public_stats


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
    return [(left, right) for index, left in enumerate(names) for right in names[index + 1 :]]


def quantile(values: list[float], probability: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def summarize_distribution(values: list[float]) -> dict[str, float]:
    mean_value = sum(values) / len(values) if values else 0.0
    variance = sum((value - mean_value) ** 2 for value in values) / len(values) if values else 0.0
    return {
        "mean": mean_value,
        "std": math.sqrt(variance),
        "median": median(values) if values else 0.0,
        "q025": quantile(values, 0.025),
        "q975": quantile(values, 0.975),
    }


def empirical_p_value(values: list[float], observed: float) -> float:
    return (1 + sum(1 for value in values if value >= observed)) / (len(values) + 1)


def empirical_percentile(values: list[float], observed: float) -> float:
    if not values:
        return 0.0
    return sum(1 for value in values if value <= observed) / len(values)


def group_tokens(line_rows: list[dict[str, object]], key: str, mapped_key: str) -> tuple[dict[str, list[str]], Counter[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    line_counts: Counter[str] = Counter()
    for row in line_rows:
        if not row[mapped_key]:
            continue
        tokens = list(row["tokens"])
        if not tokens:
            continue
        label = str(row[key])
        grouped[label].extend(tokens)
        line_counts[label] += 1
    return dict(grouped), line_counts


def summary_rows_for_groups(grouped_tokens: dict[str, list[str]], line_counts: Counter[str], label_name: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for label in sorted(grouped_tokens):
        tokens = grouped_tokens[label]
        counter = Counter(tokens)
        rows.append(
            {
                label_name: label,
                "line_count": line_counts[label],
                "token_count": len(tokens),
                "unique_token_count": len(counter),
                "type_token_ratio": len(counter) / len(tokens) if tokens else 0.0,
                "token_entropy_bits": entropy(counter),
                "mean_token_length": sum(len(token) for token in tokens) / len(tokens) if tokens else 0.0,
            }
        )
    return rows


def token_frequency_rows(grouped_tokens: dict[str, list[str]], group_name: str, top_n: int) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    count_rows: list[dict[str, object]] = []
    share_rows: list[dict[str, object]] = []
    top_rows: list[dict[str, object]] = []
    for group in sorted(grouped_tokens):
        counter = Counter(grouped_tokens[group])
        total = sum(counter.values())
        for token, count in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
            row = {group_name: group, "token": token, "count": count, "share": count / total if total else 0.0}
            count_rows.append(row)
            share_rows.append(row)
        for rank, (token, count) in enumerate(counter.most_common(top_n), start=1):
            top_rows.append({group_name: group, "rank": rank, "token": token, "count": count, "share": count / total if total else 0.0})
    return count_rows, share_rows, top_rows


def filter_groups_by_tokens(grouped_tokens: dict[str, list[str]], min_tokens: int) -> dict[str, list[str]]:
    return {label: tokens for label, tokens in grouped_tokens.items() if len(tokens) >= min_tokens}


def pairwise_distance_rows(
    grouped_tokens: dict[str, list[str]],
    label_name: str,
    output_a: str,
    output_b: str,
) -> list[dict[str, object]]:
    counters = {label: Counter(tokens) for label, tokens in grouped_tokens.items()}
    rows: list[dict[str, object]] = []
    for left, right in pairwise_names(sorted(counters)):
        rows.append(
            {
                output_a: left,
                output_b: right,
                f"token_count_{label_name}_a": len(grouped_tokens[left]),
                f"token_count_{label_name}_b": len(grouped_tokens[right]),
                "jensen_shannon_divergence_bits": jensen_shannon_divergence(counters[left], counters[right]),
            }
        )
    return rows


def mean_distance(rows: list[dict[str, object]]) -> float | None:
    values = [float(row["jensen_shannon_divergence_bits"]) for row in rows]
    return sum(values) / len(values) if values else None


def build_section_hand_counts(
    line_rows: list[dict[str, object]],
) -> tuple[Counter[tuple[str, str]], Counter[tuple[str, str]], Counter[str], Counter[str], Counter[str], Counter[str]]:
    line_counts: Counter[tuple[str, str]] = Counter()
    token_counts: Counter[tuple[str, str]] = Counter()
    section_lines: Counter[str] = Counter()
    section_tokens: Counter[str] = Counter()
    hand_lines: Counter[str] = Counter()
    hand_tokens: Counter[str] = Counter()
    for row in line_rows:
        tokens = list(row["tokens"])
        if row["section_mapped"]:
            section = str(row["section"])
            section_lines[section] += 1
            section_tokens[section] += len(tokens)
        if row["hand_mapped"]:
            hand = str(row["hand"])
            hand_lines[hand] += 1
            hand_tokens[hand] += len(tokens)
        if row["both_mapped"]:
            section = str(row["section"])
            hand = str(row["hand"])
            line_counts[(section, hand)] += 1
            token_counts[(section, hand)] += len(tokens)
    return line_counts, token_counts, section_lines, section_tokens, hand_lines, hand_tokens


def section_hand_tables(
    sections: list[str],
    hands: list[str],
    line_counts: Counter[tuple[str, str]],
    token_counts: Counter[tuple[str, str]],
    section_tokens: Counter[str],
    hand_tokens: Counter[str],
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    line_rows: list[dict[str, object]] = []
    token_rows: list[dict[str, object]] = []
    percentage_rows: list[dict[str, object]] = []
    for section in sections:
        for hand in hands:
            line_count = line_counts[(section, hand)]
            token_count = token_counts[(section, hand)]
            line_rows.append({"section": section, "hand": hand, "line_count": line_count})
            token_rows.append({"section": section, "hand": hand, "token_count": token_count})
            percentage_rows.append(
                {
                    "section": section,
                    "hand": hand,
                    "line_count": line_count,
                    "token_count": token_count,
                    "percent_of_section_tokens": token_count / section_tokens[section] if section_tokens[section] else 0.0,
                    "percent_of_hand_tokens": token_count / hand_tokens[hand] if hand_tokens[hand] else 0.0,
                }
            )
    return line_rows, token_rows, percentage_rows


def nested_groups(line_rows: list[dict[str, object]], outer: str, inner: str) -> tuple[dict[str, dict[str, list[str]]], Counter[tuple[str, str]]]:
    groups: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    line_counts: Counter[tuple[str, str]] = Counter()
    for row in line_rows:
        if not row["both_mapped"]:
            continue
        tokens = list(row["tokens"])
        if not tokens:
            continue
        outer_label = str(row[outer])
        inner_label = str(row[inner])
        groups[outer_label][inner_label].extend(tokens)
        line_counts[(outer_label, inner_label)] += 1
    return {outer_label: dict(inner_groups) for outer_label, inner_groups in groups.items()}, line_counts


def nested_pairwise_distances(
    groups: dict[str, dict[str, list[str]]],
    line_counts: Counter[tuple[str, str]],
    outer_name: str,
    inner_a_name: str,
    inner_b_name: str,
    min_tokens: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, list[str]]]]:
    rows: list[dict[str, object]] = []
    valid_rows: list[dict[str, object]] = []
    valid_groups_for_null: dict[str, list[str]] = {}
    for outer_label in sorted(groups):
        valid_inner = {inner_label: tokens for inner_label, tokens in groups[outer_label].items() if len(tokens) >= min_tokens}
        excluded_inner = {inner_label: tokens for inner_label, tokens in groups[outer_label].items() if len(tokens) < min_tokens}
        valid_groups_for_null[outer_label] = sorted(valid_inner)
        for inner_label, tokens in sorted(valid_inner.items()):
            valid_rows.append(
                {
                    outer_name: outer_label,
                    "inner_group": inner_label,
                    "line_count": line_counts[(outer_label, inner_label)],
                    "token_count": len(tokens),
                    "min_tokens_per_group": min_tokens,
                    "status": "valid",
                }
            )
        for inner_label, tokens in sorted(excluded_inner.items()):
            valid_rows.append(
                {
                    outer_name: outer_label,
                    "inner_group": inner_label,
                    "line_count": line_counts[(outer_label, inner_label)],
                    "token_count": len(tokens),
                    "min_tokens_per_group": min_tokens,
                    "status": "excluded_below_min_tokens",
                }
            )
        counters = {inner_label: Counter(tokens) for inner_label, tokens in valid_inner.items()}
        for left, right in pairwise_names(sorted(counters)):
            rows.append(
                {
                    outer_name: outer_label,
                    inner_a_name: left,
                    inner_b_name: right,
                    "token_count_a": len(valid_inner[left]),
                    "token_count_b": len(valid_inner[right]),
                    "jensen_shannon_divergence_bits": jensen_shannon_divergence(counters[left], counters[right]),
                }
            )
    return rows, valid_rows, valid_groups_for_null


def section_label_null_within_hands(
    section_by_hand_groups: dict[str, dict[str, list[str]]],
    min_tokens: int,
    iterations: int,
    seed: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    summary_rows: list[dict[str, object]] = []
    iteration_rows: list[dict[str, object]] = []
    pairwise_rows: list[dict[str, object]] = []

    for hand_index, hand in enumerate(sorted(section_by_hand_groups)):
        valid_sections = {
            section: tokens
            for section, tokens in section_by_hand_groups[hand].items()
            if len(tokens) >= min_tokens
        }
        section_names = sorted(valid_sections)
        if len(section_names) < 3:
            summary_rows.append(
                {
                    "hand": hand,
                    "valid_section_count": len(section_names),
                    "valid_sections": ";".join(section_names),
                    "observed_mean_jsd_bits": "",
                    "null_mean_jsd_mean_bits": "",
                    "null_mean_jsd_std_bits": "",
                    "null_mean_jsd_median_bits": "",
                    "null_mean_jsd_q025_bits": "",
                    "null_mean_jsd_q975_bits": "",
                    "observed_minus_null_mean_bits": "",
                    "empirical_percentile": "",
                    "empirical_p_value": "",
                    "conclusion_label": "insufficient_data",
                    "signal_label": "insufficient_data",
                }
            )
            continue

        observed = mean_pairwise_jsd(valid_sections)
        sizes = [len(valid_sections[section]) for section in section_names]
        pooled = [token for section in section_names for token in valid_sections[section]]
        rng = random.Random(seed + 10000 + hand_index)
        null_values: list[float] = []
        for iteration in range(1, iterations + 1):
            shuffled = pooled[:]
            rng.shuffle(shuffled)
            offset = 0
            pseudo_groups: dict[str, list[str]] = {}
            for section, size in zip(section_names, sizes):
                pseudo_groups[section] = shuffled[offset : offset + size]
                offset += size
            null_value = mean_pairwise_jsd(pseudo_groups)
            null_values.append(null_value)
            iteration_rows.append({"hand": hand, "iteration": iteration, "null_mean_jsd_bits": null_value})

        summary = summarize_distribution(null_values)
        conclusion = null_conclusion_label(observed, summary)
        summary_rows.append(
            {
                "hand": hand,
                "valid_section_count": len(section_names),
                "valid_sections": ";".join(section_names),
                "observed_mean_jsd_bits": observed,
                "null_mean_jsd_mean_bits": summary["mean"],
                "null_mean_jsd_std_bits": summary["std"],
                "null_mean_jsd_median_bits": summary["median"],
                "null_mean_jsd_q025_bits": summary["q025"],
                "null_mean_jsd_q975_bits": summary["q975"],
                "observed_minus_null_mean_bits": observed - summary["mean"],
                "empirical_percentile": empirical_percentile(null_values, observed),
                "empirical_p_value": empirical_p_value(null_values, observed),
                "conclusion_label": conclusion,
                "signal_label": signal_label_from_null_conclusion(conclusion),
            }
        )

        pair_index = 0
        for left, right in pairwise_names(section_names):
            pair_index += 1
            observed_pair = jensen_shannon_divergence(Counter(valid_sections[left]), Counter(valid_sections[right]))
            pooled_pair = valid_sections[left] + valid_sections[right]
            size_left = len(valid_sections[left])
            rng_pair = random.Random(seed + 20000 + hand_index * 1000 + pair_index)
            pair_null_values: list[float] = []
            for _ in range(iterations):
                shuffled_pair = pooled_pair[:]
                rng_pair.shuffle(shuffled_pair)
                pair_null_values.append(
                    jensen_shannon_divergence(
                        Counter(shuffled_pair[:size_left]),
                        Counter(shuffled_pair[size_left:]),
                    )
                )
            pair_summary = summarize_distribution(pair_null_values)
            pair_conclusion = null_conclusion_label(observed_pair, pair_summary)
            pairwise_rows.append(
                {
                    "hand": hand,
                    "section_a": left,
                    "section_b": right,
                    "token_count_a": len(valid_sections[left]),
                    "token_count_b": len(valid_sections[right]),
                    "observed_jsd_bits": observed_pair,
                    "null_jsd_mean_bits": pair_summary["mean"],
                    "null_jsd_std_bits": pair_summary["std"],
                    "null_jsd_median_bits": pair_summary["median"],
                    "null_jsd_q025_bits": pair_summary["q025"],
                    "null_jsd_q975_bits": pair_summary["q975"],
                    "observed_minus_null_mean_bits": observed_pair - pair_summary["mean"],
                    "empirical_percentile": empirical_percentile(pair_null_values, observed_pair),
                    "empirical_p_value": empirical_p_value(pair_null_values, observed_pair),
                    "conclusion_label": pair_conclusion,
                }
            )
    return summary_rows, iteration_rows, pairwise_rows


def mean_pairwise_jsd(groups: dict[str, list[str]]) -> float:
    counters = {label: Counter(tokens) for label, tokens in groups.items()}
    values = [
        jensen_shannon_divergence(counters[left], counters[right])
        for left, right in pairwise_names(sorted(counters))
    ]
    return sum(values) / len(values) if values else 0.0


def null_conclusion_label(observed: float, summary: dict[str, float]) -> str:
    if observed > summary["q975"]:
        return "above_null_97_5"
    if observed < summary["mean"]:
        return "below_null_mean"
    return "within_null_interval"


def signal_label_from_null_conclusion(conclusion: str) -> str:
    if conclusion == "above_null_97_5":
        return "section_signal_above_null_within_hand"
    if conclusion == "below_null_mean":
        return "section_signal_below_null_within_hand"
    if conclusion == "insufficient_data":
        return "insufficient_data"
    return "section_signal_within_null_within_hand"


def dominance_counts(sections: list[str], hands: list[str], token_counts: Counter[tuple[str, str]], section_tokens: Counter[str]) -> tuple[int, list[dict[str, object]]]:
    dominant_rows: list[dict[str, object]] = []
    dominated = 0
    for section in sections:
        if section_tokens[section] == 0:
            continue
        best_hand = ""
        best_tokens = 0
        for hand in hands:
            count = token_counts[(section, hand)]
            if count > best_tokens:
                best_hand = hand
                best_tokens = count
        share = best_tokens / section_tokens[section]
        if share >= 0.9:
            dominated += 1
        dominant_rows.append(
            {
                "section": section,
                "dominant_hand": best_hand,
                "dominant_hand_token_count": best_tokens,
                "section_token_count": section_tokens[section],
                "dominant_hand_token_share": share,
                "dominant_at_90_percent": share >= 0.9,
            }
        )
    return dominated, dominant_rows


def signal_label(
    section_mean: float | None,
    section_within_hand_mean: float | None,
    valid_within_pairs: int,
    full_pair_count: int,
    dominated_section_count: int,
    section_count: int,
) -> str:
    if section_mean is None or section_within_hand_mean is None or valid_within_pairs == 0:
        return "insufficient_data"
    if section_count and dominated_section_count >= math.ceil(section_count / 2) and valid_within_pairs < full_pair_count:
        return "section_hand_strongly_confounded"
    if section_within_hand_mean >= 0.8 * section_mean:
        return "section_signal_preserved_within_hand"
    return "section_signal_reduced_within_hand"


def section_currier_hand_coverage(line_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    counts: Counter[tuple[str, str, str]] = Counter()
    token_counts: Counter[tuple[str, str, str]] = Counter()
    for row in line_rows:
        if not (row["section_mapped"] and row["hand_mapped"] and row["currier_mapped"]):
            continue
        key = (str(row["section"]), str(row["currier_language"]), str(row["hand"]))
        counts[key] += 1
        token_counts[key] += len(list(row["tokens"]))
    return [
        {
            "section": section,
            "currier_language": currier,
            "hand": hand,
            "line_count": counts[(section, currier, hand)],
            "token_count": token_counts[(section, currier, hand)],
        }
        for section, currier, hand in sorted(counts)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run exp-008 hand-section interaction controls.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--section-metadata", default=Path("data/metadata/folio_sections.csv"), type=Path)
    parser.add_argument("--hand-metadata", default=Path("data/metadata/folio_hands.csv"), type=Path)
    parser.add_argument("--currier-metadata", default=Path("data/metadata/folio_currier.csv"), type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--transcriber-code", default="H")
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--min-tokens-per-group", type=int, default=100)
    parser.add_argument("--min-count", type=int, default=10)
    parser.add_argument("--top-n", type=int, default=30)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    section_metadata, section_metadata_created = load_section_metadata(args.input, args.section_metadata)
    hand_metadata, hand_metadata_created = load_hand_metadata(args.input, args.hand_metadata)
    currier_metadata = load_optional_currier_metadata(args.currier_metadata)

    line_rows, unmapped_section_rows, unmapped_hand_rows, parse_stats = parse_selected_lines(
        args.input,
        args.transcriber_code,
        section_metadata,
        hand_metadata,
        currier_metadata,
    )

    section_hand_line_counts, section_hand_token_counts, section_line_counts, section_token_counts, hand_line_counts, hand_token_counts = build_section_hand_counts(line_rows)
    sections = sorted(section_token_counts)
    hands = sorted(hand_token_counts)
    section_hand_line_rows, section_hand_token_rows, section_hand_percentage_rows = section_hand_tables(
        sections,
        hands,
        section_hand_line_counts,
        section_hand_token_counts,
        section_token_counts,
        hand_token_counts,
    )

    section_groups, section_lines = group_tokens(line_rows, "section", "section_mapped")
    hand_groups, hand_lines = group_tokens(line_rows, "hand", "hand_mapped")
    valid_hand_groups = filter_groups_by_tokens(hand_groups, args.min_tokens_per_group)
    section_distance_rows = pairwise_distance_rows(section_groups, "section", "section_a", "section_b")
    hand_distance_rows = pairwise_distance_rows(valid_hand_groups, "hand", "hand_a", "hand_b")

    hand_summary_rows = summary_rows_for_groups(hand_groups, hand_lines, "hand")
    hand_token_count_rows, hand_token_share_rows, top_tokens_by_hand_rows = token_frequency_rows(hand_groups, "hand", args.top_n)

    section_by_hand_groups, section_by_hand_line_counts = nested_groups(line_rows, "hand", "section")
    hand_by_section_groups, hand_by_section_line_counts = nested_groups(line_rows, "section", "hand")
    section_within_hand_rows, section_within_hand_group_rows, valid_sections_by_hand = nested_pairwise_distances(
        section_by_hand_groups,
        section_by_hand_line_counts,
        "hand",
        "section_a",
        "section_b",
        args.min_tokens_per_group,
    )
    hand_within_section_rows, hand_within_section_group_rows, valid_hands_by_section = nested_pairwise_distances(
        hand_by_section_groups,
        hand_by_section_line_counts,
        "section",
        "hand_a",
        "hand_b",
        args.min_tokens_per_group,
    )
    within_hand_null_summary_rows, within_hand_null_iteration_rows, pairwise_within_hand_null_rows = section_label_null_within_hands(
        section_by_hand_groups,
        args.min_tokens_per_group,
        args.iterations,
        args.seed,
    )

    section_only_mean = mean_distance(section_distance_rows)
    hand_only_mean = mean_distance(hand_distance_rows)
    section_within_hand_mean = mean_distance(section_within_hand_rows)
    hand_within_section_mean = mean_distance(hand_within_section_rows)
    full_pair_count = len(pairwise_names(sections))
    dominated_section_count, dominant_section_rows = dominance_counts(sections, hands, section_hand_token_counts, section_token_counts)
    overall_label = signal_label(
        section_only_mean,
        section_within_hand_mean,
        len(section_within_hand_rows),
        full_pair_count,
        dominated_section_count,
        len(sections),
    )

    null_above_count = sum(1 for row in within_hand_null_summary_rows if row["signal_label"] == "section_signal_above_null_within_hand")
    null_feasible_count = sum(1 for row in within_hand_null_summary_rows if row["signal_label"] != "insufficient_data")
    signal_attribution_rows = [
        {
            "comparison_level": "section_only_recomputed",
            "mean_jsd_bits": section_only_mean if section_only_mean is not None else "",
            "valid_comparison_count": len(section_distance_rows),
            "token_coverage": sum(section_token_counts.values()),
            "reference_mean_jsd_bits": EXP003_REFERENCE_MEAN_JSD,
            "notes": "Internal exp-008 replication check of full section distances.",
        },
        {
            "comparison_level": "hand_only",
            "mean_jsd_bits": hand_only_mean if hand_only_mean is not None else "",
            "valid_comparison_count": len(hand_distance_rows),
            "token_coverage": sum(hand_token_counts[hand] for hand in valid_hand_groups),
            "reference_mean_jsd_bits": "",
            "notes": f"Only hand groups with at least {args.min_tokens_per_group} tokens are used for pairwise distances.",
        },
        {
            "comparison_level": "section_within_hand",
            "mean_jsd_bits": section_within_hand_mean if section_within_hand_mean is not None else "",
            "valid_comparison_count": len(section_within_hand_rows),
            "token_coverage": sum(len(section_by_hand_groups[hand][section]) for hand in section_by_hand_groups for section in valid_sections_by_hand.get(hand, [])),
            "reference_mean_jsd_bits": "",
            "notes": "Pairwise section JSD computed inside each hand category.",
        },
        {
            "comparison_level": "hand_within_section",
            "mean_jsd_bits": hand_within_section_mean if hand_within_section_mean is not None else "",
            "valid_comparison_count": len(hand_within_section_rows),
            "token_coverage": sum(len(hand_by_section_groups[section][hand]) for section in hand_by_section_groups for hand in valid_hands_by_section.get(section, [])),
            "reference_mean_jsd_bits": "",
            "notes": "Pairwise hand JSD computed inside each section where enough hand groups exist.",
        },
        {
            "comparison_level": "within_hand_section_label_null",
            "mean_jsd_bits": "",
            "valid_comparison_count": null_feasible_count,
            "token_coverage": "",
            "reference_mean_jsd_bits": "",
            "notes": f"{null_above_count} of {null_feasible_count} feasible hand categories were above their 97.5% section-label null quantile.",
        },
        {
            "comparison_level": "overall",
            "mean_jsd_bits": "",
            "valid_comparison_count": len(section_within_hand_rows),
            "token_coverage": sum(hand_token_counts.values()),
            "reference_mean_jsd_bits": "",
            "notes": overall_label,
        },
    ]

    metadata_coverage = {
        "input_line_count": parse_stats.get("input_lines", 0),
        "selected_transcriber_code": args.transcriber_code,
        "selected_line_count": parse_stats.get("selected_lines", 0),
        "non_empty_selected_line_count": parse_stats.get("non_empty_selected_lines", 0),
        "section_mapped_line_count": parse_stats.get("section_mapped_selected_lines", 0),
        "unmapped_section_line_count": parse_stats.get("unmapped_section_selected_lines", 0),
        "hand_mapped_line_count": parse_stats.get("hand_mapped_selected_lines", 0),
        "unmapped_hand_line_count": parse_stats.get("unmapped_hand_selected_lines", 0),
        "both_mapped_line_count": parse_stats.get("both_mapped_selected_lines", 0),
        "section_count": len(sections),
        "hand_category_count": len(hands),
        "section_names": sections,
        "hand_category_names": hands,
        "unknown_hand_labels_treated_as_unmapped": sorted(UNKNOWN_HAND_LABELS),
        "min_tokens_per_group": args.min_tokens_per_group,
        "dominant_section_count_at_90_percent": dominated_section_count,
        "section_only_recomputed_mean_jsd_bits": section_only_mean,
        "exp003_reference_mean_jsd_bits": EXP003_REFERENCE_MEAN_JSD,
        "exp003_reference_difference_bits": section_only_mean - EXP003_REFERENCE_MEAN_JSD if section_only_mean is not None else "",
        "overall_signal_label": overall_label,
    }

    write_json(args.output / "metadata_coverage.json", metadata_coverage)
    write_csv(args.output / "section_hand_contingency_lines.csv", section_hand_line_rows, ["section", "hand", "line_count"])
    write_csv(args.output / "section_hand_contingency_tokens.csv", section_hand_token_rows, ["section", "hand", "token_count"])
    write_csv(args.output / "section_hand_percentages.csv", section_hand_percentage_rows, ["section", "hand", "line_count", "token_count", "percent_of_section_tokens", "percent_of_hand_tokens"])
    write_csv(args.output / "dominant_hand_by_section.csv", dominant_section_rows, ["section", "dominant_hand", "dominant_hand_token_count", "section_token_count", "dominant_hand_token_share", "dominant_at_90_percent"])
    write_csv(args.output / "hand_summary.csv", hand_summary_rows, ["hand", "line_count", "token_count", "unique_token_count", "type_token_ratio", "token_entropy_bits", "mean_token_length"])
    write_csv(args.output / "hand_token_counts.csv", hand_token_count_rows, ["hand", "token", "count", "share"])
    write_csv(args.output / "hand_token_shares.csv", hand_token_share_rows, ["hand", "token", "count", "share"])
    write_csv(args.output / "top_tokens_by_hand.csv", top_tokens_by_hand_rows, ["hand", "rank", "token", "count", "share"])
    write_csv(args.output / "pairwise_hand_distances.csv", hand_distance_rows, ["hand_a", "hand_b", "token_count_hand_a", "token_count_hand_b", "jensen_shannon_divergence_bits"])
    write_csv(args.output / "section_only_recomputed_distances.csv", section_distance_rows, ["section_a", "section_b", "token_count_section_a", "token_count_section_b", "jensen_shannon_divergence_bits"])
    write_csv(args.output / "section_within_hand_distances.csv", section_within_hand_rows, ["hand", "section_a", "section_b", "token_count_a", "token_count_b", "jensen_shannon_divergence_bits"])
    write_csv(args.output / "section_within_hand_groups.csv", section_within_hand_group_rows, ["hand", "inner_group", "line_count", "token_count", "min_tokens_per_group", "status"])
    write_csv(args.output / "hand_within_section_distances.csv", hand_within_section_rows, ["section", "hand_a", "hand_b", "token_count_a", "token_count_b", "jensen_shannon_divergence_bits"])
    write_csv(args.output / "hand_within_section_groups.csv", hand_within_section_group_rows, ["section", "inner_group", "line_count", "token_count", "min_tokens_per_group", "status"])
    write_csv(args.output / "within_hand_null_summary.csv", within_hand_null_summary_rows, ["hand", "valid_section_count", "valid_sections", "observed_mean_jsd_bits", "null_mean_jsd_mean_bits", "null_mean_jsd_std_bits", "null_mean_jsd_median_bits", "null_mean_jsd_q025_bits", "null_mean_jsd_q975_bits", "observed_minus_null_mean_bits", "empirical_percentile", "empirical_p_value", "conclusion_label", "signal_label"])
    write_json(args.output / "within_hand_null_summary.json", within_hand_null_summary_rows)
    write_csv(args.output / "within_hand_null_iterations.csv", within_hand_null_iteration_rows, ["hand", "iteration", "null_mean_jsd_bits"])
    write_csv(args.output / "pairwise_within_hand_null_control.csv", pairwise_within_hand_null_rows, ["hand", "section_a", "section_b", "token_count_a", "token_count_b", "observed_jsd_bits", "null_jsd_mean_bits", "null_jsd_std_bits", "null_jsd_median_bits", "null_jsd_q025_bits", "null_jsd_q975_bits", "observed_minus_null_mean_bits", "empirical_percentile", "empirical_p_value", "conclusion_label"])
    write_json(args.output / "pairwise_within_hand_null_control.json", pairwise_within_hand_null_rows)
    write_csv(args.output / "signal_attribution_summary.csv", signal_attribution_rows, ["comparison_level", "mean_jsd_bits", "valid_comparison_count", "token_coverage", "reference_mean_jsd_bits", "notes"])
    write_csv(args.output / "unmapped_section_lines.csv", unmapped_section_rows, ["locator", "folio_id", "reason"])
    write_csv(args.output / "unmapped_hand_lines.csv", unmapped_hand_rows, ["locator", "folio_id", "hand", "reason"])

    section_currier_hand_rows = section_currier_hand_coverage(line_rows)
    write_csv(args.output / "section_currier_hand_coverage.csv", section_currier_hand_rows, ["section", "currier_language", "hand", "line_count", "token_count"])

    run_summary = {
        "experiment": "exp-008_hand-section-interaction-control",
        "run_date_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "script": "scripts/exp008_hand_section_interaction_control.py",
        "input": args.input,
        "input_sha256": file_sha256(args.input),
        "section_metadata": args.section_metadata,
        "section_metadata_created_by_script": section_metadata_created,
        "hand_metadata": args.hand_metadata,
        "hand_metadata_created_by_script": hand_metadata_created,
        "currier_metadata": args.currier_metadata if args.currier_metadata.exists() else "",
        "metadata_source": "IVTFF page-header metadata in data/raw/LSI_ivtff_0d.txt; $I for section labels, $H for Currier hand, and optional $L for Currier coverage planning; source documentation https://www.voynich.nu/transcr.html",
        "output": args.output,
        "parameters": {
            "transcriber_code": args.transcriber_code,
            "iterations": args.iterations,
            "seed": args.seed,
            "min_tokens_per_group": args.min_tokens_per_group,
            "min_count": args.min_count,
            "top_n": args.top_n,
            "parser_policy": "cleaned exp-002b policy: remove comments, replace inline <...> markup with token boundaries, split on periods/commas/whitespace, lowercase and strip non-ASCII letters",
            "hand_mapping_policy": "Use documented IVTFF page-header $H labels; treat blank, ? and - as unmapped for hand-controlled comparisons.",
            "within_hand_section_label_null": "pool valid section-group tokens inside each hand category and randomly reassign section labels preserving observed group sizes",
            "optional_matched_size_within_hand_resampling": "not implemented in this run",
            "optional_hand_label_null_within_sections": "not implemented in this run",
            "optional_section_currier_hand_summary": "implemented as coverage only; no three-way model was run",
        },
        "parse_stats": parse_stats,
        "metadata_coverage": metadata_coverage,
        "valid_sections_by_hand": valid_sections_by_hand,
        "valid_hands_by_section": valid_hands_by_section,
        "within_hand_null_summary": within_hand_null_summary_rows,
        "signal_attribution_summary": signal_attribution_rows,
        "artifacts": [
            "run_summary.json",
            "metadata_coverage.json",
            "section_hand_contingency_lines.csv",
            "section_hand_contingency_tokens.csv",
            "section_hand_percentages.csv",
            "dominant_hand_by_section.csv",
            "hand_summary.csv",
            "hand_token_counts.csv",
            "hand_token_shares.csv",
            "top_tokens_by_hand.csv",
            "pairwise_hand_distances.csv",
            "section_only_recomputed_distances.csv",
            "section_within_hand_distances.csv",
            "section_within_hand_groups.csv",
            "hand_within_section_distances.csv",
            "hand_within_section_groups.csv",
            "within_hand_null_summary.csv",
            "within_hand_null_summary.json",
            "within_hand_null_iterations.csv",
            "pairwise_within_hand_null_control.csv",
            "pairwise_within_hand_null_control.json",
            "signal_attribution_summary.csv",
            "unmapped_section_lines.csv",
            "unmapped_hand_lines.csv",
            "section_currier_hand_coverage.csv",
        ],
    }
    write_json(args.output / "run_summary.json", run_summary)

    print(
        json.dumps(
            {
                "selected_lines": parse_stats.get("selected_lines", 0),
                "both_mapped_lines": parse_stats.get("both_mapped_selected_lines", 0),
                "section_only_mean_jsd_bits": section_only_mean,
                "hand_only_mean_jsd_bits": hand_only_mean,
                "section_within_hand_mean_jsd_bits": section_within_hand_mean,
                "hand_within_section_mean_jsd_bits": hand_within_section_mean,
                "within_hand_null_summary": within_hand_null_summary_rows,
                "overall_signal_label": overall_label,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
