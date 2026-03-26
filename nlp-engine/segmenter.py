import re
import spacy
from extractor import extract_text
from cleaner import clean_text

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")


def segment_rules(text):
    """
    Segments cleaned text into meaningful rules
    """

    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)

    doc = nlp(text)
    rules = []

    for sent in doc.sents:
        sentence = sent.text.strip()

        # Keep only meaningful rules
        if (
            len(sentence.split()) > 8 and
            not sentence.lower().startswith(("such", "this", "these", "those", "it")) and
            any(word in sentence.lower() for word in [
                "must", "should", "shall", "required", "will"
            ])
        ):
            rules.append(sentence)

    return rules


# ==============================
# TESTING
# ==============================

if __name__ == "__main__":
    file_path = "../sample-docs/old.pdf"

    print("Extracting text from PDF...\n")
    raw_text = extract_text(file_path)

    print("Cleaning text...\n")
    cleaned_text = clean_text(raw_text)

    print("Segmenting rules...\n")
    rules = segment_rules(cleaned_text)

    print("\n--- FINAL CLEAN RULES ---\n")

    for i, rule in enumerate(rules):
        print(f"{i+1}. {rule}\n")

    print(f"\nTotal Rules Extracted: {len(rules)}")