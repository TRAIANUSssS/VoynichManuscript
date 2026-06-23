# Artifacts

- `artifacts/exp006/run_summary.json` - run metadata, parser audit counts, metadata sources, key numerical summaries, and generated artifact list.
- `artifacts/exp006/metadata_coverage.json` - section and Currier mapping coverage for selected `H` lines.
- `artifacts/exp006/section_currier_contingency_lines.csv` - line-count contingency table by section and Currier language.
- `artifacts/exp006/section_currier_contingency_tokens.csv` - token-count contingency table by section and Currier language.
- `artifacts/exp006/section_currier_percentages.csv` - section-token and Currier-token percentage table.
- `artifacts/exp006/currier_summary.csv` - line counts, token counts, TTR, entropy, and token-length statistics by Currier category.
- `artifacts/exp006/currier_token_counts.csv` - token counts by Currier category.
- `artifacts/exp006/currier_token_shares.csv` - token shares by Currier category.
- `artifacts/exp006/top_tokens_by_currier.csv` - top tokens by Currier category.
- `artifacts/exp006/pairwise_currier_distances.csv` - pairwise JSD between Currier categories.
- `artifacts/exp006/section_only_recomputed_distances.csv` - recomputed section-only JSD distances for internal replication.
- `artifacts/exp006/section_summary_recomputed.csv` - recomputed section summary statistics.
- `artifacts/exp006/section_within_currier_groups.csv` - section group coverage within each Currier category.
- `artifacts/exp006/section_within_currier_distances.csv` - pairwise section JSD distances within Currier categories.
- `artifacts/exp006/currier_within_section_groups.csv` - Currier group coverage within each section.
- `artifacts/exp006/currier_within_section_distances.csv` - pairwise Currier JSD distances within sections where possible.
- `artifacts/exp006/signal_attribution_summary.csv` - conservative summary comparing section-only, Currier-only, section-within-Currier, and Currier-within-section distances.
- `artifacts/exp006/unmapped_section_lines.csv` - explicit audit file for section-unmapped selected lines.
- `artifacts/exp006/unmapped_currier_lines.csv` - explicit audit file for Currier-unmapped selected lines.

Not generated in this run:

- Plot PNG files
- Matched-size within-Currier section resampling artifacts
- Section-label null controls within Currier categories
- Currier-label null controls within sections
