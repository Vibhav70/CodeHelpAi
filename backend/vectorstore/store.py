import chromadb
from typing import List, Dict, Any

# Import our configuration and embedding utility
from .config import CHROMA_DB_PATH
from backend.vectorstore.embeddings import get_embedding

# Import the LangChain Document object for type hinting and consistency
from langchain_core.documents import Document

class VectorStore:
    """
    A wrapper class for managing a ChromaDB vector store for a specific project.
    """
    def __init__(self, project_id: int):
        if not project_id:
            raise ValueError("Project ID is required to initialize the VectorStore.")
            
        self.project_id = project_id
        
        # Initialize a persistent ChromaDB client that saves data to the specified path.
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        
        # Get or create a collection for the project. Collections are like tables in ChromaDB.
        # Each project gets its own isolated collection, ensuring data separation.
        self.collection_name = f"project_{self.project_id}"
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=get_embedding()
        )

    def add_documents(self, documents: List[Document], ids: List[str]):
        """
        Adds or updates (upserts) a list of documents in the ChromaDB collection.
        """
        if not documents:
            return
            
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        
        # Chroma's 'add' also handles updates if the IDs already exist, making it an upsert.
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added/updated {len(documents)} documents in collection '{self.collection_name}'.")

    def delete_summaries(self, ids_to_delete: List[str]):
        """
        Deletes summaries from the ChromaDB collection by their unique IDs.
        This is much more direct and efficient than the FAISS workaround.
        """
        if not ids_to_delete:
            return

        self.collection.delete(ids=ids_to_delete)
        print(f"Deleted {len(ids_to_delete)} documents from collection '{self.collection_name}'.")

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Searches the collection for the most similar documents to a query.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        # Format the results to match the expected output structure of our RAG pipeline
        formatted_results = []
        if results and results.get('documents'):
            for i, doc_text in enumerate(results['documents'][0]):
                formatted_results.append({
                    "text": doc_text,
                    "metadata": results['metadatas'][0][i],
                    "score": results['distances'][0][i] # Chroma returns distances, lower is better
                })
        return formatted_results
