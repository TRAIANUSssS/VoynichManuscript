# Results

Run date: 2026-06-21

## Command

```bash
python scripts/exp002_word_position_patterns.py --input data/raw/LSI_ivtff_0d.txt --output artifacts/exp002/ --transcriber-code H
```

## Script

- Script path: `scripts/exp002_word_position_patterns.py`

## Input Data

- Input file: `data/raw/LSI_ivtff_0d.txt`
- Input SHA-256: `3f3f2af18cde10efe75c582f49b07b651c3397022fcbfa5854fecc424c121afa`
- Source: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html

## Parameters

- Transcriber code: `H`
- Minimum count for overrepresentation ranking: `10`
- Top tokens per position class: `30`
- Token separators: period, comma, whitespace
- Normalization: lowercase; remove non-ASCII-letter uncertain/editorial marks
- Distance metric: Jensen-Shannon divergence in bits

## Parse Counts

| Metric | Value |
|---|---:|
| Input lines | 38,939 |
| IVTFF data lines | 17,344 |
| Selected `H` lines | 5,216 |
| Non-empty selected `H` lines | 5,207 |
| Empty selected `H` lines | 9 |
| Total normalized tokens | 37,118 |
| Multi-token lines | 4,395 |
| Single-token lines | 812 |

## Position Summary

| Position class | Token count | Token share | Unique token count |
|---|---:|---:|---:|
| `line_initial` | 4,395 | 0.11840616412522226 | 2,020 |
| `line_medial` | 27,516 | 0.7413114930761355 | 5,945 |
| `line_final` | 4,395 | 0.11840616412522226 | 2,227 |
| `single_token_line` | 812 | 0.021876178673419903 | 653 |

## Top Tokens

Top line-initial tokens:

| Token | Count | Share |
|---|---:|---:|
| `daiin` | 148 | 0.03367463026166098 |
| `saiin` | 54 | 0.012286689419795221 |
| `dain` | 47 | 0.010693970420932878 |
| `sol` | 38 | 0.008646188850967008 |
| `dar` | 35 | 0.007963594994311717 |

Top line-medial tokens:

| Token | Count | Share |
|---|---:|---:|
| `daiin` | 519 | 0.018861753161796772 |
| `chedy` | 451 | 0.01639046373019334 |
| `ol` | 447 | 0.016245093763628433 |
| `aiin` | 423 | 0.015372873964238988 |
| `shedy` | 398 | 0.014464311673208316 |

Top line-final tokens:

| Token | Count | Share |
|---|---:|---:|
| `daiin` | 84 | 0.01911262798634812 |
| `dy` | 83 | 0.01888509670079636 |
| `am` | 60 | 0.013651877133105802 |
| `dam` | 48 | 0.010921501706484642 |
| `daiinplant` | 43 | 0.009783845278725825 |

## Distribution Distances

| Comparison | Jensen-Shannon divergence, bits |
|---|---:|
| `line_initial` vs `line_medial` | 0.529873240757701 |
| `line_final` vs `line_medial` | 0.5310279149774855 |
| `line_initial` vs `line_final` | 0.7331851577131896 |

## Output Artifacts

- `artifacts/exp002/position_summary.json`
- `artifacts/exp002/position_summary.csv`
- `artifacts/exp002/token_position_counts.csv`
- `artifacts/exp002/token_position_shares.csv`
- `artifacts/exp002/token_position_overrepresentation.csv`
- `artifacts/exp002/top_initial_tokens.csv`
- `artifacts/exp002/top_medial_tokens.csv`
- `artifacts/exp002/top_final_tokens.csv`
- `artifacts/exp002/distribution_distances.json`
- `artifacts/exp002/plots/top_initial_tokens.png`
- `artifacts/exp002/plots/top_final_tokens.png`
- `artifacts/exp002/plots/position_distribution_comparison.png`

## Errors Or Warnings

- No runtime error occurred.
- The token total matches `exp-001`: 37,118 normalized tokens.
- Runtime limitation: normalization compatible with `exp-001` can convert IVTFF angle-tag markup into token text.
