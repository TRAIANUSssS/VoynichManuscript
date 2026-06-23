# Findings

OBS-2026-06-23-001:
`exp-008` ran with transcriber code `H`, the cleaned `exp-002b` parser policy, section metadata from `data/metadata/folio_sections.csv`, hand metadata from `data/metadata/folio_hands.csv`, 1000 iterations, seed `20260621`, and minimum group size `100` tokens.

OBS-2026-06-23-002:
All 5,216 selected `H` lines mapped to sections. 3,134 selected `H` lines mapped to valid hand labels, while 2,082 selected lines had blank hand labels and were written to `artifacts/exp008/unmapped_hand_lines.csv`.

OBS-2026-06-23-003:
Valid hand categories in the run were `1`, `2`, `3`, `4`, `5`, `X`, and `Y`.

OBS-2026-06-23-004:
The section-only recomputed mean pairwise JSD was `0.5554700431523788`, matching the historical `exp-003` reference value exactly in this run.

OBS-2026-06-23-005:
The hand-only mean pairwise JSD across valid hand groups was `0.5822290801216097`.

OBS-2026-06-23-006:
Four section-within-hand comparisons met the configured token threshold. Their mean JSD was `0.5681240941907049`.

OBS-2026-06-23-007:
Eight hand-within-section comparisons met the configured token threshold. Their mean JSD was `0.6461215587388383`.

OBS-2026-06-23-008:
No hand category had at least three valid section groups with at least `100` tokens each, so the within-hand section-label null control was not feasible and every hand received `insufficient_data` for that control.

OBS-2026-06-23-009:
The generated overall summary label was `section_signal_preserved_within_hand`.

INF-2026-06-23-001:
The available section-within-hand comparisons show that section-level token-frequency differences can still be measured inside some hand categories.

INF-2026-06-23-002:
The `section_signal_preserved_within_hand` label should be read narrowly because it is based on only four valid section-within-hand pairs and no feasible within-hand null-control distribution.

INF-2026-06-23-003:
The result does not show that the section signal is independent of hand. Sparse hand coverage and missing hand labels limit the strength of the comparison.

INF-2026-06-23-004:
The measurable hand-only and hand-within-section distances are consistent with hand category being a potentially important source of token-frequency variation, but this run does not identify a causal source.

HYP-2026-06-23-001:
The section signal may reflect a combination of section metadata, hand category, Currier category, quire or folio structure, layout, line position, transcription choices, and token-count effects.

HYP-2026-06-23-002:
Some remaining section-level signal may persist after hand stratification, but the current metadata coverage is too sparse for strong attribution.

TODO-2026-06-23-001:
Test sensitivity to the `100` token threshold before relying on the section-within-hand summary label.

TODO-2026-06-23-002:
Run a hand metadata coverage audit or add a cited independent hand metadata source before stronger hand-control claims.

TODO-2026-06-23-003:
Consider matched-size within-hand section resampling for the four available section-within-hand pairs.

TODO-2026-06-23-004:
Run quire, folio-neighborhood, layout, and line-position controls before stronger claims about section structure.

ERR-2026-06-23-001:
No runtime blocker occurred. The main limitations are 2,082 blank hand-label selected lines, no feasible within-hand section-label null control, no independent hand taxonomy, and sparse section-by-hand coverage.

ERR-2026-06-23-002:
This experiment does not provide evidence of meaning, translation, language identity, authorship, or decipherment, and it does not confirm or reject any hypothesis.
