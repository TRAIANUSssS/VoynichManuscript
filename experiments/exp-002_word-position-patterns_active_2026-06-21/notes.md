# Notes

## Implementation Notes

- The script duplicates the small IVTFF parsing and normalization rules from `exp-001` rather than refactoring shared utilities during this experiment.
- Refactoring shared parser utilities should be done as a separate cleanup task so `exp-001` behavior remains easy to audit.
- `single_token_line` was kept as a separate position class because such lines do not have distinct initial, medial, and final positions.
- `min_count = 10` was used for overrepresentation ranking to reduce very-low-count artifacts in ranked tables. It is not a project-wide standard.

## Follow-Up Notes

TODO-2026-06-21-001:
Audit IVTFF notation beyond `{...}` comments, especially angle-tag forms such as `<!plant>` and `<$>`.

TODO-2026-06-21-002:
Consider adding token-level output with line locator, folio locator, raw token, normalized token, and position class.

TODO-2026-06-21-003:
Consider rerunning after an EVA-aware parser distinguishes transcription glyphs from IVTFF structural markup.
