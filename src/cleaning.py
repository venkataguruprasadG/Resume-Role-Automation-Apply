# src/cleaning.py
import re


def normalize_text(text):
    # Lowercase everything
    text = text.lower()
    # Remove extra spaces and newlines
    text = re.sub(r"\s+", " ", text)
    return text
