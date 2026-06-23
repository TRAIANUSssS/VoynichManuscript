"""Section-label null controls within Currier categories for exp-007.

This script reuses the cleaned IVTFF parser policy from exp-002b, section
mapping from exp-003 through exp-006, and Currier mapping from exp-006. It
tests whether section labels preserve token-frequency structure above random
section-label reassignment separately inside Currier categories.
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


def conclusion_label(observed: float, summary: dict[str, float]) -> str:
    if observed > summary["q975"]:
        return "above_null_97_5"
    if observed < summary["mean"]:
        return "below_null_mean"
    return "within_null_interval"


def signal_label_from_conclusion(conclusion: str) -> str:
    if conclusion == "above_null_97_5":
        return "section_signal_above_null_within_currier"
    if conclusion == "below_null_mean":
        return "section_signal_below_null_within_currier"
    if conclusion == "insufficient_data":
        return "insufficient_data"
    return "section_signal_within_null_within_currier"


def overall_signal_label(currier_labels: list[str]) -> str:
    usable = [label for label in currier_labels if label != "insufficient_data"]
    if not usable:
        return "section_currier_too_sparse_for_null_control"
    above_count = sum(1 for label in usable if label == "section_signal_above_null_within_currier")
    if above_count == len(usable) and len(usable) >= 2:
        return "section_signal_above_null_in_both_currier_groups"
    if above_count == 1:
        return "section_signal_above_null_in_one_currier_group"
    if above_count == 0:
        return "section_signal_not_above_null_within_currier"
    return "mixed_result"


def build_section_currier_groups(line_rows: list[dict[str, object]]) -> tuple[dict[str, dict[str, list[str]]], Counter[tuple[str, str]], Counter[str], Counter[str]]:
    groups: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    line_counts: Counter[tuple[str, str]] = Counter()
    section_token_counts: Counter[str] = Counter()
    currier_token_counts: Counter[str] = Counter()
    for row in line_rows:
        if not row["both_mapped"]:
            continue
        tokens = list(row["tokens"])
        if not tokens:
            continue
        section = str(row["section"])
        currier = str(row["currier_language"])
        groups[currier][section].extend(tokens)
        line_counts[(currier, section)] += 1
        section_token_counts[section] += len(tokens)
        currier_token_counts[currier] += len(tokens)
    return {currier: dict(sections) for currier, sections in groups.items()}, line_counts, section_token_counts, currier_token_counts


def all_section_counts(line_rows: list[dict[str, object]]) -> tuple[Counter[str], Counter[str]]:
    section_lines: Counter[str] = Counter()
    section_tokens: Counter[str] = Counter()
    for row in line_rows:
        if not row["section_mapped"]:
            continue
        section = str(row["section"])
        tokens = list(row["tokens"])
        section_lines[section] += 1
        section_tokens[section] += len(tokens)
    return section_lines, section_tokens


def section_currier_group_rows(
    groups: dict[str, dict[str, list[str]]],
    line_counts: Counter[tuple[str, str]],
    all_sections: list[str],
    all_curriers: list[str],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for currier in all_curriers:
        for section in all_sections:
            rows.append(
                {
                    "currier_language": currier,
                    "section": section,
                    "line_count": line_counts[(currier, section)],
                    "token_count": len(groups.get(currier, {}).get(section, [])),
                }
            )
    return rows


def valid_and_excluded_group_rows(
    groups: dict[str, dict[str, list[str]]],
    line_counts: Counter[tuple[str, str]],
    all_sections: list[str],
    all_curriers: list[str],
    min_tokens: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, dict[str, list[str]]]]:
    valid_rows: list[dict[str, object]] = []
    excluded_rows: list[dict[str, object]] = []
    valid_groups: dict[str, dict[str, list[str]]] = defaultdict(dict)
    for currier in all_curriers:
        for section in all_sections:
            tokens = groups.get(currier, {}).get(section, [])
            token_count = len(tokens)
            row = {
                "currier_language": currier,
                "section": section,
                "line_count": line_counts[(currier, section)],
                "token_count": token_count,
                "min_tokens_per_section": min_tokens,
            }
            if token_count >= min_tokens:
                valid_rows.append({**row, "status": "valid"})
                valid_groups[currier][section] = tokens
            else:
                reason = "zero_tokens" if token_count == 0 else "below_min_tokens"
                excluded_rows.append({**row, "reason": reason})
    return valid_rows, excluded_rows, {currier: dict(sections) for currier, sections in valid_groups.items()}


def observed_distances(valid_groups: dict[str, dict[str, list[str]]]) -> tuple[list[dict[str, object]], dict[str, float | None]]:
    rows: list[dict[str, object]] = []
    means: dict[str, float | None] = {}
    for currier in sorted(valid_groups):
        counters = {section: Counter(tokens) for section, tokens in valid_groups[currier].items()}
        values: list[float] = []
        for left, right in pairwise_names(sorted(counters)):
            observed = jensen_shannon_divergence(counters[left], counters[right])
            values.append(observed)
            rows.append(
                {
                    "currier_language": currier,
                    "section_a": left,
                    "section_b": right,
                    "token_count_a": len(valid_groups[currier][left]),
                    "token_count_b": len(valid_groups[currier][right]),
                    "observed_jsd_bits": observed,
                }
            )
        means[currier] = sum(values) / len(values) if values else None
    return rows, means


def mean_pairwise_jsd(groups: dict[str, list[str]]) -> float:
    counters = {section: Counter(tokens) for section, tokens in groups.items()}
    values = [
        jensen_shannon_divergence(counters[left], counters[right])
        for left, right in pairwise_names(sorted(counters))
    ]
    return sum(values) / len(values) if values else 0.0


def run_within_currier_nulls(
    valid_groups: dict[str, dict[str, list[str]]],
    observed_means: dict[str, float | None],
    iterations: int,
    seed: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    summary_rows: list[dict[str, object]] = []
    iteration_rows: list[dict[str, object]] = []
    for offset, currier in enumerate(sorted(valid_groups)):
        sections = sorted(valid_groups[currier])
        if len(sections) < 3:
            summary_rows.append(
                {
                    "currier_language": currier,
                    "valid_section_count": len(sections),
                    "valid_sections": ";".join(sections),
                    "observed_mean_jsd_bits": observed_means.get(currier) if observed_means.get(currier) is not None else "",
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
        rng = random.Random(seed + offset)
        sizes = {section: len(valid_groups[currier][section]) for section in sections}
        pooled_tokens: list[str] = []
        for section in sections:
            pooled_tokens.extend(valid_groups[currier][section])
        total_size = len(pooled_tokens)
        null_means: list[float] = []
        for iteration in range(1, iterations + 1):
            sample = rng.sample(pooled_tokens, total_size)
            pseudo_groups: dict[str, list[str]] = {}
            cursor = 0
            for section in sections:
                size = sizes[section]
                pseudo_groups[section] = sample[cursor:cursor + size]
                cursor += size
            null_mean = mean_pairwise_jsd(pseudo_groups)
            null_means.append(null_mean)
            iteration_rows.append({"currier_language": currier, "iteration": iteration, "null_mean_jsd_bits": null_mean})
        observed = float(observed_means[currier]) if observed_means[currier] is not None else 0.0
        summary = summarize_distribution(null_means)
        conclusion = conclusion_label(observed, summary)
        summary_rows.append(
            {
                "currier_language": currier,
                "valid_section_count": len(sections),
                "valid_sections": ";".join(sections),
                "observed_mean_jsd_bits": observed,
                "null_mean_jsd_mean_bits": summary["mean"],
                "null_mean_jsd_std_bits": summary["std"],
                "null_mean_jsd_median_bits": summary["median"],
                "null_mean_jsd_q025_bits": summary["q025"],
                "null_mean_jsd_q975_bits": summary["q975"],
                "observed_minus_null_mean_bits": observed - summary["mean"],
                "empirical_percentile": empirical_percentile(null_means, observed),
                "empirical_p_value": empirical_p_value(null_means, observed),
                "conclusion_label": conclusion,
                "signal_label": signal_label_from_conclusion(conclusion),
            }
        )
    return summary_rows, iteration_rows


def run_pairwise_nulls(
    valid_groups: dict[str, dict[str, list[str]]],
    iterations: int,
    seed: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    iteration_rows: list[dict[str, object]] = []
    pair_index = 1000
    for currier in sorted(valid_groups):
        sections = sorted(valid_groups[currier])
        counters = {section: Counter(valid_groups[currier][section]) for section in sections}
        for left, right in pairwise_names(sections):
            pair_index += 1
            tokens_a = valid_groups[currier][left]
            tokens_b = valid_groups[currier][right]
            observed = jensen_shannon_divergence(counters[left], counters[right])
            pooled = tokens_a + tokens_b
            size_a = len(tokens_a)
            size_b = len(tokens_b)
            rng = random.Random(seed + pair_index)
            null_values: list[float] = []
            for iteration in range(1, iterations + 1):
                sample = rng.sample(pooled, size_a + size_b)
                null_value = jensen_shannon_divergence(Counter(sample[:size_a]), Counter(sample[size_a:size_a + size_b]))
                null_values.append(null_value)
                iteration_rows.append(
                    {
                        "currier_language": currier,
                        "section_a": left,
                        "section_b": right,
                        "iteration": iteration,
                        "null_jsd_bits": null_value,
                    }
                )
            summary = summarize_distribution(null_values)
            conclusion = conclusion_label(observed, summary)
            rows.append(
                {
                    "currier_language": currier,
                    "section_a": left,
                    "section_b": right,
                    "token_count_a": size_a,
                    "token_count_b": size_b,
                    "observed_jsd_bits": observed,
                    "null_jsd_mean_bits": summary["mean"],
                    "null_jsd_std_bits": summary["std"],
                    "null_jsd_median_bits": summary["median"],
                    "null_jsd_q025_bits": summary["q025"],
                    "null_jsd_q975_bits": summary["q975"],
                    "observed_minus_null_mean_bits": observed - summary["mean"],
                    "empirical_percentile": empirical_percentile(null_values, observed),
                    "empirical_p_value": empirical_p_value(null_values, observed),
                    "conclusion_label": conclusion,
                }
            )
    return rows, iteration_rows


def read_exp006_references(exp006_signal_summary: Path, exp006_section_within_currier: Path) -> dict[str, float]:
    references = {
        "exp003_full_section_mean_jsd_bits": 0.5554700431523788,
        "exp006_section_within_currier_mean_jsd_bits": 0.48050447382407735,
        "exp006_currier_a_section_within_currier_mean_jsd_bits": 0.5355956685429015,
        "exp006_currier_b_section_within_currier_mean_jsd_bits": 0.46497751540843016,
    }
    if not exp006_signal_summary.exists():
        rows = []
    else:
        with exp006_signal_summary.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            if row.get("comparison_level") == "section_only_recomputed":
                references["exp003_full_section_mean_jsd_bits"] = float(row["mean_jsd_bits"])
            if row.get("comparison_level") == "section_within_currier":
                references["exp006_section_within_currier_mean_jsd_bits"] = float(row["mean_jsd_bits"])
    if exp006_section_within_currier.exists():
        with exp006_section_within_currier.open("r", encoding="utf-8", newline="") as handle:
            distance_rows = list(csv.DictReader(handle))
        curriers = sorted({row["currier_language"] for row in distance_rows})
        for currier in curriers:
            values = [
                float(row["jensen_shannon_divergence_bits"])
                for row in distance_rows
                if row["currier_language"] == currier
            ]
            if values:
                references[f"exp006_currier_{currier.lower()}_section_within_currier_mean_jsd_bits"] = sum(values) / len(values)
    return references


def comparison_summary_rows(
    within_summary: list[dict[str, object]],
    references: dict[str, float],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in within_summary:
        currier = str(row["currier_language"])
        exp006_key = f"exp006_currier_{currier.lower()}_section_within_currier_mean_jsd_bits"
        rows.append(
            {
                "currier_language": currier,
                "exp003_full_section_mean_jsd_bits": references["exp003_full_section_mean_jsd_bits"],
                "exp006_section_within_currier_mean_jsd_bits": references["exp006_section_within_currier_mean_jsd_bits"],
                "exp006_same_currier_section_within_currier_mean_jsd_bits": references.get(exp006_key, ""),
                "exp007_observed_mean_jsd_bits": row["observed_mean_jsd_bits"],
                "exp007_null_mean_jsd_bits": row["null_mean_jsd_mean_bits"],
                "exp007_null_q975_bits": row["null_mean_jsd_q975_bits"],
                "exp007_empirical_p_value": row["empirical_p_value"],
                "exp007_conclusion_label": row["conclusion_label"],
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Run exp-007 within-Currier section-label null controls.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--section-metadata", default=Path("data/metadata/folio_sections.csv"), type=Path)
    parser.add_argument("--currier-metadata", default=Path("data/metadata/folio_currier.csv"), type=Path)
    parser.add_argument("--metadata", dest="section_metadata_alias", type=Path, help="Alias for --section-metadata.")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--transcriber-code", default="H")
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--min-tokens-per-section", type=int, default=100)
    parser.add_argument("--min-count", type=int, default=10)
    parser.add_argument("--top-n", type=int, default=30)
    parser.add_argument("--exp006-signal-summary", default=Path("artifacts/exp006/signal_attribution_summary.csv"), type=Path)
    parser.add_argument("--exp006-section-within-currier", default=Path("artifacts/exp006/section_within_currier_distances.csv"), type=Path)
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

    groups, line_counts, section_token_counts, currier_token_counts = build_section_currier_groups(line_rows)
    all_section_line_counts, all_section_token_counts = all_section_counts(line_rows)
    all_sections = sorted(all_section_token_counts)
    all_curriers = sorted(currier_token_counts)
    group_count_rows = section_currier_group_rows(groups, line_counts, all_sections, all_curriers)
    valid_group_rows, excluded_group_rows, valid_groups = valid_and_excluded_group_rows(
        groups,
        line_counts,
        all_sections,
        all_curriers,
        args.min_tokens_per_section,
    )
    observed_rows, observed_means = observed_distances(valid_groups)
    within_summary_rows, within_iteration_rows = run_within_currier_nulls(
        valid_groups,
        observed_means,
        args.iterations,
        args.seed,
    )
    pairwise_rows, pairwise_iteration_rows = run_pairwise_nulls(valid_groups, args.iterations, args.seed)
    signal_labels = [str(row["signal_label"]) for row in within_summary_rows]
    overall_label = overall_signal_label(signal_labels)
    references = read_exp006_references(args.exp006_signal_summary, args.exp006_section_within_currier)
    comparison_rows = comparison_summary_rows(within_summary_rows, references)

    signal_summary_rows = [
        {
            "scope": "currier",
            "currier_language": row["currier_language"],
            "valid_section_count": row["valid_section_count"],
            "valid_sections": row["valid_sections"],
            "observed_mean_jsd_bits": row["observed_mean_jsd_bits"],
            "null_mean_jsd_bits": row["null_mean_jsd_mean_bits"],
            "null_q975_bits": row["null_mean_jsd_q975_bits"],
            "empirical_p_value": row["empirical_p_value"],
            "conclusion_label": row["conclusion_label"],
            "signal_label": row["signal_label"],
        }
        for row in within_summary_rows
    ]
    signal_summary_rows.append(
        {
            "scope": "overall",
            "currier_language": "all_valid_currier_categories",
            "valid_section_count": "",
            "valid_sections": "",
            "observed_mean_jsd_bits": "",
            "null_mean_jsd_bits": "",
            "null_q975_bits": "",
            "empirical_p_value": "",
            "conclusion_label": "",
            "signal_label": overall_label,
        }
    )

    metadata_coverage = {
        "selected_line_count": parse_stats.get("selected_lines", 0),
        "non_empty_selected_line_count": parse_stats.get("non_empty_selected_lines", 0),
        "section_mapped_line_count": parse_stats.get("section_mapped_selected_lines", 0),
        "unmapped_section_line_count": parse_stats.get("unmapped_section_selected_lines", 0),
        "currier_mapped_line_count": parse_stats.get("currier_mapped_selected_lines", 0),
        "unmapped_currier_line_count": parse_stats.get("unmapped_currier_selected_lines", 0),
        "both_mapped_line_count": parse_stats.get("both_mapped_selected_lines", 0),
        "section_names": all_sections,
        "currier_controlled_section_names": sorted(section_token_counts),
        "currier_categories": all_curriers,
        "section_count": len(all_sections),
        "currier_controlled_section_count": len(section_token_counts),
        "currier_category_count": len(all_curriers),
        "unknown_currier_labels_treated_as_unmapped": sorted(UNKNOWN_CURRIER_LABELS),
        "min_tokens_per_section": args.min_tokens_per_section,
    }

    write_json(args.output / "metadata_coverage.json", metadata_coverage)
    write_csv(
        args.output / "section_token_counts.csv",
        [
            {"section": section, "line_count": all_section_line_counts[section], "token_count": all_section_token_counts[section]}
            for section in all_sections
        ],
        ["section", "line_count", "token_count"],
    )
    write_csv(
        args.output / "currier_token_counts.csv",
        [
            {"currier_language": currier, "token_count": currier_token_counts[currier]}
            for currier in all_curriers
        ],
        ["currier_language", "token_count"],
    )
    write_csv(args.output / "section_currier_group_counts.csv", group_count_rows, ["currier_language", "section", "line_count", "token_count"])
    write_csv(args.output / "valid_groups_by_currier.csv", valid_group_rows, ["currier_language", "section", "line_count", "token_count", "min_tokens_per_section", "status"])
    write_csv(args.output / "excluded_groups_by_currier.csv", excluded_group_rows, ["currier_language", "section", "line_count", "token_count", "min_tokens_per_section", "reason"])
    write_csv(args.output / "within_currier_observed_distances.csv", observed_rows, ["currier_language", "section_a", "section_b", "token_count_a", "token_count_b", "observed_jsd_bits"])
    write_csv(
        args.output / "within_currier_null_summary.csv",
        within_summary_rows,
        [
            "currier_language",
            "valid_section_count",
            "valid_sections",
            "observed_mean_jsd_bits",
            "null_mean_jsd_mean_bits",
            "null_mean_jsd_std_bits",
            "null_mean_jsd_median_bits",
            "null_mean_jsd_q025_bits",
            "null_mean_jsd_q975_bits",
            "observed_minus_null_mean_bits",
            "empirical_percentile",
            "empirical_p_value",
            "conclusion_label",
            "signal_label",
        ],
    )
    write_json(args.output / "within_currier_null_summary.json", within_summary_rows)
    write_csv(
        args.output / "pairwise_within_currier_null_control.csv",
        pairwise_rows,
        [
            "currier_language",
            "section_a",
            "section_b",
            "token_count_a",
            "token_count_b",
            "observed_jsd_bits",
            "null_jsd_mean_bits",
            "null_jsd_std_bits",
            "null_jsd_median_bits",
            "null_jsd_q025_bits",
            "null_jsd_q975_bits",
            "observed_minus_null_mean_bits",
            "empirical_percentile",
            "empirical_p_value",
            "conclusion_label",
        ],
    )
    write_json(args.output / "pairwise_within_currier_null_control.json", pairwise_rows)
    write_csv(
        args.output / "signal_summary.csv",
        signal_summary_rows,
        [
            "scope",
            "currier_language",
            "valid_section_count",
            "valid_sections",
            "observed_mean_jsd_bits",
            "null_mean_jsd_bits",
            "null_q975_bits",
            "empirical_p_value",
            "conclusion_label",
            "signal_label",
        ],
    )
    write_json(args.output / "signal_summary.json", signal_summary_rows)
    write_csv(
        args.output / "historical_comparison_summary.csv",
        comparison_rows,
        [
            "currier_language",
            "exp003_full_section_mean_jsd_bits",
            "exp006_section_within_currier_mean_jsd_bits",
            "exp006_same_currier_section_within_currier_mean_jsd_bits",
            "exp007_observed_mean_jsd_bits",
            "exp007_null_mean_jsd_bits",
            "exp007_null_q975_bits",
            "exp007_empirical_p_value",
            "exp007_conclusion_label",
        ],
    )
    write_csv(args.output / "unmapped_section_lines.csv", unmapped_section_rows, ["locator", "folio_id", "reason"])
    write_csv(args.output / "unmapped_currier_lines.csv", unmapped_currier_rows, ["locator", "folio_id", "currier_language", "reason"])
    write_csv(args.output / "within_currier_null_iterations.csv", within_iteration_rows, ["currier_language", "iteration", "null_mean_jsd_bits"])
    write_csv(args.output / "pairwise_within_currier_null_iterations.csv", pairwise_iteration_rows, ["currier_language", "section_a", "section_b", "iteration", "null_jsd_bits"])

    run_summary = {
        "experiment": "exp-007_section-label-null-control-within-currier",
        "run_date_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "script": "scripts/exp007_section_label_null_control_within_currier.py",
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
            "min_tokens_per_section": args.min_tokens_per_section,
            "min_count": args.min_count,
            "top_n": args.top_n,
            "parser_policy": "cleaned exp-002b policy: remove comments, replace inline <...> markup with token boundaries, split on periods/commas/whitespace, lowercase and strip non-ASCII letters",
            "currier_mapping_policy": "Use documented IVTFF page-header $L labels; treat blank, ? and - as unmapped for Currier-controlled comparisons.",
            "global_within_currier_null": "pool valid section-group tokens inside each Currier category and randomly reassign section labels preserving observed group sizes",
            "pairwise_within_currier_null": "pool each valid section pair inside Currier and randomly reassign pair labels preserving observed group sizes",
            "optional_matched_controls": "not implemented in this run",
        },
        "parse_stats": parse_stats,
        "metadata_coverage": metadata_coverage,
        "valid_groups_by_currier": valid_group_rows,
        "excluded_groups_by_currier": excluded_group_rows,
        "within_currier_null_summary": within_summary_rows,
        "pairwise_within_currier_null_control_rows": len(pairwise_rows),
        "signal_summary": signal_summary_rows,
        "historical_references": references,
        "artifacts": [
            "run_summary.json",
            "metadata_coverage.json",
            "section_currier_group_counts.csv",
            "section_token_counts.csv",
            "currier_token_counts.csv",
            "valid_groups_by_currier.csv",
            "excluded_groups_by_currier.csv",
            "within_currier_observed_distances.csv",
            "within_currier_null_summary.csv",
            "within_currier_null_summary.json",
            "pairwise_within_currier_null_control.csv",
            "pairwise_within_currier_null_control.json",
            "signal_summary.csv",
            "signal_summary.json",
            "historical_comparison_summary.csv",
            "unmapped_section_lines.csv",
            "unmapped_currier_lines.csv",
            "within_currier_null_iterations.csv",
            "pairwise_within_currier_null_iterations.csv",
        ],
    }
    write_json(args.output / "run_summary.json", run_summary)

    print(
        json.dumps(
            {
                "selected_lines": parse_stats.get("selected_lines", 0),
                "both_mapped_lines": parse_stats.get("both_mapped_selected_lines", 0),
                "within_currier_null_summary": within_summary_rows,
                "overall_signal_label": overall_label,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
