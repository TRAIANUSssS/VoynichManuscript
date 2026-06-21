# Results

Run date: 2026-06-21

## Command

```bash
python scripts/exp003_section_frequency_comparison.py --input data/raw/LSI_ivtff_0d.txt --metadata data/metadata/folio_sections.csv --output artifacts/exp003/ --transcriber-code H
```

## Script

- Script path: `scripts/exp003_section_frequency_comparison.py`

## Input Data

- Input file: `data/raw/LSI_ivtff_0d.txt`
- Input SHA-256: `3f3f2af18cde10efe75c582f49b07b651c3397022fcbfa5854fecc424c121afa`
- Source: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html

## Metadata

- Metadata path: `data/metadata/folio_sections.csv`
- Metadata source: IVTFF page header parsable information in `data/raw/LSI_ivtff_0d.txt`; code meanings documented in the raw file comments and https://www.voynich.nu/transcr.html
- Metadata created by script during this run: `true`

## Parameters

- Transcriber code: `H`
- Minimum count for overrepresentation ranking: `10`
- Top tokens per section: `30`
- Parser policy: cleaned `exp-002b` policy.

## Parser And Mapping Counts

| Metric | Value |
|---|---:|
| Input lines | 38,939 |
| IVTFF data lines | 17,344 |
| Selected `H` lines | 5,216 |
| Non-empty selected `H` lines | 5,207 |
| Empty selected `H` lines | 9 |
| Mapped selected lines | 5,216 |
| Unmapped selected lines | 0 |
| Lines with angle tags | 2,229 |
| Angle tags removed | 4,467 |
| Unique angle-tag forms removed | 111 |
| Discarded empty tokens | 78 |
| Section count | 8 |

## Section Summary

Section `line_count` below counts non-empty mapped selected lines.

| Section | Lines | Tokens | Unique tokens | TTR | Token entropy bits | Mean token length |
|---|---:|---:|---:|---:|---:|---:|
| astronomical | 240 | 850 | 628 | 0.7388235294117647 | 9.00256820629607 | 5.395294117647059 |
| biological | 917 | 6,918 | 1,550 | 0.22405319456490316 | 8.578814525917462 | 5.012575888985256 |
| cosmological | 323 | 2,550 | 1,156 | 0.4533333333333333 | 9.235654823952277 | 4.747843137254902 |
| herbal | 1,630 | 11,418 | 3,358 | 0.29409703976177964 | 9.880016575194244 | 4.835698020669119 |
| pharmaceutical | 456 | 2,579 | 1,139 | 0.44164404808065144 | 9.080395878210997 | 5.0158976347421484 |
| stars | 1,083 | 10,694 | 3,100 | 0.2898821769216383 | 9.847957033756035 | 5.322049747521975 |
| text | 223 | 1,626 | 920 | 0.5658056580565806 | 9.261077674818397 | 5.031980319803198 |
| zodiac | 335 | 1,332 | 808 | 0.6066066066066066 | 9.082003995987538 | 5.201951951951952 |

## Pairwise Section Distances

Minimum section JSD: 0.3347291601069759 (`biological` vs `stars`)

Maximum section JSD: 0.7132735389659056 (`astronomical` vs `biological`)

Mean section JSD: 0.5554700431523788

## Section Vs Position Distance Comparison

| Metric | Value |
|---|---:|
| Section min JSD bits | 0.3347291601069759 |
| Section mean JSD bits | 0.5554700431523788 |
| Section max JSD bits | 0.7132735389659056 |
| `exp-002b` position min JSD bits | 0.43994932334109943 |
| `exp-002b` position mean JSD bits | 0.5398947694637786 |
| `exp-002b` position max JSD bits | 0.674520700840175 |

## Output Artifacts

- `artifacts/exp003/run_summary.json`
- `artifacts/exp003/parser_audit.json`
- `artifacts/exp003/section_summary.csv`
- `artifacts/exp003/section_summary.json`
- `artifacts/exp003/section_token_counts.csv`
- `artifacts/exp003/section_token_shares.csv`
- `artifacts/exp003/section_token_overrepresentation.csv`
- `artifacts/exp003/top_tokens_by_section.csv`
- `artifacts/exp003/pairwise_section_distances.csv`
- `artifacts/exp003/pairwise_section_distances.json`
- `artifacts/exp003/unmapped_lines.csv`
- `artifacts/exp003/section_vs_position_distance_comparison.csv`
- `artifacts/exp003/section_vs_position_distance_comparison.json`
- `artifacts/exp003/plots/section_token_counts.png`
- `artifacts/exp003/plots/section_ttr_entropy.png`
- `artifacts/exp003/plots/pairwise_section_distances_heatmap.png`

## Errors Or Warnings

- No runtime error occurred.
- No selected lines were unmapped.
- Section labels are sourced from IVTFF `$I` illustration type metadata and should not be treated as independently verified section taxonomy.
