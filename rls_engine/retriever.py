# rls_engine/retriever.py
from rls_engine.embeddings import generate_embedding

def retrieve_similar_policies(cur, table: str, operation: str, query_text: str, limit: int = 3):
    """
    Retrieves the most semantically relevant, 100% verified previous 
    policies to use as few-shot exemplars inside the generator prompt.
    """
    query_embedding = generate_embedding(query_text)

    # Explicitly cast %s parameter payload directly to ::vector
    cur.execute("""
        SELECT policy_sql
        FROM rls_embeddings
        WHERE table_name = %s 
          AND operation = %s 
          AND is_verified = TRUE
        ORDER BY embedding <=> %s::vector ASC
        LIMIT %s;
    """, (table, operation.upper(), query_embedding, limit))

    return [r[0] for r in cur.fetchall()]