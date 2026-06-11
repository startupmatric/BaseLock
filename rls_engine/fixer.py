import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def extract_create_policy(sql: str):
    """
    Extract ONLY the first CREATE POLICY statement
    """
    pattern = re.compile(r"(create policy.*?;)", re.IGNORECASE | re.DOTALL)
    match = pattern.search(sql)

    if match:
        return match.group(1).strip()

    return None


def fix_policy(original_sql: str, issues: list, table: str, schema: str):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # 🔥 STRICT PROMPT
    system_prompt = f"""
You are a PostgreSQL RLS policy generator.

STRICT RULES (MUST FOLLOW):

- Output ONLY ONE SQL statement
- Output ONLY CREATE POLICY
- NO explanations
- NO markdown
- NO comments
- NO extra text

SECURITY RULES:

- Must use user_id (NOT id)
- Must use current_setting('request.jwt.claim.sub')::integer
- MUST use TO authenticated (NOT public, NOT current_user)
- NO OR conditions
- NO EXISTS
- NO GRANT / ALTER / privileges
- NO ::regclass
- Must include USING clause
- Must include WITH CHECK for write operations

Table: {table}

Schema:
{schema}

Fix this policy:
{original_sql}

Issues:
{issues}

Return ONLY the corrected SQL.
"""

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt}
        ],
        "temperature": 0
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)

        if response.status_code != 200:
            return f"FIX ERROR: {response.text}"

        result = response.json()

        if "choices" not in result:
            return f"FIX ERROR: {result}"

        raw_output = result["choices"][0]["message"]["content"].strip()

        # =========================
        # 🔥 STEP 1: REMOVE MARKDOWN
        # =========================
        cleaned = raw_output.replace("```sql", "").replace("```", "").strip()

        # =========================
        # 🔥 STEP 2: EXTRACT SQL
        # =========================
        sql = extract_create_policy(cleaned)

        if not sql:
            return "FIX ERROR: Could not extract CREATE POLICY"

        # =========================
        # 🔥 STEP 3: NORMALIZE
        # =========================
        sql = " ".join(sql.split())

        lower_sql = sql.lower()

        # =========================
        # 🔥 STEP 4: HARD SAFETY FIXES
        # =========================

        # Fix PUBLIC / current_user
        if "to public" in lower_sql or "to current_user" in lower_sql:
            sql = re.sub(r"to\s+(public|current_user)", "TO authenticated", sql, flags=re.IGNORECASE)

        # Fix regclass
        if "::regclass" in sql:
            sql = sql.replace("::regclass", "::integer")

        # =========================
        # 🔥 STEP 5: BLOCK DANGEROUS SQL
        # =========================
        unsafe_keywords = ["grant", "alter", "drop", "truncate", "revoke"]

        for keyword in unsafe_keywords:
            if keyword in lower_sql:
                return f"FIX ERROR: Unsafe keyword detected ({keyword})"

        # =========================
        # 🔥 STEP 6: ENSURE SEMICOLON
        # =========================
        if not sql.endswith(";"):
            sql += ";"

        # =========================
        # 🔥 STEP 7: FINAL STRUCTURE CHECK
        # =========================
        if not sql.lower().startswith("create policy"):
            return "FIX ERROR: Invalid SQL structure"

        return sql

    except Exception as e:
        return f"FIX EXCEPTION: {str(e)}"