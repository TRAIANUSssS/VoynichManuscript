# exp-001: Baseline Statistics

Experiment ID: exp-001
Status: active
Created: 2026-06-21
Run date: 2026-06-21

## Goal

Test the end-to-end Voynich Lab workflow: documented raw input, reproducible script, generated artifacts, results documentation, findings, and logs.

This experiment is not a decipherment attempt and does not make claims about manuscript meaning.

## Related Hypotheses

- H-001
- H-002
- H-003
- H-004
- H-005
- H-006

## Data Used

- Raw file: `data/raw/LSI_ivtff_0d.txt`
- Source URL: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html
- Selected line set: IVTFF transcriber code `H`, identified in the file comments as Takeshi Takahashi's full transcription.

## Current Conclusion

OBS-2026-06-21-001:
The workflow produced reproducible baseline counts, CSV tables, PNG charts, and run metadata under `artifacts/exp001/`.

INF-2026-06-21-001:
The project now has a working first-pass text-statistics pipeline, but the output should be treated as a baseline workflow test rather than evidence for any interpretation of the manuscript.

## Files

- `protocol.md`
- `results.md`
- `findings.md`
- `rejected_findings.md`
- `questions.md`
- `artifacts.md`
