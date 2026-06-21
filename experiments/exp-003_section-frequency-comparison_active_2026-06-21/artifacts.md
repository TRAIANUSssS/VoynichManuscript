# Artifacts

Artifact directory: `artifacts/exp003/`

## Core Outputs

- `artifacts/exp003/run_summary.json`
- `artifacts/exp003/parser_audit.json`
- `artifacts/exp003/section_summary.csv`
- `artifacts/exp003/section_summary.json`

## Token Tables

- `artifacts/exp003/section_token_counts.csv`
- `artifacts/exp003/section_token_shares.csv`
- `artifacts/exp003/section_token_overrepresentation.csv`
- `artifacts/exp003/top_tokens_by_section.csv`

## Distances

- `artifacts/exp003/pairwise_section_distances.csv`
- `artifacts/exp003/pairwise_section_distances.json`
- `artifacts/exp003/section_vs_position_distance_comparison.csv`
- `artifacts/exp003/section_vs_position_distance_comparison.json`

## Mapping Audit

- `artifacts/exp003/unmapped_lines.csv`

## Plots

- `artifacts/exp003/plots/section_token_counts.png`
- `artifacts/exp003/plots/section_ttr_entropy.png`
- `artifacts/exp003/plots/pairwise_section_distances_heatmap.png`

## Metadata

- `data/metadata/folio_sections.csv`

## Reproduction Command

```bash
python scripts/exp003_section_frequency_comparison.py --input data/raw/LSI_ivtff_0d.txt --metadata data/metadata/folio_sections.csv --output artifacts/exp003/ --transcriber-code H
```
