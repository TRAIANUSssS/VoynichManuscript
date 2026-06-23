# Scripts

This directory will contain reproducible command-line scripts for experiments.

Scripts should accept explicit input and output paths, avoid hidden state, and write run metadata when reasonable.

Current scripts:

- `exp001_baseline_stats.py` - baseline token, glyph/character, word-length, entropy, CSV, JSON, and chart generation for `exp-001`.
- `exp002_word_position_patterns.py` - token frequency, position-class, overrepresentation, and distribution-distance outputs for `exp-002`.
- `exp002b_clean_ivtff_parser_rerun.py` - cleaned IVTFF angle-tag parser audit and old-vs-cleaned reruns for `exp-001` and `exp-002`.
- `exp003_section_frequency_comparison.py` - cleaned-parser section frequency comparison using IVTFF-derived folio section metadata.
- `exp004_section_frequency_resampling_control.py` - common-size and pairwise matched-size resampling controls for `exp-003` section-frequency comparisons.
- `exp005_section_label_null_control.py` - pooled-label null controls for full-section, matched-size, and global section-label comparisons.
- `exp006_currier_section_interaction_control.py` - Currier-language and section interaction control using IVTFF page-header `$L` metadata.
- `exp007_section_label_null_control_within_currier.py` - section-label null controls run separately within Currier categories.
