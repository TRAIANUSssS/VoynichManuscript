# Findings

OBS-2026-06-21-001:
The run selected 5,216 `H` lines, of which 5,207 contained at least one normalized token.

OBS-2026-06-21-002:
The total normalized token count was 37,118, matching the `exp-001` baseline token count.

OBS-2026-06-21-003:
The run classified 4,395 line-initial tokens, 27,516 line-medial tokens, 4,395 line-final tokens, and 812 single-token-line tokens.

OBS-2026-06-21-004:
`daiin` was the most frequent token in line-initial, line-medial, and line-final position-class top-token tables.

OBS-2026-06-21-005:
The Jensen-Shannon divergence values were 0.529873240757701 bits for `line_initial` vs `line_medial`, 0.5310279149774855 bits for `line_final` vs `line_medial`, and 0.7331851577131896 bits for `line_initial` vs `line_final`.

OBS-2026-06-21-006:
Several highly overrepresented line-final tokens include strings affected by IVTFF angle-tag markup under the current normalization, such as `daiinplant`.

INF-2026-06-21-001:
The position-class distributions are measurably different under Jensen-Shannon divergence, but this does not identify the cause of the differences.

INF-2026-06-21-002:
Because markup-derived token text appears in the output, some line-final overrepresentation results may reflect parser behavior rather than manuscript text.

HYP-2026-06-21-001:
Some token forms may have position-sensitive behavior within transcription lines, but this requires a parser check that handles IVTFF markup more carefully and comparison against control corpora.

TODO-2026-06-21-001:
Create a parser-focused follow-up that removes or models IVTFF angle-tag markup before rerunning `exp-001` and `exp-002`.

TODO-2026-06-21-002:
Compare line-position distributions across folios, sections, Currier languages, and at least one control corpus before interpreting the pattern.

ERR-2026-06-21-001:
The current `exp-001`-compatible normalization can admit IVTFF markup words into normalized tokens. This does not invalidate the reproducibility of `exp-002`, but it limits interpretability.
