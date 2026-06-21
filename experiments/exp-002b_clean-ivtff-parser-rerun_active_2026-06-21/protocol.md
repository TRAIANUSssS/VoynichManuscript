# Protocol

Protocol version: 1.0
Written: 2026-06-21
Status: active

## Question

How do `exp-001` baseline statistics and `exp-002` line-position statistics change when inline IVTFF angle-tag markup is excluded from normalized manuscript tokens?

## Data

- Input file: `data/raw/LSI_ivtff_0d.txt`
- Source: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html
- Transcriber code: `H`
- Historical baseline summary: `artifacts/exp001/run_summary.json`
- Historical baseline top tokens: `artifacts/exp001/top_tokens.csv`
- Historical position summary: `artifacts/exp002/position_summary.json`

## Parser Policy

1. Select IVTFF data lines ending in transcriber code `;H>`.
2. Remove `{...}` comments.
3. Replace inline angle-tag markup matching `<...>` in selected line text with a token boundary before tokenization.
4. Split tokens on periods, commas, and whitespace.
5. Normalize tokens by lowercasing and removing non-ASCII-letter uncertain/editorial marks.
6. Preserve old `exp-001` and `exp-002` outputs unchanged.

DEC-2026-06-21-001:
The cleaned parser replaces angle tags with token boundaries rather than deleting them without a boundary. This avoids turning `ol<-><!plant>oltchey` into the joined token `ololtchey`.

## Reruns

The script produces:

- cleaned baseline statistics comparable to `exp-001`;
- cleaned line-position statistics comparable to `exp-002`;
- old-vs-cleaned comparison tables;
- parser-audit examples of removed angle tags.

## Metrics

- old and cleaned token count;
- old and cleaned unique token count;
- old and cleaned type-token ratio;
- old and cleaned glyph/character count;
- old and cleaned unique glyph/character count;
- old and cleaned glyph entropy;
- old and cleaned token entropy;
- old and cleaned mean token length;
- old and cleaned top tokens;
- old and cleaned token counts and unique token counts by position class;
- old and cleaned Jensen-Shannon divergence between position distributions.

## Expected Outputs

Output directory: `artifacts/exp002b/`

- `baseline_clean/run_summary.json`
- `baseline_clean/token_frequencies.csv`
- `baseline_clean/glyph_frequencies.csv`
- `baseline_clean/word_length_distribution.csv`
- `baseline_clean/top_tokens.csv`
- `baseline_clean/top_glyphs.csv`
- `position_clean/position_summary.json`
- `position_clean/position_summary.csv`
- `position_clean/token_position_counts.csv`
- `position_clean/token_position_shares.csv`
- `position_clean/token_position_overrepresentation.csv`
- `position_clean/distribution_distances.json`
- `comparisons/comparison_summary.json`
- `comparisons/comparison_metrics.csv`
- `comparisons/comparison_top_tokens.csv`
- `comparisons/comparison_position_summary.csv`
- `comparisons/comparison_distribution_distances.csv`
- `parser_audit/angle_tag_examples.csv`

## Known Limitations

- The cleaned parser removes all inline `<...>` forms from selected text, including forms that may encode editorial uncertainty or layout notes.
- The parser does not yet distinguish all IVTFF markup categories semantically.
- EVA digraphs are still counted as character sequences for glyph/character counts.
- No folio, section, hand, Currier-language, or control-corpus metadata is used.
