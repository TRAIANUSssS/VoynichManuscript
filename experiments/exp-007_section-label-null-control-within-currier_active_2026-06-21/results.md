# Results

Run date: 2026-06-23

## Commands

Default metadata command:

```bash
python scripts/exp007_section_label_null_control_within_currier.py --input data/raw/LSI_ivtff_0d.txt --output artifacts/exp007/ --transcriber-code H --iterations 1000 --seed 20260621
```

Metadata-explicit verification command:

```bash
python scripts/exp007_section_label_null_control_within_currier.py --input data/raw/LSI_ivtff_0d.txt --section-metadata data/metadata/folio_sections.csv --currier-metadata data/metadata/folio_currier.csv --output artifacts/exp007/ --transcriber-code H --iterations 1000 --seed 20260621
```

## Script

- Script path: `scripts/exp007_section_label_null_control_within_currier.py`

## Input Data

- Input file: `data/raw/LSI_ivtff_0d.txt`
- Input SHA-256: `3f3f2af18cde10efe75c582f49b07b651c3397022fcbfa5854fecc424c121afa`
- Source: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html

## Metadata

- Section metadata path: `data/metadata/folio_sections.csv`
- Currier metadata path: `data/metadata/folio_currier.csv`
- Metadata source: IVTFF page-header metadata in `data/raw/LSI_ivtff_0d.txt`; `$I` for section labels and `$L` for Currier language.
- Currier mapping policy: blank, `?`, and `-` Currier labels are treated as unmapped.

## Parameters

- Transcriber code: `H`
- Iterations: `1000`
- Random seed: `20260621`
- Minimum tokens per section: `100`
- Minimum count argument: `10`
- Top-N argument: `30`
- Parser policy: cleaned `exp-002b` policy.
- Optional matched controls: not implemented.

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
| Currier-mapped selected lines | 4,464 |
| Unmapped Currier selected lines | 752 |
| Both section-and-Currier mapped selected lines | 4,464 |
| Lines with angle tags | 2,229 |
| Angle tags removed | 4,467 |
| Unique angle-tag forms removed | 111 |
| Discarded empty tokens | 78 |

## Section And Currier Coverage

| Section | Total tokens |
|---|---:|
| astronomical | 850 |
| biological | 6,918 |
| cosmological | 2,550 |
| herbal | 11,418 |
| pharmaceutical | 2,579 |
| stars | 10,694 |
| text | 1,626 |
| zodiac | 1,332 |

| Currier | Tokens |
|---|---:|
| A | 11,450 |
| B | 23,224 |

## Valid Groups

| Currier | Valid sections | Valid section count |
|---|---|---:|
| A | herbal; pharmaceutical; text | 3 |
| B | biological; cosmological; herbal; stars; text | 5 |

Excluded zero-token groups:

- Currier A: `astronomical`, `biological`, `cosmological`, `stars`, `zodiac`
- Currier B: `astronomical`, `pharmaceutical`, `zodiac`

## Within-Currier Null Summary

| Currier | Observed mean JSD | Null mean | Null 97.5% | Observed minus null mean | Empirical p-value | Conclusion |
|---|---:|---:|---:|---:|---:|---|
| A | 0.5355956685429015 | 0.38805169568795816 | 0.39941216554950554 | 0.14754397285494336 | 0.000999000999000999 | `above_null_97_5` |
| B | 0.46397711540843006 | 0.3449325698805918 | 0.35311149369219175 | 0.11904454552783827 | 0.000999000999000999 | `above_null_97_5` |

Overall signal label:

```text
section_signal_above_null_in_both_currier_groups
```

## Pairwise Within-Currier Null Control

- Valid pair count: `13`
- Pairs above the 97.5% null quantile: `13`
- Pairs within the null interval: `0`
- Pairs below the null mean: `0`

### Selected Pairwise Results

| Currier | Section pair | Observed JSD | Null mean | Null 97.5% | Empirical p-value | Conclusion |
|---|---|---:|---:|---:|---:|---|
| A | herbal vs pharmaceutical | 0.46003087758166394 | 0.3140958894303598 | 0.3227612126383757 | 0.000999000999000999 | `above_null_97_5` |
| A | herbal vs text | 0.5577860920405742 | 0.3969625920717335 | 0.41232882278715915 | 0.000999000999000999 | `above_null_97_5` |
| A | pharmaceutical vs text | 0.5889700360064665 | 0.45147480659290373 | 0.46728794365315 | 0.000999000999000999 | `above_null_97_5` |
| B | biological vs stars | 0.3347291601069759 | 0.21772033695514914 | 0.22231144311518566 | 0.000999000999000999 | `above_null_97_5` |
| B | cosmological vs text | 0.5593658182320294 | 0.4628100936004154 | 0.4826961810711343 | 0.000999000999000999 | `above_null_97_5` |
| B | herbal vs text | 0.5024211645291627 | 0.4353382732843017 | 0.4552030820807488 | 0.000999000999000999 | `above_null_97_5` |

## Historical Comparison

| Metric | Value |
|---|---:|
| `exp-003` full section-only mean JSD | 0.5554700431523788 |
| `exp-006` section-within-Currier mean JSD | 0.48050447382407735 |
| `exp-006` Currier A section-within-Currier mean JSD from pairwise artifact | 0.5355956685429015 |
| `exp-006` Currier B section-within-Currier mean JSD from pairwise artifact | 0.46397711540843006 |

## Output Artifacts

- `artifacts/exp007/run_summary.json`
- `artifacts/exp007/metadata_coverage.json`
- `artifacts/exp007/section_currier_group_counts.csv`
- `artifacts/exp007/section_token_counts.csv`
- `artifacts/exp007/currier_token_counts.csv`
- `artifacts/exp007/valid_groups_by_currier.csv`
- `artifacts/exp007/excluded_groups_by_currier.csv`
- `artifacts/exp007/within_currier_observed_distances.csv`
- `artifacts/exp007/within_currier_null_summary.csv`
- `artifacts/exp007/within_currier_null_summary.json`
- `artifacts/exp007/pairwise_within_currier_null_control.csv`
- `artifacts/exp007/pairwise_within_currier_null_control.json`
- `artifacts/exp007/signal_summary.csv`
- `artifacts/exp007/signal_summary.json`
- `artifacts/exp007/historical_comparison_summary.csv`
- `artifacts/exp007/unmapped_section_lines.csv`
- `artifacts/exp007/unmapped_currier_lines.csv`
- `artifacts/exp007/within_currier_null_iterations.csv`
- `artifacts/exp007/pairwise_within_currier_null_iterations.csv`

## Errors Or Warnings

- No runtime error occurred.
- No selected lines were unmapped from sections.
- 752 selected lines were unmapped from Currier-controlled comparisons because their Currier labels were blank.
- `astronomical` and `zodiac` had no valid Currier-labeled tokens.
- Currier A had only 3 valid section groups.
- Empirical p-values are limited by 1000 iterations; the minimum possible value with the selected formula is `0.000999000999000999`.
