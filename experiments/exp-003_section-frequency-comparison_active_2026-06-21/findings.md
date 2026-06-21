# Findings

OBS-2026-06-21-001:
All 5,216 selected `H` lines mapped to a section from `data/metadata/folio_sections.csv`.

OBS-2026-06-21-002:
The run produced eight section categories: `astronomical`, `biological`, `cosmological`, `herbal`, `pharmaceutical`, `stars`, `text`, and `zodiac`.

OBS-2026-06-21-003:
Token counts by section were uneven. The largest section by token count was `herbal` with 11,418 tokens; the smallest was `astronomical` with 850 tokens.

OBS-2026-06-21-004:
The minimum pairwise section Jensen-Shannon divergence was 0.3347291601069759 bits for `biological` vs `stars`.

OBS-2026-06-21-005:
The maximum pairwise section Jensen-Shannon divergence was 0.7132735389659056 bits for `astronomical` vs `biological`.

OBS-2026-06-21-006:
The mean pairwise section Jensen-Shannon divergence was 0.5554700431523788 bits, compared with the cleaned `exp-002b` mean position-class divergence of 0.5398947694637786 bits.

INF-2026-06-21-001:
The section-level token distributions are measurably different under Jensen-Shannon divergence, but the experiment does not identify whether the differences reflect section/topic, Currier language, hand, page layout, sample size, or transcription effects.

INF-2026-06-21-002:
High TTR values in smaller sections such as `astronomical` and `zodiac` may be strongly affected by sample size, so they should not be compared naively with larger sections.

HYP-2026-06-21-001:
Some IVTFF `$I` section categories may have distinct token-frequency profiles, but this requires follow-up controls for section size, Currier language, hand, and line position.

TODO-2026-06-21-001:
Run a follow-up that stratifies or compares section differences against Currier language and hand metadata already present in the same IVTFF page headers.

TODO-2026-06-21-002:
Add a resampling or bootstrap comparison so smaller sections can be compared with larger sections at matched token counts.

ERR-2026-06-21-001:
No blocker occurred. The main limitation is that section metadata comes from IVTFF `$I` illustration type codes, not an independently verified section taxonomy.
