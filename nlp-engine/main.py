import json
from extractor import extract_text
from cleaner import clean_text
from segmenter import segment_rules
from classifier import classify_rules
from change_detector import detect_changes_sectorwise
from analyzer import analyze_changes

OLD_PATH = "../sample-docs/old.pdf"
NEW_PATH = "../sample-docs/new.pdf"


def process_document(path):
    text = extract_text(path)
    text = clean_text(text)
    rules = segment_rules(text)
    classified = classify_rules(rules)
    return classified


if __name__ == "__main__":
    print("Processing OLD document...")
    old_data = process_document(OLD_PATH)

    print("Processing NEW document...")
    new_data = process_document(NEW_PATH)

    print("Detecting changes...")
    summary, changes = detect_changes_sectorwise(old_data, new_data)

    print("Analyzing causes...")
    changes = analyze_changes(changes)

    final_output = {
        "summary": summary,
        "sector_wise_changes": changes
    }

    with open("final_output.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)

    print("\n✅ FINAL OUTPUT GENERATED")