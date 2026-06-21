"""Matched-token-count section resampling control for exp-004.

This script reuses the cleaned IVTFF parser policy from exp-002b and the
folio-to-section mapping used by exp-003. It measures how section-level token
frequency differences change when section comparisons use matched token counts.
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


def build_section_tokens(parsed_rows: list[dict[str, object]]) -> tuple[dict[str, list[str]], dict[str, int]]:
    section_tokens: dict[str, list[str]] = defaultdict(list)
    section_lines: Counter[str] = Counter()
    for row in parsed_rows:
        section = str(row["section"])
        section_lines[section] += 1
        section_tokens[section].extend(row["tokens"])
    return dict(section_tokens), dict(section_lines)


def sample_counter(tokens: list[str], sample_size: int, rng: random.Random) -> Counter[str]:
    return Counter(rng.sample(tokens, sample_size))


def section_pair_rows(sections: list[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for index, left in enumerate(sections):
        for right in sections[index + 1 :]:
            pairs.append((left, right))
    return pairs


def load_observed_pairwise_distances(path: Path) -> dict[tuple[str, str], float]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        rows = json.load(handle)
    observed: dict[tuple[str, str], float] = {}
    for row in rows:
        key = tuple(sorted((row["section_a"], row["section_b"])))
        observed[key] = float(row["jensen_shannon_divergence_bits"])
    return observed


def common_size_resampling(
    section_tokens: dict[str, list[str]],
    iterations: int,
    rng: random.Random,
) -> tuple[int, list[dict[str, object]], list[dict[str, object]]]:
    sections = sorted(section_tokens)
    common_sample_size = min(len(tokens) for tokens in section_tokens.values())
    metric_store: dict[str, dict[str, list[float]]] = {
        section: {"ttr": [], "token_entropy_bits": []} for section in sections
    }
    pair_values: dict[tuple[str, str], list[float]] = {pair: [] for pair in section_pair_rows(sections)}

    for _ in range(iterations):
        sampled_counters: dict[str, Counter[str]] = {}
        for section in sections:
            counter = sample_counter(section_tokens[section], common_sample_size, rng)
            sampled_counters[section] = counter
            metric_store[section]["ttr"].append(len(counter) / common_sample_size if common_sample_size else 0.0)
            metric_store[section]["token_entropy_bits"].append(entropy(counter))

        for left, right in pair_values:
            pair_values[(left, right)].append(jensen_shannon_divergence(sampled_counters[left], sampled_counters[right]))

    section_rows: list[dict[str, object]] = []
    for section in sections:
        ttr_summary = summarize_distribution(metric_store[section]["ttr"])
        entropy_summary = summarize_distribution(metric_store[section]["token_entropy_bits"])
        section_rows.append(
            {
                "section": section,
                "original_token_count": len(section_tokens[section]),
                "common_sample_size": common_sample_size,
                "ttr_mean": ttr_summary["mean"],
                "ttr_std": ttr_summary["std"],
                "ttr_median": ttr_summary["median"],
                "ttr_q025": ttr_summary["q025"],
                "ttr_q975": ttr_summary["q975"],
                "token_entropy_mean_bits": entropy_summary["mean"],
                "token_entropy_std_bits": entropy_summary["std"],
                "token_entropy_median_bits": entropy_summary["median"],
                "token_entropy_q025_bits": entropy_summary["q025"],
                "token_entropy_q975_bits": entropy_summary["q975"],
            }
        )

    pair_rows: list[dict[str, object]] = []
    for left, right in section_pair_rows(sections):
        summary = summarize_distribution(pair_values[(left, right)])
        pair_rows.append(
            {
                "section_a": left,
                "section_b": right,
                "common_sample_size": common_sample_size,
                "jsd_mean_bits": summary["mean"],
                "jsd_std_bits": summary["std"],
                "jsd_median_bits": summary["median"],
                "jsd_q025_bits": summary["q025"],
                "jsd_q975_bits": summary["q975"],
            }
        )
    return common_sample_size, section_rows, pair_rows


def pairwise_matched_resampling(
    section_tokens: dict[str, list[str]],
    iterations: int,
    rng: random.Random,
) -> list[dict[str, object]]:
    sections = sorted(section_tokens)
    rows: list[dict[str, object]] = []
    for left, right in section_pair_rows(sections):
        sample_size = min(len(section_tokens[left]), len(section_tokens[right]))
        values: list[float] = []
        for _ in range(iterations):
            counter_left = sample_counter(section_tokens[left], sample_size, rng)
            counter_right = sample_counter(section_tokens[right], sample_size, rng)
            values.append(jensen_shannon_divergence(counter_left, counter_right))
        summary = summarize_distribution(values)
        rows.append(
            {
                "section_a": left,
                "section_b": right,
                "token_count_a": len(section_tokens[left]),
                "token_count_b": len(section_tokens[right]),
                "pairwise_sample_size": sample_size,
                "jsd_mean_bits": summary["mean"],
                "jsd_std_bits": summary["std"],
                "jsd_median_bits": summary["median"],
                "jsd_q025_bits": summary["q025"],
                "jsd_q975_bits": summary["q975"],
            }
        )
    return rows


def add_observed_values(
    common_pair_rows: list[dict[str, object]],
    pairwise_rows: list[dict[str, object]],
    observed_distances: dict[tuple[str, str], float],
) -> list[dict[str, object]]:
    comparison_rows: list[dict[str, object]] = []
    common_by_pair = {
        tuple(sorted((str(row["section_a"]), str(row["section_b"])))): row for row in common_pair_rows
    }
    pairwise_by_pair = {
        tuple(sorted((str(row["section_a"]), str(row["section_b"])))): row for row in pairwise_rows
    }

    for pair in sorted(set(common_by_pair) | set(pairwise_by_pair)):
        observed = observed_distances.get(pair)
        common_row = common_by_pair[pair]
        pairwise_row = pairwise_by_pair[pair]
        comparison_rows.append(
            {
                "section_a": pair[0],
                "section_b": pair[1],
                "observed_exp003_jsd_bits": observed,
                "common_size_mean_jsd_bits": common_row["jsd_mean_bits"],
                "common_size_delta_vs_observed_bits": (common_row["jsd_mean_bits"] - observed) if observed is not None else "",
                "pairwise_matched_mean_jsd_bits": pairwise_row["jsd_mean_bits"],
                "pairwise_matched_delta_vs_observed_bits": (pairwise_row["jsd_mean_bits"] - observed) if observed is not None else "",
                "common_sample_size": common_row["common_sample_size"],
                "pairwise_sample_size": pairwise_row["pairwise_sample_size"],
            }
        )
        common_row["observed_exp003_jsd_bits"] = observed
        common_row["difference_vs_observed_bits"] = (common_row["jsd_mean_bits"] - observed) if observed is not None else ""
        pairwise_row["observed_exp003_jsd_bits"] = observed
        pairwise_row["difference_vs_observed_bits"] = (pairwise_row["jsd_mean_bits"] - observed) if observed is not None else ""
    return comparison_rows


def json_ready(value: object) -> object:
    if isinstance(value, Path):
        return str(value.as_posix())
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Run exp-004 matched-token-count section resampling control.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--metadata", default=Path("data/metadata/folio_sections.csv"), type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--transcriber-code", default="H")
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--common-sample-size", default="auto")
    parser.add_argument("--pairwise-sample-size", default="auto")
    parser.add_argument("--min-count", type=int, default=10)
    parser.add_argument("--top-n", type=int, default=30)
    parser.add_argument(
        "--observed-distances",
        default=Path("artifacts/exp003/pairwise_section_distances.json"),
        type=Path,
    )
    args = parser.parse_args()

    if args.common_sample_size != "auto":
        raise ValueError("Only --common-sample-size auto is implemented for exp-004.")
    if args.pairwise_sample_size != "auto":
        raise ValueError("Only --pairwise-sample-size auto is implemented for exp-004.")

    args.output.mkdir(parents=True, exist_ok=True)
    metadata, metadata_created = load_or_create_metadata(args.input, args.metadata)
    parsed_rows, unmapped_rows, parse_stats = parse_selected_lines(args.input, args.transcriber_code, metadata)
    section_tokens, section_lines = build_section_tokens(parsed_rows)
    sections = sorted(section_tokens)
    section_counts_rows = [
        {
            "section": section,
            "line_count": section_lines[section],
            "token_count": len(section_tokens[section]),
        }
        for section in sections
    ]
    write_csv(args.output / "section_token_counts.csv", section_counts_rows, ["section", "line_count", "token_count"])
    write_csv(args.output / "unmapped_lines.csv", unmapped_rows, ["locator", "folio_id", "reason"])

    observed_distances = load_observed_pairwise_distances(args.observed_distances)
    rng_common = random.Random(args.seed)
    rng_pairwise = random.Random(args.seed + 1)

    common_sample_size, common_section_rows, common_pair_rows = common_size_resampling(section_tokens, args.iterations, rng_common)
    pairwise_rows = pairwise_matched_resampling(section_tokens, args.iterations, rng_pairwise)
    comparison_rows = add_observed_values(common_pair_rows, pairwise_rows, observed_distances)

    write_csv(
        args.output / "common_size_resampling_summary.csv",
        common_section_rows,
        [
            "section",
            "original_token_count",
            "common_sample_size",
            "ttr_mean",
            "ttr_std",
            "ttr_median",
            "ttr_q025",
            "ttr_q975",
            "token_entropy_mean_bits",
            "token_entropy_std_bits",
            "token_entropy_median_bits",
            "token_entropy_q025_bits",
            "token_entropy_q975_bits",
        ],
    )
    with (args.output / "common_size_resampling_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(common_section_rows, handle, indent=2)
        handle.write("\n")

    write_csv(
        args.output / "common_size_pairwise_jsd.csv",
        common_pair_rows,
        [
            "section_a",
            "section_b",
            "common_sample_size",
            "observed_exp003_jsd_bits",
            "jsd_mean_bits",
            "jsd_std_bits",
            "jsd_median_bits",
            "jsd_q025_bits",
            "jsd_q975_bits",
            "difference_vs_observed_bits",
        ],
    )
    with (args.output / "common_size_pairwise_jsd.json").open("w", encoding="utf-8") as handle:
        json.dump(common_pair_rows, handle, indent=2)
        handle.write("\n")

    write_csv(
        args.output / "pairwise_matched_jsd.csv",
        pairwise_rows,
        [
            "section_a",
            "section_b",
            "token_count_a",
            "token_count_b",
            "pairwise_sample_size",
            "observed_exp003_jsd_bits",
            "jsd_mean_bits",
            "jsd_std_bits",
            "jsd_median_bits",
            "jsd_q025_bits",
            "jsd_q975_bits",
            "difference_vs_observed_bits",
        ],
    )
    with (args.output / "pairwise_matched_jsd.json").open("w", encoding="utf-8") as handle:
        json.dump(pairwise_rows, handle, indent=2)
        handle.write("\n")

    write_csv(
        args.output / "observed_vs_resampled_jsd.csv",
        comparison_rows,
        [
            "section_a",
            "section_b",
            "observed_exp003_jsd_bits",
            "common_size_mean_jsd_bits",
            "common_size_delta_vs_observed_bits",
            "pairwise_matched_mean_jsd_bits",
            "pairwise_matched_delta_vs_observed_bits",
            "common_sample_size",
            "pairwise_sample_size",
        ],
    )

    common_jsd_values = [float(row["jsd_mean_bits"]) for row in common_pair_rows]
    pairwise_jsd_values = [float(row["jsd_mean_bits"]) for row in pairwise_rows]
    observed_values = list(observed_distances.values())
    run_summary = {
        "experiment": "exp-004_section-frequency-resampling-control",
        "run_date_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "script": "scripts/exp004_section_frequency_resampling_control.py",
        "input": args.input,
        "input_sha256": file_sha256(args.input),
        "metadata": args.metadata,
        "metadata_created_by_script": metadata_created,
        "metadata_source": "Reuse exp-003 folio-to-section mapping derived from IVTFF page headers ($I illustration type).",
        "output": args.output,
        "parameters": {
            "transcriber_code": args.transcriber_code,
            "iterations": args.iterations,
            "seed": args.seed,
            "common_sample_size_mode": args.common_sample_size,
            "pairwise_sample_size_mode": args.pairwise_sample_size,
            "min_count": args.min_count,
            "top_n": args.top_n,
            "parser_policy": "cleaned exp-002b policy: remove comments, replace inline <...> markup with token boundaries, split on periods/commas/whitespace, lowercase and strip non-ASCII letters",
            "sampling_mode": "without replacement within each section sample",
        },
        "parse_stats": parse_stats,
        "section_count": len(sections),
        "sections": sections,
        "section_token_counts": section_counts_rows,
        "common_sample_size": common_sample_size,
        "observed_exp003_pairwise_jsd_available": bool(observed_distances),
        "observed_exp003_mean_pairwise_jsd_bits": (sum(observed_values) / len(observed_values)) if observed_values else None,
        "common_size_mean_pairwise_jsd_bits": (sum(common_jsd_values) / len(common_jsd_values)) if common_jsd_values else None,
        "pairwise_matched_mean_pairwise_jsd_bits": (sum(pairwise_jsd_values) / len(pairwise_jsd_values)) if pairwise_jsd_values else None,
        "null_control": {
            "implemented": False,
            "status": "todo",
        },
        "artifacts": [
            "run_summary.json",
            "section_token_counts.csv",
            "common_size_resampling_summary.csv",
            "common_size_resampling_summary.json",
            "common_size_pairwise_jsd.csv",
            "common_size_pairwise_jsd.json",
            "pairwise_matched_jsd.csv",
            "pairwise_matched_jsd.json",
            "observed_vs_resampled_jsd.csv",
            "unmapped_lines.csv",
        ],
    }
    with (args.output / "run_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(json_ready(run_summary), handle, indent=2)
        handle.write("\n")

    print(
        json.dumps(
            {
                "section_count": len(sections),
                "common_sample_size": common_sample_size,
                "observed_mean_jsd_bits": run_summary["observed_exp003_mean_pairwise_jsd_bits"],
                "common_size_mean_jsd_bits": run_summary["common_size_mean_pairwise_jsd_bits"],
                "pairwise_matched_mean_jsd_bits": run_summary["pairwise_matched_mean_pairwise_jsd_bits"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
