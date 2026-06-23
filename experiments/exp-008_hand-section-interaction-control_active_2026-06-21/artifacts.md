# Artifacts

- `artifacts/exp008/run_summary.json` - run metadata, parser audit counts, metadata sources, summary labels, and generated artifact list.
- `artifacts/exp008/metadata_coverage.json` - section and hand mapping coverage for selected `H` lines.
- `artifacts/exp008/section_hand_contingency_lines.csv` - line counts for each section-by-hand group.
- `artifacts/exp008/section_hand_contingency_tokens.csv` - token counts for each section-by-hand group.
- `artifacts/exp008/section_hand_percentages.csv` - section and hand percentage shares for each section-by-hand group.
- `artifacts/exp008/dominant_hand_by_section.csv` - dominant valid hand category per section and dominance share.
- `artifacts/exp008/hand_summary.csv` - hand-level line, token, unique-token, TTR, entropy, and mean-token-length summary.
- `artifacts/exp008/hand_token_counts.csv` - token counts by valid hand category.
- `artifacts/exp008/hand_token_shares.csv` - token shares by valid hand category.
- `artifacts/exp008/top_tokens_by_hand.csv` - top tokens per valid hand category.
- `artifacts/exp008/pairwise_hand_distances.csv` - pairwise JSD between hand categories meeting the token threshold.
- `artifacts/exp008/section_only_recomputed_distances.csv` - full section-only pairwise JSD replication check.
- `artifacts/exp008/section_within_hand_distances.csv` - pairwise section JSD inside valid hand categories.
- `artifacts/exp008/section_within_hand_groups.csv` - valid and excluded section groups inside hand categories.
- `artifacts/exp008/hand_within_section_distances.csv` - pairwise hand JSD inside valid sections.
- `artifacts/exp008/hand_within_section_groups.csv` - valid and excluded hand groups inside sections.
- `artifacts/exp008/within_hand_null_summary.csv` - within-hand section-label null feasibility and summary labels.
- `artifacts/exp008/within_hand_null_summary.json` - JSON copy of the within-hand null summary.
- `artifacts/exp008/within_hand_null_iterations.csv` - raw within-hand null iteration values; header-only in this run because no hand category was feasible.
- `artifacts/exp008/pairwise_within_hand_null_control.csv` - pairwise within-hand null-control summaries; header-only in this run because no hand category was feasible.
- `artifacts/exp008/pairwise_within_hand_null_control.json` - JSON copy of pairwise within-hand null-control summaries.
- `artifacts/exp008/signal_attribution_summary.csv` - section-only, hand-only, section-within-hand, hand-within-section, null-control, and overall summary.
- `artifacts/exp008/unmapped_section_lines.csv` - explicit audit file for section-unmapped selected lines.
- `artifacts/exp008/unmapped_hand_lines.csv` - explicit audit file for hand-unmapped selected lines.
- `artifacts/exp008/section_currier_hand_coverage.csv` - optional section-Currier-hand coverage table for planning only.

Not generated in this run:

- Plot PNG files
- Matched-size within-hand section resampling
- Hand-label null controls within sections
- Three-way Currier-hand-section model
