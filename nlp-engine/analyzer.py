from cause_predictor import predict_cause


def analyze_changes(changes):
    for sector in changes:
        for item in changes[sector]["modified"]:
            old = item["old"]
            new = item["new"]

            item["predicted_cause"] = predict_cause(old, new)

    return changes