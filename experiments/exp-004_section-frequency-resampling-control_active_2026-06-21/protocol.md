# Protocol

## Question

Do IVTFF `$I` section categories still show measurable differences in cleaned token-frequency profiles when compared at matched token counts?

## Related Hypotheses

- `H-005: Text Structure Relates to Manuscript Sections and Images`
- `H-006: Different Scribes or Hands Affect Text Statistics`

## Input Data

- Input transcription: `data/raw/LSI_ivtff_0d.txt`
- Metadata: `data/metadata/folio_sections.csv`
- Transcriber code: `H`
- Observed comparison source: `artifacts/exp003/pairwise_section_distances.json`

## Parser Policy

Use the cleaned parser policy introduced in `exp-002b` and reused in `exp-003`:

1. Select IVTFF data lines for transcriber code `H`.
2. Remove `{...}` comments.
3. Replace inline `<...>` markup with token boundaries before tokenization.
4. Split on periods, commas, and whitespace.
5. Lowercase tokens and remove non-ASCII-letter uncertain/editorial marks.
6. Do not allow IVTFF markup content to become normalized manuscript tokens.

## Section Mapping Policy

Reuse `exp-003` section mapping logic through `data/metadata/folio_sections.csv`, which was derived from IVTFF page-header `$I` illustration-type metadata.

## Method

### Control A: Common-Size Section Resampling

- Build cleaned token lists for each mapped section.
- Set `common_sample_size` to the minimum section token count.
- For each iteration, sample `common_sample_size` tokens without replacement from each section.
- Compute section-level TTR, section-level token entropy, and pairwise section JSD.
- Repeat for `1000` iterations with a fixed random seed.

### Control B: Pairwise Matched-Size Resampling

- For each section pair, set sample size to the minimum token count of the pair.
- For each iteration, sample without replacement from each section in the pair and compute JSD.
- Repeat for `1000` iterations with a fixed random seed.

### Optional Control C

- Not implemented in this run.
- Record as follow-up: pooled-label null or permutation-style control for pairwise section JSD.

## Metrics

- Parser and mapping audit counts.
- Original token counts by section.
- Common sample size.
- Section-level common-size TTR summaries.
- Section-level common-size token-entropy summaries.
- Pairwise common-size JSD summaries.
- Pairwise matched-size JSD summaries.
- Differences between observed `exp-003` JSD and resampled mean JSD.

## Success Criteria

- Deterministic run with fixed seed.
- Cleaned parser policy preserved.
- `exp-003` section mapping reused.
- Common-size and pairwise matched-size controls generated as artifacts.
- Reproducible facts recorded in `results.md`.
- Cautious interpretation recorded in `findings.md`.

## Known Limitations

- The global common-size control is constrained by the smallest section, expected to be `astronomical`.
- Section labels come from IVTFF `$I` illustration-type metadata and are not an independently verified taxonomy.
- This experiment controls sample size only; it does not control Currier language, hand, line position, quire, or folio structure.
- Null-control resampling was not implemented in this run.
