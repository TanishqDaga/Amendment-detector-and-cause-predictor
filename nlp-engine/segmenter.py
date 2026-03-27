import re
import spacy
from extractor import extract_text
from cleaner import clean_text

# Load model once
nlp = spacy.load("en_core_web_sm")


def segment_rules(text):
    """
    Segments cleaned text into meaningful rules
    using context-aware grouping
    """

    # Normalize text
    text = re.sub(r'\s+', ' ', text)

    doc = nlp(text)

    rules = []
    current_rule = ""

    for sent in doc.sents:
        sentence = sent.text.strip()

# Remove section titles like "1. Attendance"
        sentence = re.sub(r'^\d+\.\s*[A-Za-z]+\s*', '', sentence)

        # ❌ Skip very short sentences
        if len(sentence.split()) < 6:
            continue

        # ❌ Remove TOC / headings remnants
        if re.search(
            r'Preamble|Scope|Admission|Academic System|Course Plan|Course Flowchart|PAGE NOS',
            sentence,
            re.IGNORECASE
        ):
            continue

        # ❌ Remove weak context sentences
        if sentence.lower().startswith(("under this", "thus", "therefore")):
            continue

        # ✅ Start new rule if strong indicator
        if any(word in sentence.lower() for word in [
            "must", "should", "shall", "required", "will", "eligible"
        ]):
            if current_rule:
                rules.append(current_rule.strip())
            current_rule = sentence
        else:
            # Continue previous rule (context building)
            current_rule += " " + sentence

    # Add last rule
    if current_rule:
        rules.append(current_rule.strip())

    # Final filtering (remove weak/short rules)
    rules = [r for r in rules if len(r.split()) > 10]

    return rules


# ==============================
# TESTING
# ==============================

if __name__ == "__main__":
    file_path = "../sample-docs/old.pdf"

    print("Extracting text...\n")
    raw_text = extract_text(file_path)

    print("Cleaning text...\n")
    cleaned_text = clean_text(raw_text)

    print("Segmenting rules...\n")
    rules = segment_rules(cleaned_text)

    print("\n--- FINAL RULES ---\n")

    for i, rule in enumerate(rules):
        print(f"{i+1}. {rule}\n")

    print(f"\nTotal Rules Extracted: {len(rules)}")