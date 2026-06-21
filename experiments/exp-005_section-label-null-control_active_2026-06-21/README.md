# exp-005 Section Label Null Control

- Experiment ID: `exp-005_section-label-null-control`
- Status: `active`
- Date: `2026-06-21`
- Goal: test whether section-level token-frequency distances remain larger than expected under random section-label assignment.
- Related hypotheses: `H-005`, `H-006`
- Data used: `data/raw/LSI_ivtff_0d.txt` with `data/metadata/folio_sections.csv`, transcriber code `H`
- Current conclusion: under this pooled-label null model, the observed section-level distances are consistently larger than random label assignment would predict, but the cause of the section signal remains unresolved.

## Files

- `protocol.md` - research question, parser policy, null-control design, metrics, and limitations.
- `results.md` - reproducible run facts and numerical outputs.
- `findings.md` - labeled observations and cautious interpretations.
- `artifacts.md` - generated artifact index.
- `questions.md` - follow-up questions and next checks.

## Key Artifact Paths

- `artifacts/exp005/run_summary.json`
- `artifacts/exp005/pairwise_null_control.csv`
- `artifacts/exp005/pairwise_matched_null_control.csv`
- `artifacts/exp005/global_section_label_permutation.csv`
- `artifacts/exp005/observed_vs_null_jsd.csv`
