import re
import spacy
from sentence_transformers import SentenceTransformer, util

# Load models
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Reference sentence (what a "good rule" looks like)
REFERENCE_SENTENCE = "Students must maintain minimum attendance and follow academic regulations"

ref_embedding = model.encode(REFERENCE_SENTENCE, convert_to_tensor=True)


# ==============================
# RULE-BASED CLEANING
# ==============================

def basic_cleaning(lines):
    cleaned = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # ❌ Remove headers / repeated text
        if "ffcs academic regulations" in line.lower():
            continue

        # ❌ Remove version / page artifacts
        if "version" in line.lower():
            continue

        # ❌ Remove table of contents
        if "contents" in line.lower() or "page nos" in line.lower():
            continue

        # ❌ Remove pure numbers
        if re.match(r'^\d+$', line):
            continue

        # ❌ Remove noisy table rows
        if len(line.split()) > 40:
            continue

        cleaned.append(line)

    return cleaned


# ==============================
# NLP + ML FILTERING
# ==============================

def is_meaningful_sentence(sentence):
    sentence = sentence.strip()

    # ❌ Too short
    if len(sentence.split()) < 6:
        return False

    # ❌ Starts with weak reference words
    if sentence.lower().startswith(("such", "this", "these", "those", "it")):
        return False

    # ❌ No verb (not a proper sentence)
    doc = nlp(sentence)
    has_verb = any(token.pos_ == "VERB" for token in doc)
    if not has_verb:
        return False

    # ❌ No subject
    has_subject = any(token.dep_ in ("nsubj", "nsubjpass") for token in doc)
    if not has_subject:
        return False

    # ✅ Semantic similarity check
    sentence_embedding = model.encode(sentence, convert_to_tensor=True)
    similarity = util.cos_sim(sentence_embedding, ref_embedding).item()

    # Threshold (tuneable)
    if similarity < 0.3:
        return False

    return True


# ==============================
# FINAL CLEAN FUNCTION
# ==============================

def clean_text(text):
    # Step 1: Split into lines
    lines = text.split("\n")

    # Step 2: Basic cleaning
    lines = basic_cleaning(lines)

    # Step 3: Merge lines into sentences
    text = " ".join(lines)
    doc = nlp(text)

    # Step 4: Extract sentences
    sentences = [sent.text.strip() for sent in doc.sents]

    # Step 5: ML filtering
    final_sentences = []

    for sentence in sentences:
        if is_meaningful_sentence(sentence):
            final_sentences.append(sentence)

    return " ".join(final_sentences)