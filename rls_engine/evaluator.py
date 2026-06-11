def evaluate_policy(sql: str, table: str):
    # =========================
    # 🔥 NORMALIZATION
    # =========================
    sql_lower = sql.lower()
    normalized_sql = " ".join(sql_lower.split())

    issues = []

    # =========================
    # 🔹 STRUCTURE RULES
    # =========================
    if not normalized_sql.startswith("create policy"):
        issues.append("Not a CREATE POLICY statement")

    if f"on {table}" not in normalized_sql:
        issues.append(f"Policy not applied to correct table: {table}")

    # =========================
    # 🔹 OWNERSHIP MODEL
    # =========================
    ownership_field = "user_id"

    if ownership_field not in normalized_sql:
        issues.append("Missing user_id ownership check")

    # =========================
    # 🔹 REQUIRED SECURITY ELEMENTS
    # =========================
    if "request.jwt.claim.sub" not in normalized_sql:
        issues.append("Missing JWT identity check")

    # Detect operation type
    is_for_update = "for update" in normalized_sql
    is_for_insert = "for insert" in normalized_sql
    is_for_delete = "for delete" in normalized_sql
    is_for_select = "for select" in normalized_sql

    # =========================
    # 🔹 CLAUSE VALIDATION
    # =========================
    if is_for_insert:
        if "with check" not in normalized_sql:
            issues.append("Missing WITH CHECK for INSERT")
    elif is_for_update:
        if "using" not in normalized_sql:
            issues.append("Missing USING clause")
        if "with check" not in normalized_sql:
            issues.append("Missing WITH CHECK for UPDATE")
    else:
        if "using" not in normalized_sql:
            issues.append("Missing USING clause")
        if "with check" in normalized_sql:
            issues.append("WITH CHECK not allowed for SELECT/DELETE")

    # =========================
    # 🔹 SECURITY BLOCKS
    # =========================
    if " or " in normalized_sql:
        issues.append("Dangerous OR condition (can bypass security)")

    if "request.jwt.claim.role" in normalized_sql:
        issues.append("Role-based access not allowed")

    if "exists (" in normalized_sql or "using ( select" in normalized_sql:
        issues.append("Subqueries not allowed")

    if any(ref in normalized_sql for ref in ["users.", "tasks.", "projects."]):
        issues.append("Cross-table reference detected")

    # =========================
    # 🔹 OWNERSHIP COUNT CONTROL
    # =========================
    if is_for_update:
        if normalized_sql.count("user_id") > 2:
            issues.append("Multiple ownership conditions detected")
    else:
        if normalized_sql.count("user_id") > 1:
            issues.append("Multiple ownership conditions detected")

    # =========================
    # 🔹 ROLE RULES
    # =========================
    if " to " not in normalized_sql:
        issues.append("Missing TO authenticated")
    elif "to authenticated" not in normalized_sql:
        issues.append("Policy must use TO authenticated")

    # =========================
    # 🔥 FIXED TYPE SAFETY (UUID + INTEGER SUPPORT)
    # =========================
    if "current_setting('request.jwt.claim.sub')" in normalized_sql:
        if "::uuid" not in normalized_sql and "::integer" not in normalized_sql:
            issues.append("JWT sub must be cast (::uuid or ::integer)")

    # =========================
    # 🔹 TYPE BLOCKS
    # =========================
    if "::regclass" in normalized_sql:
        issues.append("Invalid type cast: regclass")

    # =========================
    # 🔹 DANGEROUS SQL
    # =========================
    dangerous_keywords = ["alter", "grant", "revoke", "drop", "truncate"]
    for keyword in dangerous_keywords:
        if keyword in normalized_sql:
            issues.append(f"Dangerous SQL detected: {keyword}")

    # =========================
    # 🔹 MULTI-STATEMENT BLOCK
    # =========================
    if sql.count(";") > 1:
        issues.append("Multiple SQL statements detected")

    # =========================
    # 🔥 STRICT OWNERSHIP RULE
    # =========================
    if "user_id =" not in normalized_sql:
        issues.append("Ownership must use 'user_id = ...' format")

    # =========================
    # 🔥 FINAL RESULT
    # =========================
    if len(issues) == 0:
        return {
            "status": "correct",
            "message": "Policy looks secure",
            "details": {
                "table": table,
                "ownership": "user_id",
            }
        }
    else:
        return {
            "status": "incorrect",
            "issues": list(set(issues))
        }