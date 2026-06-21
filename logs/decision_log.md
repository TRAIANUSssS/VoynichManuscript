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
