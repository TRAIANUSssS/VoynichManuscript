# Results

Run date: 2026-06-21

## Command

```bash
python scripts/exp004_section_frequency_resampling_control.py --input data/raw/LSI_ivtff_0d.txt --metadata data/metadata/folio_sections.csv --output artifacts/exp004/ --transcriber-code H --iterations 1000 --seed 20260621
```

## Script

- Script path: `scripts/exp004_section_frequency_resampling_control.py`

## Input Data

- Input file: `data/raw/LSI_ivtff_0d.txt`
- Input SHA-256: `3f3f2af18cde10efe75c582f49b07b651c3397022fcbfa5854fecc424c121afa`
- Source: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html

## Metadata

- Metadata path: `data/metadata/folio_sections.csv`
- Metadata created during this run: `false`
- Metadata source: reused `exp-003` folio-to-section mapping derived from IVTFF page-header `$I` illustration-type metadata

## Parameters

- Transcriber code: `H`
- Iterations: `1000`
- Random seed: `20260621`
- Common sample size mode: `auto`
- Pairwise sample size mode: `auto`
- Minimum count argument: `10`
- Top-N argument: `30`
- Sampling mode: without replacement within each section sample
- Parser policy: cleaned `exp-002b` policy

## Parser And Mapping Counts

| Metric | Value |
|---|---:|
| Input lines | 38,939 |
| IVTFF data lines | 17,344 |
| Selected `H` lines | 5,216 |
| Non-empty selected `H` lines | 5,207 |
| Empty selected `H` lines | 9 |
| Mapped selected lines | 5,216 |
| Unmapped selected lines | 0 |
| Lines with angle tags | 2,229 |
| Angle tags removed | 4,467 |
| Unique angle-tag forms removed | 111 |
| Discarded empty tokens | 78 |
| Section count | 8 |

## Section Token Counts

| Section | Non-empty mapped lines | Token count |
|---|---:|---:|
| astronomical | 240 | 850 |
| biological | 917 | 6,918 |
| cosmological | 323 | 2,550 |
| herbal | 1,630 | 11,418 |
| pharmaceutical | 456 | 2,579 |
| stars | 1,083 | 10,694 |
| text | 223 | 1,626 |
| zodiac | 335 | 1,332 |

## Common-Size Control

- Common sample size: `850`

### Section-Level Common-Size Summaries

| Section | Original tokens | TTR mean | TTR 2.5% | TTR 97.5% | Token entropy mean (bits) | Entropy 2.5% | Entropy 97.5% |
|---|---:|---:|---:|---:|---:|---:|---:|
| astronomical | 850 | 0.7388235294117647 | 0.7388235294117647 | 0.7388235294117647 | 9.00256820629607 | 9.00256820629607 | 9.00256820629607 |
| biological | 6,918 | 0.4450435294117647 | 0.4188235294117647 | 0.47294117647058825 | 7.745084458676661 | 7.603998155105172 | 7.888665167782867 |
| cosmological | 2,550 | 0.6002505882352941 | 0.5741176470588235 | 0.6258823529411764 | 8.495034438368874 | 8.390069664268843 | 8.601988421964611 |
| herbal | 11,418 | 0.5985623529411764 | 0.5694117647058824 | 0.6305882352941177 | 8.436249692666152 | 8.298521752634805 | 8.566700387763987 |
| pharmaceutical | 2,579 | 0.577564705882353 | 0.5517647058823529 | 0.6047058823529412 | 8.355862299522606 | 8.237025756530851 | 8.47400327399838 |
| stars | 10,694 | 0.5912329411764706 | 0.5635294117647058 | 0.62 | 8.468454962890688 | 8.356272792364614 | 8.589745219272153 |
| text | 1,626 | 0.6571647058823529 | 0.6352941176470588 | 0.6788235294117647 | 8.744202099843598 | 8.659084457269886 | 8.822428303086477 |
| zodiac | 1,332 | 0.6636352941176471 | 0.6447058823529411 | 0.6811764705882353 | 8.70516564832458 | 8.627959001254608 | 8.779293110751267 |

### Pairwise Common-Size JSD Summary

- Observed `exp-003` mean pairwise JSD: `0.5554700431523788` bits
- Common-size mean pairwise JSD: `0.6479551071976217` bits
- Minimum common-size mean pairwise JSD: `0.5133877274319135` bits for `biological` vs `stars`
- Maximum common-size mean pairwise JSD: `0.7512128927329023` bits for `astronomical` vs `biological`

## Pairwise Matched-Size Control

- Pairwise matched mean JSD across all section pairs: `0.5870200377032155` bits
- Minimum pairwise matched mean JSD: `0.3453271743396462` bits for `biological` vs `stars`
- Maximum pairwise matched mean JSD: `0.7512494759958205` bits for `astronomical` vs `biological`

## Comparison To Prior Experiments

| Comparison metric | Value |
|---|---:|
| Observed `exp-003` mean pairwise JSD (source: `artifacts/exp003/pairwise_section_distances.json`) | 0.5554700431523788 |
| Common-size mean pairwise JSD | 0.6479551071976217 |
| Pairwise matched mean pairwise JSD | 0.5870200377032155 |
| Cleaned `exp-002b` mean position-class JSD (source: `artifacts/exp002b/position_clean/distribution_distances.json` via `exp-003`) | 0.5398947694637786 |

## Selected Pairwise Comparisons

| Section pair | Observed `exp-003` JSD | Common-size mean JSD | Pairwise matched mean JSD | Pairwise sample size |
|---|---:|---:|---:|---:|
| astronomical vs biological | 0.7132735389659056 | 0.7512128927329023 | 0.7512494759958205 | 850 |
| biological vs stars | 0.3347291601069759 | 0.5133877274319135 | 0.3453271743396462 | 6,918 |
| herbal vs stars | 0.4462304641923659 | 0.6501049318500001 | 0.4480812950059133 | 10,694 |
| cosmological vs pharmaceutical | 0.5613311195084363 | 0.6488501988352975 | 0.5617662076758468 | 2,550 |
| text vs zodiac | 0.6146855682868653 | 0.6666041565900942 | 0.6235050719700023 | 1,332 |

## Output Artifacts

- `artifacts/exp004/run_summary.json`
- `artifacts/exp004/section_token_counts.csv`
- `artifacts/exp004/common_size_resampling_summary.csv`
- `artifacts/exp004/common_size_resampling_summary.json`
- `artifacts/exp004/common_size_pairwise_jsd.csv`
- `artifacts/exp004/common_size_pairwise_jsd.json`
- `artifacts/exp004/pairwise_matched_jsd.csv`
- `artifacts/exp004/pairwise_matched_jsd.json`
- `artifacts/exp004/observed_vs_resampled_jsd.csv`
- `artifacts/exp004/unmapped_lines.csv`

## Errors Or Warnings

- No runtime error occurred.
- No selected lines were unmapped.
- The optional pooled-label null control was not implemented in this run.
- The common-size control is constrained by the smallest section size (`850` tokens in `astronomical`).
