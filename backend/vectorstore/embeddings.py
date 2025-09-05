
# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# # Initialize the embedding model.
# # We use "text-embedding-004" as it is a powerful and efficient model.
# # This object will be used to convert text queries and documents into vectors.
# embedding_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# def get_embedding(text: str) -> list[float]:
#     """
#     A simple wrapper to generate an embedding for a single piece of text.
#     """
#     return embedding_model.embed_query(text)

from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os
load_dotenv()
# You can manage your API key here or through environment variables
# from backend.config import GOOGLE_API_KEY

def get_embedding():
    """
    Returns a pre-configured embedding function object compatible with ChromaDB.

    This uses the Google Generative AI model via Chroma's own utility functions,
    which correctly handle the embedding process for the ChromaDB client.
    """
    # If you have your API key in a variable, you can pass it here.
    # Otherwise, ensure the GOOGLE_API_KEY environment variable is set.
    # api_key = GOOGLE_API_KEY
    
    google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    return google_ef