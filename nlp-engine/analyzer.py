import re
from cause_predictor import predict_cause


def extract_numbers(text):
    return re.findall(r'\d+\.?\d*', text)


def analyze_changes(changes):
    final_analysis = {}

    for sector, data in changes.items():
        sector_analysis = []

        for item in data["modified"]:
            old = item["old"]
            new = item["new"]

            old_words = set(old.lower().split())
            new_words = set(new.lower().split())

            added_words = new_words - old_words
            removed_words = old_words - new_words

            old_nums = extract_numbers(old)
            new_nums = extract_numbers(new)

            cause = predict_cause(old, new)

            sector_analysis.append({
                "old_rule": old,
                "new_rule": new,
                "added_keywords": list(added_words),
                "removed_keywords": list(removed_words),
                "old_numbers": old_nums,
                "new_numbers": new_nums,
                "predicted_cause": cause
            })

        final_analysis[sector] = sector_analysis

    return final_analysis