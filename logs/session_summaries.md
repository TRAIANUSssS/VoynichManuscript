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
