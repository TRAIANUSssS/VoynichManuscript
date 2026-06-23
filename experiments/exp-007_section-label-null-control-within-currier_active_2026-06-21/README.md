# exp-007 Section Label Null Control Within Currier

- Experiment ID: `exp-007_section-label-null-control-within-currier`
- Status: `active`
- Date: `2026-06-21`
- Run date: `2026-06-23`
- Goal: test whether IVTFF `$I` section labels preserve token-frequency structure above random section-label reassignment inside Currier A and Currier B separately.
- Related hypotheses: `H-005`, `H-006`
- Data used: `data/raw/LSI_ivtff_0d.txt`, transcriber code `H`
- Section metadata: `data/metadata/folio_sections.csv`
- Currier metadata: `data/metadata/folio_currier.csv`
- Current conclusion: section labels were above the tested within-Currier null model in both Currier A and Currier B among valid section groups, but coverage remains sparse and the source of the signal is not identified.

## Files

- `protocol.md` - research question, parser policy, metadata policy, null-control design, labels, and limitations.
- `results.md` - reproducible run facts and numerical outputs.
- `findings.md` - labeled observations and cautious interpretations.
- `artifacts.md` - generated artifact index.
- `questions.md` - follow-up questions and next checks.

## Key Artifact Paths

- `artifacts/exp007/run_summary.json`
- `artifacts/exp007/metadata_coverage.json`
- `artifacts/exp007/within_currier_null_summary.csv`
- `artifacts/exp007/pairwise_within_currier_null_control.csv`
- `artifacts/exp007/signal_summary.csv`
- `artifacts/exp007/unmapped_currier_lines.csv`
