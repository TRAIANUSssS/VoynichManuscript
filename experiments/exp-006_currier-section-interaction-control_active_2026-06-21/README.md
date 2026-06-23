# exp-006 Currier Section Interaction Control

- Experiment ID: `exp-006_currier-section-interaction-control`
- Status: `active`
- Date: `2026-06-21`
- Run date: `2026-06-23`
- Goal: test whether IVTFF `$I` section-level token-frequency differences remain visible after accounting for Currier language labels.
- Related hypotheses: `H-005`, `H-006`
- Data used: `data/raw/LSI_ivtff_0d.txt`, transcriber code `H`
- Section metadata: `data/metadata/folio_sections.csv`
- Currier metadata: `data/metadata/folio_currier.csv`
- Current conclusion: Currier and section are strongly confounded in this dataset slice. Section differences remain measurable inside Currier categories where comparisons are possible, but many section-Currier combinations are absent and the source of the section signal remains unresolved.

## Files

- `protocol.md` - research question, parser policy, metadata policy, comparison design, labels, and limitations.
- `results.md` - reproducible run facts and numerical outputs.
- `findings.md` - labeled observations and cautious interpretations.
- `artifacts.md` - generated artifact index.
- `questions.md` - follow-up questions and next checks.

## Key Artifact Paths

- `artifacts/exp006/run_summary.json`
- `artifacts/exp006/metadata_coverage.json`
- `artifacts/exp006/section_currier_contingency_tokens.csv`
- `artifacts/exp006/pairwise_currier_distances.csv`
- `artifacts/exp006/section_within_currier_distances.csv`
- `artifacts/exp006/currier_within_section_distances.csv`
- `artifacts/exp006/signal_attribution_summary.csv`
- `artifacts/exp006/unmapped_currier_lines.csv`
