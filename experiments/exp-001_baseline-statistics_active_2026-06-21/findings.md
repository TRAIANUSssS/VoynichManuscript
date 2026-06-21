# Findings

OBS-2026-06-21-001:
The script selected 5,216 `H` transcription lines from 17,344 IVTFF data lines and produced 37,118 normalized tokens.

OBS-2026-06-21-002:
The run produced 9,051 unique normalized tokens and a type-token ratio of 0.24384395710975806.

OBS-2026-06-21-003:
The most frequent normalized token in this run is `daiin`, with 751 occurrences in `artifacts/exp001/top_tokens.csv`.

OBS-2026-06-21-004:
The most frequent counted EVA character in this run is `o`, with 25,592 occurrences in `artifacts/exp001/top_glyphs.csv`.

INF-2026-06-21-001:
The workflow is sufficient for a first reproducibility test because it connects a documented raw source, a command-line script, generated artifacts, and experiment documentation.

INF-2026-06-21-002:
The frequency outputs are suitable as internal baselines for later comparison, but they are not yet evidence for linguistic structure because no control corpus, folio split, section split, Currier-language split, or alternate transcription has been tested.

HYP-2026-06-21-001:
Later experiments may test whether these frequency and length patterns remain similar under alternate transcription policies or when split by folio, section, or Currier language.

TODO-2026-06-21-001:
Create a follow-up experiment that compares this baseline against at least one control corpus and one alternate preprocessing policy.

TODO-2026-06-21-002:
Decide whether EVA digraphs such as `ch` and `sh` should be modeled as glyph units rather than character sequences in a future protocol version.
