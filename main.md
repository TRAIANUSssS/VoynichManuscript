# Voynich Lab

## What This Is

Voynich Lab is a reproducible research workspace for studying the Voynich Manuscript through documented hypotheses, controlled experiments, statistical analysis, and careful review.

## Main Goal

The goal is to create a durable research memory. The project should preserve observations, interpretations, failed attempts, contradictions, and decisions without making unsupported decipherment claims.

## Current Status

Status: first baseline workflow run completed on 2026-06-21.

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

## Recent Important Decisions

- 2026-06-21: Create a documentation-first research structure for Voynich Lab.
- 2026-06-21: Use the IVTFF EVA interlinear transcription `H` lines as the scoped baseline input for `exp-001`.

## Next Steps

- Review `exp-001` artifacts and limitations.
- Decide whether the next experiment should add control corpora, folio metadata, or EVA-aware glyph parsing.
- Add verified sources for manuscript background notes.
