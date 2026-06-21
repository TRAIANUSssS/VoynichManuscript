# Transcription Policy

## Current Transcription

Current experiment transcription for `exp-001`: IVTFF EVA interlinear transcription, local file `data/raw/LSI_ivtff_0d.txt`.

Source URL: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt

Source documentation: https://www.voynich.nu/transcr.html

Scope note: this is an experiment-level choice for `exp-001`, not a final project-wide transcription default.

## Version

Source file header: `#=IVTFF Eva- 1.5`

Source file comments include: release `1.6e6 - ?? Dec 1998`; last edited notes from December 1998. Treat exact version status as `needs-verification` against current IVTFF documentation.

## Normalization

For `exp-001` only:

- select IVTFF data lines ending in transcriber code `;H>`;
- remove inline `{...}` comments;
- split tokens on periods, commas, and whitespace;
- lowercase tokens;
- remove non-ASCII-letter uncertain/editorial marks before counting.

## Tokenization

For `exp-001`, token boundaries are periods, commas, and whitespace after comment removal.

## Line Breaks

For `exp-001`, line breaks are not modeled as features. The parser counts selected lines for run metadata only.

## Folio Metadata

For `exp-001`, folio metadata is not joined to token data.

## Uncertain Glyphs

For `exp-001`, uncertain/editorial marks are stripped. This is a baseline simplification and should be revisited before stronger analysis.

## Open Decisions

- Should a future protocol use an EVA-aware glyph parser rather than single-character counts?
- Should later experiments preserve line, folio, section, scribe/hand, and Currier-language metadata?
- How should uncertain or editorial transcription marks be modeled rather than stripped?
