from similarity import match_rules


def detect_changes_sectorwise(old_data, new_data):
    final_output = {}

    for sector in old_data.keys():
        old_rules = old_data.get(sector, [])
        new_rules = new_data.get(sector, [])

        matches, used_new = match_rules(old_rules, new_rules)

        added = []
        deleted = []
        modified = []

        for i, j, score in matches:
            old = old_rules[i]
            new = new_rules[j]

            if score < 0.98:
                modified.append({
                    "old": old,
                    "new": new,
                    "similarity": score
                })

        for j, rule in enumerate(new_rules):
            if j not in used_new:
                added.append(rule)

        final_output[sector] = {
            "added": added,
            "deleted": deleted,
            "modified": modified
        }

    return final_output