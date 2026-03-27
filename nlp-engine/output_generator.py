import json


def generate_output_sectorwise(changes, analysis, numerical_results):
    summary = {
        "total_added": 0,
        "total_deleted": 0,
        "total_modified": 0
    }

    for sector, data in changes.items():
        summary["total_added"] += len(data["added"])
        summary["total_deleted"] += len(data["deleted"])
        summary["total_modified"] += len(data["modified"])

    output = {
        "summary": summary,
        "sector_wise_changes": changes,
        "analysis": analysis,
        "numerical_changes": numerical_results
    }

    with open("final_output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print("✅ Final structured output saved")