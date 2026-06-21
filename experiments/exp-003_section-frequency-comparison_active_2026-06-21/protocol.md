# Protocol

Protocol version: 1.0
Written: 2026-06-21
Status: executed once on 2026-06-21

## Research Question

Do different manuscript sections have measurably different token-frequency profiles when using the cleaned IVTFF parser policy and IVTFF transcriber code `H`?

## Data

- Input file: `data/raw/LSI_ivtff_0d.txt`
- Source: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html
- Metadata file: `data/metadata/folio_sections.csv`
- Metadata source: IVTFF page header parsable information in `data/raw/LSI_ivtff_0d.txt`
- Transcriber code: `H`

## Metadata Policy

The metadata file is derived from IVTFF page header lines such as:

```text
<f5r> <! $I=H $Q=A $P=I $L=A $H=1>
```

The IVTFF file comments define `$I` as illustration type and list the codes:

- `T`: Text
- `H`: Herbal
- `A`: Astronomical
- `Z`: Zodiac
- `B`: Biological
- `C`: Cosmological
- `P`: Pharmaceutical
- `S`: Stars

## Parser Policy

This experiment uses the cleaned parser policy from `exp-002b`:

1. Select IVTFF data lines for transcriber code `H`.
2. Remove `{...}` comments.
3. Replace inline `<...>` markup in selected line text with token boundaries.
4. Split tokens on periods, commas, and whitespace.
5. Normalize tokens by lowercasing and removing non-ASCII-letter uncertain/editorial marks.
6. Do not allow IVTFF markup content to become normalized manuscript tokens.

## Method

1. Extract page/folio ID from each IVTFF line locator.
2. Join each selected line to `data/metadata/folio_sections.csv`.
3. Report unmapped lines in `artifacts/exp003/unmapped_lines.csv`.
4. Compute section-level line, token, type, entropy, glyph/character, and length metrics.
5. Compute token counts, token shares, top tokens, and overrepresentation by section.
6. Compute pairwise Jensen-Shannon divergence between section token distributions.
7. Compare section-level distance range with cleaned position-level distances from `exp-002b`.

## Parameters

- `--transcriber-code H`
- `--min-count 10`
- `--top-n 30`

## Known Limitations

- Section labels come from IVTFF `$I` illustration type metadata, not an independent codicological reclassification.
- Section categories are uneven in size; TTR and entropy comparisons are affected by sample size.
- The experiment does not control for Currier language, hand, folio, quire, or line position.
- EVA digraphs are still counted as character sequences in glyph/character metrics.
- Jensen-Shannon divergence measures distribution distance but does not explain cause.
