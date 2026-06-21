# Scripts

This directory will contain reproducible command-line scripts for experiments.

Scripts should accept explicit input and output paths, avoid hidden state, and write run metadata when reasonable.

Current scripts:

- `exp001_baseline_stats.py` - baseline token, glyph/character, word-length, entropy, CSV, JSON, and chart generation for `exp-001`.
- `exp002_word_position_patterns.py` - token frequency, position-class, overrepresentation, and distribution-distance outputs for `exp-002`.
- `exp002b_clean_ivtff_parser_rerun.py` - cleaned IVTFF angle-tag parser audit and old-vs-cleaned reruns for `exp-001` and `exp-002`.
