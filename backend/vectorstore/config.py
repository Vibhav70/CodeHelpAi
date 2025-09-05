import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "vectorstore/chroma_db")

# --- Embedding Model Configuration ---
# EMBEDDING_MODEL_PROVIDER = "google_genai"
EMBEDDING_MODEL_PROVIDER = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-004")

db_dir = os.path.dirname(CHROMA_DB_PATH)
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
