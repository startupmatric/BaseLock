# main.py
import os
import time
import re
from fastapi import FastAPI, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# 1. CRITICAL CONTEXT ORDERING: Load environment configurations before dependent initialization layers
load_dotenv()

# 2. APPLICATION BLOCK ASSEMBLY: Instantiate FastAPI immediately after environment preparation
app = FastAPI(title="BaseLock AI Infrastructure Platform v2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional Fallbacks for Adversarial Modules
try:
    from rls_engine.attacker import simulate_attack_cases
except ImportError:
    def simulate_attack_cases():
        return [
            "CREATE POLICY p ON projects USING (true);",
            "CREATE POLICY p ON projects USING (user_id = 1 OR true);",
            "CREATE POLICY p ON projects USING (EXISTS (SELECT 1));",
            "DROP TABLE users;",
            "CREATE POLICY p ON projects USING (user_id::text = '1');"
        ]

from identity.service import get_user_context
from db.session import get_user_connection
from rls_engine.evaluator import evaluate_policy
from rls_engine.apply import apply_policy
from rls_engine.schema import get_schema
from rls_engine.generator import generate_rls_policy
from rls_engine.retriever import retrieve_similar_policies
from rls_engine.store import store_policy_embedding

# ======================================================================
# 🔐 PLATFORM LOGIC & SECURITY INTERCEPTORS (FIREWALL V2)
# ======================================================================
def enforce_strict_rules(sql: str):
    """
    Advanced Policy Firewall: Replaces crude string blocking with 
    pattern-intent inspection. Allows safe database subqueries while 
    intercepting structural injection and escalation attacks.
    """
    sql_upper = sql.upper()
    sql_lower = sql.lower()
    
    # 1. Catch Logical Disjunction Exploits (OR-Bypass)
    if " OR " in sql_upper or re.search(r"\b(or)\b\s+true", sql_lower) or re.search(r"=\s*.*or\b", sql_lower):
        raise ValueError("Security Violation: Intercepted OR-disjunction logic. Potential global access bypass risk.")
        
    # 2. Control Subquery Scope (Allow safe EXISTS, block complex exploitation vectors)
    if "exists" in sql_lower:
        if " join " in sql_lower or "from (" in sql_lower:
            raise ValueError("Security Violation: Complex join topologies or nested inline views are restricted.")
            
    # 3. Intercept Data Defacement Tactics
    if "drop " in sql_lower or "truncate " in sql_lower or "alter " in sql_lower:
        raise ValueError("Security Violation: Destructive DDL statements intercepted within policy predicate.")

    # 4. Block Global Role Escalation Boundaries
    if "true" in sql_lower and not re.search(r"['\"].*true.*['\"]", sql_lower):
        if re.search(r"\btrue\b", sql_lower):
            raise ValueError("Security Violation: Always-True policy shortcut detected.")
            
    if "to public" in sql_lower:
        raise ValueError("Security Violation: Public role linkage forbidden. Policy must explicitly isolate to authenticated.")
        
    if "current_user" in sql_lower:
        raise ValueError("Security Violation: 'current_user' evaluation context detected. Use request claims parameters instead.")
        
    return True

def calculate_confidence_score(sql: str, eval_accuracy: float) -> float:
    """Confidence scoring tailored to look for secure UUID matching constraints."""
    score = 0
    sql_lower = sql.lower()
    if "nullif" in sql_lower: score += 20
    if "authenticated" in sql_lower: score += 20
    if "user_id" in sql_lower: score += 30
    if eval_accuracy >= 100.0: score += 30
    return float(score)

def rank_policy(accuracy: float, confidence: float, latency_ms: float) -> float:
    """Computes a weighted scalar metric optimization index representing overall system grade."""
    normalized_latency_penalty = min(latency_ms * 0.1, 10.0)
    score = (accuracy * 0.6) + (confidence * 0.3) - normalized_latency_penalty
    return round(max(0.0, min(100.0, score)), 2)

def get_safe_template(table: str, operation: str) -> str:
    """Fallback template written to deploy secure UUID context checks via request.jwt.claim.sub."""
    operation = operation.upper()
    base = "user_id = nullif(current_setting('request.jwt.claim.sub', true), '')::uuid"
    if operation == "SELECT":
        return f"CREATE POLICY {table}_select ON {table} FOR SELECT TO authenticated USING ({base});"
    if operation == "INSERT":
        return f"CREATE POLICY {table}_insert ON {table} FOR INSERT TO authenticated WITH CHECK ({base});"
    if operation == "UPDATE":
        return f"CREATE POLICY {table}_update ON {table} FOR UPDATE TO authenticated USING ({base}) WITH CHECK ({base});"
    return f"CREATE POLICY {table}_delete ON {table} FOR DELETE TO authenticated USING ({base});"

# ======================================================================
# 🔄 SERVICE CONTROLLERS & CONTROLLER ROUTING
# ======================================================================
@app.post("/generate-rls")
def generate_rls(table: str, operation: str = "SELECT", authorization: str = Header(...)):
    start_time = time.time()
    token = authorization.replace("Bearer ", "").strip()
    context = get_user_context(token)

    if not context:
        return {"error": "Invalid token mapping authorization block context."}

    operation = operation.upper()
    schema = get_schema()
    similar_policies = []

    # 1. RAG Core Pull
    try:
        conn_r, cur_r = get_user_connection(context.user_id)
        conn_r.rollback()
        similar_policies = retrieve_similar_policies(
            cur_r, table, operation, f"Secure UUID token validation context filtering for {table} {operation}"
        )
        cur_r.close()
        conn_r.close()
    except Exception as e:
        print("[RAG EXTRACTION EXCEPTION]:", e)

    # 2. Generative Compilation
    try:
        sql = generate_rls_policy(table, schema, operation, similar_policies=similar_policies)
        if evaluate_policy(sql, table)["status"] != "correct":
            sql = None
    except:
        sql = None

    if not sql:
        sql = get_safe_template(table, operation)

    # 3. Static Code Hardening Gate
    try:
        enforce_strict_rules(sql)
    except ValueError as val_error:
        return {"error": "Strict Rules Interception Violation", "details": str(val_error)}

    final_eval = evaluate_policy(sql, table)
    if final_eval["status"] != "correct":
        return {"error": "Syntax validation halted.", "issues": final_eval["issues"]}

    # 4. Transaction Emit With Timeout Safety Boundaries
    conn, cur = get_user_connection(context.user_id)
    try:
        conn.rollback()
        cur.execute("SET statement_timeout = 3000;")
        cur.execute(f"DROP POLICY IF EXISTS {table}_{operation.lower()} ON {table};")
        apply_policy(cur, sql)
        conn.commit()
    except Exception as db_err:
        conn.rollback()
        return {"error": "Transactional execution error", "details": str(db_err)}
    finally:
        cur.close()
        conn.close()

    # 5. Optimization Scoring Computations
    eval_result = run_auto_eval(context.user_id, table, operation, sql)
    accuracy = eval_result.get("accuracy", 0.0)
    confidence = calculate_confidence_score(sql, accuracy)
    latency_ms = round((time.time() - start_time) * 1000, 2)
    rank_score = rank_policy(accuracy, confidence, latency_ms)

    # 6. High-Accuracy Continuous Versioning Registry Ingestion
    if accuracy >= 90.0:
        try:
            conn2, cur2 = get_user_connection(context.user_id)
            conn2.rollback()
            
            cur2.execute("""
                SELECT COALESCE(MAX(version), 0) FROM rls_policy_versions 
                WHERE table_name=%s AND operation=%s
            """, (table, operation))
            next_version = cur2.fetchone()[0] + 1

            cur2.execute("""
                INSERT INTO rls_policy_versions 
                (table_name, operation, policy_sql, version, created_by, confidence_score, accuracy_score, latency_ms)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (table, operation, sql, next_version, getattr(context, "email", "system"), confidence, accuracy, latency_ms))
            conn2.commit()
        except Exception as e:
            print("[VERSION STORAGE EXCEPTION]:", e)
        finally:
            cur2.close()
            conn2.close()

    # 7. Reinforcement Vector Loop Database Store
    try:
        conn3, cur3 = get_user_connection(context.user_id)
        conn3.rollback()
        store_policy_embedding(cur3, table, operation, sql, accuracy)
        conn3.commit()
    except Exception as e:
        print("[LEARNING MATRIX LOG INCIDENT]:", e)
    finally:
        cur3.close()
        conn3.close()

    return {
        "status": "success",
        "sql": sql,
        "metrics": {
            "accuracy": accuracy,
            "confidence_score": confidence,
            "latency_ms": latency_ms,
            "rank_score": rank_score
        },
        "eval": eval_result
    }

def run_auto_eval(user_id, table, operation, sql):
    conn, cur = get_user_connection(user_id)
    try:
        conn.rollback()
        cur.execute("SELECT name, test_query, expected_result FROM rls_eval_cases")
        cases = cur.fetchall()
        
        # FIXED OPTION A ALIGNMENT: Seeding matching structural UUID format definitions
        OWNER_ID = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
        STRANGER_ID = "b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22"
        
        results = []
        passed = 0
        
        for name, query, expected in cases:
            # Multi-user sandbox contextual trace loops swap directly via request.jwt.claim.sub
            jwt_sub = OWNER_ID if "own" in name.lower() else STRANGER_ID
            actual = "blocked"
            try:
                cur.execute("SAVEPOINT rls_eval;")
                cur.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;")
                cur.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY;")
                cur.execute(f"DROP POLICY IF EXISTS {table}_{operation.lower()} ON {table};")
                cur.execute(sql)
                cur.execute(f"GRANT SELECT, INSERT, UPDATE, DELETE ON {table} TO authenticated;")
                cur.execute("RESET ROLE; SET LOCAL ROLE authenticated;")
                cur.execute("SET LOCAL request.jwt.claim.sub = %s;", (jwt_sub,))
                
                cur.execute(query)
                actual = "allowed" if cur.fetchall() else "blocked"
                cur.execute("RELEASE SAVEPOINT rls_eval;")
            except:
                cur.execute("ROLLBACK TO SAVEPOINT rls_eval;")
                actual = "blocked"
                
            if actual == expected:
                passed += 1
            results.append({"name": name, "expected": expected, "actual": actual, "passed": actual == expected})
            
        total = len(results)
        return {
            "total": total, "passed": passed, "failed": total - passed,
            "accuracy": round((passed / total) * 100, 2) if total else 0.0, "results": results
        }
    finally:
        cur.close()
        conn.close()

@app.get("/policy-analytics")
def get_analytics(table: str, operation: str, authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "").strip()
    context = get_user_context(token)
    
    if not context:
        return {"error": "Invalid auth token context parameter structure."}
        
    conn, cur = get_user_connection(context.user_id)
    try:
        conn.rollback()
        cur.execute("""
            SELECT version, accuracy_score, confidence_score, latency_ms, policy_sql, created_at
            FROM rls_policy_versions
            WHERE table_name=%s AND operation=%s
            ORDER BY version ASC
        """, (table, operation.upper()))
        rows = cur.fetchall()
        return {
            "timeline": [
                {
                    "version": r[0], "accuracy": float(r[1]), "confidence": float(r[2]),
                    "latency": float(r[3]), "sql": r[4], "timestamp": r[5].isoformat()
                } for r in rows
            ]
        }
    finally:
        cur.close()
        conn.close()

@app.get("/attack-test")
def attack_test():
    return simulate_attack_cases()

@app.get("/", response_class=FileResponse)
def serve_dashboard():
    return FileResponse(os.path.join("templates", "dashboard.html"))