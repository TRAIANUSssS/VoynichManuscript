# Protocol

## Question

Does the IVTFF `$I` section-level token-frequency signal remain after controlling for IVTFF `$H` hand categories?

Subquestions:

1. What is the distribution of hand categories across IVTFF `$I` sections?
2. Are some sections dominated by one hand category?
3. How large are token-frequency distances between hand groups?
4. Do section-level JSD distances remain visible within the same hand category?
5. Do hand-level JSD distances remain visible within individual sections?
6. Are within-hand section-label null controls feasible under the configured token threshold?
7. Does controlling for hand reduce, preserve, or leave unresolved the section-level signal?

## Related Hypotheses

- `H-005: Text Structure Relates to Manuscript Sections and Images`
- `H-006: Different Scribes or Hands Affect Text Statistics`

TODO:
No separate section-hand interaction hypothesis ID currently exists. Do not create one without explicit approval.

## Input Data

- Input transcription: `data/raw/LSI_ivtff_0d.txt`
- Source: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html
- Transcriber code: `H`

## Metadata

- Section metadata: `data/metadata/folio_sections.csv`
- Hand metadata: `data/metadata/folio_hands.csv`
- Optional Currier coverage metadata: `data/metadata/folio_currier.csv`

Metadata source:

- IVTFF page headers in `data/raw/LSI_ivtff_0d.txt`.
- The raw file comments define `$I` as illustration type, `$L` as Currier's language, and `$H` as Currier's hand.
- The raw file comments also describe `$H` as the calligraphic hand with values in `1-5XY`.

Hand mapping policy:

- Use documented IVTFF page-header `$H` labels.
- Treat blank, `?`, and `-` labels as unmapped for hand-controlled comparisons.
- Do not infer hand from section names.
- Do not infer hand from Currier labels.
- Write unmapped selected lines to `artifacts/exp008/unmapped_hand_lines.csv`.

## Parser Policy

Use the cleaned parser policy introduced in `exp-002b` and reused from `exp-003` through `exp-007`:

1. Select IVTFF data lines for transcriber code `H`.
2. Remove `{...}` comments.
3. Replace inline `<...>` markup with token boundaries before tokenization.
4. Split on periods, commas, and whitespace.
5. Lowercase tokens and remove non-ASCII-letter uncertain/editorial marks.
6. Do not allow IVTFF markup content to become normalized manuscript tokens.

## Method

### Part A: Metadata Coverage Audit

Compute selected line counts, section mapping counts, hand mapping counts, both-mapped counts, section names, hand categories, and section-by-hand line and token contingency tables.

### Part B: Hand-Only Comparison

Group cleaned tokens by valid hand category. For each hand category, compute line count, token count, unique token count, type-token ratio, token entropy, mean token length, token counts, token shares, top tokens, and pairwise hand JSD values.

For pairwise hand distances, keep hand groups with at least `--min-tokens-per-group` tokens.

### Part C: Section-Only Replication Check

Recompute section-level token-frequency distances using the same cleaned parser and section metadata. Compare the recomputed mean pairwise section JSD to the historical `exp-003` value:

```text
0.5554700431523788
```

This does not replace `exp-003`.

### Part D: Section Within Hand

For each hand category, group tokens by section, keep section groups with at least `--min-tokens-per-group` tokens, and compute pairwise section JSD values within that hand category.

### Part E: Hand Within Section

For each section, group tokens by hand category, keep hand groups with at least `--min-tokens-per-group` tokens, and compute pairwise hand JSD values within that section where possible.

### Part F: Section-Label Null Control Within Hand Categories

For each hand category separately:

1. Keep valid section groups with at least `--min-tokens-per-group` tokens.
2. Require at least three valid section groups.
3. If feasible, pool tokens inside the hand category.
4. Randomly reassign tokens to pseudo-section groups preserving observed group sizes.
5. Repeat for `--iterations`.
6. Report observed mean JSD, null distribution summaries, empirical percentile, empirical p-value, and signal label.

If fewer than three valid section groups exist inside a hand, label the null control `insufficient_data`.

### Part G: Signal Attribution Summary

Compare:

- full section-only mean JSD;
- hand-only mean JSD;
- section-within-hand mean JSD;
- hand-within-section mean JSD;
- within-hand null-control feasibility;
- valid comparison counts;
- token coverage.

Summary labels:

- `section_signal_preserved_within_hand`: section-within-hand comparisons are available and the mean is at least 80% of the full section mean.
- `section_signal_reduced_within_hand`: section-within-hand comparisons are available and the mean is below 80% of the full section mean.
- `section_hand_strongly_confounded`: at least half of represented sections are at least 90% dominated by one hand category and within-hand comparisons are sparse relative to all section pairs.
- `insufficient_data`: too few groups meet the threshold for a meaningful comparison.

These labels are descriptive outputs, not causal conclusions.

## Optional Controls

Implemented:

- Section-Currier-hand coverage table as a planning artifact only.

Not implemented:

- Matched-size within-hand section resampling.
- Hand-label null controls within sections.
- Three-way Currier-hand-section model.
- Plot generation.

## Parameters

- Iterations: `1000`
- Seed: `20260621`
- Minimum tokens per group: `100`
- Minimum count argument: `10`
- Top-N argument: `30`

## Expected Outputs

- Metadata coverage JSON.
- Section-hand contingency CSV files.
- Hand summary, token count, token share, and top-token CSV files.
- Pairwise hand distance CSV.
- Section-only recomputed distance CSV.
- Section-within-hand distance CSV.
- Hand-within-section distance CSV.
- Within-hand null-control summary files.
- Signal attribution summary CSV.
- Unmapped section and hand audit files.
- Section-Currier-hand coverage CSV.

## Known Limitations

- IVTFF `$H` labels are source-derived page-header metadata, not independently verified hand taxonomy.
- Blank, `?`, and `-` hand labels are treated as unmapped.
- Hand metadata covers only part of the selected `H` line set.
- Several sections have no valid hand-mapped tokens at the configured threshold.
- No hand has three valid section groups at the configured threshold, so the within-hand section-label null control is not feasible in this run.
- This experiment does not control for quire, folio neighborhood, layout, line position, alternate transcription policies, or unresolved Currier coverage.
- This experiment does not test meaning, translation, language identity, authorship, or decipherment.
