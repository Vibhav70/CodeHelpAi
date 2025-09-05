import json
import os
from typing import List, Dict, Any

from backend.vectorstore.store import VectorStore
from langchain_core.documents import Document

def _build_id_from_metadata(metadata: Dict[str, Any]) -> str:
    """Creates a unique and consistent ID from a document's metadata."""
    file_path = metadata.get('source', '')
    item_type = metadata.get('type', '')
    item_name = metadata.get('name', '')
    
    if item_type == 'method':
        class_name = metadata.get('class', '')
        return f"{file_path}::{class_name}::{item_name}"
    
    return f"{file_path}::{item_name}"

def format_summaries_for_ingestion(db_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Transforms raw summaries from the JSON DB into a structured list of dictionaries,
    ensuring all summaries are valid strings before processing.
    """
    formatted_docs = []

    def process_summaries(summary_dict, item_type):
        for key, summary_object in summary_dict.items():
            summary_text = summary_object.get('summary') if isinstance(summary_object, dict) else summary_object
            if not isinstance(summary_text, str) or not summary_text.strip():
                print(f"Skipping invalid or empty summary for key: {key}")
                continue
            
            try:
                parts = key.split("::")
                metadata = {}
                if item_type == 'function' and len(parts) == 2:
                    file_path, func_name = parts
                    metadata = {"source": file_path, "type": "function", "name": func_name}
                elif item_type == 'class' and len(parts) == 2:
                    file_path, class_name = parts
                    metadata = {"source": file_path, "type": "class", "name": class_name}
                elif item_type == 'method' and len(parts) == 3:
                    file_path, class_name, method_name = parts
                    metadata = {"source": file_path, "type": "method", "class": class_name, "name": method_name}
                else:
                    raise ValueError("Malformed key")
                
                formatted_docs.append({"text": summary_text, "metadata": metadata})
            except ValueError:
                print(f"Skipping malformed {item_type} key: {key}")

    process_summaries(db_data.get("functions", {}), 'function')
    process_summaries(db_data.get("classes", {}), 'class')
    process_summaries(db_data.get("methods", {}), 'method')

    return formatted_docs


def ingest_summaries_to_vector_store(project_id: int) -> int:
    """
    Ingests saved summaries for a specific project into its ChromaDB collection.
    """
    print(f"--- Starting ChromaDB ingestion for project ID: {project_id} ---")
    
    summaries_db_path = f"project_data/{project_id}/summaries_db.json"
    
    if not os.path.exists(summaries_db_path):
        print(f"Error: Summaries database not found for project {project_id}.")
        return 0

    try:
        with open(summaries_db_path, "r", encoding="utf-8") as f:
            summaries_data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading summaries database for project {project_id}: {e}.")
        return 0

    documents_to_add = format_summaries_for_ingestion(summaries_data)

    if not documents_to_add:
        print(f"No valid summaries found to ingest for project {project_id}.")
        return 0

    # Convert the formatted dictionaries into LangChain Document objects
    langchain_documents = [
        Document(page_content=doc["text"], metadata=doc["metadata"]) for doc in documents_to_add
    ]
    ids = [_build_id_from_metadata(doc.metadata) for doc in langchain_documents]

    # Instantiate the VectorStore for the specific project
    vector_store = VectorStore(project_id=project_id)
    
    # Add the documents to the project's ChromaDB collection
    vector_store.add_documents(documents=langchain_documents, ids=ids)

    print(f"--- ChromaDB ingestion complete for project {project_id}. Added/updated {len(langchain_documents)} summaries. ---")
    return len(langchain_documents)