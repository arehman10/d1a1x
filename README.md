# ISIC Classification Utilities

This repository contains a simple ISIC Rev.4 classifier and a small demo app
built with Streamlit. The classifier maps free‑text firm activity descriptions
to four‑digit ISIC codes using token overlap and fuzzy string matching.

## Installation

Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Alternatively, you can install the minimal packages directly:

```bash
pip install pandas streamlit
```

## Running the Streamlit app

Launch the web interface with:

```bash
streamlit run isic_app.py
```

The app lets you classify a single activity description or upload a CSV file
(with a `d1a1x` column) and obtain the predicted ISIC codes. The processed file
can be downloaded directly from the app.

## Command line usage

The `isic_classifier.py` module can also be run from the command line:

```bash
python isic_classifier.py input.csv output.csv
```

The input CSV must contain a `d1a1x` column. The script will produce a copy of
the file with `isic_code` and `match_score` columns added.

## Testing

Run the tests with:

```bash
pytest -q
```
