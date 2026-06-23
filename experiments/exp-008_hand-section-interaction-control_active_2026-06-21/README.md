# exp-008 Hand-Section Interaction Control

- Experiment ID: `exp-008_hand-section-interaction-control`
- Status: `active`
- Date: `2026-06-21`
- Run date: `2026-06-23`
- Goal: test whether IVTFF `$I` section-level token-frequency differences remain visible after accounting for IVTFF `$H` hand categories.
- Related hypotheses: `H-005`, `H-006`
- Data used: `data/raw/LSI_ivtff_0d.txt`, transcriber code `H`
- Section metadata: `data/metadata/folio_sections.csv`
- Hand metadata: `data/metadata/folio_hands.csv`
- Current conclusion: section-within-hand distances remain measurable in four valid section pairs and their mean is close to the full section-only mean, but hand metadata coverage is sparse and no hand has enough valid section groups for the within-hand section-label null control.

## Files

- `protocol.md` - research question, parser policy, metadata policy, method, labels, and limitations.
- `results.md` - reproducible run facts and numerical outputs.
- `findings.md` - labeled observations and cautious interpretations.
- `artifacts.md` - generated artifact index.
- `questions.md` - follow-up questions and next checks.

## Key Artifact Paths

- `artifacts/exp008/run_summary.json`
- `artifacts/exp008/metadata_coverage.json`
- `artifacts/exp008/section_hand_contingency_tokens.csv`
- `artifacts/exp008/hand_summary.csv`
- `artifacts/exp008/pairwise_hand_distances.csv`
- `artifacts/exp008/section_within_hand_distances.csv`
- `artifacts/exp008/hand_within_section_distances.csv`
- `artifacts/exp008/within_hand_null_summary.csv`
- `artifacts/exp008/signal_attribution_summary.csv`
- `artifacts/exp008/unmapped_hand_lines.csv`
