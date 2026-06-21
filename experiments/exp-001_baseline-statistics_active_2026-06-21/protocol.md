# Protocol

Protocol version: 1.0
Written: 2026-06-21
Status: executed once on 2026-06-21

## Question

Can Voynich Lab load a documented transcription and produce basic reproducible text statistics with saved outputs and documented limitations?

## Hypothesis

HYP-2026-06-21-001:
A documented IVTFF EVA transcription can support a reproducible first-pass baseline statistics workflow.

This hypothesis concerns workflow feasibility only. It does not concern manuscript meaning.

## Data

- Raw input: `data/raw/LSI_ivtff_0d.txt`
- Source URL: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html
- Selected line set: IVTFF transcriber code `H`
- Raw data rule: the downloaded file is treated as read-only.

## Preprocessing

1. Read the IVTFF text file.
2. Select only data lines whose locator ends with `;H>`.
3. Remove inline `{...}` comments.
4. Split tokens on periods, commas, and whitespace.
5. Normalize tokens by lowercasing and removing non-ASCII-letter uncertain/editorial marks.
6. Count EVA transcription characters after token normalization.

## Metrics

- token count;
- unique token count;
- type-token ratio;
- token frequency table;
- glyph/character frequency table;
- word-length distribution;
- top 20 tokens;
- top 20 glyphs/characters;
- token entropy;
- glyph/character entropy;
- run metadata.

## Expected Outputs

Outputs should be written to `artifacts/exp001/`:

- `token_frequencies.csv`
- `glyph_frequencies.csv`
- `word_length_distribution.csv`
- `top_tokens.csv`
- `top_glyphs.csv`
- `run_summary.json`
- `word_length_distribution.png`
- `top_tokens.png`
- `glyph_frequencies.png`

## Success Criteria

- The script runs from the command line with explicit input and output paths.
- Raw input provenance is documented.
- Outputs are saved under `artifacts/exp001/`.
- `results.md` contains reproducible facts only.
- Interpretive notes are kept in `findings.md` and labelled.

## Failure Criteria

- The run depends on notebook state or undocumented local state.
- Data provenance is undocumented.
- Output files are missing or not reproducible.
- Results and interpretation are mixed together.

## Known Limitations

- This protocol uses one IVTFF transcriber code only.
- EVA digraphs such as `ch` and `sh` are counted as separate characters in this baseline.
- Uncertain and editorial marks are stripped rather than modeled.
- Folio, section, scribe/hand, and Currier-language metadata are not used.
- No control corpus is included.
