import argparse
import csv
import os
import re
import sys
from typing import List, Tuple

try:  # pragma: no cover - allow running without openai installed
    import openai  # type: ignore
except Exception:  # pragma: no cover
    class _DummyChatCompletion:
        @staticmethod
        def create(*args, **kwargs):
            raise RuntimeError("openai package is required to use the ChatGPT classifier")

    class openai:  # type: ignore
        ChatCompletion = _DummyChatCompletion


def load_isic(path: str = "isic.csv") -> List[Tuple[str, str]]:
    """Load ISIC code descriptions from a semicolon separated file."""
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        return [(code.strip(), desc.strip()) for code, desc in reader]


def _tokenize(text: str) -> set:
    """Return a set of word tokens from the given text."""
    return set(re.findall(r"\b\w+\b", text.lower()))


def classify(activity: str, isic_data: List[Tuple[str, str]]) -> Tuple[str, float]:
    """Return the ISIC code with the highest token overlap score."""
    tokens = _tokenize(activity)
    best_code = None
    best_score = 0.0
    for code, desc in isic_data:
        desc_tokens = _tokenize(desc)
        if not desc_tokens:
            continue
        score = len(tokens & desc_tokens) / len(desc_tokens)
        if score > best_score:
            best_score = score
            best_code = code
    return best_code, best_score


def classify_chatgpt(activity: str, isic_data: List[Tuple[str, str]], *, api_key: str | None = None) -> str:
    """Classify a single activity using the ChatGPT API.

    The function provides the list of available ISIC codes and asks the model to
    return only the 4-digit code that best matches the description.
    """
    openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
    options = "\n".join(f"{code}: {desc}" for code, desc in isic_data)
    messages = [
        {
            "role": "system",
            "content": (
                "Select the most appropriate 4-digit ISIC code from the provided list "
                "that matches the user's business activity description. Respond with "
                "only the 4-digit code."
            ),
        },
        {
            "role": "user",
            "content": f"Available codes:\n{options}\n\nActivity: {activity}",
        },
    ]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=0)
    return str(response["choices"][0]["message"]["content"]).strip()


def classify_file(
    input_csv: str,
    output_csv: str,
    column: str = "d1a1x",
    isic_path: str = "isic.csv",
    use_gpt: bool = False,
    api_key: str | None = None,
) -> None:
    """Classify activities in a CSV file and write results to a new CSV.

    When ``use_gpt`` is ``True`` the classification is performed via the
    ChatGPT API. Otherwise, the local token-overlap classifier is used.
    """
    isic_data = load_isic(isic_path)
    with open(input_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        if use_gpt:
            code = classify_chatgpt(row[column], isic_data, api_key=api_key)
            row['isic_code'] = code
        else:
            code, ratio = classify(row[column], isic_data)
            row['isic_code'] = code
            row['match_score'] = f"{ratio:.2f}"

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify activities into ISIC codes")
    parser.add_argument("input_csv")
    parser.add_argument("output_csv")
    parser.add_argument("--gpt", action="store_true", help="Use ChatGPT for classification")
    parser.add_argument("--api-key", help="OpenAI API key (defaults to OPENAI_API_KEY env variable)")
    args = parser.parse_args()
    classify_file(args.input_csv, args.output_csv, use_gpt=args.gpt, api_key=args.api_key)
