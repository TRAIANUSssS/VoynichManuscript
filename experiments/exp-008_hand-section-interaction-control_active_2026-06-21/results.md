# Results

Run date: 2026-06-23

## Commands

Default command:

```bash
python scripts/exp008_hand_section_interaction_control.py --input data/raw/LSI_ivtff_0d.txt --output artifacts/exp008/ --transcriber-code H --iterations 1000 --seed 20260621
```

Metadata-explicit verification command:

```bash
python scripts/exp008_hand_section_interaction_control.py --input data/raw/LSI_ivtff_0d.txt --section-metadata data/metadata/folio_sections.csv --hand-metadata data/metadata/folio_hands.csv --output artifacts/exp008/ --transcriber-code H --iterations 1000 --seed 20260621
```

## Script

- Script path: `scripts/exp008_hand_section_interaction_control.py`

## Input Data

- Input file: `data/raw/LSI_ivtff_0d.txt`
- Input SHA-256: `3f3f2af18cde10efe75c582f49b07b651c3397022fcbfa5854fecc424c121afa`
- Source: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html

## Metadata

- Section metadata path: `data/metadata/folio_sections.csv`
- Hand metadata path: `data/metadata/folio_hands.csv`
- Optional Currier metadata path: `data/metadata/folio_currier.csv`
- Metadata source: IVTFF page-header metadata in `data/raw/LSI_ivtff_0d.txt`; `$I` for section labels, `$H` for Currier hand, and `$L` for optional coverage planning.
- Hand mapping policy: blank, `?`, and `-` hand labels are treated as unmapped.

## Parameters

- Transcriber code: `H`
- Iterations: `1000`
- Random seed: `20260621`
- Minimum tokens per group: `100`
- Minimum count argument: `10`
- Top-N argument: `30`
- Parser policy: cleaned `exp-002b` policy.
- Optional matched-size within-hand resampling: not implemented.
- Optional hand-label null within sections: not implemented.
- Optional section-Currier-hand summary: coverage table only.

## Parser And Mapping Counts

| Metric | Value |
|---|---:|
| Input lines | 38,939 |
| IVTFF data lines | 17,344 |
| Selected `H` lines | 5,216 |
| Non-empty selected `H` lines | 5,207 |
| Empty selected `H` lines | 9 |
| Section-mapped selected lines | 5,216 |
| Unmapped section selected lines | 0 |
| Hand-mapped selected lines | 3,134 |
| Unmapped hand selected lines | 2,082 |
| Both section-and-hand mapped selected lines | 3,134 |
| Lines with angle tags | 2,229 |
| Angle tags removed | 4,467 |
| Unique angle-tag forms removed | 111 |
| Discarded empty tokens | 78 |

## Metadata Coverage

| Metric | Value |
|---|---:|
| Section count | 8 |
| Hand category count | 7 |
| Minimum tokens per group | 100 |
| Dominant sections at >=90% one hand | 1 |

Section names:

```text
astronomical, biological, cosmological, herbal, pharmaceutical, stars, text, zodiac
```

Hand category names:

```text
1, 2, 3, 4, 5, X, Y
```

## Hand Summary

| Hand | Lines | Tokens | Unique tokens | TTR | Entropy bits | Mean token length |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 1,139 | 7,273 | 2,213 | 0.30427608964663827 | 9.333090592305568 | 4.759384023099134 |
| 2 | 1,221 | 9,704 | 2,283 | 0.23526380873866448 | 9.085969723854443 | 4.978153338829348 |
| 3 | 188 | 1,820 | 833 | 0.4576923076923077 | 8.839731587392114 | 5.101098901098901 |
| 4 | 161 | 875 | 541 | 0.6182857142857143 | 8.598583745119873 | 5.209142857142857 |
| 5 | 61 | 546 | 319 | 0.5842490842490843 | 7.86329146384734 | 4.957875457875458 |
| X | 282 | 2,741 | 1,170 | 0.4268515140459686 | 9.20223850157018 | 5.352790952207224 |
| Y | 75 | 760 | 488 | 0.6421052631578947 | 8.482442255626697 | 5.264473684210526 |

## Signal Attribution Summary

| Comparison level | Mean JSD | Valid comparisons | Token coverage | Reference mean JSD | Notes |
|---|---:|---:|---:|---:|---|
| section-only recomputed | 0.5554700431523788 | 28 | 37,967 | 0.5554700431523788 | Internal `exp-008` replication check of full section distances. |
| hand-only | 0.5822290801216097 | 21 | 23,719 |  | Hand groups with at least 100 tokens. |
| section-within-hand | 0.5681240941907049 | 4 | 23,719 |  | Pairwise section JSD computed inside each hand category. |
| hand-within-section | 0.6461215587388383 | 8 | 23,719 |  | Pairwise hand JSD computed inside sections where enough hand groups exist. |
| within-hand section-label null |  | 0 |  |  | 0 of 0 feasible hand categories were above their 97.5% section-label null quantile. |
| overall |  | 4 | 23,719 |  | `section_signal_preserved_within_hand` |

## Section-Only Replication Check

| Metric | Value |
|---|---:|
| Recomputed section-only mean JSD | 0.5554700431523788 |
| Historical `exp-003` reference mean JSD | 0.5554700431523788 |
| Difference | 0.0 |

## Section Within Hand

| Hand | Section pair | Token count A | Token count B | JSD |
|---|---|---:|---:|---:|
| 1 | herbal vs text | 7,060 | 213 | 0.6065797757758608 |
| 2 | biological vs herbal | 6,918 | 2,786 | 0.4347931720064342 |
| 3 | cosmological vs text | 1,487 | 333 | 0.5694432596869899 |
| 4 | herbal vs pharmaceutical | 579 | 296 | 0.6616801692935346 |

## Hand Within Section

| Section | Hand pair | Token count A | Token count B | JSD |
|---|---|---:|---:|---:|
| herbal | 1 vs 2 | 7,060 | 2,786 | 0.5674616183215448 |
| herbal | 1 vs 4 | 7,060 | 579 | 0.58281850116782 |
| herbal | 1 vs 5 | 7,060 | 546 | 0.6417680255007447 |
| herbal | 2 vs 4 | 2,786 | 579 | 0.7060004818166368 |
| herbal | 2 vs 5 | 2,786 | 546 | 0.4853878482451518 |
| herbal | 4 vs 5 | 579 | 546 | 0.7829508712714852 |
| stars | X vs Y | 2,741 | 760 | 0.5600711079976806 |
| text | 1 vs 3 | 213 | 333 | 0.8425140155896425 |

## Within-Hand Section-Label Null Control

| Hand | Valid section count | Valid sections | Conclusion |
|---|---:|---|---|
| 1 | 2 | herbal; text | `insufficient_data` |
| 2 | 2 | biological; herbal | `insufficient_data` |
| 3 | 2 | cosmological; text | `insufficient_data` |
| 4 | 2 | herbal; pharmaceutical | `insufficient_data` |
| 5 | 1 | herbal | `insufficient_data` |
| X | 1 | stars | `insufficient_data` |
| Y | 1 | stars | `insufficient_data` |

No within-hand null distribution was generated because no hand category had at least three valid section groups with at least 100 tokens each.

## Output Artifacts

- `artifacts/exp008/run_summary.json`
- `artifacts/exp008/metadata_coverage.json`
- `artifacts/exp008/section_hand_contingency_lines.csv`
- `artifacts/exp008/section_hand_contingency_tokens.csv`
- `artifacts/exp008/section_hand_percentages.csv`
- `artifacts/exp008/dominant_hand_by_section.csv`
- `artifacts/exp008/hand_summary.csv`
- `artifacts/exp008/hand_token_counts.csv`
- `artifacts/exp008/hand_token_shares.csv`
- `artifacts/exp008/top_tokens_by_hand.csv`
- `artifacts/exp008/pairwise_hand_distances.csv`
- `artifacts/exp008/section_only_recomputed_distances.csv`
- `artifacts/exp008/section_within_hand_distances.csv`
- `artifacts/exp008/section_within_hand_groups.csv`
- `artifacts/exp008/hand_within_section_distances.csv`
- `artifacts/exp008/hand_within_section_groups.csv`
- `artifacts/exp008/within_hand_null_summary.csv`
- `artifacts/exp008/within_hand_null_summary.json`
- `artifacts/exp008/within_hand_null_iterations.csv`
- `artifacts/exp008/pairwise_within_hand_null_control.csv`
- `artifacts/exp008/pairwise_within_hand_null_control.json`
- `artifacts/exp008/signal_attribution_summary.csv`
- `artifacts/exp008/unmapped_section_lines.csv`
- `artifacts/exp008/unmapped_hand_lines.csv`
- `artifacts/exp008/section_currier_hand_coverage.csv`

## Errors Or Warnings

- No runtime error occurred.
- No selected lines were unmapped from sections.
- 2,082 selected lines were unmapped from hand-controlled comparisons because their hand labels were blank.
- No hand category had at least three valid section groups at the configured `100` token threshold, so within-hand section-label null controls are marked `insufficient_data`.
- `astronomical` and `zodiac` had no valid hand-mapped tokens.
- The `section_signal_preserved_within_hand` label is based on four section-within-hand pairwise comparisons and should be treated as coverage-limited.
