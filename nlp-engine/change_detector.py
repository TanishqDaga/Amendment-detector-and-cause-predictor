from sentence_transformers import SentenceTransformer, util
import re

model = SentenceTransformer('all-MiniLM-L6-v2')


def extract_numbers(text):
    return re.findall(r'\d+\.?\d*', text)


def detect_changes_sectorwise(old_data, new_data):
    result = {}

    total_added = 0
    total_deleted = 0
    total_modified = 0

    for sector in old_data.keys():
        old_rules = old_data.get(sector, [])
        new_rules = new_data.get(sector, [])

        used = set()

        modified = []
        added = []
        deleted = []

        for old in old_rules:
            best_match = None
            best_score = 0

            for i, new in enumerate(new_rules):
                if i in used:
                    continue

                score = util.cos_sim(
                    model.encode(old, convert_to_tensor=True),
                    model.encode(new, convert_to_tensor=True)
                ).item()

                if score > best_score:
                    best_score = score
                    best_match = (i, new)

            if best_score > 0.7:
                used.add(best_match[0])

                if old != best_match[1]:
                    modified.append({
                        "old": old,
                        "new": best_match[1],
                        "similarity": round(best_score, 4),
                        "old_numbers": extract_numbers(old),
                        "new_numbers": extract_numbers(best_match[1])
                    })
                    total_modified += 1
            else:
                deleted.append(old)
                total_deleted += 1

        for i, new in enumerate(new_rules):
            if i not in used:
                added.append(new)
                total_added += 1

        result[sector] = {
            "added": added,
            "deleted": deleted,
            "modified": modified
        }

    summary = {
        "total_added": total_added,
        "total_deleted": total_deleted,
        "total_modified": total_modified
    }

    return summary, result