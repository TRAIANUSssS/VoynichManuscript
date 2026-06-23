# Voynich Lab

## What This Is

Voynich Lab is a reproducible research workspace for studying the Voynich Manuscript through documented hypotheses, controlled experiments, statistical analysis, and careful review.

## Main Goal

The goal is to create a durable research memory. The project should preserve observations, interpretations, failed attempts, contradictions, and decisions without making unsupported decipherment claims.

## Current Status

Status: baseline, line-position, cleaned-parser, section-frequency, section-frequency resampling-control, section-label null-control, Currier-section interaction-control, within-Currier section-label null-control, and hand-section interaction-control experiments completed.

Initial raw transcription source has been added for `exp-001`: `data/raw/LSI_ivtff_0d.txt`, documented in `datasets/voynich_sources.md` and `methods/transcription_policy.md`.

## How a New Chat or Model Should Read the Documentation

Recommended order:

1. `main.md`
2. `philosophy.md`
3. `project_rules.md`
4. `glossary.md`
5. `hypotheses/hypotheses.md`
6. The relevant experiment folder from `experiments/`

## Document Map

- `knowledge/` - manuscript background, claims, sections, timeline, writing system, and bibliography.
- `hypotheses/` - hypothesis registry.
- `experiments/` - experiment concepts and later protocols/results/findings.
- `datasets/` - data source and corpus documentation.
- `methods/` - reusable analysis rules.
- `logs/` - decisions, changelog, conflicts, and session summaries.
- `prompts/` - task and session templates.

## Active Hypotheses

See `hypotheses/hypotheses.md`.

Initial hypotheses are open concepts, not conclusions.

## Active Experiments

- `experiments/exp-001_baseline-statistics_active_2026-06-21/` - first baseline statistics workflow run completed once; follow-up review pending.
- `experiments/exp-002_word-position-patterns_active_2026-06-21/` - line-position token distribution run completed once; parser-markup limitation needs follow-up.
- `experiments/exp-002b_clean-ivtff-parser-rerun_active_2026-06-21/` - parser-focused rerun completed; old and cleaned outputs compared.
- `experiments/exp-003_section-frequency-comparison_active_2026-06-21/` - section-frequency comparison completed using IVTFF `$I` metadata.
- `experiments/exp-004_section-frequency-resampling-control_active_2026-06-21/` - matched-token-count control completed for the `exp-003` section-frequency result.
- `experiments/exp-005_section-label-null-control_active_2026-06-21/` - pooled-label null control completed for observed and matched section-frequency distances.
- `experiments/exp-006_currier-section-interaction-control_active_2026-06-21/` - Currier-language interaction control completed; section and Currier are strongly confounded in the current metadata slice.
- `experiments/exp-007_section-label-null-control-within-currier_active_2026-06-21/` - within-Currier section-label null control completed; valid section labels were above the tested null inside both Currier A and Currier B.
- `experiments/exp-008_hand-section-interaction-control_active_2026-06-21/` - hand-section interaction control completed; section-within-hand distances remain measurable where coverage exists, but within-hand null controls were not feasible because hand-section coverage is sparse.

## Recent Important Decisions

- 2026-06-21: Create a documentation-first research structure for Voynich Lab.
- 2026-06-21: Use the IVTFF EVA interlinear transcription `H` lines as the scoped baseline input for `exp-001`.
- 2026-06-21: Keep single-token lines as a separate position class in `exp-002`.
- 2026-06-21: For cleaned IVTFF parsing, replace inline `<...>` markup with token boundaries before normalization.
- 2026-06-21: Use IVTFF `$I` page-header illustration type as the source-derived section metadata for `exp-003`.
- 2026-06-21: Treat `exp-003` section-frequency results as exploratory until matched-token-count resampling or bootstrap controls are run.
- 2026-06-21: After `exp-004`, prefer pairwise matched-size JSD for pair-specific section comparison and keep common-size resampling as a global stress test.
- 2026-06-21: After `exp-005`, prefer null-control comparisons over raw observed section JSD when evaluating whether section labels carry measurable information.
- 2026-06-23: For `exp-006`, use IVTFF page-header `$L` labels as Currier metadata and treat blank, `?`, and `-` labels as unmapped for Currier-controlled comparisons.
- 2026-06-23: After `exp-007`, treat section signal as still above the tested within-Currier null in valid groups, while keeping Currier coverage gaps and other metadata confounders unresolved.
- 2026-06-23: For `exp-008`, use IVTFF page-header `$H` labels as hand metadata and treat blank, `?`, and `-` labels as unmapped for hand-controlled comparisons.

## Next Steps

- Recommended next experiment: `exp-009_hand-metadata-coverage-audit`.
- Purpose: audit the 2,082 blank or unmapped hand-label lines, summarize their distribution by section, folio, and Currier if available, test threshold sensitivity, and decide whether hand metadata coverage can be improved or must remain a documented limitation.
- Later follow-up: matched-size within-hand section resampling, Currier metadata coverage audit, quire-section interaction control, layout controls, folio-neighborhood controls, and line-position controls.
- Add verified sources for manuscript background notes.
