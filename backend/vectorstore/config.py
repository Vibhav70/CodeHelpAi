import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists.
# This is useful for managing secrets and environment-specific settings.
load_dotenv()

# --- Vector Database Configuration ---
# This defines the local path where the FAISS vector store will be saved.
# FAISS is a library for efficient similarity search and clustering of dense
# vectors. It's a great choice for running locally.
# VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "vectorstore/db/faiss_index")


# EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")


# db_dir = os.path.dirname(VECTOR_DB_PATH)
# if not os.path.exists(db_dir):
#     os.makedirs(db_dir)

VECTOR_STORE_DIR = "vector_store_data"
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-004")
# Define the specific path for the FAISS index file
FAISS_INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "code_summaries.faiss")

# Ensure the directory exists
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)