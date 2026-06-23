# Protocol

## Question

Do section-label null controls inside Currier categories show token-frequency structure stronger than random section-label reassignment?

Subquestions:

1. Inside Currier A, is observed mean section-pair JSD above the null distribution created by random section-label reassignment?
2. Inside Currier B, is observed mean section-pair JSD above the equivalent null distribution?
3. Which section pairs remain above pairwise within-Currier null expectations?
4. Is the result limited by sparse section-by-Currier coverage?

## Related Hypotheses

- `H-005: Text Structure Relates to Manuscript Sections and Images`
- `H-006: Different Scribes or Hands Affect Text Statistics`

TODO:
No Currier-specific hypothesis ID currently exists. Do not create one without explicit approval.

## Input Data

- Input transcription: `data/raw/LSI_ivtff_0d.txt`
- Source: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html
- Transcriber code: `H`

## Metadata

- Section metadata: `data/metadata/folio_sections.csv`
- Currier metadata: `data/metadata/folio_currier.csv`

Reuse the section mapping logic from `exp-003` through `exp-006` and the Currier mapping logic from `exp-006`.

Currier mapping policy:

- Use documented IVTFF page-header `$L` labels.
- Treat blank, `?`, and `-` Currier labels as unmapped.
- Do not infer or fill missing Currier labels.

## Parser Policy

Use the cleaned parser policy introduced in `exp-002b`:

1. Select IVTFF data lines for transcriber code `H`.
2. Remove `{...}` comments.
3. Replace inline `<...>` markup with token boundaries before tokenization.
4. Split on periods, commas, and whitespace.
5. Lowercase tokens and remove non-ASCII-letter uncertain/editorial marks.
6. Do not allow IVTFF markup content to become normalized manuscript tokens.

## Method

### Part A: Metadata And Coverage Audit

Compute selected line counts, section mapping counts, Currier mapping counts, section-by-Currier token counts, valid groups by Currier, and excluded groups by Currier.

### Part B: Observed Section Distances Within Currier

For each Currier category:

1. Select lines with that Currier category.
2. Group tokens by section.
3. Keep sections with at least `--min-tokens-per-section` tokens.
4. Compute pairwise section JSD values.
5. Compute mean pairwise section JSD.

### Part C: Section-Label Null Control Within Currier

For each Currier category with at least three valid section groups:

1. Pool tokens from valid section groups inside the Currier category.
2. Preserve observed section group sizes.
3. Randomly reassign pooled tokens to pseudo-section groups for `1000` iterations.
4. Compute mean pairwise JSD for each pseudo-section grouping.
5. Compare the observed mean pairwise JSD against the null distribution.

Empirical p-value:

```text
(1 + count(null_mean_jsd >= observed_mean_jsd)) / (iterations + 1)
```

### Part D: Pairwise Section Null Controls Within Currier

For each valid section pair inside each Currier category:

1. Pool the two section token sets.
2. Preserve the two observed group sizes.
3. Randomly reassign pooled tokens into pseudo-pair groups for `1000` iterations.
4. Compare observed pairwise JSD to the pairwise null distribution.

## Labels

Pairwise conclusion labels:

- `above_null_97_5`
- `within_null_interval`
- `below_null_mean`
- `insufficient_data`

Currier-level signal labels:

- `section_signal_above_null_within_currier`
- `section_signal_within_null_within_currier`
- `section_signal_below_null_within_currier`
- `insufficient_data`

Overall labels:

- `section_signal_above_null_in_both_currier_groups`
- `section_signal_above_null_in_one_currier_group`
- `section_signal_not_above_null_within_currier`
- `section_currier_too_sparse_for_null_control`
- `mixed_result`

These labels are descriptive outputs, not confirmations of hypotheses.

## Parameters

- Iterations: `1000`
- Seed: `20260621`
- Minimum tokens per section: `100`
- Minimum count argument: `10`
- Top-N argument: `30`

## Known Limitations

- Blank Currier labels remain excluded, not inferred.
- `astronomical` and `zodiac` have no valid Currier-labeled tokens under the current mapping.
- Currier A has only three valid section groups.
- The null model controls random section-label reassignment inside Currier categories; it does not control hand, quire, layout, folio neighborhood, line position, or alternate transcription policies.
- This experiment does not test meaning, translation, language identity, authorship, or decipherment.
