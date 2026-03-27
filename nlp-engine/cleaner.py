import re
import spacy

nlp = spacy.load("en_core_web_sm")

def remove_table_of_contents(text):
    """
    Removes large TOC blocks like:
    PAGE NOS. Preamble Scope Admission ...
    """
    # Remove everything between PAGE NOS and first real section
    text = re.sub(
        r'PAGE NOS\..*?Preamble',
        'Preamble',
        text,
        flags=re.IGNORECASE | re.DOTALL
    )
    return text


def remove_numbered_index(text):
    """
    Removes patterns like:
    1.0 Preamble 2.0 Scope 3.0 Admission ...
    """
    return re.sub(r'(\d+\.\d+\s+[A-Za-z]+\s*){3,}', '', text)


def remove_headers(text):
    text = re.sub(r'FFCS Academic Regulations.*?Version.*?\d+\.\d+', '', text, flags=re.IGNORECASE)
    return text


def remove_long_garbage_lines(text):
    """
    Removes very long non-sentence blocks (like TOC)
    """
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        if len(line.split()) > 80:  # very long = likely garbage
            continue
        cleaned.append(line)

    return "\n".join(cleaned)


def clean_text(text):
    # STEP 1: remove TOC globally
    text = remove_table_of_contents(text)

    # STEP 2: remove numbered index patterns
    text = remove_numbered_index(text)

    # STEP 3: remove headers
    text = remove_headers(text)

    # STEP 4: remove long garbage lines
    text = remove_long_garbage_lines(text)

    # STEP 5: normalize spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()