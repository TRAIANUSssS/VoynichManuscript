# Findings

OBS-2026-06-23-001:
`exp-007` ran with transcriber code `H`, the cleaned `exp-002b` parser policy, section metadata from `data/metadata/folio_sections.csv`, Currier metadata from `data/metadata/folio_currier.csv`, 1000 iterations, seed `20260621`, and minimum section group size `100` tokens.

OBS-2026-06-23-002:
All 5,216 selected `H` lines mapped to sections. 4,464 selected `H` lines mapped to valid Currier labels, while 752 selected lines had blank Currier labels and were written to `artifacts/exp007/unmapped_currier_lines.csv`.

OBS-2026-06-23-003:
Currier A had 3 valid section groups: `herbal`, `pharmaceutical`, and `text`. Currier B had 5 valid section groups: `biological`, `cosmological`, `herbal`, `stars`, and `text`.

OBS-2026-06-23-004:
Inside Currier A, observed mean section-pair JSD was `0.5355956685429015`, while the within-Currier section-label null mean was `0.38805169568795816` and the null 97.5% quantile was `0.39941216554950554`.

OBS-2026-06-23-005:
Inside Currier B, observed mean section-pair JSD was `0.46397711540843006`, while the within-Currier section-label null mean was `0.3449325698805918` and the null 97.5% quantile was `0.35311149369219175`.

OBS-2026-06-23-006:
Both Currier A and Currier B observed mean section-pair JSD values were above their 97.5% null quantiles. Both empirical p-values were `0.000999000999000999`, the minimum possible value under the 1000-iteration setup and selected empirical p-value formula.

OBS-2026-06-23-007:
All 13 valid pairwise within-Currier section comparisons were above their pairwise 97.5% null quantiles.

OBS-2026-06-23-008:
The generated overall summary label was `section_signal_above_null_in_both_currier_groups`.

INF-2026-06-23-001:
Under this within-Currier section-label null model, random section-label reassignment inside Currier A and inside Currier B did not reproduce the observed section-level token-frequency distances.

INF-2026-06-23-002:
The result weakens the possibility that the section signal is fully explained by Currier A/B composition alone.

INF-2026-06-23-003:
The result does not show that section effects are independent of all metadata factors. Hand, quire, folio, layout, line position, transcription choices, and unresolved Currier coverage remain possible contributors.

INF-2026-06-23-004:
Currier A remains sparse because only three section groups meet the token threshold, so the Currier A result should be treated as useful but coverage-limited.

HYP-2026-06-23-001:
Some section-level token-frequency structure may remain after fixing Currier category.

HYP-2026-06-23-002:
The remaining signal may reflect section category, hand, folio or quire structure, layout, transcription effects, or a combination of factors.

TODO-2026-06-23-001:
Audit blank Currier labels before relying on Currier-controlled analyses for sections excluded by the current mapping.

TODO-2026-06-23-002:
Run hand-section interaction controls to test whether hand metadata explains part of the remaining within-Currier section signal.

TODO-2026-06-23-003:
Consider matched-size within-Currier null controls to reduce sensitivity to uneven section group sizes.

ERR-2026-06-23-001:
No runtime blocker occurred. The main limitations are sparse section-by-Currier coverage, 752 blank Currier labels, and the absence of controls for hand, quire, layout, folio neighborhood, line position, and alternate transcription policies.

ERR-2026-06-23-002:
This experiment does not provide evidence of meaning, translation, language identity, authorship, or decipherment, and it does not confirm or reject any hypothesis.
