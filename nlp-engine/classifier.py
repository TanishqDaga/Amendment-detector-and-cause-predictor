import re
import json
from collections import defaultdict
from extractor import extract_text
from segmenter import segment_rules
from cleaner import clean_text   # ✅ NEW

# ==============================
# ENHANCED KEYWORD DICTIONARY
# ==============================

SECTOR_KEYWORDS = {
    "Academics & Curriculum": [
        "curriculum", "course", "courses", "credit", "credits", "syllabus",
        "programme", "program", "semester", "project", "internship",
        "lab", "laboratory", "lecture", "tutorial", "ltpc",
        "course plan", "course code", "course type", "flowchart",
        "foundation core", "discipline core", "elective",
        "open elective", "skill enhancement", "ability enhancement",
        "minor", "honours", "degree", "academic system",
        "learning", "study", "module", "subject"
    ],

    "Examinations & Evaluation": [
        "exam", "examination", "evaluation", "marks", "grade", "grading",
        "assessment", "test", "cat", "fat", "continuous assessment",
        "internal assessment", "final assessment", "result", "score",
        "passing", "fail", "pass", "performance", "gpa", "cgpa",
        "relative grading", "absolute grading", "answer sheet",
        "re-evaluation", "viva", "review",
        "weightage", "assignment", "digital assignment",
        "hot", "higher order thinking"
    ],

    "Admissions & Registration": [
        "admission", "admissions", "enroll", "enrollment", "register",
        "registration", "course registration", "add/drop", "withdrawal",
        "student admission", "eligibility", "selection", "counseling",
        "entry", "intake", "bridge course", "proctor",
        "backlog", "re-register", "re-registration",
        "prerequisite", "co-requisite", "anti-requisite",
        "credit limit", "minimum credits", "maximum credits"
    ],

    "Finance & Fees": [
        "fee", "fees", "payment", "amount", "cost", "charges",
        "scholarship", "financial", "money", "payment due",
        "late fee", "penalty", "refund", "dues",
        "re-registration fee", "registration fee"
    ],

    "Discipline & Conduct": [
        "discipline", "conduct", "behavior", "attendance", "absence",
        "malpractice", "indiscipline", "rules", "regulation",
        "violation", "misconduct", "debarred",
        "attendance requirement", "minimum attendance",
        "code of conduct", "compliance"
    ],

    "Student Support & Misc": [
        "seminar", "workshop", "conference", "training",
        "activity", "event", "hackathon", "makeathon",
        "additional learning", "support", "assistance",
        "guidance", "faculty", "advisor",
        "placement", "career", "extra curricular",
        "co curricular"
    ]
}

# ==============================
# KEYWORD CLASSIFIER
# ==============================

def classify_rule_keyword(rule):
    rule_lower = rule.lower()
    scores = {}

    for sector, keywords in SECTOR_KEYWORDS.items():
        score = 0
        for word in keywords:
            if word in rule_lower:
                score += 2 if " " in word else 1
        scores[sector] = score

    best_sector = max(scores, key=scores.get)

    if scores[best_sector] == 0:
        return "Student Support & Misc"

    return best_sector


# ==============================
# SEMANTIC CLASSIFIER
# ==============================

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')  # loaded once

SECTOR_DESCRIPTIONS = {
    "Academics & Curriculum": "courses syllabus curriculum credits academic structure projects internships semester",
    "Examinations & Evaluation": "exam marks grading evaluation assessment CAT FAT tests scoring system",
    "Admissions & Registration": "admission enrollment registration process joining university student intake",
    "Finance & Fees": "fees payment cost scholarship financial charges money transactions",
    "Discipline & Conduct": "attendance discipline behavior rules misconduct malpractice absence conduct",
    "Student Support & Misc": "general rules support services activities miscellaneous policies"
}


def classify_rule_semantic(rule):
    rule_embedding = model.encode(rule, convert_to_tensor=True)

    best_sector = None
    best_score = -1

    for sector, desc in SECTOR_DESCRIPTIONS.items():
        desc_embedding = model.encode(desc, convert_to_tensor=True)
        score = util.cos_sim(rule_embedding, desc_embedding).item()

        if score > best_score:
            best_score = score
            best_sector = sector

    return best_sector


# ==============================
# HYBRID CLASSIFIER
# ==============================

def classify_rule(rule):
    sector = classify_rule_keyword(rule)

    if sector == "Student Support & Misc":
        sector = classify_rule_semantic(rule)

    return sector


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

    print("Cleaning text...")   # ✅ NEW STEP
    text = clean_text(raw_text)

    print("Segmenting rules...")
    rules = segment_rules(text)

    print(f"Total rules found: {len(rules)}")

    print("\nClassifying rules...\n")
    categorized = classify_rules(rules)

    # PRINT FULL OUTPUT
    for sector, items in categorized.items():
        print("\n==============================")
        print(f"{sector} ({len(items)} rules)")
        print("==============================\n")

        for i, rule in enumerate(items):
            print(f"{i+1}. {rule}\n")

    # SAVE TO FILE
    output_path = "classified_rules.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(categorized, f, indent=4, ensure_ascii=False)

    print(f"\nFull classified output saved to: {output_path}")