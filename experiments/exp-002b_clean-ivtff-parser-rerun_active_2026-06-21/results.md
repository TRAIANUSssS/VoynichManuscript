# Results

Run date: 2026-06-21

## Command

```bash
python scripts/exp002b_clean_ivtff_parser_rerun.py --input data/raw/LSI_ivtff_0d.txt --output artifacts/exp002b/ --transcriber-code H
```

## Script

- Script path: `scripts/exp002b_clean_ivtff_parser_rerun.py`

## Input Data

- Input file: `data/raw/LSI_ivtff_0d.txt`
- Input SHA-256: `3f3f2af18cde10efe75c582f49b07b651c3397022fcbfa5854fecc424c121afa`
- Source: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html

## Historical Inputs Compared

- Old `exp-001` summary: `artifacts/exp001/run_summary.json`
- Old `exp-001` top tokens: `artifacts/exp001/top_tokens.csv`
- Old `exp-002` summary: `artifacts/exp002/position_summary.json`

## Parameters

- Transcriber code: `H`
- Token separators: period, comma, whitespace
- Angle-tag policy: replace inline `<...>` markup in selected text with token boundaries before tokenization
- Normalization: lowercase; remove non-ASCII-letter uncertain/editorial marks after IVTFF markup removal
- Position classes: `line_initial`, `line_medial`, `line_final`, `single_token_line`
- Minimum count for overrepresentation ranking: `10`
- Top position tokens: `30`

## Parser Audit Counts

| Metric | Value |
|---|---:|
| Input lines | 38,939 |
| IVTFF data lines | 17,344 |
| Selected `H` lines | 5,216 |
| Non-empty selected `H` lines | 5,207 |
| Empty selected `H` lines | 9 |
| Lines with angle tags | 2,229 |
| Angle tags removed | 4,467 |
| Unique angle-tag forms removed | 111 |
| Discarded empty tokens | 78 |

## Baseline Comparison

| Metric | Old value | Cleaned value | Delta |
|---|---:|---:|---:|
| Token count | 37,118 | 37,967 | 849 |
| Unique token count | 9,051 | 8,071 | -980 |
| Type-token ratio | 0.24384395710975806 | 0.21257934522084967 | -0.03126461188890839 |
| Glyph/character count | 201,527 | 191,545 | -9,982 |
| Unique glyph/character count | 26 | 22 | -4 |
| Glyph/character entropy, bits | 3.9233922700249884 | 3.8609603705527977 | -0.06243189947219063 |
| Token entropy, bits | 10.675741463409675 | 10.451632120067082 | -0.2241093433425938 |
| Mean token length | 5.4293604181259765 | 5.045039112913846 | -0.38432130521213015 |

## Top Token Comparison

| Rank | Old token | Old count | Cleaned token | Cleaned count |
|---:|---|---:|---|---:|
| 1 | `daiin` | 751 | `daiin` | 864 |
| 2 | `ol` | 507 | `ol` | 539 |
| 3 | `chedy` | 490 | `chedy` | 501 |
| 4 | `aiin` | 448 | `aiin` | 470 |
| 5 | `shedy` | 424 | `shedy` | 427 |
| 6 | `chol` | 378 | `chol` | 396 |
| 7 | `ar` | 344 | `or` | 367 |
| 8 | `or` | 344 | `ar` | 353 |
| 9 | `chey` | 336 | `chey` | 344 |
| 10 | `qokeey` | 307 | `dar` | 319 |

## Position Summary Comparison

| Position class | Old token count | Cleaned token count | Token delta | Old unique count | Cleaned unique count | Unique delta |
|---|---:|---:|---:|---:|---:|---:|
| `line_initial` | 4,395 | 4,395 | 0 | 2,020 | 1,976 | -44 |
| `line_medial` | 27,516 | 28,365 | 849 | 5,945 | 5,545 | -400 |
| `line_final` | 4,395 | 4,395 | 0 | 2,227 | 1,894 | -333 |
| `single_token_line` | 812 | 812 | 0 | 653 | 646 | -7 |

## Position Distribution Comparison

| Comparison | Old JSD bits | Cleaned JSD bits | Delta |
|---|---:|---:|---:|
| `line_initial_vs_line_medial` | 0.529873240757701 | 0.5052142842100613 | -0.02465895654763972 |
| `line_final_vs_line_medial` | 0.5310279149774855 | 0.43994932334109943 | -0.09107859163638604 |
| `line_initial_vs_line_final` | 0.7331851577131896 | 0.674520700840175 | -0.05866445687301458 |

## Output Artifacts

- `artifacts/exp002b/baseline_clean/run_summary.json`
- `artifacts/exp002b/baseline_clean/token_frequencies.csv`
- `artifacts/exp002b/baseline_clean/glyph_frequencies.csv`
- `artifacts/exp002b/baseline_clean/word_length_distribution.csv`
- `artifacts/exp002b/baseline_clean/top_tokens.csv`
- `artifacts/exp002b/baseline_clean/top_glyphs.csv`
- `artifacts/exp002b/position_clean/position_summary.json`
- `artifacts/exp002b/position_clean/position_summary.csv`
- `artifacts/exp002b/position_clean/token_position_counts.csv`
- `artifacts/exp002b/position_clean/token_position_shares.csv`
- `artifacts/exp002b/position_clean/token_position_overrepresentation.csv`
- `artifacts/exp002b/position_clean/distribution_distances.json`
- `artifacts/exp002b/comparisons/comparison_summary.json`
- `artifacts/exp002b/comparisons/comparison_metrics.csv`
- `artifacts/exp002b/comparisons/comparison_top_tokens.csv`
- `artifacts/exp002b/comparisons/comparison_position_summary.csv`
- `artifacts/exp002b/comparisons/comparison_distribution_distances.csv`
- `artifacts/exp002b/parser_audit/angle_tag_examples.csv`

## Errors Or Warnings

- No runtime error occurred.
- Old `exp-001` and `exp-002` outputs were not overwritten.
- This rerun changes parser behavior, so its outputs should not be merged silently with historical outputs.
