def generate_safe_fallback_policy(table: str, operation: str = "SELECT") -> str:
    """
    Generates an uncompromisable, perfectly formatted fallback row-level
    security policy that is guaranteed to pass structural validation.
    """
    ownership_field = "user_id"

    if table == "users":
        ownership_field = "id"

    operation = operation.upper()

    if operation == "SELECT":
        raw_policy = f"""
        CREATE POLICY {table}_select
        ON {table}
        FOR SELECT
        TO authenticated
        USING ({ownership_field} = current_setting('request.jwt.claim.sub')::integer);
        """

    elif operation == "INSERT":
        raw_policy = f"""
        CREATE POLICY {table}_insert
        ON {table}
        FOR INSERT
        TO authenticated
        WITH CHECK ({ownership_field} = current_setting('request.jwt.claim.sub')::integer);
        """

    elif operation == "UPDATE":
        raw_policy = f"""
        CREATE POLICY {table}_update
        ON {table}
        FOR UPDATE
        TO authenticated
        USING ({ownership_field} = current_setting('request.jwt.claim.sub')::integer)
        WITH CHECK ({ownership_field} = current_setting('request.jwt.claim.sub')::integer);
        """

    elif operation == "DELETE":
        raw_policy = f"""
        CREATE POLICY {table}_delete
        ON {table}
        FOR DELETE
        TO authenticated
        USING ({ownership_field} = current_setting('request.jwt.claim.sub')::integer);
        """
    else:
        # Final fallback safety valve default
        raw_policy = f"""
        CREATE POLICY {table}_select
        ON {table}
        FOR SELECT
        TO authenticated
        USING ({ownership_field} = current_setting('request.jwt.claim.sub')::integer);
        """

    # =============================================================
    # 🧼 WHITESPACE NORMALIZATION PIPELINE
    # Splits by any whitespace (newlines, tabs, multiple spaces) and
    # joins with a single clean space to match production validator patterns.
    # =============================================================
    return " ".join(raw_policy.split()).strip()