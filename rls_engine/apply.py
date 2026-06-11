def apply_policy(cur, sql: str):
    try:
        cur.execute(sql)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}