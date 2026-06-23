# Results

Run date: 2026-06-23

## Commands

Default metadata command:

```bash
python scripts/exp006_currier_section_interaction_control.py --input data/raw/LSI_ivtff_0d.txt --output artifacts/exp006/ --transcriber-code H --iterations 1000 --seed 20260621
```

Metadata-explicit verification command:

```bash
python scripts/exp006_currier_section_interaction_control.py --input data/raw/LSI_ivtff_0d.txt --section-metadata data/metadata/folio_sections.csv --currier-metadata data/metadata/folio_currier.csv --output artifacts/exp006/ --transcriber-code H --iterations 1000 --seed 20260621
```

## Script

- Script path: `scripts/exp006_currier_section_interaction_control.py`

## Input Data

- Input file: `data/raw/LSI_ivtff_0d.txt`
- Input SHA-256: `3f3f2af18cde10efe75c582f49b07b651c3397022fcbfa5854fecc424c121afa`
- Source: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html

## Metadata

- Section metadata path: `data/metadata/folio_sections.csv`
- Currier metadata path: `data/metadata/folio_currier.csv`
- Metadata source: IVTFF page-header metadata in `data/raw/LSI_ivtff_0d.txt`; `$I` for section labels and `$L` for Currier language.
- Currier mapping policy: blank, `?`, and `-` Currier labels are treated as unmapped for Currier-controlled comparisons.

## Parameters

- Transcriber code: `H`
- Iterations: `1000`
- Random seed: `20260621`
- Minimum tokens per group: `100`
- Minimum count argument: `10`
- Top-N argument: `30`
- Parser policy: cleaned `exp-002b` policy.
- Optional matched-size within-Currier resampling: not implemented.
- Optional nested null controls: not implemented.

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

## Metadata Coverage

| Metric | Value |
|---|---:|
| Section count | 8 |
| Currier category count | 2 |
| Currier categories | `A`, `B` |
| Unknown Currier labels treated as unmapped | blank, `?`, `-` |

All 752 unmapped Currier selected lines had blank Currier labels in the metadata used for this run.

## Section Token Counts

| Section | Token count |
|---|---:|
| astronomical | 850 |
| biological | 6,918 |
| cosmological | 2,550 |
| herbal | 11,418 |
| pharmaceutical | 2,579 |
| stars | 10,694 |
| text | 1,626 |
| zodiac | 1,332 |

## Currier Summary

| Currier language | Lines | Tokens | Unique tokens | TTR | Token entropy bits | Mean token length |
|---|---:|---:|---:|---:|---:|---:|
| A | 1,809 | 11,450 | 3,410 | 0.29781659388646287 | 9.864768151461604 | 4.865065502183406 |
| B | 2,646 | 23,224 | 4,926 | 0.21210816396830864 | 9.885541852551832 | 5.144720978298312 |

## Section By Currier Token Contingency

| Section | Currier A tokens | Currier B tokens |
|---|---:|---:|
| biological | 0 | 6,918 |
| cosmological | 0 | 1,487 |
| herbal | 7,925 | 3,445 |
| pharmaceutical | 2,579 | 0 |
| stars | 0 | 10,694 |
| text | 946 | 680 |

No tokens from `astronomical` or `zodiac` had valid Currier labels under this mapping policy.

## Distance Summaries

| Comparison level | Mean JSD bits | Valid comparison count | Token coverage | Summary label |
|---|---:|---:|---:|---|
| Section-only recomputed | 0.5554700431523788 | 28 | 37,967 | `reference` |
| Currier-only | 0.4743758913991697 | 1 | 34,674 | `currier_reference` |
| Section within Currier | 0.48050447382407735 | 13 | 34,674 | `section_currier_strongly_confounded` |
| Currier within section | 0.6082754348261923 | 2 | 34,674 | `within_section_currier_reference` |

## Section-Only Replication Check

| Metric | Value |
|---|---:|
| Historical `exp-003` mean pairwise section JSD | 0.5554700431523788 |
| Recomputed section mean pairwise JSD | 0.5554700431523788 |

## Pairwise Currier Distance

| Currier pair | Token count A | Token count B | JSD bits |
|---|---:|---:|---:|
| A vs B | 11,450 | 23,224 | 0.4743758913991697 |

## Section Within Currier Distances

| Currier | Valid section pairs | Mean JSD bits |
|---|---:|---:|
| A | 3 | 0.5355956685429015 |
| B | 10 | 0.46497751540843016 |

Overall section-within-Currier mean pairwise JSD was `0.48050447382407735` across 13 valid pairs.

## Currier Within Section Distances

| Section | Currier pair | JSD bits |
|---|---|---:|
| herbal | A vs B | 0.5470516861625053 |
| text | A vs B | 0.6694991834898794 |

Overall Currier-within-section mean pairwise JSD was `0.6082754348261923` across 2 valid comparisons.

## Output Artifacts

- `artifacts/exp006/run_summary.json`
- `artifacts/exp006/metadata_coverage.json`
- `artifacts/exp006/section_currier_contingency_lines.csv`
- `artifacts/exp006/section_currier_contingency_tokens.csv`
- `artifacts/exp006/section_currier_percentages.csv`
- `artifacts/exp006/currier_summary.csv`
- `artifacts/exp006/currier_token_counts.csv`
- `artifacts/exp006/currier_token_shares.csv`
- `artifacts/exp006/top_tokens_by_currier.csv`
- `artifacts/exp006/pairwise_currier_distances.csv`
- `artifacts/exp006/section_only_recomputed_distances.csv`
- `artifacts/exp006/section_summary_recomputed.csv`
- `artifacts/exp006/section_within_currier_groups.csv`
- `artifacts/exp006/section_within_currier_distances.csv`
- `artifacts/exp006/currier_within_section_groups.csv`
- `artifacts/exp006/currier_within_section_distances.csv`
- `artifacts/exp006/signal_attribution_summary.csv`
- `artifacts/exp006/unmapped_section_lines.csv`
- `artifacts/exp006/unmapped_currier_lines.csv`

## Errors Or Warnings

- No runtime error occurred.
- No selected lines were unmapped from sections.
- 752 selected lines were unmapped from Currier-controlled comparisons because their Currier labels were blank.
- Section-Currier coverage is sparse: valid Currier labels were available only for six of eight sections, and several represented sections had only one Currier category.
- Optional resampling and nested null controls were not implemented in this run.
