# rls_engine/generator.py
import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def generate_rls_policy(table_name: str, schema: str, operation: str, similar_policies: list = None):
    """
    Generates a secure PostgreSQL RLS policy utilizing schema metadata 
    and RAG context containing historically verified high-performing policies.
    """
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    operation = operation.upper()

    # 1. PROCESS SEMANTIC MEMORY CONTEXT
    context_str = ""
    if similar_policies and len(similar_policies) > 0:
        formatted_policies = "\n".join([f"- {p}" for p in similar_policies])
        context_str = f"\nPREVIOUS 100% VERIFIED HIGH-ACCURACY POLICIES (Use as reference patterns):\n{formatted_policies}\n"

    # 2. ASSEMBLE ADAPTIVE EXPERT PROMPT
    system_prompt = f"""
You are a PostgreSQL RLS security expert.

TARGET DB SCHEMA CONFIGURATION:
{schema}
{context_str}
STRICT REASONING RULES:
- Output ONLY ONE CREATE POLICY statement
- MUST be FOR {operation} ONLY
- No explanation, no markdown wrap blocks, no inline comments

SECURITY COMPLIANCE DIRECTIVES:
- MUST use EXACTLY this structure to avoid empty string validation runtime crashes:
  user_id = nullif(current_setting('request.jwt.claim.sub', true), '')::uuid

- MUST include explicitly:
  TO authenticated
  {"WITH CHECK (...)" if operation in ["INSERT", "UPDATE"] else "USING (...)"}

- DO NOT ALLOW OR UTILIZE UNDER ANY CIRCUMSTANCES (VIOLATION CRASHES THE ENGINE):
  OR, EXISTS, ANY, JOIN, SELECT, subqueries, multi-table joins, TO public, current_user, ::text, ::regclass

TABLE TARGET: {table_name}

SYNTAX EXPECTATION EXAMPLE:
CREATE POLICY {table_name}_{operation.lower()} ON {table_name} FOR {operation} TO authenticated {"WITH CHECK" if operation in ["INSERT", "UPDATE"] else "USING"} (user_id = nullif(current_setting('request.jwt.claim.sub', true), '')::uuid);
"""

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "system", "content": system_prompt}],
        "temperature": 0  # Forces max determinism
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)

        if response.status_code != 200:
            return f"LLM ERROR: {response.text}"

        result = response.json()

        if "choices" not in result:
            return f"LLM ERROR: {result}"

        raw_sql = result["choices"][0]["message"]["content"].strip()

        # 3. STRUCTURAL CLEANING & NORMALIZATION
        raw_sql = raw_sql.replace("```sql", "").replace("```", "").strip()

        match = re.search(r"create policy[\s\S]*?;", raw_sql, re.IGNORECASE)
        if not match:
            return f"INVALID POLICY GENERATED: {raw_sql}"

        sql = match.group(0).strip()
        sql = " ".join(sql.split())
        sql_lower = sql.lower()

        # 4. PARSING VALIDATION RADAR
        if f"on {table_name}" not in sql_lower:
            return f"INVALID POLICY (wrong table): {sql}"

        if "request.jwt.claim.sub" not in sql_lower:
            return f"INVALID POLICY (missing JWT): {sql}"

        if "::uuid" not in sql_lower:
            return f"INVALID POLICY (must use ::uuid): {sql}"

        if operation in ["INSERT", "UPDATE"]:
            if "with check" not in sql_lower:
                return f"INVALID POLICY (missing WITH CHECK): {sql}"
        else:
            if "using" not in sql_lower:
                return f"INVALID POLICY (missing USING): {sql}"

        if "to authenticated" not in sql_lower:
            return f"INVALID POLICY (missing TO authenticated): {sql}"

        match_op = re.search(r"\bfor\s+([a-z_]+)", sql_lower)
        if not match_op:
            return f"INVALID POLICY (missing FOR clause): {sql}"

        if match_op.group(1) != operation.lower():
            return f"INVALID POLICY (wrong operation): {sql}"

        # 5. VERIFY ISOLATION BOUNDARIES (BLOCKLISTS)
        blocked = [
            " or ",
            "exists",
            "any(",
            " join ",
            "users.",
            "tasks.",
            "current_user",
            "::text",
            "::regclass",
            "to public"
        ]

        for b in blocked:
            if b in sql_lower:
                return f"INVALID POLICY (unsafe: {b.strip()}): {sql}"

        if sql.count(";") > 1:
            return f"INVALID POLICY (multiple statements): {sql}"

        return sql

    except Exception as e:
        return f"EXCEPTION: {str(e)}"