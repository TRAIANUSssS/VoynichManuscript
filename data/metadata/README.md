# Metadata

This directory stores machine-readable metadata used by experiments.

## Current Files

- `folio_sections.csv` - folio-to-section mapping derived from IVTFF page header parsable information in `data/raw/LSI_ivtff_0d.txt`.
- `folio_currier.csv` - folio-to-Currier-language mapping derived from IVTFF page header `$L` metadata in `data/raw/LSI_ivtff_0d.txt`.

Source documentation:

- https://www.voynich.nu/transcr.html

Notes:

- Section labels come from IVTFF `$I` illustration type codes.
- Currier labels come from IVTFF `$L` page-header codes.
- Blank, `?`, and `-` Currier labels are treated as unmapped for `exp-006` Currier-controlled comparisons.
- This metadata should be treated as source-derived experiment metadata, not as an independently verified section taxonomy.
