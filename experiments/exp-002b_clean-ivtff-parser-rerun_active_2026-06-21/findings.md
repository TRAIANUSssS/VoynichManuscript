# Findings

OBS-2026-06-21-001:
The cleaned parser removed 4,467 inline angle tags from 2,229 selected `H` lines, with 111 unique angle-tag forms removed.

OBS-2026-06-21-002:
The cleaned baseline token count was 37,967, which is 849 higher than the old `exp-001` token count of 37,118.

OBS-2026-06-21-003:
The cleaned unique token count was 8,071, which is 980 lower than the old `exp-001` unique token count of 9,051.

OBS-2026-06-21-004:
The cleaned glyph/character count was 191,545, which is 9,982 lower than the old `exp-001` glyph/character count of 201,527.

OBS-2026-06-21-005:
The cleaned token entropy was 10.451632120067082 bits, compared with 10.675741463409675 bits in the old `exp-001` run.

OBS-2026-06-21-006:
The top token remained `daiin`, increasing from 751 old occurrences to 864 cleaned occurrences.

OBS-2026-06-21-007:
The cleaned line-medial token count increased by 849, while line-initial, line-final, and single-token-line counts were unchanged.

OBS-2026-06-21-008:
All three reported Jensen-Shannon divergence comparisons decreased after cleaning.

INF-2026-06-21-001:
The old parser inflated unique-token and glyph/character counts by allowing IVTFF markup text to enter normalized token strings.

INF-2026-06-21-002:
The cleaned token count increased because replacing tags with token boundaries splits some strings that were previously joined across markup.

INF-2026-06-21-003:
The large decrease in line-final unique token count is consistent with removing markup-derived suffixes such as `plant` from tokens that previously appeared line-final.

HYP-2026-06-21-001:
Some position-distribution differences seen in old `exp-002` may have been partly parser artifacts. This requires rerunning future position experiments with the cleaned parser and then checking folio, section, hand, and control-corpus baselines.

TODO-2026-06-21-001:
Use the cleaned parser policy for future baseline and line-position experiments unless a later protocol explicitly replaces it.

TODO-2026-06-21-002:
Add token-level audit output with locator, raw text span, cleaned token, and removed markup context if parser behavior becomes a central research question.

ERR-2026-06-21-001:
The historical `exp-001` and `exp-002` parser policy did not remove inline angle-tag markup before token normalization. Those results are preserved as historical outputs but should be treated as parser-limited.
