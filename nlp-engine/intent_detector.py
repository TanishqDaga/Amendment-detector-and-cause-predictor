def detect_intent(old, new):
    text = (old + " " + new).lower()

    if "attendance" in text:
        return "attendance"

    if "fee" in text or "₹" in text:
        return "finance"

    if "registration" in text:
        return "registration"

    if "evaluation" in text or "cat" in text or "fat" in text:
        return "evaluation"

    if "discipline" in text or "misconduct" in text:
        return "discipline"

    if "internship" in text:
        return "internship"

    return "general"