
# For now, we'll use a fixed dimension for our mock embeddings.
# A real sentence-transformer model like 'all-MiniLM-L6-v2' produces a 384-dimensional vector.
# EMBEDDING_DIM = 384

# def get_embedding_model():
#     """
#     Placeholder function to simulate loading a real embedding model.
#     In a real implementation, this would load the model specified in the config,
#     e.g., from the sentence-transformers library.
#     """
#     print(f"--- Mock loading embedding model: {EMBEDDING_MODEL_NAME} ---")
#     # In a real scenario, this would return a model object.
#     return None

# def get_embedding(text: str, model=None) -> list[float]:
#     """
#     Generates a mock embedding for a given piece of text.

#     This function simulates the process of converting text into a dense vector
#     embedding. Currently, it returns a random, normalized vector of a fixed
#     dimension. This will be replaced with a call to a real sentence-transformer
#     model.

#     Args:
#         text: The input string to be embedded.
#         model: A placeholder for a real model object (currently unused).

#     Returns:
#         A list of floats representing the mock embedding.
#     """
#     # Generate a random vector.
#     random_vector = np.random.rand(EMBEDDING_DIM).astype(np.float32)
    
#     # Normalize the vector to have a unit length (a common practice).
#     norm = np.linalg.norm(random_vector)
#     if norm == 0:
#         return [0.0] * EMBEDDING_DIM
        
#     normalized_vector = random_vector / norm
    
#     return normalized_vector.tolist()

# # Simulate loading the model on startup.
# get_embedding_model()


from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Initialize the embedding model.
# We use "text-embedding-004" as it is a powerful and efficient model.
# This object will be used to convert text queries and documents into vectors.
embedding_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

def get_embedding(text: str) -> list[float]:
    """
    A simple wrapper to generate an embedding for a single piece of text.
    """
    return embedding_model.embed_query(text)