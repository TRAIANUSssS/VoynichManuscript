# exp-002b: Clean IVTFF Parser Rerun

Experiment ID: exp-002b
Status: active
Created: 2026-06-21

## Goal

Audit and improve IVTFF token extraction so inline angle-tag markup and metadata do not become normalized manuscript tokens, then rerun `exp-001` and `exp-002` under the cleaned parser policy.

## Related Experiments

- `experiments/exp-001_baseline-statistics_active_2026-06-21/`
- `experiments/exp-002_word-position-patterns_active_2026-06-21/`

## Data Used

- Raw input: `data/raw/LSI_ivtff_0d.txt`
- Source: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Transcriber code: `H`

## Current Conclusion

OBS-2026-06-21-001:
The cleaned parser removes inline `<...>` tag content from normalized token text and changes baseline and position-distribution outputs relative to the historical `exp-001` and `exp-002` runs.

INF-2026-06-21-001:
Future text-statistics experiments should use a documented IVTFF markup policy rather than the original `exp-001` parser.

## Files

- `protocol.md`
- `results.md`
- `findings.md`
- `artifacts.md`
- `questions.md`
