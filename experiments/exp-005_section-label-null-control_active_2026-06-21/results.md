# Results

Run date: 2026-06-21

## Command

```bash
python scripts/exp005_section_label_null_control.py --input data/raw/LSI_ivtff_0d.txt --metadata data/metadata/folio_sections.csv --output artifacts/exp005/ --transcriber-code H --iterations 1000 --seed 20260621
```

## Script

- Script path: `scripts/exp005_section_label_null_control.py`

## Input Data

- Input file: `data/raw/LSI_ivtff_0d.txt`
- Input SHA-256: `3f3f2af18cde10efe75c582f49b07b651c3397022fcbfa5854fecc424c121afa`
- Source: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
- Source documentation: https://www.voynich.nu/transcr.html

## Metadata

- Metadata path: `data/metadata/folio_sections.csv`
- Metadata created during this run: `false`
- Metadata source: reused `exp-003` / `exp-004` folio-to-section mapping derived from IVTFF page-header `$I` illustration-type metadata

## Parameters

- Transcriber code: `H`
- Iterations: `1000`
- Random seed: `20260621`
- Minimum count argument: `10`
- Top-N argument: `30`
- Sample mode argument: `pairwise-matched`
- Parser policy: cleaned `exp-002b` policy
- Pairwise null control: pooled-label, size-matched to observed full section sizes
- Pairwise matched null control: pooled-label, size-matched to `exp-004` pairwise matched sample sizes
- Global permutation control: all-section pooled-label reassignment preserving observed section token counts

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

## Historical Comparison Values

| Metric | Value |
|---|---:|
| Observed `exp-003` mean pairwise JSD | 0.5554700431523788 |
| Historical `exp-004` pairwise matched mean pairwise JSD | 0.5870200377032155 |

## Pairwise Pooled-Label Null Control

- Pair count: `28`
- Pairs above the 97.5% null quantile: `28`
- Pairs within the null interval: `0`
- Pairs below the null mean: `0`

### Selected pairwise pooled-label results

| Section pair | Observed JSD | Null mean JSD | Null 97.5% | Observed minus null mean | Empirical p-value | Conclusion |
|---|---:|---:|---:|---:|---:|---|
| astronomical vs biological | 0.7132735389659056 | 0.3282154603135074 | 0.3442137381861082 | 0.3850580786523982 | 0.000999000999000999 | above_null_97_5 |
| biological vs stars | 0.3347291601069759 | 0.21769569417044324 | 0.22234728512297827 | 0.11703346593653266 | 0.000999000999000999 | above_null_97_5 |
| herbal vs stars | 0.4462304641923659 | 0.23893037775790366 | 0.24317928673317699 | 0.20730008643446224 | 0.000999000999000999 | above_null_97_5 |
| cosmological vs text | 0.46739630245416325 | 0.4176911369450756 | 0.42943875031054035 | 0.049705165509087657 | 0.000999000999000999 | above_null_97_5 |
| text vs zodiac | 0.6146855682868653 | 0.5088249393407724 | 0.5224323608125266 | 0.10586062894609283 | 0.000999000999000999 | above_null_97_5 |

## Pairwise Matched Pooled-Label Null Control

- Pair count: `28`
- Pairs above the 97.5% matched null quantile: `28`

### Selected pairwise matched null results

| Section pair | `exp-004` matched mean JSD | Matched null mean JSD | Matched null 97.5% | Difference | Empirical p-value | Conclusion |
|---|---:|---:|---:|---:|---:|---|
| astronomical vs biological | 0.7512494759958205 | 0.3922085964760815 | 0.4186463803027656 | 0.359040879519739 | 0.000999000999000999 | above_null_97_5 |
| biological vs stars | 0.3453271743396462 | 0.2320445595807326 | 0.23802016578259266 | 0.1132826147589136 | 0.000999000999000999 | above_null_97_5 |
| herbal vs stars | 0.4480812950059133 | 0.2413752726268444 | 0.2457332055520904 | 0.2067060223790689 | 0.000999000999000999 | above_null_97_5 |
| cosmological vs pharmaceutical | 0.5617662076758468 | 0.3834991851827905 | 0.39312180397015817 | 0.17826702249305632 | 0.000999000999000999 | above_null_97_5 |
| text vs zodiac | 0.6235050719700023 | 0.5214820091968599 | 0.5382705000327036 | 0.10202306277314233 | 0.000999000999000999 | above_null_97_5 |

## Global Section-Label Permutation

| Metric | Value |
|---|---:|
| Observed mean pairwise JSD | 0.5554700431523788 |
| Null mean pairwise JSD mean | 0.3788255370327812 |
| Null mean pairwise JSD standard deviation | 0.003030097354796408 |
| Null mean pairwise JSD median | 0.3788888389830416 |
| Null mean pairwise JSD 2.5% quantile | 0.37312659371797946 |
| Null mean pairwise JSD 97.5% quantile | 0.38500785795761844 |
| Observed minus null mean | 0.1766445061195976 |
| Empirical percentile | 1.0 |
| Empirical p-value | 0.000999000999000999 |

## Output Artifacts

- `artifacts/exp005/run_summary.json`
- `artifacts/exp005/section_token_counts.csv`
- `artifacts/exp005/pairwise_null_control.csv`
- `artifacts/exp005/pairwise_null_control.json`
- `artifacts/exp005/observed_vs_null_jsd.csv`
- `artifacts/exp005/pairwise_matched_null_control.csv`
- `artifacts/exp005/pairwise_matched_null_control.json`
- `artifacts/exp005/global_section_label_permutation.csv`
- `artifacts/exp005/global_section_label_permutation.json`
- `artifacts/exp005/unmapped_lines.csv`

## Errors Or Warnings

- No runtime error occurred.
- No selected lines were unmapped.
- Empirical p-values are limited by `1000` iterations and should be treated as exploratory null-model summaries.
- The experiment evaluates whether section labels preserve measurable token-frequency structure under this null model; it does not identify the cause of that structure.
