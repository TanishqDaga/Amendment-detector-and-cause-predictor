from extractor import extract_text
from cleaner import clean_text
from segmenter import segment_rules
from classifier import classify_rules

from change_detector import detect_changes_sectorwise
from analyzer import analyze_changes
from numerical_analyzer import numerical_comparison
from output_generator import generate_output_sectorwise


OLD_PATH = "../sample-docs/old.pdf"
NEW_PATH = "../sample-docs/new.pdf"


def process_document(path):
    text = extract_text(path)
    text = clean_text(text)
    rules = segment_rules(text)
    categorized = classify_rules(rules)

    return categorized


if __name__ == "__main__":
    print("Processing OLD document...")
    old_data = process_document(OLD_PATH)

    print("Processing NEW document...")
    new_data = process_document(NEW_PATH)

    print("\nDetecting changes...")
    changes = detect_changes_sectorwise(old_data, new_data)
    print("Analyzing changes...")
    analysis = analyze_changes(changes)

    print("Performing numerical analysis...")
    numerical_results = numerical_comparison(analysis)

    print("Generating output...")
    generate_output_sectorwise(changes, analysis, numerical_results)

    print("\n🚀 PIPELINE COMPLETE")