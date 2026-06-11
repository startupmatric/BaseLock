def is_safe_query(sql: str):
    sql = sql.lower()

    forbidden = ["delete", "update", "drop", "insert", "alter"]

    for word in forbidden:
        if word in sql:
            return False

    if not sql.strip().startswith("select"):
        return False

    return True