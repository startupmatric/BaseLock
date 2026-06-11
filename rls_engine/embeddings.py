# rls_engine/embeddings.py
from sentence_transformers import SentenceTransformer

# Load a production-grade 384-dimensional dense vector model locally
# (Automated download on first launch; completely free)
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str) -> list[float]:
    """
    Generates a 384-dimensional dense vector embedding locally 
    without hitting any external rate-limited web endpoints.
    """
    if not text or not text.strip():
        raise ValueError("Cannot generate embedding for empty or whitespace text.")
        
    try:
        # Normalize code formatting structures
        clean_text = text.replace("\n", " ").strip()
        embedding_vector = model.encode(clean_text)
        
        # Convert the raw numpy array directly to a standard python float list
        return embedding_vector.tolist()
    except Exception as e:
        print(f"[LOCAL EMBEDDING INCIDENT]: Vector pipeline failed: {e}")
        raise e