import os

from extractor import extract_text
from cleaner import clean_text
from segmenter import segment_rules
from classifier import classify_rules

from similarity import match_rules
from analyzer import analyze_changes
from numerical_analyzer import numerical_comparison
from output_generator import generate_output_sectorwise


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OLD_PATH = os.path.join(BASE_DIR, "sample-docs", "old.pdf")
NEW_PATH = os.path.join(BASE_DIR, "sample-docs", "new.pdf")


def process_document(path):
    text = extract_text(path)
    text = clean_text(text)
    rules = segment_rules(text)
    categorized = classify_rules(rules)
    return categorized


# 🔥 NEW: flatten rules for global matching
def flatten_rules(data):
    all_rules = []
    rule_to_sector = {}

    for sector, rules in data.items():
        for r in rules:
            all_rules.append(r)
            rule_to_sector[r] = sector

    return all_rules, rule_to_sector


# 🔥 NEW: assign sector AFTER matching
def assign_sectorwise(changes, old_map, new_map):
    sector_output = {}

    # helper
    def init_sector(sector):
        if sector not in sector_output:
            sector_output[sector] = {
                "added": [],
                "deleted": [],
                "modified": []
            }

    # 🔥 MODIFIED
    for change in changes["modified"]:
        sector = new_map.get(change["new"], "Unknown")
        init_sector(sector)
        sector_output[sector]["modified"].append(change)

    # 🔥 ADDED
    for rule in changes["added"]:
        sector = new_map.get(rule, "Unknown")
        init_sector(sector)
        sector_output[sector]["added"].append(rule)

    # 🔥 DELETED
    for rule in changes["deleted"]:
        sector = old_map.get(rule, "Unknown")
        init_sector(sector)
        sector_output[sector]["deleted"].append(rule)

    return sector_output


def detect_changes(old_rules, new_rules):
    matches, used_new = match_rules(old_rules, new_rules)

    added = []
    deleted = []
    modified = []

    used_old = set()

    for i, j, score in matches:
        old = old_rules[i]
        new = new_rules[j]

        used_old.add(i)

        if score < 0.98:
            modified.append({
                "old": old,
                "new": new,
                "similarity": score
            })

    # 🔥 ADDED RULES (very important)
    for j, rule in enumerate(new_rules):
        if j not in used_new:
            added.append(rule)

    # 🔥 DELETED RULES
    for i, rule in enumerate(old_rules):
        if i not in used_old:
            deleted.append(rule)

    return {
        "added": added,
        "deleted": deleted,
        "modified": modified
    }


if __name__ == "__main__":
    print("Processing OLD document...")
    old_data = process_document(OLD_PATH)

    print("Processing NEW document...")
    new_data = process_document(NEW_PATH)

    # 🔥 GLOBAL MATCHING
    old_rules, old_map = flatten_rules(old_data)
    new_rules, new_map = flatten_rules(new_data)

    print("\nDetecting changes...")
    changes = detect_changes(old_rules, new_rules)
    sector_changes = assign_sectorwise(changes, old_map, new_map)

    print("Analyzing changes...")
    analysis = analyze_changes(sector_changes)

    print("Performing numerical analysis...")
    numerical_results = numerical_comparison(analysis)

    print("Generating output...")
    generate_output_sectorwise(sector_changes, analysis, numerical_results)

    print("\n🚀 PIPELINE COMPLETE")