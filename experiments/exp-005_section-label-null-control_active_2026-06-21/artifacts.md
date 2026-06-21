# Artifacts

- `artifacts/exp005/run_summary.json` - run metadata, parser audit counts, section counts, and high-level null-control summary values.
- `artifacts/exp005/section_token_counts.csv` - section token counts and non-empty mapped line counts.
- `artifacts/exp005/pairwise_null_control.csv` - full-section pooled-label null-control summary for each section pair.
- `artifacts/exp005/pairwise_null_control.json` - JSON copy of the pairwise pooled-label null-control summary.
- `artifacts/exp005/observed_vs_null_jsd.csv` - compact observed-versus-null comparison table for full-section pairwise JSD.
- `artifacts/exp005/pairwise_matched_null_control.csv` - pooled-label matched null-control summary for each section pair using `exp-004` matched-size reference logic.
- `artifacts/exp005/pairwise_matched_null_control.json` - JSON copy of the pairwise matched null-control summary.
- `artifacts/exp005/global_section_label_permutation.csv` - global pooled-label permutation summary preserving observed section token counts.
- `artifacts/exp005/global_section_label_permutation.json` - JSON copy of the global permutation summary.
- `artifacts/exp005/unmapped_lines.csv` - explicit unmapped-line audit file for selected lines.

Not generated in this run:

- Raw per-iteration CSV artifacts
- Plot PNG files
