# exp-004 Section Frequency Resampling Control

- Experiment ID: `exp-004_section-frequency-resampling-control`
- Status: `active`
- Date: `2026-06-21`
- Goal: test whether the section-level token-frequency differences observed in `exp-003` remain visible after matched-token-count resampling.
- Related hypotheses: `H-005`, `H-006`
- Data used: `data/raw/LSI_ivtff_0d.txt` with `data/metadata/folio_sections.csv`, transcriber code `H`
- Current conclusion: the observed `exp-003` section differences remain measurable under resampling controls, but the magnitude depends on whether comparisons are forced to the global minimum section size or matched pairwise.

## Files

- `protocol.md` - question, parser policy, resampling design, success criteria, and limitations.
- `results.md` - reproducible run facts and numerical outputs.
- `findings.md` - labeled observations and cautious interpretations.
- `artifacts.md` - generated artifact index.
- `questions.md` - follow-up questions and next checks.

## Key Artifact Paths

- `artifacts/exp004/run_summary.json`
- `artifacts/exp004/common_size_resampling_summary.csv`
- `artifacts/exp004/common_size_pairwise_jsd.csv`
- `artifacts/exp004/pairwise_matched_jsd.csv`
- `artifacts/exp004/observed_vs_resampled_jsd.csv`
