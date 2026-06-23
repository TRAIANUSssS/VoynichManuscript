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

## 2026-06-21 - exp-005 consolidation

### Scope

Summarize:

- `exp-005_section-label-null-control`
- its relationship to `exp-003_section-frequency-comparison`
- its relationship to `exp-004_section-frequency-resampling-control`
- implications for the next source-of-signal experiments

### Observations

OBS:
- `exp-005` ran section-label null controls with 1000 iterations and seed 20260621.
- `exp-005` used transcriber code `H` and the cleaned parser policy from `exp-002b`.
- `exp-005` reused the section mapping logic from `exp-003` / `exp-004`.
- All selected `H` lines were mapped to sections; unmapped selected lines = 0.
- All 28 observed pairwise section JSD values were above the 97.5% null quantile.
- All 28 `exp-004` pairwise matched reference JSD values were above the 97.5% matched null quantile.
- Global observed mean pairwise JSD was 0.5554700431523788.
- Global null mean was 0.3788255370327812.
- Global null 97.5% quantile was 0.38500785795761844.
- Observed minus global null mean was 0.1766445061195976.

### Interpretations

INF:
- Random section-label assignment did not reproduce the observed section-level token-frequency distances.
- The section-level token-frequency signal is stronger than expected under this tested null model.
- Combined with `exp-003` and `exp-004`, this makes the section signal more robust as an observed statistical property of the cleaned transcription data.
- The result still does not explain the source of the signal.

### Hypotheses / Open Possibilities

HYP:
- IVTFF `$I` section labels preserve non-random token-frequency information.
- Some section-level variation may reflect Currier language, scribal hand, folio or quire structure, layout, metadata, transcription effects, or a combination of factors.
- The section signal may be partly indirect rather than caused by section or topic categories alone.

### Limitations

TODO / ERR:
- Do not treat null-control results as evidence of meaning, translation, language identity, authorship, or decipherment.
- Do not mark any hypothesis as confirmed or rejected.
- Empirical p-values are limited by the 1000-iteration setup.
- The source of the section-level signal remains unresolved.
- Currier-language and hand controls are needed before stronger interpretation.

### Current Research State

The section-level token-frequency signal is:

- reproducible under the cleaned parser
- robust to token-count matching
- stronger than expected under random section-label assignment

However, the source of the signal is not yet known.

### Next Recommended Experiment

Recommended next experiment:
`exp-006_currier-section-interaction-control`

Purpose:
Test whether the IVTFF `$I` section-level token-frequency signal remains after controlling for Currier language categories, or whether the section signal is largely explained by Currier A/B distribution.

Alternative / follow-up:
`exp-006_hand-section-interaction-control`

## 2026-06-23 - exp-006 Currier-section interaction control

Context:
The project needed a source-of-signal control after `exp-005` showed that IVTFF `$I` section labels preserve non-random token-frequency structure under a pooled-label null model.

What was done:
Added `scripts/exp006_currier_section_interaction_control.py`, created explicit Currier metadata at `data/metadata/folio_currier.csv`, ran the script with the cleaned parser policy on `data/raw/LSI_ivtff_0d.txt` using transcriber code `H`, and generated artifacts under `artifacts/exp006/`. Created the `exp-006` experiment documentation folder with protocol, results, findings, artifacts, and questions.

Results:
The run selected 5,216 `H` lines. All selected lines mapped to sections, while 4,464 mapped to valid Currier labels and 752 had blank Currier labels. The recomputed section-only mean pairwise JSD matched `exp-003` at `0.5554700431523788`. Currier A vs B JSD was `0.4743758913991697`. Section-within-Currier mean JSD was `0.48050447382407735` across 13 valid pairs. Currier-within-section mean JSD was `0.6082754348261923` across 2 valid section comparisons.

Open questions:
Currier and section are strongly confounded in this dataset slice. The result does not identify the source of the section signal and does not support claims about meaning, translation, language identity, authorship, or decipherment.

Next actions:
Run a hand-section interaction control, then add constrained null controls or matched-size resampling within Currier categories if stronger source-of-signal testing is needed.

## 2026-06-21 - exp-006 consolidation

### Scope

Summarize:

- `exp-006_currier-section-interaction-control`
- its relationship to `exp-003`, `exp-004`, and `exp-005` section-frequency results
- implications for future source-of-signal experiments

### Observations

OBS:
- `exp-006` used transcriber code `H` and the cleaned parser policy from `exp-002b`.
- `exp-006` reused section mapping logic from `exp-003`, `exp-004`, and `exp-005`.
- All 5,216 selected `H` lines were mapped to sections.
- 4,464 selected `H` lines had valid Currier labels.
- 752 selected `H` lines had blank or unmapped Currier labels.
- Currier A contained 11,450 tokens, 3,410 unique tokens, TTR 0.2978, entropy 9.8648 bits, and mean token length 4.8651.
- Currier B contained 23,224 tokens, 4,926 unique tokens, TTR 0.2121, entropy 9.8855 bits, and mean token length 5.1447.
- Currier A vs Currier B JSD was 0.4743758913991697.
- Section-by-Currier coverage was highly uneven.
- `biological` and `stars` were entirely Currier B under the current mapping.
- `pharmaceutical` was entirely Currier A under the current mapping.
- `herbal` and `text` contained both Currier A and Currier B tokens.
- `astronomical` and `zodiac` had no valid Currier-labeled tokens under the current mapping.
- Full section-only mean JSD from `exp-003` was 0.5554700431523788.
- Section-within-Currier mean JSD was 0.48050447382407735.
- Section-within-Currier mean JSD for Currier A was 0.5355956685429015.
- Section-within-Currier mean JSD for Currier B was 0.46497751540843016.
- Valid Currier-within-section comparisons were available only for `herbal` and `text`.
- The generated summary label was `section_currier_strongly_confounded`.

### Interpretations

INF:
- Currier language is a strong confounder for section-frequency analysis.
- Section-level differences weaken after Currier control, but do not disappear where enough data exists.
- Currier likely explains part of the section-level token-frequency signal.
- Current data do not show that Currier fully explains the section-level signal.
- Current data also do not show that the section-level signal is independent of Currier.
- Section and Currier are strongly confounded in the current metadata coverage.

### Hypotheses / Open Possibilities

HYP:
- The section-level signal may reflect a combination of section category, Currier language, hand, layout, folio or quire structure, and transcription effects.
- Some section differences may remain inside Currier categories.
- Some apparent section differences may be indirect reflections of Currier composition.
- Blank Currier labels may affect coverage and should be audited before stronger claims.

### Limitations

TODO / ERR:
- Do not treat Currier control as proof of language identity.
- Do not treat Currier as a complete explanation of the section signal.
- Do not treat the section signal as independent of Currier without additional controls.
- Currier metadata coverage is incomplete.
- Section-by-Currier groups are sparse and uneven.
- `astronomical` and `zodiac` cannot be evaluated under the current Currier mapping.
- Currier-within-section analysis is available only for two sections.
- Additional within-Currier null controls are needed.

### Current Research State

The section-level token-frequency signal is:

- reproducible under the cleaned parser
- robust to token-count matching
- stronger than expected under random section-label assignment
- partly confounded with Currier language
- not fully explained by Currier based on current available comparisons

However, the source of the signal remains unresolved.

### Next Recommended Experiment

Recommended next experiment:
`exp-007_section-label-null-control-within-currier`

Purpose:
Test whether section-label effects remain stronger than random section-label assignment inside Currier A and inside Currier B separately.

Alternative / supporting task:
`exp-007_currier-metadata-coverage-audit`

Purpose:
Audit the 752 blank Currier lines and check whether Currier coverage can be improved or documented more precisely before further interaction controls.

## 2026-06-23 - exp-007 within-Currier section-label null control

Context:
`exp-006` found that section and Currier metadata are strongly confounded. `exp-007` tested whether section labels remain stronger than random section-label reassignment inside Currier A and inside Currier B separately.

What was done:
Added `scripts/exp007_section_label_null_control_within_currier.py`, ran it on `data/raw/LSI_ivtff_0d.txt` with transcriber code `H`, reused `data/metadata/folio_sections.csv` and `data/metadata/folio_currier.csv`, and generated artifacts under `artifacts/exp007/`. Created the active `exp-007` experiment folder with protocol, results, findings, artifact index, and questions.

Results:
The run selected 5,216 `H` lines. All selected lines mapped to sections, 4,464 mapped to valid Currier labels, and 752 had blank Currier labels. Currier A had 3 valid section groups and observed mean section-pair JSD `0.5355956685429015`, above its null 97.5% quantile `0.39941216554950554`. Currier B had 5 valid section groups and observed mean section-pair JSD `0.46397711540843006`, above its null 97.5% quantile `0.35311149369219175`. All 13 valid pairwise within-Currier section comparisons were above their pairwise 97.5% null quantiles.

Open questions:
The result weakens the idea that Currier A/B composition fully explains the tested section signal among valid groups, but it does not identify the source of the remaining signal. Coverage remains limited by 752 blank Currier labels and by the absence of valid Currier-labeled `astronomical` and `zodiac` tokens.

Next actions:
Audit Currier metadata coverage before treating the current within-Currier scope as final, then test hand, quire, layout, line position, and matched-size within-Currier controls.

## 2026-06-21 - exp-007 consolidation

### Scope

Summarize:

- `exp-007_section-label-null-control-within-currier`
- its relationship to `exp-006_currier-section-interaction-control`
- its relationship to `exp-003` through `exp-005` section-frequency results
- implications for future source-of-signal experiments

### Observations

OBS:
- `exp-007` used transcriber code `H` and the cleaned parser policy from `exp-002b`.
- `exp-007` used section metadata from `data/metadata/folio_sections.csv` and Currier metadata from `data/metadata/folio_currier.csv`.
- `exp-007` ran with 1000 iterations, seed `20260621`, and minimum section group size `100` tokens.
- All 5,216 selected `H` lines were mapped to sections.
- 4,464 selected `H` lines had valid Currier labels.
- 752 selected `H` lines had blank or unmapped Currier labels.
- Currier A had 3 valid section groups: `herbal`, `pharmaceutical`, and `text`.
- Currier A observed mean JSD was 0.5355956685429015.
- Currier A null mean was 0.38805169568795816.
- Currier A null 97.5% quantile was 0.39941216554950554.
- Currier B had 5 valid section groups: `biological`, `cosmological`, `herbal`, `stars`, and `text`.
- Currier B observed mean JSD was 0.46397711540843006.
- Currier B null mean was 0.3449325698805918.
- Currier B null 97.5% quantile was 0.35311149369219175.
- All 13 valid pairwise comparisons inside Currier groups were above the 97.5% null quantile.
- The final summary label was `section_signal_above_null_in_both_currier_groups`.

### Interpretations

INF:
- Section labels preserve non-random token-frequency structure inside both Currier A and Currier B under this null model.
- Currier A/B composition alone is unlikely to fully explain the section-level signal.
- `exp-007` strengthens the claim that some section-level signal remains after fixing Currier category.
- The source of the remaining signal is still unresolved.
- Currier A results are useful but coverage-limited because only 3 valid section groups passed the token threshold.

### Hypotheses / Open Possibilities

HYP:
- Remaining section-level signal may reflect scribal hand, folio or quire structure, layout effects, line-position effects, transcription choices, metadata effects, or a combination of factors.
- Some section-level differences may remain independently of Currier A/B, but this does not imply meaning or language identity.
- Blank Currier labels may still affect coverage and should be remembered as a metadata limitation.

### Limitations

TODO / ERR:
- Do not treat within-Currier null-control success as evidence of meaning, translation, language identity, authorship, or decipherment.
- Do not mark any hypothesis as confirmed or rejected.
- Currier A has only three valid section groups.
- 752 selected `H` lines remain blank or unmapped for Currier.
- `astronomical` and `zodiac` cannot be evaluated under the current Currier mapping.
- Matched-size within-Currier null controls were not implemented.
- Hand, quire, layout, and folio-neighborhood controls are still needed.

### Current Research State

The section-level token-frequency signal is:

- reproducible under the cleaned parser
- robust to token-count matching
- stronger than expected under global random section-label assignment
- partly confounded with Currier language
- still above null inside both Currier A and Currier B under `exp-007`

However, the source of the signal remains unresolved.

### Next Recommended Experiment

Recommended next experiment:
`exp-008_hand-section-interaction-control`

Purpose:
Test whether the remaining section-level token-frequency signal is partly explained by scribal hand, and whether section-label effects remain visible after accounting for hand.

Alternative / supporting future controls:

- quire-section interaction control
- layout or folio-neighborhood control
- matched-size within-Currier null control
- Currier metadata coverage audit

## 2026-06-23 - exp-008 hand-section interaction control

Context:
`exp-008` followed the section-frequency, Currier-control, and within-Currier null-control sequence. The goal was to test whether section-level token-frequency differences remain visible after accounting for IVTFF `$H` hand categories.

What was done:
- Added `scripts/exp008_hand_section_interaction_control.py`.
- Created `data/metadata/folio_hands.csv` from IVTFF page-header `$H` metadata.
- Generated `artifacts/exp008/` coverage, hand-only, section-only, section-within-hand, hand-within-section, within-hand null-control, and signal-attribution artifacts.
- Created `experiments/exp-008_hand-section-interaction-control_active_2026-06-21/` with README, protocol, results, findings, artifact index, and questions.
- Updated project navigation, script/artifact/metadata indexes, dataset documentation, decision log, and changelog.

Results:
- Selected `H` lines: `5216`.
- Section-mapped selected lines: `5216`.
- Hand-mapped selected lines: `3134`.
- Unmapped hand selected lines: `2082`.
- Hand categories: `1`, `2`, `3`, `4`, `5`, `X`, `Y`.
- Section-only recomputed mean JSD: `0.5554700431523788`.
- Historical `exp-003` reference mean JSD: `0.5554700431523788`.
- Hand-only mean JSD: `0.5822290801216097`.
- Section-within-hand mean JSD: `0.5681240941907049` from `4` valid pairs.
- Hand-within-section mean JSD: `0.6461215587388383` from `8` valid pairs.
- Within-hand section-label null controls: `insufficient_data` for every hand category because no hand had at least three valid section groups at the `100` token threshold.
- Generated summary label: `section_signal_preserved_within_hand`.

Interpretation:
- OBS: Section-within-hand distances remain measurable for four valid pairs.
- OBS: The section-only replication exactly matched the `exp-003` reference mean in this run.
- INF: The generated summary label is coverage-limited because it is based on four valid pairs and no feasible within-hand null distribution.
- INF: Hand remains a plausible contributor or confounder; this run does not show independence from hand.
- HYP: The remaining section signal may reflect a combination of section, hand, Currier, quire, folio, layout, line-position, and transcription effects.

Open questions:
- Can blank hand labels be resolved from a cited source?
- How sensitive are section-within-hand distances to the `100` token threshold?
- Do the four available section-within-hand pairs remain measurable under matched-size resampling?
- Should an independent hand metadata source be added before stronger hand-control interpretation?

Next actions:
- Run hand metadata coverage or threshold-sensitivity checks before stronger claims about hand and section interaction.
- Consider matched-size within-hand section resampling for the four available pairs.
- Continue with quire, layout, folio-neighborhood, and line-position controls after hand metadata limitations are clarified.

## 2026-06-21 - exp-008 consolidation

### Scope

Summarize:

- `exp-008_hand-section-interaction-control`
- its relationship to `exp-003` through `exp-007` section-frequency and Currier-control results
- implications for hand metadata coverage and future source-of-signal experiments

### Observations

OBS:
- `exp-008` used transcriber code `H` and the cleaned parser policy from `exp-002b`.
- `exp-008` reused section mapping logic from `exp-003` through `exp-007`.
- `exp-008` used hand metadata from IVTFF page-header `$H` labels.
- `exp-008` ran with 1000 iterations, seed `20260621`, and minimum token threshold `100`.
- All 5,216 selected `H` lines were mapped to sections.
- 3,134 selected `H` lines had valid hand labels.
- 2,082 selected `H` lines had blank or unmapped hand labels.
- `astronomical` and `zodiac` had no valid hand-mapped tokens under the current mapping policy.
- Valid hand categories were `1`, `2`, `3`, `4`, `5`, `X`, and `Y`.
- Hand-only mean pairwise JSD was `0.5822290801216097`.
- Full section-only mean JSD from `exp-003` was `0.5554700431523788`.
- There were 4 valid section-within-hand comparisons.
- Section-within-hand mean JSD was `0.5681240941907049`.
- There were 8 valid hand-within-section comparisons.
- Hand-within-section mean JSD was `0.6461215587388383`.
- No hand category had at least three valid section groups with at least 100 tokens each.
- Strict within-hand section-label null controls were not feasible.
- The generated experiment label was `section_signal_preserved_within_hand`.

Section-within-hand pair values:

- Hand `1`: `herbal` vs `text` = `0.6065797757758608`
- Hand `2`: `biological` vs `herbal` = `0.4347931720064342`
- Hand `3`: `cosmological` vs `text` = `0.5694432596869899`
- Hand `4`: `herbal` vs `pharmaceutical` = `0.6616801692935346`

### Interpretations

INF:
- Hand categories show measurable token-frequency differences.
- Hand is a serious candidate confounder for section-frequency analysis.
- Available section-within-hand comparisons remain measurable, but the evidence is sparse.
- The `section_signal_preserved_within_hand` label must be read narrowly because it is based on only 4 valid section-within-hand comparisons and no feasible within-hand section-label null control.
- `exp-008` does not show that hand fully explains the section-level signal.
- `exp-008` also does not show that the section-level signal is independent of hand.
- Current hand metadata coverage is too sparse for strong hand-control conclusions.

### Hypotheses / Open Possibilities

HYP:
- Some remaining section-level signal may reflect scribal hand or hand-related transcription variation.
- Some apparent hand-level signal may be entangled with section, Currier, layout, quire, or folio structure.
- Better hand metadata coverage may change the interpretation of section-within-hand results.
- The remaining section-level signal may reflect multiple overlapping metadata factors rather than a single source.

### Limitations

TODO / ERR:
- Do not treat hand-control results as evidence of authorship, language identity, meaning, or decipherment.
- Do not treat hand as a complete explanation of section-level signal.
- Do not treat section-level signal as independent of hand.
- Do not mark any hypothesis as confirmed or rejected.
- 2,082 selected `H` lines remain blank or unmapped for hand.
- `astronomical` and `zodiac` cannot be evaluated under current hand mapping.
- Within-hand section-label null controls were not feasible due to sparse section-by-hand coverage.
- Additional hand metadata audit is needed before stronger hand-based conclusions.

### Current Research State

The section-level token-frequency signal is:

- reproducible under the cleaned parser
- robust to token-count matching
- stronger than expected under global random section-label assignment
- partly confounded with Currier language
- still above null inside both Currier A and Currier B under `exp-007`
- potentially confounded with hand, but current hand metadata coverage is too sparse for strong conclusions

The source of the signal remains unresolved.

### Next Recommended Experiment

Recommended next experiment:
`exp-009_hand-metadata-coverage-audit`

Purpose:
Audit the 2,082 blank or unmapped hand-label lines, summarize their distribution by section, folio, and Currier if available, test threshold sensitivity, and determine whether hand metadata coverage can be improved or only documented as a limitation.

Alternative / later controls:

- quire-section interaction control
- layout or folio-neighborhood control
- joint Currier-hand coverage summary
- lower-threshold exploratory within-hand controls
