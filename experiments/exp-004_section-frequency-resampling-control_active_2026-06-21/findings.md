# Findings

OBS-2026-06-21-001:
All 5,216 selected `H` lines mapped to the reused `exp-003` section metadata, and `artifacts/exp004/unmapped_lines.csv` contains no unmapped selected lines.

OBS-2026-06-21-002:
The common sample size was `850`, equal to the smallest section token count (`astronomical`).

OBS-2026-06-21-003:
The observed `exp-003` mean pairwise section JSD was `0.5554700431523788` bits. Under `exp-004`, the common-size mean pairwise JSD was `0.6479551071976217` bits and the pairwise matched mean pairwise JSD was `0.5870200377032155` bits.

OBS-2026-06-21-004:
The smallest and largest section pairs remained the same across observed and resampled comparisons: the smallest pair stayed `biological` vs `stars`, and the largest pair stayed `astronomical` vs `biological`.

OBS-2026-06-21-005:
For `biological` vs `stars`, observed JSD was `0.3347291601069759`, common-size mean JSD was `0.5133877274319135`, and pairwise matched mean JSD was `0.3453271743396462`.

OBS-2026-06-21-006:
For `herbal` vs `stars`, observed JSD was `0.4462304641923659`, common-size mean JSD was `0.6501049318500001`, and pairwise matched mean JSD was `0.4480812950059133`.

OBS-2026-06-21-007:
Common-size section TTR values for large sections were much higher than their original full-section TTR values from `exp-003`; for example, `herbal` changed from `0.29409703976177964` in `exp-003` to mean `0.5985623529411764` at common sample size `850`.

INF-2026-06-21-001:
The section-level differences observed in `exp-003` were not removed by matched-token-count resampling. The rank order of the closest and most distant section pairs remained stable in this run.

INF-2026-06-21-002:
The global common-size control appears harsher than the pairwise matched control because it forces every comparison down to the `850`-token floor set by `astronomical`. This increases many pairwise distances relative to both observed `exp-003` values and pairwise matched-size values.

INF-2026-06-21-003:
Naive section TTR comparisons from uneven full-section counts are sample-size-sensitive. The common-size resampling shows that large sections can appear much more type-rich when reduced to the smallest section size.

INF-2026-06-21-004:
The pairwise matched-size control is more conservative than the global common-size control for large-large section comparisons. In this run it stayed close to the observed `exp-003` JSD for pairs such as `herbal` vs `stars` and `cosmological` vs `pharmaceutical`.

HYP-2026-06-21-001:
Some section-level token-distribution differences may be robust to token-count matching, but remaining differences may still reflect Currier language, hand, layout, or other metadata effects rather than section/topic alone.

TODO-2026-06-21-001:
Add a pooled-label null or permutation-style control so observed and resampled JSD values can be compared against a label-randomized baseline.

TODO-2026-06-21-002:
Run section-by-Currier-language and section-by-hand interaction controls before making stronger claims about section structure.

TODO-2026-06-21-003:
Record whether future section-frequency summaries should report both common-size and pairwise matched-size controls by default.

ERR-2026-06-21-001:
No runtime blocker occurred. The main unresolved limitation is that this experiment controls token count only and does not isolate Currier language, hand, line position, or other metadata confounders.
