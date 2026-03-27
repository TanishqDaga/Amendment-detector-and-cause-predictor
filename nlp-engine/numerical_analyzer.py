def numerical_comparison(analysis):
    results = {}

    for sector, items in analysis.items():
        sector_results = []

        for item in items:
            if item["old_numbers"] != item["new_numbers"]:
                sector_results.append(item)

        results[sector] = sector_results

    return results