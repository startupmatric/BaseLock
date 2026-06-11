def simulate_attack_cases():
    return [
        "CREATE POLICY p ON projects USING (true);",
        "CREATE POLICY p ON projects USING (user_id = 1 OR true);",
        "CREATE POLICY p ON projects USING (EXISTS (SELECT 1));",
        "DROP TABLE users;",
        "CREATE POLICY p ON projects USING (user_id = current_user);",
        "CREATE POLICY p ON projects USING (user_id::text = '1');",
    ]