def explain_issues(issues: list):
    explanations = []

    for issue in issues:
        if "OR condition" in issue:
            explanations.append("OR conditions can allow bypassing security checks.")
        
        elif "EXISTS" in issue:
            explanations.append("Subqueries can expose unintended data access paths.")
        
        elif "Missing JWT" in issue:
            explanations.append("Without JWT identity, access is not user-restricted.")
        
        elif "Missing user_id" in issue:
            explanations.append("No ownership check means any user can access all data.")
        
        elif "TO authenticated" in issue:
            explanations.append("Policy must restrict access to authenticated users.")
        
        else:
            explanations.append(issue)

    return explanations