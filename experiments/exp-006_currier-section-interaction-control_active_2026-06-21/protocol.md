# Protocol

## Question

Does the IVTFF `$I` section-level token-frequency signal remain after controlling for Currier language categories?

Subquestions:

1. What is the distribution of Currier categories across IVTFF `$I` sections?
2. Are some sections dominated by one Currier category?
3. How large is the token-frequency distance between Currier groups?
4. Do section-level JSD distances remain visible within Currier A and within Currier B?
5. Which section pairs can be compared within the same Currier category with enough tokens?
6. Does controlling for Currier reduce, preserve, or expose confounding in the section-level signal?

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

Both metadata files are derived from IVTFF page-header parsable information in `data/raw/LSI_ivtff_0d.txt`.

- `$I` supplies the IVTFF illustration-type code used as the section label source.
- `$L` supplies the Currier language label.

Currier mapping policy:

- Use documented IVTFF page-header `$L` labels.
- Treat blank, `?`, and `-` Currier labels as unmapped for Currier-controlled comparisons.
- Do not infer Currier labels from section names.

## Parser Policy

Use the cleaned parser policy introduced in `exp-002b` and reused in `exp-003`, `exp-004`, and `exp-005`:

1. Select IVTFF data lines for transcriber code `H`.
2. Remove `{...}` comments.
3. Replace inline `<...>` markup with token boundaries before tokenization.
4. Split on periods, commas, and whitespace.
5. Lowercase tokens and remove non-ASCII-letter uncertain/editorial marks.
6. Do not allow IVTFF markup content to become normalized manuscript tokens.

## Method

### Part A: Metadata Coverage Audit

Compute selected line counts, section mapping counts, Currier mapping counts, both-mapped counts, section names, Currier category names, and section-by-Currier line and token contingency tables.

### Part B: Currier-Only Comparison

Group cleaned tokens by Currier category. For each group, compute line count, token count, unique token count, TTR, token entropy, mean token length, top tokens, and pairwise JSD between Currier categories.

### Part C: Section-Only Replication Check

Recompute section-level token-frequency distances using the same cleaned parser and section metadata. Compare the recomputed mean pairwise section JSD to the historical `exp-003` value:

```text
0.5554700431523788
```

This does not replace `exp-003`.

### Part D: Section Within Currier

For each Currier category, group tokens by section, keep only section groups with at least `--min-tokens-per-group` tokens, and compute pairwise section JSD values within that Currier category.

### Part E: Currier Within Section

For each section, group tokens by Currier category, keep only Currier groups with at least `--min-tokens-per-group` tokens, and compute Currier JSD values within that section where possible.

### Part F: Signal Attribution Summary

Compare:

- recomputed section-only mean JSD;
- Currier-only mean JSD;
- section-within-Currier mean JSD;
- Currier-within-section mean JSD;
- valid comparison counts;
- token coverage.

Summary labels:

- `section_signal_preserved_within_currier`: section-within-Currier comparisons are available and the mean is at least 80% of the full section mean.
- `section_signal_reduced_within_currier`: section-within-Currier comparisons are available and the mean is below 80% of the full section mean.
- `section_currier_strongly_confounded`: at least half of represented sections are at least 90% dominated by one Currier category and within-Currier comparisons are sparse relative to all 28 section pairs.
- `insufficient_data`: too few groups meet the threshold for a meaningful comparison.

These labels are descriptive outputs, not causal conclusions.

## Parameters

- Iterations: `1000`
- Seed: `20260621`
- Minimum tokens per group: `100`
- Minimum token count argument: `10`
- Top-N argument: `30`

The `iterations` and `seed` parameters are recorded for consistency with the experiment sequence. Optional resampling/null controls were not implemented in this run.

## Expected Outputs

- Metadata coverage JSON.
- Section-Currier contingency CSV files.
- Currier summary and token frequency CSV files.
- Pairwise Currier distance CSV.
- Section-within-Currier distance CSV.
- Currier-within-section distance CSV.
- Signal attribution summary CSV.
- Unmapped Currier line audit CSV.

## Known Limitations

- Currier metadata is page-header metadata from the same IVTFF source, not an independently verified taxonomy.
- Blank, `?`, and `-` Currier labels are treated as unmapped.
- Section and Currier categories may be strongly confounded.
- Sparse section-Currier combinations can limit interaction analysis.
- This experiment does not control for hand, quire, folio neighborhood, layout, line position, or transcription alternatives.
- This experiment does not test meaning, translation, language identity, authorship, or decipherment.
