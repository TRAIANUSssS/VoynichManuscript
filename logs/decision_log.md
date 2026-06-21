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
