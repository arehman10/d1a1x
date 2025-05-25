# ISIC Classifier

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
