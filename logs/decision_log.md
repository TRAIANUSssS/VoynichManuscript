# Decision Log

## 2026-06-21 - Initial documentation structure

Decision:
Create a documentation-first research structure for Voynich Lab.

Reason:
The project will involve multiple chats, Codex tasks, experiments, and possible contradictions. Documentation must serve as project memory.

Consequences:
All experiments must be documented. Major decisions must be logged. Results and findings must be separated.

Open questions:
Which Voynich transcription should be used first?

## 2026-06-21 - Scoped transcription choice for exp-001

Decision:
Use `data/raw/LSI_ivtff_0d.txt` and analyze only IVTFF transcriber code `H` for the first baseline statistics workflow test.

Reason:
The raw file is publicly accessible, machine-readable, and identifies `H` as Takeshi Takahashi's full transcription in its comments. Using one transcriber code avoids mixing multiple transcriptions in the first workflow test.

Consequences:
`exp-001` results are reproducible against a specific local file hash and parser policy. This does not establish a project-wide default transcription and does not validate the transcription as superior to alternatives.

Open questions:
License/status still needs verification. Future experiments should test alternate transcriptions, alternate IVTFF versions, and alternate token/glyph parsing policies.

## 2026-06-21 - Position classes for exp-002

Decision:
For `exp-002`, classify tokens as `line_initial`, `line_medial`, `line_final`, or `single_token_line`, keeping single-token lines separate from initial and final counts.

Reason:
Single-token lines do not have distinct beginning and ending tokens. Keeping them separate avoids double-counting and makes the position-class counts reproducible.

Consequences:
Initial and final token totals are equal to the number of multi-token lines. Single-token lines require separate interpretation and should not be merged into initial/final categories without a new protocol version.

Open questions:
Future parser work should decide whether line-position analysis should be repeated after IVTFF angle-tag markup is removed or modeled.

## 2026-06-21 - Clean inline IVTFF angle tags before token normalization

Decision:
For cleaned reruns and recommended future parser policy, replace inline `<...>` markup inside selected IVTFF line text with token boundaries before tokenization and normalization.

Reason:
The old parser allowed markup text such as `plant` to become part of normalized manuscript tokens. Replacing tags with boundaries prevents markup from becoming tokens and avoids joining neighboring token text across removed tags.

Consequences:
Cleaned reruns are not directly interchangeable with old `exp-001` and `exp-002` outputs. Future experiments should state which parser policy they use.

Open questions:
Future parser versions may need to classify IVTFF angle-tag roles instead of treating all inline `<...>` forms uniformly.

## 2026-06-21 - Use IVTFF page headers as exp-003 section metadata

Decision:
Use IVTFF page header parsable information, specifically `$I` illustration type, to derive `data/metadata/folio_sections.csv` for `exp-003`.

Reason:
The repository did not contain a prior folio-to-section metadata file. The selected transcription source includes page header metadata and documents `$I` code meanings in its comments, with source documentation at https://www.voynich.nu/transcr.html.

Consequences:
`exp-003` section labels are source-derived IVTFF illustration-type categories. They are suitable for a first reproducible section comparison but should not be treated as an independently verified project taxonomy.

Open questions:
Future work should decide whether IVTFF `$I` categories become the project default or remain experiment-level metadata.

## 2026-06-21 - Report unmapped section lines explicitly

Decision:
For `exp-003`, selected transcription lines without a matching metadata folio are written to `artifacts/exp003/unmapped_lines.csv` rather than silently dropped.

Reason:
Section statistics must be auditable and reproducible.

Consequences:
The run can distinguish corpus coverage from section-level results. In the first `exp-003` run, no selected lines were unmapped.

Open questions:
Future metadata joins should use the same explicit unmapped-line reporting unless a later protocol replaces it.

## 2026-06-21 - Treat exp-003 section distances as exploratory until resampling

Decision:
Treat `exp-003` section-frequency differences as exploratory until a matched-token-count resampling or bootstrap control is run.

Reason:
`exp-003` section token counts are uneven, and section-level differences may be affected by sample size, Currier language, hand, layout, line position, or metadata effects.

Consequences:
Project summaries may report the observed section-distance values, but they should not interpret section differences as evidence of meaning, language identity, cipher structure, authorship, translation, or decipherment.

Open questions:
Whether section-level differences remain stable under matched-token-count resampling.

## 2026-06-21 - Recommend exp-004 section-frequency resampling control

Decision:
Use `exp-004_section-frequency-resampling-control` as the recommended next experiment before interpreting section-level differences.

Reason:
The next methodological need is to test whether the `exp-003` section-frequency distances persist when section sample sizes are controlled.

Consequences:
Do not create `exp-004` until a task packet or explicit instruction requests it. The recommendation is recorded for future planning only.

Open questions:
Which resampling design, number of bootstrap iterations, and comparison metrics should be used.

## 2026-06-21 - Prefer pairwise matched-size control for pair-specific section comparison

Decision:
After `exp-004`, keep common-size resampling as a global stress test but prefer pairwise matched-size JSD when comparing individual section pairs.

Reason:
The `exp-004` run showed that forcing every pair to the `850`-token `astronomical` floor can inflate distances for larger section pairs. Pairwise matched-size resampling stayed closer to the observed `exp-003` values for large-large comparisons such as `herbal` vs `stars` and `cosmological` vs `pharmaceutical`.

Consequences:
Future section-comparison writeups should report which control they use and should not treat global common-size and pairwise matched-size results as interchangeable. Pairwise matched-size results are better suited to pair-specific interpretation, while common-size results remain useful as a conservative all-sections-at-once control.

Open questions:
Whether a pooled-label null control should become a required companion to pairwise matched-size JSD.

## 2026-06-21 - Treat exp-004 resampling robustness as non-explanatory

Decision:
Treat the `exp-004` result as evidence that section-frequency differences are robust to token-count matching, but not as evidence that the cause of the section signal has been identified.

Reason:
`exp-004` showed that section differences remained measurable after matched-token-count resampling, but it did not control for random section-label assignment, Currier language, hand, layout, or other metadata confounders.

Consequences:
Project-level summaries may state that uneven section token counts do not fully explain the `exp-003` signal, but they must not present the section signal as explained, causal, or semantically meaningful.

Open questions:
How much of the remaining signal survives after null-control, Currier-language, hand, and line-position controls.

## 2026-06-21 - Recommend exp-005 section-label null control

Decision:
Use `exp-005_section-label-null-control` as the recommended next experiment after `exp-004`.

Reason:
`exp-004` answered whether section differences remain visible after matched token-count resampling, but it did not answer whether the observed or pairwise matched distances are larger than expected under random section-label assignment.

Consequences:
Future work should add a label-randomized null model before stronger inferential claims about section structure. `exp-005` should focus on observed-versus-null and pairwise-matched-versus-null section JSD comparisons rather than on new interpretive claims.

Open questions:
Whether the null-control design should use pooled pairwise permutations only, a global label shuffle, or both.

## 2026-06-21 - Require null-control comparison before stronger section-structure claims

Decision:
Treat pooled-label null-control comparison as a required step before making stronger claims about section-frequency structure.

Reason:
`exp-005` showed that observed section distances and `exp-004` pairwise matched references are larger than expected under this random section-label null model, but the result is still a control against one baseline rather than a direct explanation.

Consequences:
Future section-frequency interpretation should prefer observed-versus-null and matched-versus-null comparisons over raw observed JSD alone. Stronger claims still require additional controls for Currier language, hand, layout, and related metadata factors.

Open questions:
Which constrained null models should be added next.

## 2026-06-21 - Treat empirical p-values from exp-005 as exploratory

Decision:
Treat empirical p-values from `exp-005` as exploratory null-model summaries, not definitive proof.

Reason:
The run used 1000 iterations, so the smallest attainable empirical p-value is `0.000999000999000999`. This is useful evidence against the tested null, but it does not by itself establish cause, meaning, or final statistical certainty.

Consequences:
Project documentation may report the empirical p-values and percentile results, but it must continue to emphasize the null-model scope and the remaining need for metadata-stratified controls.

Open questions:
Whether later null-control runs should increase iteration counts or add alternative baselines.

## 2026-06-21 - Treat exp-005 as evidence of non-random section-label structure

Decision:
Treat `exp-005` as evidence that IVTFF `$I` section labels preserve non-random token-frequency structure under the tested pooled-label null model.

Reason:
All 28 observed pairwise section JSD values were above the 97.5% null quantile, all 28 `exp-004` pairwise matched references were above the 97.5% matched null quantile, and the global observed mean pairwise JSD exceeded the global null distribution.

Consequences:
Project summaries may describe the section signal as non-random under this tested null model, but they must still avoid claims about meaning, translation, language identity, authorship, or decipherment.

Open questions:
Which metadata factors account for the preserved section-label signal.

## 2026-06-21 - Prioritize Currier and hand interaction controls after exp-005

Decision:
Treat the source of the section signal as unresolved and prioritize Currier-language and scribal-hand controls before stronger claims about section structure.

Reason:
`exp-005` strengthens the case that the section signal is not a token-count artifact or a trivial random-label effect, but it does not distinguish section labels from possible confounders such as Currier language, hand, layout, or folio structure.

Consequences:
The recommended next experiment is `exp-006_currier-section-interaction-control` when Currier metadata is available or easiest to reproduce, with `exp-006_hand-section-interaction-control` as an alternative or follow-up.

Open questions:
Whether Currier language or hand explains most of the currently observed section signal.

## 2026-06-23 - Use IVTFF page-header Currier labels for exp-006

Decision:
Use Currier language labels from IVTFF page-header `$L` metadata for `exp-006`, stored explicitly in `data/metadata/folio_currier.csv`.

Reason:
The same raw transcription source used for prior experiments documents `$L` as Currier language metadata. Creating an explicit Currier metadata file makes the source and mapping auditable without inferring labels from section names.

Consequences:
Currier-controlled comparisons in `exp-006` use source-derived page-header metadata from `data/raw/LSI_ivtff_0d.txt` and cite https://www.voynich.nu/transcr.html. The labels remain experiment metadata, not independent proof of language identity.

Open questions:
Whether a separately curated Currier metadata source should be added later for verification.

## 2026-06-23 - Treat blank Currier labels as unmapped in exp-006

Decision:
For `exp-006`, treat blank, `?`, and `-` Currier labels as unmapped for Currier-controlled comparisons and write affected lines to `artifacts/exp006/unmapped_currier_lines.csv`.

Reason:
Using unknown or blank labels as if they were Currier A/B categories would silently introduce unsupported metadata. Explicit unmapped-line reporting preserves reproducibility.

Consequences:
The Currier-controlled analysis covers 4,464 of 5,216 selected `H` lines. The 752 selected lines with blank Currier labels are excluded from Currier-controlled comparisons but remain documented.

Open questions:
Whether the blank Currier labels can be resolved from a cited source before a future rerun.

## 2026-06-23 - Treat exp-006 as confounded rather than explanatory

Decision:
Treat the `exp-006` result as evidence that section and Currier metadata are strongly confounded in the current dataset slice, not as a final explanation of the section signal.

Reason:
The run found measurable section-within-Currier distances, but section-Currier coverage is sparse: several sections appear only under one valid Currier category, two sections have no valid Currier-labeled tokens, and only `herbal` and `text` support within-section Currier A/B comparisons at the configured threshold.

Consequences:
Future work should prioritize hand-section interaction controls and constrained null or resampling controls within Currier categories before stronger claims about section structure.

Open questions:
How much of the remaining section signal survives hand, quire, folio, and layout controls.

## 2026-06-23 - Prioritize within-Currier section-label null controls after exp-006

Decision:
Use `exp-007_section-label-null-control-within-currier` as the recommended next experiment after `exp-006`.

Reason:
`exp-006` showed that Currier language is a strong confounder for section-frequency analysis, while section-within-Currier distances remain measurable where enough data exists. The next methodological need is to test whether section-label effects remain stronger than random section-label assignment separately inside Currier A and Currier B.

Consequences:
Do not treat the section-level signal as independent of Currier, and do not treat Currier as a complete explanation based on `exp-006` alone. Prioritize within-Currier null controls before hand, quire, layout, or broader source-of-signal controls unless metadata coverage forces an audit first.

Open questions:
Whether `exp-007_currier-metadata-coverage-audit` should precede the null-control experiment to resolve or better document the 752 blank Currier lines.

## 2026-06-23 - Treat exp-007 as within-Currier null evidence only

Decision:
Treat `exp-007` as evidence that valid IVTFF `$I` section groups remain above the tested section-label null model inside both Currier A and Currier B, but not as evidence of meaning, language identity, or independence from all metadata confounders.

Reason:
Both Currier A and Currier B observed mean section-pair JSD values were above their 97.5% within-Currier null quantiles. However, Currier A has only three valid section groups, 752 selected lines still have blank Currier labels, and no hand, quire, folio, layout, line-position, or alternate-transcription controls were applied.

Consequences:
Future summaries may state that Currier A/B composition alone does not fully explain the tested section signal among valid groups, but they must continue to describe the source of the remaining signal as unresolved.

Open questions:
How much of the remaining signal is explained by hand, quire, folio, layout, line position, transcription policy, or unresolved Currier metadata coverage.

## 2026-06-23 - Prioritize Currier metadata coverage audit after exp-007

Decision:
Use `exp-008_currier-metadata-coverage-audit` as the recommended next task before broader source-of-signal interpretation.

Reason:
`exp-007` still excludes 752 selected lines with blank Currier labels, and `astronomical` and `zodiac` have no valid Currier-labeled tokens under the current mapping. Auditing this coverage gap should clarify whether the missing labels are irreducible source metadata limits or can be documented more precisely from cited sources.

Consequences:
Hand-section and layout/quire controls remain important follow-ups, but Currier coverage should be audited before treating the current within-Currier scope as final.

Open questions:
Whether a cited external or source-derived metadata reference can resolve any blank Currier labels without guessing.

## 2026-06-23 - Prioritize hand-section interaction after exp-007

Decision:
Use `exp-008_hand-section-interaction-control` as the recommended next experiment after the `exp-007` consolidation.

Reason:
`exp-007` showed that valid section groups remain above the tested section-label null model inside both Currier A and Currier B. This weakens Currier A/B composition as a complete explanation, so the next major unresolved confounder is scribal hand.

Consequences:
Future work should test whether the remaining section-level token-frequency signal is partly explained by hand and whether section-label effects remain visible after accounting for hand. Currier metadata coverage audit, quire/layout controls, and matched-size within-Currier null controls remain supporting follow-ups.

Open questions:
Whether hand metadata coverage is sufficient for the same level of controlled section-label testing.

## 2026-06-23 - Use IVTFF page-header hand labels for exp-008

Decision:
Use Currier hand labels from IVTFF page-header `$H` metadata for `exp-008`, stored explicitly in `data/metadata/folio_hands.csv`.

Reason:
The same raw transcription source used by prior experiments documents `$H` as Currier's hand metadata. Creating an explicit hand metadata file makes the source and mapping auditable without inferring hand from section names or Currier language.

Consequences:
Hand-controlled comparisons in `exp-008` use source-derived page-header metadata from `data/raw/LSI_ivtff_0d.txt` and cite https://www.voynich.nu/transcr.html. The labels remain experiment metadata, not independent proof of scribal identity, authorship, or textual meaning.

Open questions:
Whether a separately curated or scholarly hand metadata source should be added later for verification.

## 2026-06-23 - Treat blank hand labels as unmapped in exp-008

Decision:
For `exp-008`, treat blank, `?`, and `-` hand labels as unmapped for hand-controlled comparisons and write affected selected lines to `artifacts/exp008/unmapped_hand_lines.csv`.

Reason:
Using unknown or blank labels as if they were hand categories would silently introduce unsupported metadata. Explicit unmapped-line reporting preserves reproducibility.

Consequences:
The hand-controlled analysis covers 3,134 of 5,216 selected `H` lines. The 2,082 selected lines with blank hand labels are excluded from hand-controlled comparisons but remain documented.

Open questions:
Whether blank hand labels can be resolved from a cited source before a future rerun.

## 2026-06-23 - Treat exp-008 hand control as coverage-limited

Decision:
Treat `exp-008` as evidence that section-within-hand distances are measurable where coverage exists, but not as strong evidence that the section signal is independent of hand.

Reason:
Only four section-within-hand pairs met the configured token threshold, and no hand category had at least three valid section groups for the within-hand section-label null control.

Consequences:
Future work should prioritize hand metadata coverage, threshold sensitivity, or matched-size within-hand controls before stronger claims about hand and section interaction.

Open questions:
Whether lowering thresholds, adding independently cited hand metadata, or using pair-specific matched controls changes the interpretation.
