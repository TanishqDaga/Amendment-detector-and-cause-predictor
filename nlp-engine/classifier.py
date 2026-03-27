import re
import json
from collections import defaultdict
from extractor import extract_text
from segmenter import segment_rules
from cleaner import clean_text

# ==============================
# KEYWORD DICTIONARY
# ==============================

SECTOR_KEYWORDS = {
    "Academics & Curriculum": [
        "curriculum", "course", "courses", "credit", "credits", "syllabus",
        "programme", "program", "semester", "project", "internship",
        "lab", "laboratory", "lecture", "tutorial", "ltpc",
        "elective", "minor", "honours", "degree"
    ],

    "Examinations & Evaluation": [
        "exam", "evaluation", "marks", "grade", "grading",
        "assessment", "test", "cat", "fat", "gpa", "cgpa",
        "result", "pass", "fail", "assignment"
    ],

    "Admissions & Registration": [
        "admission", "enroll", "registration", "register",
        "eligibility", "selection", "intake",
        "prerequisite", "credit limit"
    ],

    "Finance & Fees": [
        "fee", "fees", "payment", "amount",
        "scholarship", "refund", "dues"
    ],

    "Discipline & Conduct": [
        "attendance", "discipline", "malpractice",
        "misconduct", "debarred", "absence"
    ],

    "Student Support & Misc": []
}

# ==============================
# KEYWORD SCORING
# ==============================

def get_keyword_scores(rule):
    rule_lower = rule.lower()
    scores = {}

    for sector, keywords in SECTOR_KEYWORDS.items():
        score = 0
        for word in keywords:
            if word in rule_lower:
                score += 2 if " " in word else 1
        scores[sector] = score

    return scores


# ==============================
# SEMANTIC MODEL
# ==============================

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

SECTOR_DESCRIPTIONS = {
    "Academics & Curriculum": "courses syllabus curriculum credits academic structure projects",
    "Examinations & Evaluation": "exam marks grading evaluation assessment results",
    "Admissions & Registration": "admission enrollment registration eligibility process",
    "Finance & Fees": "fees payment cost scholarship money refund",
    "Discipline & Conduct": "attendance discipline behavior rules misconduct",
    "Student Support & Misc": "general rules support activities policies"
}

# Precompute embeddings (IMPORTANT optimization)
sector_embeddings = {
    sector: model.encode(desc, convert_to_tensor=True)
    for sector, desc in SECTOR_DESCRIPTIONS.items()
}


def get_semantic_scores(rule):
    rule_embedding = model.encode(rule, convert_to_tensor=True)
    scores = {}

    for sector, emb in sector_embeddings.items():
        score = util.cos_sim(rule_embedding, emb).item()
        scores[sector] = score

    return scores


# ==============================
# FINAL HYBRID CLASSIFIER
# ==============================

def classify_rule(rule):
    keyword_scores = get_keyword_scores(rule)
    semantic_scores = get_semantic_scores(rule)

    # Normalize keyword scores
    max_kw = max(keyword_scores.values()) + 1e-5
    keyword_scores = {k: v / max_kw for k, v in keyword_scores.items()}

    # Combine scores (weighted)
    final_scores = {}

    for sector in SECTOR_KEYWORDS.keys():
        final_scores[sector] = (
            0.4 * keyword_scores[sector] +
            0.6 * semantic_scores[sector]
        )

    # Pick best
    best_sector = max(final_scores, key=final_scores.get)

    return best_sector


def classify_rules(rules):
    categorized = defaultdict(list)

    for rule in rules:
        sector = classify_rule(rule)
        categorized[sector].append(rule)

    return categorized


# ==============================
# MAIN EXECUTION
# ==============================

if __name__ == "__main__":
    print("Extracting text...")
    raw_text = extract_text("../sample-docs/old.pdf")

    print("Cleaning text...")
    text = clean_text(raw_text)

    print("Segmenting rules...")
    rules = segment_rules(text)

    print(f"Total rules found: {len(rules)}")

    print("\nClassifying rules...\n")
    categorized = classify_rules(rules)

    # PRINT OUTPUT
    for sector, items in categorized.items():
        print("\n==============================")
        print(f"{sector} ({len(items)} rules)")
        print("==============================\n")

        for i, rule in enumerate(items):
            print(f"{i+1}. {rule}\n")

    # SAVE TO FILE
    with open("classified_rules.json", "w", encoding="utf-8") as f:
        json.dump(categorized, f, indent=4, ensure_ascii=False)

    print("\n✅ Output saved to classified_rules.json")