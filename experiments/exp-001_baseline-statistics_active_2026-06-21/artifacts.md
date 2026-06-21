# Artifacts

Artifact directory: `artifacts/exp001/`

## Tables

- `artifacts/exp001/token_frequencies.csv`
- `artifacts/exp001/glyph_frequencies.csv`
- `artifacts/exp001/word_length_distribution.csv`
- `artifacts/exp001/top_tokens.csv`
- `artifacts/exp001/top_glyphs.csv`

## Metadata

- `artifacts/exp001/run_summary.json`

## Charts

- `artifacts/exp001/word_length_distribution.png`
- `artifacts/exp001/top_tokens.png`
- `artifacts/exp001/glyph_frequencies.png`

## Reproduction Command

```bash
python scripts/exp001_baseline_stats.py --input data/raw/LSI_ivtff_0d.txt --output artifacts/exp001/ --transcriber-code H
```
