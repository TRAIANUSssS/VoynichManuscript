# exp-001: Baseline Statistics

Status: concept
Created: 2026-06-21

## Goal

Test the end-to-end workflow for reproducible analysis, artifact generation, and documentation. This experiment is not intended to decipher the manuscript.

## Related Hypotheses

- H-001
- H-002
- H-003
- H-004
- H-005
- H-006

## Research Question

Can the project load a documented transcription and produce basic reproducible text statistics with saved outputs and documented limitations?

## Data

Current transcription: not selected.

Status: `needs-source`

## Planned Metrics

- token count;
- type count;
- token frequencies;
- glyph frequencies;
- word-length distribution;
- basic entropy;
- simple charts.

## Expected Outputs

- CSV files for token and glyph frequencies;
- JSON run metadata;
- charts for basic distributions;
- results documentation.

## Success Criteria

- The command can be rerun from a clean checkout.
- Input data and parameters are documented.
- Outputs are saved under `artifacts/exp001/`.
- Results and findings are separated.

## Failure Criteria

- The run depends on hidden notebook state.
- Data provenance is undocumented.
- Results cannot be reproduced.
- Interpretation is mixed into factual results.

## Documentation Updates Required

- `datasets/`
- `methods/transcription_policy.md`
- `experiments/exp-001...`
- `logs/changelog.md`
- `logs/session_summaries.md` if the experiment is run.

## Next Steps

- Select a transcription source.
- Write a protocol before running analysis.
- Implement a command-line script.

