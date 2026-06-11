def calculate_risk(issues: list):
    if not issues:
        return {"risk": "LOW", "score": 0}

    score = 0

    for issue in issues:
        if "OR condition" in issue:
            score += 5
        elif "EXISTS" in issue:
            score += 5
        elif "Missing JWT" in issue:
            score += 4
        elif "Missing user_id" in issue:
            score += 4
        elif "Missing USING" in issue:
            score += 3
        elif "Missing TO authenticated" in issue:
            score += 3
        else:
            score += 1

    if score >= 8:
        level = "HIGH"
    elif score >= 4:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk": level,
        "score": score,
        "issues": issues
    }