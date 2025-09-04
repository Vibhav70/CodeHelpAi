# import os
# import faiss
# import numpy as np
# from typing import List, Dict, Any

# # Import our configuration and embedding model
# from .config import FAISS_INDEX_PATH
# from .embeddings import embedding_model

# # LangChain's FAISS wrapper is convenient for this
# from langchain_community.vectorstores import FAISS
# from langchain_core.documents import Document

# class VectorStore:
#     """
#     A wrapper class for managing the FAISS vector store.
#     """
#     def __init__(self):
#         self.index_path = FAISS_INDEX_PATH
#         self.db = self._load_db()

#     def _load_db(self):
#         """Loads the FAISS index from disk if it exists, otherwise creates a new one."""
#         if os.path.exists(self.index_path):
#             print(f"Loading existing FAISS index from {self.index_path}")
#             try:
#                 return FAISS.load_local(
#                     folder_path=os.path.dirname(self.index_path),
#                     embeddings=embedding_model,
#                     index_name=os.path.basename(self.index_path).replace(".faiss", ""),
#                     allow_dangerous_deserialization=True # Required for FAISS
#                 )
#             except Exception as e:
#                 print(f"Error loading FAISS index: {e}. Creating a new one.")
#                 return self._create_empty_db()
#         else:
#             print("No FAISS index found. Creating a new one.")
#             return self._create_empty_db()
            
#     def _create_empty_db(self):
#         """Creates an empty FAISS index to start with."""
#         initial_doc = Document(page_content="initialization", metadata={"source": "init"})
#         return FAISS.from_documents([initial_doc], embedding_model)

#     def add_summaries(self, summaries: List[Dict[str, Any]]):
#         """
#         Adds a list of summaries to the vector store.
#         Each summary should be a dict with 'text' and 'metadata'.
#         """
#         if not summaries:
#             return

#         documents = [
#             Document(page_content=summary['text'], metadata=summary['metadata'])
#             for summary in summaries
#         ]
        
#         self.db.add_documents(documents)
#         self.save()

#     def delete_summaries(self, ids_to_delete: List[str]):
#         """
#         Deletes summaries from the vector store based on a list of unique IDs.
#         """
#         if not ids_to_delete or not self.db:
#             return

#         # The FAISS wrapper stores documents in a docstore with unique internal IDs.
#         # We need to find which of these internal IDs correspond to the documents we want to delete.
#         internal_ids_to_remove = []
#         for internal_id, doc in self.db.docstore._dict.items():
#             # Reconstruct the unique ID from the document's metadata
#             doc_metadata = doc.metadata
#             unique_id = ""
#             if doc_metadata.get('type') == 'method':
#                 unique_id = f"{doc_metadata.get('source')}::{doc_metadata.get('class')}::{doc_metadata.get('name')}"
#             else:
#                  unique_id = f"{doc_metadata.get('source')}::{doc_metadata.get('name')}"
            
#             if unique_id in ids_to_delete:
#                 internal_ids_to_remove.append(internal_id)

#         if not internal_ids_to_remove:
#             print("No matching documents found in vector store for deletion.")
#             return

#         # Use the LangChain FAISS wrapper's delete method
#         self.db.delete(internal_ids_to_remove)
#         self.save()
#         print(f"Deleted {len(internal_ids_to_remove)} documents from the vector store.")


#     def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
#         """
#         Searches the vector store for the most similar documents to a query.
#         """
#         if not self.db:
#             return []
        
#         results_with_scores = self.db.similarity_search_with_score(query, k=top_k)
        
#         formatted_results = []
#         for doc, score in results_with_scores:
#             formatted_results.append({
#                 "text": doc.page_content,
#                 "metadata": doc.metadata,
#                 "score": float(score)
#             })
#         return formatted_results

#     def save(self):
#         """Saves the current FAISS index to disk."""
#         if self.db:
#             self.db.save_local(
#                 folder_path=os.path.dirname(self.index_path),
#                 index_name=os.path.basename(self.index_path).replace(".faiss", "")
#             )
#             print(f"FAISS index saved to {self.index_path}")

# # Create a singleton instance to be used across the application
# vector_store = VectorStore()


import os
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore
from .embeddings import embedding_model
from .config import VECTOR_STORE_DIR

class VectorStore:
    def __init__(self, project_id: int):
        self.project_id = project_id
        # Each project gets its own directory for its vector store index
        self.index_path = os.path.join(VECTOR_STORE_DIR, str(project_id), "faiss_index")
        
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        
        self.vector_store = self._load_or_create_store()

    def _load_or_create_store(self):
        """Loads a vector store from disk or creates a new one if it doesn't exist."""
        if os.path.exists(f"{self.index_path}.faiss"):
            print(f"Loading existing vector store for project {self.project_id}...")
            return FAISS.load_local(
                folder_path=os.path.dirname(self.index_path),
                index_name=os.path.basename(self.index_path),
                embeddings=embedding_model,
                allow_dangerous_deserialization=True
            )
        else:
            print(f"Creating new vector store for project {self.project_id}...")
            # Get embedding dimension from the model
            embedding_dimension = len(embedding_model.embed_query("test"))
            # Create a new FAISS index
            index = faiss.IndexFlatL2(embedding_dimension)
            # Use LangChain's in-memory docstore
            docstore = InMemoryDocstore({})
            index_to_docstore_id = {}
            return FAISS(
                embedding_function=embedding_model,
                index=index,
                docstore=docstore,
                index_to_docstore_id=index_to_docstore_id
            )

    def save(self):
        """Saves the current state of the vector store to disk."""
        self.vector_store.save_local(
            folder_path=os.path.dirname(self.index_path),
            index_name=os.path.basename(self.index_path)
        )
    
    def delete_by_ids(self, ids_to_delete: list[str]):
        """Deletes documents from the vector store by their unique IDs."""
        if not ids_to_delete:
            return
        # LangChain's FAISS wrapper can delete by a list of its internal docstore IDs
        self.vector_store.delete(ids_to_delete)
        self.save()

    def add_documents(self, docs: list, metadatas: list, ids: list[str]):
        """Adds new documents to the vector store with specified unique IDs."""
        if not docs:
            return
        self.vector_store.add_texts(texts=docs, metadatas=metadatas, ids=ids)
        self.save()

    def search(self, query: str, top_k: int = 5):
        """Performs a similarity search in the vector store."""
        return self.vector_store.similarity_search(query, k=top_k)

