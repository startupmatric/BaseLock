def execute_query(cur, sql: str):
    cur.execute(sql)
    rows = cur.fetchall()

    columns = [desc[0] for desc in cur.description]

    result = []
    for row in rows:
        result.append(dict(zip(columns, row)))

    return result