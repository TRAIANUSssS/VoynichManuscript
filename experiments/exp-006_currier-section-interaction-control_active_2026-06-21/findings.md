# Findings

OBS-2026-06-23-001:
`exp-006` ran with transcriber code `H`, the cleaned `exp-002b` parser policy, section metadata from `data/metadata/folio_sections.csv`, Currier metadata from `data/metadata/folio_currier.csv`, minimum token threshold `100`, iterations `1000`, and seed `20260621`.

OBS-2026-06-23-002:
All 5,216 selected `H` lines mapped to sections, and 4,464 selected `H` lines mapped to valid Currier labels. The remaining 752 selected lines had blank Currier labels and were written to `artifacts/exp006/unmapped_currier_lines.csv`.

OBS-2026-06-23-003:
The recomputed section-only mean pairwise JSD was `0.5554700431523788`, matching the historical `exp-003` mean pairwise section JSD.

OBS-2026-06-23-004:
Currier A contained 11,450 cleaned tokens and Currier B contained 23,224 cleaned tokens. The A-vs-B JSD was `0.4743758913991697`.

OBS-2026-06-23-005:
The section-Currier token contingency was sparse. `biological`, `cosmological`, and `stars` had valid Currier B tokens only; `pharmaceutical` had valid Currier A tokens only; `herbal` and `text` had both A and B tokens; `astronomical` and `zodiac` had no valid Currier-labeled tokens under this mapping policy.

OBS-2026-06-23-006:
Section-within-Currier comparisons produced 13 valid section pairs with overall mean JSD `0.48050447382407735`. Currier A had 3 valid section pairs with mean JSD `0.5355956685429015`; Currier B had 10 valid section pairs with mean JSD `0.46497751540843016`.

OBS-2026-06-23-007:
Currier-within-section comparisons were possible only for `herbal` and `text`. Their A-vs-B JSD values were `0.5470516861625053` and `0.6694991834898794`, respectively.

OBS-2026-06-23-008:
The generated signal attribution label for section-within-Currier comparison was `section_currier_strongly_confounded`.

INF-2026-06-23-001:
Currier language is a substantial metadata factor in this dataset slice, and section-level comparisons are not independent of Currier composition.

INF-2026-06-23-002:
Section-level token-frequency differences remain measurable within Currier categories where enough data exists, but sparse section-Currier coverage prevents a clean separation of section effects from Currier effects.

INF-2026-06-23-003:
The lower section-within-Currier mean JSD compared with the full section-only mean JSD is consistent with Currier composition explaining part of the section-level signal, but it does not show that Currier fully explains the signal.

INF-2026-06-23-004:
Because only `herbal` and `text` support within-section Currier A/B comparisons at the configured threshold, the Currier-within-section result should be treated as a limited coverage check rather than a global result.

HYP-2026-06-23-001:
The section signal may reflect a combination of IVTFF section metadata, Currier language, hand, layout, folio or quire structure, and transcription effects.

HYP-2026-06-23-002:
Some section-level variation may remain after Currier control, but a stronger test needs less sparse metadata combinations or additional constrained controls.

TODO-2026-06-23-001:
Run a hand-section interaction control before making stronger claims about section structure.

TODO-2026-06-23-002:
Add constrained null controls within Currier categories, such as section-label permutations inside Currier A and Currier B.

TODO-2026-06-23-003:
Consider matched-size section resampling within Currier categories to reduce the effect of uneven section-Currier group sizes.

TODO-2026-06-23-004:
Investigate whether blank Currier labels can be resolved from a cited metadata source before rerunning interaction analysis.

ERR-2026-06-23-001:
No runtime blocker occurred. The main limitation is interpretive and coverage-based: Currier and section are strongly confounded, and 752 selected lines lack valid Currier labels under the current mapping policy.

ERR-2026-06-23-002:
This experiment does not provide evidence of meaning, translation, language identity, authorship, or decipherment, and it does not confirm or reject any hypothesis.
