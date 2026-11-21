import re


def preprocess_text(text: str, lowercase: bool = True) -> str:
    """Clean whitespace and optionally lowercase text."""
    if not text:
        return ""

    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned.lower() if lowercase else cleaned