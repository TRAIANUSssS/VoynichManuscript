# Protocol

## Question

Are observed pairwise token-frequency distances between IVTFF `$I` section categories larger than expected under random section-label assignment?

## Related Hypotheses

- `H-005: Text Structure Relates to Manuscript Sections and Images`
- `H-006: Different Scribes or Hands Affect Text Statistics`

## Input Data

- Input transcription: `data/raw/LSI_ivtff_0d.txt`
- Metadata: `data/metadata/folio_sections.csv`
- Transcriber code: `H`
- Historical comparison artifacts:
  - `artifacts/exp003/pairwise_section_distances.json`
  - `artifacts/exp004/pairwise_matched_jsd.json`

## Parser Policy

Use the cleaned parser policy introduced in `exp-002b` and reused in `exp-003` and `exp-004`:

1. Select IVTFF data lines for transcriber code `H`.
2. Remove `{...}` comments.
3. Replace inline `<...>` markup with token boundaries before tokenization.
4. Split on periods, commas, and whitespace.
5. Lowercase tokens and remove non-ASCII-letter uncertain/editorial marks.
6. Do not allow IVTFF markup content to become normalized manuscript tokens.

## Section Mapping Policy

Reuse `exp-003` / `exp-004` section mapping logic through `data/metadata/folio_sections.csv`, which was derived from IVTFF page-header `$I` illustration-type metadata.

## Method

### Control A: Pairwise Pooled-Label Null Control

- For each section pair, compute observed full-section JSD.
- Pool tokens from both sections.
- For each iteration, randomly assign pooled tokens into two groups matching the original section sizes.
- Compute null JSD for the randomized pair.
- Repeat for `1000` iterations with a fixed random seed.

### Control B: Pairwise Matched Pooled-Label Null Control

- For each section pair, use the `exp-004` pairwise matched sample size.
- Pool tokens from both sections.
- For each iteration, randomly assign pooled tokens into two groups of equal matched size.
- Compare the resulting null distribution to the `exp-004` pairwise matched mean JSD when available.
- Repeat for `1000` iterations with a fixed random seed.

### Control C: Global Section-Label Permutation

- Pool tokens from all sections.
- Preserve the observed token count of each section.
- For each iteration, randomly reassign pooled tokens back into section-sized groups.
- Compute the mean pairwise section JSD of the randomized grouping.
- Compare the observed `exp-003` mean pairwise JSD to this null distribution.

## Metrics

- Parser and mapping audit counts.
- Original token counts by section.
- Historical observed `exp-003` mean pairwise JSD.
- Historical `exp-004` pairwise matched mean pairwise JSD.
- Pairwise pooled-label null summaries.
- Pairwise matched pooled-label null summaries.
- Global permutation null summary.
- Empirical percentiles and empirical p-values.

## Success Criteria

- Deterministic run with fixed seed.
- Cleaned parser policy preserved.
- `exp-003` / `exp-004` section mapping reused.
- Pairwise pooled-label null control generated as artifacts.
- Reproducible facts recorded in `results.md`.
- Cautious interpretation recorded in `findings.md`.

## Known Limitations

- The null model tests whether section labels preserve measurable information, not what causes that information.
- Empirical p-values from finite null iterations are exploratory summaries, not final proof.
- The experiment does not control Currier language, hand, line position, quire, or folio structure.
- Section labels still come from IVTFF `$I` illustration-type metadata and are not an independently verified taxonomy.
