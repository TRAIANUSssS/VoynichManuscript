# exp-003: Section Frequency Comparison

Experiment ID: exp-003
Status: active
Created: 2026-06-21
Run date: 2026-06-21

## Goal

Compare cleaned token-frequency profiles across IVTFF manuscript sections using the parser policy established in `exp-002b`.

This experiment tests section-level variation in transcription statistics. It does not make claims about meaning, language identity, cipher status, or decipherment.

## Related Hypotheses

- H-001: Voynichese as Natural Language in an Unknown Writing System
- H-002: Voynichese as Cipher or Encoded Known Language
- H-003: Voynichese as Artificial or Constructed Language
- H-004: Voynichese as Pseudotext or Meaningfully Generated Nonsense
- H-005: Text Structure Relates to Manuscript Sections and Images

## Data Used

- Transcription: `data/raw/LSI_ivtff_0d.txt`
- Metadata: `data/metadata/folio_sections.csv`
- Metadata source: IVTFF page header parsable information in `data/raw/LSI_ivtff_0d.txt`; code meanings documented in the raw file comments and https://www.voynich.nu/transcr.html
- Transcriber code: `H`

## Current Conclusion

OBS-2026-06-21-001:
The run mapped all selected `H` lines to IVTFF `$I` section categories and generated section summaries, token tables, overrepresentation tables, pairwise section distances, and section-vs-position distance comparisons.

INF-2026-06-21-001:
The section-level distributions differ measurably under Jensen-Shannon divergence, but this result does not identify the cause of the differences and should be checked against section sizes, Currier language, hand, and control corpora.

## Files

- `protocol.md`
- `results.md`
- `findings.md`
- `artifacts.md`
- `questions.md`
