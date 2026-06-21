# Manuscript Sections

## IVTFF `$I` Illustration-Type Categories

Status: source-derived metadata used for `exp-003`; needs independent review before becoming a project-wide section taxonomy.

Source:
- `data/raw/LSI_ivtff_0d.txt`
- https://www.voynich.nu/transcr.html

The IVTFF file comments define `$I` as illustration type with these codes:

- `T`: Text
- `H`: Herbal
- `A`: Astronomical
- `Z`: Zodiac
- `B`: Biological
- `C`: Cosmological
- `P`: Pharmaceutical
- `S`: Stars

Machine-readable mapping:
- `data/metadata/folio_sections.csv`

Note:
These labels are used as metadata categories in `exp-003`. They should not be treated as independently verified section boundaries without further source review.

## Open Questions

- How should section boundaries be represented in machine-readable metadata?
- Which section labels are conventional, and which are interpretive?
- How should uncertain folio assignments be handled?
- Should IVTFF `$I` illustration-type categories become the default project section taxonomy?
