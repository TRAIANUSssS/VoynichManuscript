# Findings

OBS-2026-06-21-001:
All 5,216 selected `H` lines mapped to the reused `exp-003` / `exp-004` section metadata, and `artifacts/exp005/unmapped_lines.csv` contains no unmapped selected lines.

OBS-2026-06-21-002:
The pairwise pooled-label null control ran for 28 section pairs with 1000 iterations and seed 20260621.

OBS-2026-06-21-003:
For all 28 section pairs, observed full-section JSD was above the 97.5% null quantile under the pooled-label null control.

OBS-2026-06-21-004:
For all 28 section pairs, the `exp-004` pairwise matched reference JSD was above the 97.5% matched null quantile under the pooled-label matched null control.

OBS-2026-06-21-005:
The observed `exp-003` mean pairwise JSD was `0.5554700431523788`, while the global section-label permutation null mean was `0.3788255370327812`, with null 97.5% quantile `0.38500785795761844`.

OBS-2026-06-21-006:
The closest and most distant pairs remained `biological` vs `stars` and `astronomical` vs `biological`. Under the pooled-label null control, both were still above the 97.5% null quantile.

OBS-2026-06-21-007:
All reported empirical p-values in the generated pairwise and global null summaries were `0.000999000999000999`, which is the smallest attainable value under 1000 null iterations with the selected empirical p-value formula.

INF-2026-06-21-001:
Under this null model, random section-label assignment does not reproduce the observed section-level token-frequency distances. The section labels preserve measurable token-frequency information beyond random grouping.

INF-2026-06-21-002:
The null-control result strengthens the claim that the section-level signal from `exp-003` and `exp-004` is not only a token-count artifact or a trivial random grouping effect.

INF-2026-06-21-003:
This experiment still does not identify what produces the section-label signal. Currier language, scribal hand, layout, folio or quire structure, or other metadata factors may still account for part or all of the effect.

HYP-2026-06-21-001:
Some section-level token-distribution differences may reflect stable structural variation in the transcription data rather than random label assignment alone.

TODO-2026-06-21-001:
Test section, Currier language, and hand interactions before interpreting the section signal as topic or register variation.

TODO-2026-06-21-002:
Consider repeating the null model with additional designs, such as constrained permutations by Currier language, hand, quire, or folio neighborhood.

TODO-2026-06-21-003:
If stronger inferential work is needed, increase null iterations beyond 1000 or add alternative null baselines while continuing to report the exploratory nature of empirical p-values.

ERR-2026-06-21-001:
No runtime blocker occurred. The main limitation is interpretive: the null-control result shows non-random structure under this label-randomization design, but it does not explain the source or meaning of that structure.
