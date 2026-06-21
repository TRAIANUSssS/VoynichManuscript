# Results

Run date: 2026-06-21

## Command

```bash
python scripts/exp001_baseline_stats.py --input data/raw/LSI_ivtff_0d.txt --output artifacts/exp001/ --transcriber-code H
```

## Script

- Script path: `scripts/exp001_baseline_stats.py`

## Input Data

- Input file: `data/raw/LSI_ivtff_0d.txt`
- Input SHA-256: `3f3f2af18cde10efe75c582f49b07b651c3397022fcbfa5854fecc424c121afa`
- Source URL: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html

## Parameters

- Transcriber code: `H`
- Token separators: period, comma, whitespace
- Normalization: lowercase; remove non-ASCII-letter uncertain/editorial marks
- Glyph counting: single EVA transcription characters after token normalization

## Parse Counts

| Metric | Value |
|---|---:|
| Input lines | 38,939 |
| IVTFF data lines | 17,344 |
| Selected `H` lines | 5,216 |
| Discarded empty tokens | 38 |

## Baseline Metrics

| Metric | Value |
|---|---:|
| Token count | 37,118 |
| Unique token count | 9,051 |
| Type-token ratio | 0.24384395710975806 |
| Glyph/character count | 201,527 |
| Unique glyph/character count | 26 |
| Glyph/character entropy, bits | 3.9233922700249884 |
| Token entropy, bits | 10.675741463409675 |
| Mean token length | 5.4293604181259765 |

## Output Artifacts

- `artifacts/exp001/token_frequencies.csv`
- `artifacts/exp001/glyph_frequencies.csv`
- `artifacts/exp001/word_length_distribution.csv`
- `artifacts/exp001/top_tokens.csv`
- `artifacts/exp001/top_glyphs.csv`
- `artifacts/exp001/run_summary.json`
- `artifacts/exp001/word_length_distribution.png`
- `artifacts/exp001/top_tokens.png`
- `artifacts/exp001/glyph_frequencies.png`

## Errors Or Warnings

- No runtime error occurred.
- Limitation: this run does not use folio, section, scribe/hand, Currier-language, or control-corpus metadata.
