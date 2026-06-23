# Artifacts

- `artifacts/exp007/run_summary.json` - run metadata, parser audit counts, metadata sources, key null-control summaries, and generated artifact list.
- `artifacts/exp007/metadata_coverage.json` - section and Currier mapping coverage for selected `H` lines.
- `artifacts/exp007/section_currier_group_counts.csv` - token and line counts for each section-by-Currier group.
- `artifacts/exp007/section_token_counts.csv` - section token counts for selected `H` lines.
- `artifacts/exp007/currier_token_counts.csv` - token counts by valid Currier category.
- `artifacts/exp007/valid_groups_by_currier.csv` - section groups that met the minimum token threshold inside each Currier category.
- `artifacts/exp007/excluded_groups_by_currier.csv` - section groups excluded from within-Currier null controls and the reason.
- `artifacts/exp007/within_currier_observed_distances.csv` - observed pairwise section JSD values inside each Currier category.
- `artifacts/exp007/within_currier_null_summary.csv` - Currier-level observed mean JSD versus within-Currier section-label null distributions.
- `artifacts/exp007/within_currier_null_summary.json` - JSON copy of the Currier-level null summary.
- `artifacts/exp007/pairwise_within_currier_null_control.csv` - pairwise section-label null controls inside each Currier category.
- `artifacts/exp007/pairwise_within_currier_null_control.json` - JSON copy of the pairwise null-control results.
- `artifacts/exp007/signal_summary.csv` - per-Currier and overall signal labels.
- `artifacts/exp007/signal_summary.json` - JSON copy of the signal labels.
- `artifacts/exp007/historical_comparison_summary.csv` - comparison against `exp-003` and `exp-006` reference values.
- `artifacts/exp007/unmapped_section_lines.csv` - explicit audit file for section-unmapped selected lines.
- `artifacts/exp007/unmapped_currier_lines.csv` - explicit audit file for Currier-unmapped selected lines.
- `artifacts/exp007/within_currier_null_iterations.csv` - raw Currier-level null iteration values.
- `artifacts/exp007/pairwise_within_currier_null_iterations.csv` - raw pairwise null iteration values.

Not generated in this run:

- Plot PNG files
- Matched-size within-Currier section-label null controls
- Pairwise matched within-Currier null controls
