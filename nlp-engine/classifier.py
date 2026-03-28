import re
from collections import defaultdict
from extractor import extract_text
from segmenter import segment_rules
from cleaner import clean_text

from sentence_transformers import SentenceTransformer, util

# ==============================
# LOAD MODEL
# ==============================

model = SentenceTransformer('all-MiniLM-L6-v2')

# ==============================
# SECTOR DEFINITIONS (SEMANTIC)
# ==============================

SECTOR_DESCRIPTIONS = {
    "Academics & Curriculum": "attendance courses curriculum learning classroom teaching academic structure",
    "Examinations & Evaluation": "exam grading marks evaluation assessment tests assignments performance",
    "Admissions & Registration": "admission enrollment registration eligibility course registration process",
    "Finance & Fees": "fees payment penalty fine cost scholarship financial transactions",
    "Discipline & Conduct": "discipline misconduct behavior suspension expulsion rules violation conduct",
    "Student Support & Misc": "student support services counselling activities help facilities"
}

# Precompute embeddings
sector_embeddings = {
    sector: model.encode(desc, convert_to_tensor=True)
    for sector, desc in SECTOR_DESCRIPTIONS.items()
}

# ==============================
# KEYWORD DICTIONARY
# ==============================

SECTOR_KEYWORDS = {
    "Academics & Curriculum": [
        "attendance", "course", "courses", "credit", "credits", "curriculum", "syllabus",
        "programme", "program", "semester", "project", "internship",
        "lab", "laboratory", "lecture", "tutorial", "ltpc",
        "elective", "minor", "honours", "degree",
        "academic", "class", "classroom", "subject", "module",
        "learning", "teaching", "study", "session",
        "faculty", "instructor", "professor", "department",
        "academic year", "batch", "cohort",
        "training", "workshop", "practical", "theory",
        "core course", "open elective", "discipline elective",
        "capstone", "thesis", "research", "paper",
        "course structure", "course content", "course plan",
        "credit transfer", "academic requirement", "graduation requirement"
    ],

    "Examinations & Evaluation": [
        "exam", "examination", "evaluation", "marks", "grade", "grading",
        "assessment", "test", "quiz", "cat", "fat", "gpa", "cgpa",
        "result", "pass", "fail", "assignment", "score",
        "performance", "internal", "external", "midterm", "endterm",
        "final exam", "internal marks", "external marks",
        "grading system", "evaluation criteria", "rubric",
        "answer sheet", "script", "invigilation",
        "revaluation", "rechecking", "backlog", "arrear",
        "supplementary exam", "makeup exam", "retake",
        "cutoff", "percentage", "rank", "merit list",
        "result declaration", "scorecard", "marksheet",
        "exam schedule", "exam timetable", "assessment policy",
        "weightage", "continuous assessment", "internal assessment"
    ],

    "Admissions & Registration": [
        "admission", "admissions", "enroll", "enrollment", "registration", "register",
        "eligibility", "selection", "intake", "apply", "application",
        "admit", "seat", "allotment", "counselling",
        "document verification", "verification", "certificate",
        "cutoff", "merit", "rank", "quota",
        "lateral entry", "direct admission", "spot admission",
        "withdrawal", "cancellation", "drop", "re-admission",
        "registration window", "late registration",
        "course registration", "subject registration",
        "add course", "drop course", "withdraw course",
        "credit limit", "overload", "underload",
        "approval", "advisor", "faculty advisor",
        "portal", "academic portal", "student portal"
    ],

    "Finance & Fees": [
        "fee", "fees", "payment", "amount", "dues",
        "scholarship", "refund", "fine", "penalty", "charge", "charged",
        "₹", "cost", "tuition", "financial",
        "payment deadline", "late fee", "processing fee",
        "hostel fee", "mess fee", "transport fee",
        "installment", "emi", "billing", "invoice",
        "receipt", "transaction", "online payment",
        "bank", "upi", "net banking", "credit card",
        "debit card", "payment gateway",
        "funding", "grant", "aid", "financial aid",
        "waiver", "concession", "discount",
        "overdue", "arrears", "balance",
        "fee structure", "fee policy", "financial policy"
    ],

    "Discipline & Conduct": [
        "discipline", "conduct", "behavior", "misconduct",
        "malpractice", "violation", "rule violation",
        "code of conduct", "ethics", "integrity",
        "suspension", "expulsion", "debarred",
        "warning", "notice", "penalty", "punishment",
        "ragging", "harassment", "bullying",
        "cheating", "copying", "plagiarism",
        "fraud", "forgery", "misbehavior",
        "attendance shortage", "shortage",
        "indiscipline", "unethical", "breach",
        "complaint", "disciplinary action",
        "committee", "inquiry", "investigation",
        "hearing", "appeal", "sanction",
        "restriction", "ban", "prohibited",
        "compliance", "non-compliance"
    ],

    "Student Support & Misc": [
        "support", "counselling", "guidance",
        "mentorship", "advisor", "help", "assistance",
        "facility", "service", "resource",
        "library", "lab access", "internet",
        "wifi", "hostel", "accommodation",
        "transport", "bus", "medical",
        "health", "insurance", "wellness",
        "club", "activity", "event",
        "sports", "cultural", "extra curricular",
        "placement", "career", "training",
        "internship support", "job", "recruitment",
        "alumni", "network", "community",
        "portal support", "technical support"
    ]
}

# ==============================
# PRIORITY RULES
# ==============================

def priority_override(rule):
    r = rule.lower()

    # -------------------------------
    # KEYWORD GROUPS
    # -------------------------------

    academics = ["attendance", "course", "curriculum", "credit", "lecture", "semester", "internship"]
    exams = ["exam", "evaluation", "marks", "grade", "cat", "fat", "assignment", "test"]
    finance = ["fee", "fees", "₹", "penalty", "fine", "payment", "refund"]
    registration = ["registration", "register", "enroll", "enrollment", "admission"]
    discipline = ["misconduct", "discipline", "violation", "suspension", "expulsion", "malpractice"]

    # -------------------------------
    # HELPER FUNCTION
    # -------------------------------

    def contains_any(keywords):
        return any(k in r for k in keywords)

    # -------------------------------
    # RULE 1: DISCIPLINE HAS HIGHEST PRIORITY
    # -------------------------------
    if contains_any(discipline):
        return "Discipline & Conduct"

    # -------------------------------
    # RULE 2: FINANCE ONLY IF STRONG SIGNAL
    # -------------------------------
    if contains_any(finance):
        # Avoid misclassifying registration with penalty
        if contains_any(registration):
            return "Admissions & Registration"
        return "Finance & Fees"

    # -------------------------------
    # RULE 3: REGISTRATION VS ACADEMICS
    # -------------------------------
    if contains_any(registration):
        # If clearly academic context, override
        if contains_any(academics):
            return "Academics & Curriculum"
        return "Admissions & Registration"

    # -------------------------------
    # RULE 4: EXAM VS ACADEMICS (VERY IMPORTANT)
    # -------------------------------
    if contains_any(exams):
        # If attendance + exam → academics dominates
        if "attendance" in r:
            return "Academics & Curriculum"

        # If marks/grades → exam
        if any(k in r for k in ["marks", "grade", "gpa", "cgpa"]):
            return "Examinations & Evaluation"

        return "Examinations & Evaluation"

    # -------------------------------
    # RULE 5: ACADEMICS (DEFAULT HIGH PRIORITY)
    # -------------------------------
    if contains_any(academics):
        return "Academics & Curriculum"

    # -------------------------------
    # RULE 6: FALLBACK LOGIC
    # -------------------------------
    return None


# ==============================
# KEYWORD SCORING
# ==============================

def keyword_score(rule):
    r = rule.lower()
    scores = {}

    for sector, keywords in SECTOR_KEYWORDS.items():
        score = sum(1 for k in keywords if k in r)
        scores[sector] = score

    return scores


# ==============================
# SEMANTIC SCORING (SBERT)
# ==============================

def semantic_score(rule):
    rule_emb = model.encode(rule, convert_to_tensor=True)
    scores = {}

    for sector, emb in sector_embeddings.items():
        scores[sector] = util.cos_sim(rule_emb, emb).item()

    return scores


# ==============================
# FINAL HYBRID CLASSIFIER
# ==============================

def classify_rule(rule):
    # 🔥 Step 1: Priority override
    priority = priority_override(rule)
    if priority:
        return priority

    # 🔥 Step 2: Keyword score
    kw_scores = keyword_score(rule)

    # 🔥 Step 3: Semantic score
    sem_scores = semantic_score(rule)

    # Normalize keyword scores
    max_kw = max(kw_scores.values()) + 1e-5
    kw_scores = {k: v / max_kw for k, v in kw_scores.items()}

    # 🔥 Step 4: Combine (Weighted)
    final_scores = {}

    for sector in SECTOR_DESCRIPTIONS.keys():
        final_scores[sector] = (
            0.4 * kw_scores[sector] +
            0.6 * sem_scores[sector]
        )

    best_sector = max(final_scores, key=final_scores.get)

    return best_sector


def classify_rules(rules):
    categorized = defaultdict(list)

    for rule in rules:
        sector = classify_rule(rule)
        categorized[sector].append(rule)

    return categorized


# ==============================
# TESTING
# ==============================

if __name__ == "__main__":
    print("Extracting text...")
    raw_text = extract_text("../sample-docs/old.pdf")

    print("Cleaning text...")
    text = clean_text(raw_text)

    print("Segmenting rules...")
    rules = segment_rules(text)

    print("\nClassifying rules...\n")
    categorized = classify_rules(rules)

    for sector, items in categorized.items():
        print("\n==============================")
        print(f"{sector} ({len(items)} rules)")
        print("==============================\n")

        for i, rule in enumerate(items):
            print(f"{i+1}. {rule}\n")

    print("\n✅ Advanced Classification complete")