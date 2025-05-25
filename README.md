# ISIC 4.0 Activity Classifier

This repository contains a minimal utility to map free-text business activity descriptions to **ISIC Rev.4** four digit codes.

## Files
- `isic_classifier.py` – script and library for classifying activities.
- `isic.csv` – small sample of ISIC codes used for matching.
- `sample_activities.csv` – example CSV with a column `d1a1x` containing activity descriptions.
- `test_classifier.py` – simple pytest verifying classification of sample data.

## Usage

```bash
python isic_classifier.py input.csv output.csv
```

The input CSV must contain a column named `d1a1x`. The output file will contain the original data along with `isic_code` and `match_score` columns.

To classify the provided sample activities, run:

```bash
python isic_classifier.py sample_activities.csv classified.csv
```

## Running the tests

```bash
pytest -q
```

## Notes

The included `isic.csv` contains only a small subset of ISIC Rev.4 codes for demonstration purposes. For production use, replace it with the full ISIC dataset.
