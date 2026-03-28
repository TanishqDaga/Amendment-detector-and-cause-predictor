import re


def protect_decimals(text):
    """
    Replace decimal points with placeholder
    Example: 5.0 → 5<dot>0
    """
    return re.sub(r'(\d)\.(\d)', r'\1<dot>\2', text)


def restore_decimals(text):
    """
    Restore decimal points
    """
    return text.replace("<dot>", ".")


def segment_rules(text):
    # -----------------------------
    # STEP 0: Protect decimals
    # -----------------------------
    text = protect_decimals(text)

    # -----------------------------
    # STEP 1: Split by section numbers
    # -----------------------------
    sections = re.split(r'\n\d+\.\s*', text)

    rules = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # -----------------------------
        # STEP 2: Sentence splitting
        # -----------------------------
        sentences = re.split(r'(?<=[.!?])\s+', section)

        for sent in sentences:
            sent = sent.strip()

            # Restore decimals
            sent = restore_decimals(sent)

            # Skip short junk
            if len(sent.split()) < 6:
                continue

            # Remove pure headings
            if re.match(r'^[A-Za-z\s]+$', sent) and len(sent.split()) < 5:
                continue

            rules.append(sent)

    return rules