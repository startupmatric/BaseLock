# rls_engine/store.py
from rls_engine.embeddings import generate_embedding

def store_policy_embedding(cur, table: str, operation: str, sql: str, eval_accuracy: float):
    """
    Saves a generated policy along with its validation score.
    Only policies crossing a strict quality threshold are flagged as verified memory.
    """
    embedding = generate_embedding(sql)
    is_verified = (eval_accuracy >= 100.0)

    cur.execute("""
        INSERT INTO rls_embeddings 
        (table_name, operation, policy_sql, embedding, eval_accuracy, is_verified)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
    """, (table, operation.upper(), sql, embedding, eval_accuracy, is_verified))