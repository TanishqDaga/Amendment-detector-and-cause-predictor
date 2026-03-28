import re


def protect_decimals(text):
    return re.sub(r'(\d)\.(\d)', r'\1<dot>\2', text)


def restore_decimals(text):
    return text.replace("<dot>", ".")


def clean_text(text):
    # Protect decimals first
    text = protect_decimals(text)

    # Normalize spaces (keep newlines)
    text = re.sub(r'[ \t]+', ' ', text)

    # Fix broken lines
    text = re.sub(r'\n(?=[a-z])', ' ', text)

    # Ensure section numbers on new line
    text = re.sub(r'(\d+\.)', r'\n\1', text)

    # Remove extra newlines
    text = re.sub(r'\n+', '\n', text)

    # Restore decimals
    text = restore_decimals(text)

    return text.strip()