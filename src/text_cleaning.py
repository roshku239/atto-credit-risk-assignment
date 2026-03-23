import re
import pandas as pd


def clean_description(text: str) -> str:
    """Lowercase, remove punctuation, numbers, and extra spaces."""
    if pd.isna(text):
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text
