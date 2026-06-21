# Scripts

This directory will contain reproducible command-line scripts for experiments.

Scripts should accept explicit input and output paths, avoid hidden state, and write run metadata when reasonable.

Current scripts:

- `exp001_baseline_stats.py` - baseline token, glyph/character, word-length, entropy, CSV, JSON, and chart generation for `exp-001`.
- `exp002_word_position_patterns.py` - token frequency, position-class, overrepresentation, and distribution-distance outputs for `exp-002`.
