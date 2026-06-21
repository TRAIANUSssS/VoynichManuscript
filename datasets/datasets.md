# Datasets

## Raw Data

Raw data should be stored under `data/raw/` and treated as read-only after import.

Current raw Voynich data:

- `data/raw/LSI_ivtff_0d.txt`
  - Source: https://www.voynich.nu/data/beta/LSI_ivtff_0d.txt
  - Source documentation: https://www.voynich.nu/transcr.html
  - Download date: 2026-06-21
  - SHA-256: `3f3f2af18cde10efe75c582f49b07b651c3397022fcbfa5854fecc424c121afa`
  - Used by: `exp-001_baseline-statistics_active_2026-06-21`
  - License/status: `needs-verification`

## Processed Data

Processed data should be stored under `data/processed/` with transformation notes.

No processed data has been created yet.

## External Corpora

External corpora will be used for baseline comparison only after provenance, license/status, and preprocessing steps are documented.

## Data Provenance Rules

Each dataset entry should include:

- source;
- download date;
- license or usage status if known;
- transformation steps;
- known issues;
- related scripts.

## TODO

- Verify license/status for `data/raw/LSI_ivtff_0d.txt`.
- Define control corpus requirements.
