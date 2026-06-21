# Artifacts

Artifact directory: `artifacts/exp002b/`

## Cleaned Baseline Rerun

- `artifacts/exp002b/baseline_clean/run_summary.json`
- `artifacts/exp002b/baseline_clean/token_frequencies.csv`
- `artifacts/exp002b/baseline_clean/glyph_frequencies.csv`
- `artifacts/exp002b/baseline_clean/word_length_distribution.csv`
- `artifacts/exp002b/baseline_clean/top_tokens.csv`
- `artifacts/exp002b/baseline_clean/top_glyphs.csv`
- `artifacts/exp002b/baseline_clean/word_length_distribution.png`
- `artifacts/exp002b/baseline_clean/top_tokens.png`
- `artifacts/exp002b/baseline_clean/glyph_frequencies.png`

## Cleaned Position Rerun

- `artifacts/exp002b/position_clean/position_summary.json`
- `artifacts/exp002b/position_clean/position_summary.csv`
- `artifacts/exp002b/position_clean/token_position_counts.csv`
- `artifacts/exp002b/position_clean/token_position_shares.csv`
- `artifacts/exp002b/position_clean/token_position_overrepresentation.csv`
- `artifacts/exp002b/position_clean/top_initial_tokens.csv`
- `artifacts/exp002b/position_clean/top_medial_tokens.csv`
- `artifacts/exp002b/position_clean/top_final_tokens.csv`
- `artifacts/exp002b/position_clean/distribution_distances.json`
- `artifacts/exp002b/position_clean/plots/top_initial_tokens.png`
- `artifacts/exp002b/position_clean/plots/top_final_tokens.png`
- `artifacts/exp002b/position_clean/plots/position_distribution_comparison.png`

## Comparisons

- `artifacts/exp002b/comparisons/comparison_summary.json`
- `artifacts/exp002b/comparisons/comparison_metrics.csv`
- `artifacts/exp002b/comparisons/comparison_top_tokens.csv`
- `artifacts/exp002b/comparisons/comparison_position_summary.csv`
- `artifacts/exp002b/comparisons/comparison_distribution_distances.csv`

## Parser Audit

- `artifacts/exp002b/parser_audit/angle_tag_examples.csv`

## Reproduction Command

```bash
python scripts/exp002b_clean_ivtff_parser_rerun.py --input data/raw/LSI_ivtff_0d.txt --output artifacts/exp002b/ --transcriber-code H
```
