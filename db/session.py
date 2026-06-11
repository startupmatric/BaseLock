import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_user_connection(user_id: str):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    # 🔥 CRITICAL LINE (your entire system depends on this)
    cur.execute(
        "select set_config('request.jwt.claim.sub', %s, true);",
        (user_id,)
    )

    return conn, cur