# Voynich Lab

## What This Is

Voynich Lab is a reproducible research workspace for studying the Voynich Manuscript through documented hypotheses, controlled experiments, statistical analysis, and careful review.

## Main Goal

The goal is to create a durable research memory. The project should preserve observations, interpretations, failed attempts, contradictions, and decisions without making unsupported decipherment claims.

## Current Status

Status: baseline, line-position, and cleaned-parser rerun experiments completed on 2026-06-21.

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

## Recent Important Decisions

- 2026-06-21: Create a documentation-first research structure for Voynich Lab.
- 2026-06-21: Use the IVTFF EVA interlinear transcription `H` lines as the scoped baseline input for `exp-001`.
- 2026-06-21: Keep single-token lines as a separate position class in `exp-002`.
- 2026-06-21: For cleaned IVTFF parsing, replace inline `<...>` markup with token boundaries before normalization.

## Next Steps

- Decide whether cleaned parser outputs should supersede old parser-limited outputs for future baselines.
- Consider refactoring the cleaned parser into shared utilities before adding control corpora or folio metadata.
- Add verified sources for manuscript background notes.
