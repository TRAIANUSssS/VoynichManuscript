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
