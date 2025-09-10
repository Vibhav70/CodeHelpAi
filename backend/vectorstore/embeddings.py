# from chromadb.utils import embedding_functions
# from dotenv import load_dotenv
# import os
# load_dotenv()
# # You can manage your API key here or through environment variables
# # from backend.config import GOOGLE_API_KEY

# def get_embedding():
#     """
#     Returns a pre-configured embedding function object compatible with ChromaDB.

#     This uses the Google Generative AI model via Chroma's own utility functions,
#     which correctly handle the embedding process for the ChromaDB client.
#     """
#     # If you have your API key in a variable, you can pass it here.
#     # Otherwise, ensure the GOOGLE_API_KEY environment variable is set.
#     # api_key = GOOGLE_API_KEY
    
#     google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
#         api_key=os.getenv("GOOGLE_API_KEY")
#     )
#     return google_ef
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb
from chromadb.utils import embedding_functions

# --- Configuration ---
# We specify the name of the local model we want to use from the Hugging Face hub.
# "all-MiniLM-L6-v2" is a very popular and high-performing model that runs locally.
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def get_embedding():
    """
    Initializes and returns a SentenceTransformer embedding function.
    This function handles the model loading and provides error handling.
    """
    print(f"--- Initializing local embedding model: {EMBEDDING_MODEL_NAME} ---")
    try:
        # Create an instance of the embedding function using the specified model.
        # This will download the model on the first run if it's not cached.
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL_NAME
        )
        print("--- Local embedding model loaded successfully. ---")
        return embedding_function
    except Exception as e:
        # If the model fails to load, print a critical error and return None.
        print(f"CRITICAL: Failed to load local embedding model. Please ensure 'sentence-transformers' and 'torch' are installed. Error: {e}")
        return None
