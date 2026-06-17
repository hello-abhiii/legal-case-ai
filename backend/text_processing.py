import re


def preprocess_legal_text(text: str) -> str:
    """Normalize legal text consistently for training and inference."""
    text = str(text).lower()
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\(\d{4}\)\s+\d+\s+\w+\s+\d+", " ", text)
    text = re.sub(r"\b(?:section|sec\.?|ipc|i\.p\.c\.?)\s+(\d+[a-z]?)\b", r"ipc_\1", text)
    text = re.sub(r"[^a-z0-9_\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def combine_case_fields(facts: str, section: str, court: str) -> str:
    return preprocess_legal_text(f"{facts} {section} {court}")
