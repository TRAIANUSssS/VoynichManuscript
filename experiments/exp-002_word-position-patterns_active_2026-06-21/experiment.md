# exp-002: Word Position Patterns

Status: active
Created: 2026-06-21
Run date: 2026-06-21

## Research Question

Are token frequency distributions measurably different between line-initial, line-medial, line-final, and single-token-line positions in the selected `H` transcription lines of `data/raw/LSI_ivtff_0d.txt`?

## Related Hypotheses

- H-001: Voynichese as Natural Language in an Unknown Writing System
- H-002: Voynichese as Cipher or Encoded Known Language
- H-003: Voynichese as Artificial or Constructed Language
- H-004: Voynichese as Pseudotext or Meaningfully Generated Nonsense

TODO-2026-06-21-001:
No existing hypothesis explicitly targets line-position regularities or formulaic line beginnings/endings. Consider proposing a new hypothesis only after reviewing `exp-002` limitations and follow-up parser checks.

## Data

- Input file: `data/raw/LSI_ivtff_0d.txt`
- Source: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html
- Transcriber code: `H`
- Input SHA-256: `3f3f2af18cde10efe75c582f49b07b651c3397022fcbfa5854fecc424c121afa`

## Method

The script uses token parsing and normalization compatible with `exp-001`:

1. Select IVTFF data lines ending in transcriber code `;H>`.
2. Remove inline `{...}` comments.
3. Split tokens on periods, commas, and whitespace.
4. Normalize tokens by lowercasing and removing non-ASCII-letter uncertain/editorial marks.
5. Skip empty selected lines.
6. Assign position classes:
   - `single_token_line` for lines with exactly one token;
   - `line_initial` for the first token in a multi-token line;
   - `line_final` for the last token in a multi-token line;
   - `line_medial` for all other tokens in a multi-token line.

## Metrics

- selected line count;
- non-empty selected line count;
- normalized token count;
- multi-token and single-token line counts;
- token and unique-token counts by position class;
- token frequency and share by position class;
- top tokens by initial, medial, and final position;
- overrepresentation ratio by token and position;
- Jensen-Shannon divergence between selected position-class distributions.

## Parameters

- `--transcriber-code H`
- `--min-count 10`
- `--top-n 30`

## Limitations

- This experiment measures position inside transcription lines, not manuscript layout geometry.
- It does not use folio, section, scribe/hand, Currier-language, or control-corpus metadata.
- Jensen-Shannon divergence measures distribution distance but does not identify causes.
- Overrepresentation rankings are descriptive and threshold-dependent.
- Because normalization is intentionally compatible with `exp-001`, IVTFF angle-tag markup such as `<!plant>` may enter normalized token text. This must be fixed or modeled in a future parser-focused experiment before strong conclusions are drawn.
