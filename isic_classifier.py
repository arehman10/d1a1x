import csv
import re
import sys
from difflib import SequenceMatcher
from typing import List, Tuple


def load_isic(path: str = "isic.csv") -> List[Tuple[str, str]]:
    """Load ISIC code descriptions from a semicolon separated file."""
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        return [(code.strip(), desc.strip()) for code, desc in reader]


def _tokenize(text: str) -> set:
    """Return a set of word tokens from the given text."""
    return set(re.findall(r"\b\w+\b", text.lower()))


def _fuzzy_ratio(a: str, b: str) -> float:
    """Return a similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def classify(activity: str, isic_data: List[Tuple[str, str]]) -> Tuple[str, float]:
    """Return the ISIC code with the highest similarity score."""
    tokens = _tokenize(activity)
    best_code = None
    best_score = 0.0
    for code, desc in isic_data:
        desc_tokens = _tokenize(desc)
        if not desc_tokens:
            continue
        overlap = len(tokens & desc_tokens) / len(desc_tokens)
        fuzzy = _fuzzy_ratio(activity, desc)
        score = (overlap + fuzzy) / 2
        if score > best_score:
            best_score = score
            best_code = code
    return best_code, best_score


def classify_file(input_csv: str, output_csv: str, column: str = "d1a1x", isic_path: str = "isic.csv") -> None:
    """Classify activities in a CSV file and write results to a new CSV."""
    isic_data = load_isic(isic_path)
    with open(input_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        code, ratio = classify(row[column], isic_data)
        row['isic_code'] = code
        row['match_score'] = f"{ratio:.2f}"

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        classify_file(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python isic_classifier.py input.csv output.csv")
