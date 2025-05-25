# ISIC Classifier


This repository contains a minimal utility for converting firm activity descriptions to ISIC Rev.4 codes.

## Usage

1. Install the `openai` package and set your `OPENAI_API_KEY` environment variable if you want to use ChatGPT for classification.
2. Run the classifier on a CSV file:

```bash
python isic_classifier.py input.csv output.csv --gpt
```

This will read `input.csv` which must contain a column `d1a1x` with the activity description. The classified code will be written to `output.csv`.

Without the `--gpt` flag, a simple token overlap classifier is used instead of the ChatGPT API.

## Testing

Run the automated tests with:

This repository provides a simple tool for mapping free-text firm activity descriptions to four digit ISIC Rev.4 codes.

## Setup

Install the required packages:

```bash
pip install streamlit pandas
```

## Running tests

```bash
pytest -q
```

## Command line usage

The classifier can process a CSV file containing a column named `d1a1x`:

```bash
python isic_classifier.py input.csv output.csv
```

The output CSV will contain the predicted code and a match score for each row.

## Streamlit app

A basic Streamlit interface is provided for classifying a single description or uploading a CSV file.

```bash
streamlit run app.py
```

The app allows you to download the classified results as a new CSV file.

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
