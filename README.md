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

```bash
pytest -q
```
