import re
import spacy

nlp = spacy.load("en_core_web_sm")


def is_new_rule(sentence):
    sentence_lower = sentence.lower()

    if any(word in sentence_lower for word in [
        "must", "shall", "should", "required", "eligible"
    ]):
        return True

    if re.match(r'^(the|students|evaluation|attendance|registration|fee)', sentence_lower):
        return True

    return False


def segment_rules(text):
    text = re.sub(r'\s+', ' ', text)

    doc = nlp(text)

    rules = []
    current_rule = ""

    for sent in doc.sents:
        sentence = sent.text.strip()

        # remove headings
        sentence = re.sub(r'^\d+\.\s*[A-Za-z]+\s*', '', sentence)

        if len(sentence.split()) < 5:
            continue

        if is_new_rule(sentence):
            if current_rule:
                rules.append(current_rule.strip())
            current_rule = sentence
        else:
            current_rule += " " + sentence

    if current_rule:
        rules.append(current_rule.strip())

    return [r for r in rules if len(r.split()) > 8]