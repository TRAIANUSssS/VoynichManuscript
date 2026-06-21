# Changelog

## 2026-06-21 - Created starter documentation structure

- Created the initial Voynich Lab documentation structure.
- Added starter files for knowledge, hypotheses, experiments, datasets, methods, prompts, logs, scripts, notebooks, artifacts, data, and tests.
- Marked unsourced manuscript and bibliography details as `needs-source` or TODO.
- Did not run any experiment.

## 2026-06-21 - Clarified agent documentation rules

- Added rules for project document language.
- Added source requirements for manuscript, historical, scientific, bibliographic, and theory-status claims.
- Clarified the distinction between `results.md` and `findings.md`.
- Clarified when to update `changelog.md`, `decision_log.md`, and `session_summaries.md`.

## 2026-06-21 - Ran exp-001 baseline statistics workflow

- Added raw IVTFF EVA transcription file `data/raw/LSI_ivtff_0d.txt`.
- Added `scripts/exp001_baseline_stats.py`.
- Generated `artifacts/exp001/` CSV, JSON, and PNG outputs.
- Created `experiments/exp-001_baseline-statistics_active_2026-06-21/` with protocol, results, findings, questions, rejected findings, and artifact index.
- Marked the original `experiments/exp-001_baseline-statistics_concept_2026-06-21.md` as superseded.
- Updated dataset documentation, transcription policy, project navigation, decision log, and session summary.

## 2026-06-21 - Ran exp-002 word-position patterns workflow

- Added `scripts/exp002_word_position_patterns.py`.
- Generated `artifacts/exp002/` CSV, JSON, and PNG outputs.
- Created `experiments/exp-002_word-position-patterns_active_2026-06-21/` with experiment description, results, findings, and notes.
- Updated project navigation, script/artifact indexes, decision log, and session summary.
- Documented the parser-markup limitation discovered under `exp-001`-compatible normalization.

## 2026-06-21 - Ran exp-002b cleaned IVTFF parser rerun

- Added `scripts/exp002b_clean_ivtff_parser_rerun.py`.
- Generated `artifacts/exp002b/` cleaned baseline outputs, cleaned position outputs, parser audit examples, and old-vs-cleaned comparison tables.
- Created `experiments/exp-002b_clean-ivtff-parser-rerun_active_2026-06-21/`.
- Updated transcription policy, project navigation, script/artifact indexes, decision log, conflict log, and session summary.
- Preserved old `exp-001` and `exp-002` artifacts unchanged.

## 2026-06-21 - Ran exp-003 section frequency comparison

- Added `scripts/exp003_section_frequency_comparison.py`.
- Generated `data/metadata/folio_sections.csv` from IVTFF page header `$I` metadata.
- Generated `artifacts/exp003/` section summaries, token tables, overrepresentation tables, pairwise distances, section-vs-position comparisons, unmapped-line audit, and plots.
- Created `experiments/exp-003_section-frequency-comparison_active_2026-06-21/`.
- Updated section knowledge, project navigation, script/artifact indexes, decision log, and session summary.
