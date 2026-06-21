# Session Summaries

## 2026-06-21 - Initial documentation scaffold

Context:
The repository needed a starter documentation structure for Voynich Lab.

What was done:
Created the initial documentation tree, starter research documents, method notes, dataset notes, prompts, logs, and directory README files.

Results:
The project now has a navigable documentation-first structure. No experiment was run.

Open questions:
Which transcription should be used first? Which manuscript and research sources should be added first?

Next actions:
Verify sources, select a transcription, and prepare the protocol for `exp-001`.

## 2026-06-21 - exp-001 baseline statistics run

Context:
The project needed its first end-to-end workflow test from raw transcription source through reproducible artifacts and documentation.

What was done:
Downloaded the IVTFF EVA interlinear transcription to `data/raw/LSI_ivtff_0d.txt`, documented its provenance, wrote `scripts/exp001_baseline_stats.py`, ran it on transcriber code `H`, generated artifacts under `artifacts/exp001/`, and created the active `exp-001` experiment folder.

Results:
The run completed without runtime errors. It selected 5,216 `H` lines and produced 37,118 normalized tokens, 9,051 unique normalized tokens, and the requested CSV, JSON, and PNG artifacts.

Open questions:
The source license/status needs verification. Future work should decide how to model EVA digraphs, uncertain marks, folio metadata, sections, Currier language, and control corpora.

Next actions:
Review `exp-001` outputs, then create a follow-up experiment for either control-corpus comparison or improved EVA-aware parsing.

## 2026-06-21 - exp-002 word-position patterns run

Context:
The project needed a second experiment extending `exp-001` by adding token position inside selected transcription lines.

What was done:
Wrote `scripts/exp002_word_position_patterns.py`, ran it on `data/raw/LSI_ivtff_0d.txt` with transcriber code `H`, generated position summary, token-position counts, shares, overrepresentation tables, Jensen-Shannon distance metrics, and PNG plots under `artifacts/exp002/`.

Results:
The run completed without runtime errors. It selected 5,216 `H` lines, found 5,207 non-empty selected lines, classified 37,118 normalized tokens, and reported Jensen-Shannon divergence values for initial/medial/final distribution comparisons.

Open questions:
The `exp-001`-compatible normalization can admit IVTFF angle-tag markup into token text, which limits interpretation of some overrepresentation results. A parser-focused follow-up is needed before stronger claims.

Next actions:
Audit IVTFF markup handling, then rerun baseline and line-position analyses with a parser policy that distinguishes transcription text from structural markup.

## 2026-06-21 - exp-002b cleaned IVTFF parser rerun

Context:
`exp-002` revealed that the `exp-001`-compatible parser allowed IVTFF angle-tag markup to enter normalized token text.

What was done:
Added `scripts/exp002b_clean_ivtff_parser_rerun.py`, documented a cleaned parser policy, reran baseline and line-position analyses under `artifacts/exp002b/`, and created old-vs-cleaned comparison tables.

Results:
The cleaned parser removed 4,467 inline angle tags from 2,229 selected `H` lines. Cleaned token count was 37,967 versus 37,118 old tokens; cleaned unique token count was 8,071 versus 9,051 old unique tokens; all reported Jensen-Shannon position divergences decreased.

Open questions:
Future work should decide whether cleaned outputs supersede old parser-limited outputs for baseline comparisons and whether angle tags need role-specific handling.

Next actions:
Refactor the cleaned parser into shared utilities or run the next experiment using the cleaned parser policy explicitly.

## 2026-06-21 - exp-003 section frequency comparison

Context:
The project needed a metadata-aware comparison using the cleaned parser policy from `exp-002b`.

What was done:
Added `scripts/exp003_section_frequency_comparison.py`, derived `data/metadata/folio_sections.csv` from IVTFF page header `$I` metadata, ran section-level frequency comparisons on transcriber code `H`, and generated outputs under `artifacts/exp003/`.

Results:
The run mapped all 5,216 selected `H` lines to eight IVTFF section categories. Pairwise section Jensen-Shannon distances ranged from 0.3347291601069759 to 0.7132735389659056 bits, with mean 0.5554700431523788 bits.

Open questions:
The section labels are IVTFF illustration-type metadata, not an independently verified taxonomy. Follow-up should control for Currier language, hand, and section sample size.

Next actions:
Run a controlled section comparison using Currier language and hand metadata, or add matched-size resampling before interpreting section differences.

## 2026-06-21 - exp-002 to exp-003 consolidation

### Scope

Summarize the completed sequence:

- `exp-002_word-position-patterns`
- `exp-002b_clean-ivtff-parser-rerun`
- `exp-003_section-frequency-comparison`

### Observations

OBS:
- `exp-002` found measurable line-position token-distribution differences between `line_initial`, `line_medial`, `line_final`, and `single_token_line` classes.
- `exp-002` also exposed parser contamination from IVTFF inline angle-tag markup entering normalized token text.
- `exp-002b` removed inline angle tags from normalized token text and reran baseline and position comparisons with the cleaned parser policy.
- `exp-002b` removed 4,467 inline angle tags from 2,229 selected `H` lines, with 111 unique angle-tag forms removed.
- Parser cleanup reduced but did not remove position-distribution differences: `line_initial_vs_line_medial` changed from 0.529873240757701 to 0.5052142842100613 JSD bits; `line_final_vs_line_medial` changed from 0.5310279149774855 to 0.43994932334109943; `line_initial_vs_line_final` changed from 0.7331851577131896 to 0.674520700840175.
- `exp-003` mapped all 5,216 selected `H` lines to IVTFF `$I` section categories.
- `exp-003` found measurable section-level token-frequency differences: mean pairwise section JSD was 0.5554700431523788 bits, with minimum 0.3347291601069759 for `biological` vs `stars` and maximum 0.7132735389659056 for `astronomical` vs `biological`.

### Interpretations

INF:
- The original `exp-002` signal was partly affected by parser artifacts.
- The cleaned parser result suggests that line position remains a structural factor in the cleaned transcription data.
- IVTFF `$I` section categories differ by token-frequency profile, but the cause is not yet identified.
- Section-level variation is exploratory because sample sizes are uneven and confounders are uncontrolled.
- The mean section JSD from `exp-003` is close to the mean cleaned position-class JSD from `exp-002b`, so section-level variation is currently comparable in magnitude to line-position variation in this exploratory setup.

### Hypotheses / Open Possibilities

HYP:
- Some token distributions may be influenced by line position.
- Some token distributions may vary by IVTFF `$I` section category.
- Section effects may partly reflect Currier language, hand, layout, sample size, or metadata effects rather than section/topic alone.

### Limitations

TODO / ERR:
- Do not treat section differences as evidence of meaning, translation, language identification, authorship, or decipherment.
- Do not compare TTR naively across uneven section sizes.
- Do not interpret section-distance magnitudes until matched-token-count resampling or bootstrap controls are run.
- Continue using the cleaned IVTFF parser policy unless a later protocol explicitly replaces it.

### Next Recommended Experiment

Recommended next experiment:
`exp-004_section-frequency-resampling-control`

Purpose:
Test whether section-level token-frequency differences from `exp-003` remain visible after matched-token-count resampling or bootstrap controls.

## Template

Context:
...

What was done:
...

Results:
...

Open questions:
...

Next actions:
...

## 2026-06-21 - exp-004 consolidation

### Scope

Summarize:

- `exp-004_section-frequency-resampling-control`
- its relationship to `exp-003_section-frequency-comparison`
- implications for the next control experiment

### Observations

OBS:
- `exp-004` ran matched-token-count resampling with 1000 iterations and seed 20260621.
- `exp-004` reused the cleaned `exp-002b` parser policy and the `exp-003` folio-to-section mapping from `data/metadata/folio_sections.csv`.
- Observed `exp-003` mean pairwise section JSD was 0.5554700431523788 bits.
- `exp-004` common-size mean pairwise JSD was 0.6479551071976217 bits.
- `exp-004` pairwise matched mean pairwise JSD was 0.5870200377032155 bits.
- Section-level differences remained measurable after token-count matching.
- The closest pair remained `biological` vs `stars`.
- The most distant pair remained `astronomical` vs `biological`.
- The common-size control reduced all sections to the smallest available section size, which was `astronomical` at 850 tokens.
- The pooled-label null control was not implemented in `exp-004`.

### Interpretations

INF:
- Uneven section token counts do not fully explain the section-frequency differences observed in `exp-003`.
- The common-size control is harsher because it forces all comparisons to the 850-token floor, which can inflate distances under sparse small-sample comparisons.
- Pairwise matched-size control is more useful for future pairwise section comparisons because it uses the maximum fair sample size for each pair.
- The section-level signal is more robust after `exp-004`, but its cause remains unresolved.

### Hypotheses / Open Possibilities

HYP:
- Some section-level frequency differences may reflect real structural differences in the transcription data.
- Remaining differences may still be influenced by Currier language, scribal hand, folio or quire structure, layout, metadata, or transcription effects.
- Section categories may preserve a signal, but `exp-004` does not identify what produces that signal.

### Limitations

TODO / ERR:
- Do not treat resampling robustness as evidence of meaning, translation, language identity, authorship, or decipherment.
- Do not treat section differences as explained.
- Pooled-label null control was not implemented in `exp-004`.
- A null model is needed before stronger inferential claims about section structure.

### Next Recommended Experiment

Recommended next experiment:
`exp-005_section-label-null-control`

Purpose:
Test whether observed and pairwise matched section JSD values are larger than expected under random section-label assignment.

## 2026-06-21 - exp-005 section-label null control

Context:
`exp-004` showed that section-frequency differences remain measurable after token-count matching, but it did not test whether those distances were larger than expected under random section-label assignment.

What was done:
Added `scripts/exp005_section_label_null_control.py`, reused the cleaned `exp-002b` parser policy and the `exp-003` / `exp-004` folio-to-section mapping, ran 1000-iteration pooled-label null controls on transcriber code `H`, and generated pairwise full-size, pairwise matched-size, and global section-label permutation outputs under `artifacts/exp005/`.

Results:
The run completed without runtime errors. All 5,216 selected `H` lines mapped to section metadata. For all 28 section pairs, observed full-section JSD was above the 97.5% pooled-label null quantile. For all 28 pairs, the `exp-004` pairwise matched reference JSD was also above the 97.5% matched null quantile. The observed `exp-003` mean pairwise JSD was 0.5554700431523788, compared with a global null mean of 0.3788255370327812 and null 97.5% quantile 0.38500785795761844.

Open questions:
How much of the section-label signal survives after controlling for Currier language, hand, line position, or other metadata? Which constrained null models should be tried next?

Next actions:
Design a follow-up that stratifies or constrains the null model by Currier language, hand, or related metadata before stronger interpretation of the section signal.
