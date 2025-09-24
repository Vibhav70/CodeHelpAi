from typing import Dict, List, Any

# Import the necessary components
from backend.vectorstore.store import VectorStore
from backend.nodes.change_detection_node import GraphState, ChangedItem
from langchain_core.documents import Document

def _get_doc_id_from_change(change: ChangedItem) -> str:
    """Creates a unique, consistent ID for a document from a ChangedItem."""
    if change.item_type == 'method' and change.class_name:
        return f"{change.file_path}::{change.class_name}::{change.item_name}"
    return f"{change.file_path}::{change.item_name}"

def _get_doc_id_from_summary(summary: Dict[str, Any]) -> str:
    """Creates a unique, consistent ID for a document from a summary dictionary."""
    file_path = summary.get('file_path', '')
    
    if 'method_name' in summary:
        class_name = summary.get('class_name', '')
        method_name = summary.get('method_name', '')
        return f"{file_path}::{class_name}::{method_name}"
    elif 'class_name' in summary:
        class_name = summary.get('class_name', '')
        return f"{file_path}::{class_name}"
    elif 'function_name' in summary:
        func_name = summary.get('function_name', '')
        return f"{file_path}::{func_name}"
    return ""


async def vector_ingest_node(state: GraphState) -> Dict:
    """
    An incremental LangGraph node that correctly handles source code and updates
    the project-specific vector store based on detected changes.
    """
    print("--- Incremental Vector Ingestion Node Triggered ---")
    project_id = state.get("project_id")
    changes = state.get("changes", [])
    new_summaries = state.get("summaries", [])

    if not project_id:
        print("Error: project_id not found in state.")
        return {**state, "ingestion_status": "error", "error_message": "Project ID missing."}

    vector_store = VectorStore(project_id=project_id)

    if not changes and not new_summaries:
        print("No changes or summaries to process. Skipping vector store update.")
        return {**state, "ingestion_status": "skipped"}

    try:
        # --- Step 1: Prepare documents to add/update from the new summaries ---
        docs_to_add = []
        ids_to_add = []
        for summary_item in new_summaries:
            # Use Pydantic V2's model_dump() for robust serialization
            summary_dict = summary_item.model_dump()
            
            summary_text = summary_dict.get('summary', '')
            source_code = summary_dict.get('source_code', '') # <-- Source code is extracted here
            
            metadata = {}
            doc_id = _get_doc_id_from_summary(summary_dict)

            if 'method_name' in summary_dict:
                metadata = {"source": summary_dict['file_path'], "type": "method", "class": summary_dict['class_name'], "name": summary_dict['method_name'], "source_code": source_code}
            elif 'function_name' in summary_dict:
                metadata = {"source": summary_dict['file_path'], "type": "function", "name": summary_dict['function_name'], "source_code": source_code}
            elif 'class_name' in summary_dict:
                metadata = {"source": summary_dict['file_path'], "type": "class", "name": summary_dict['class_name'], "source_code": source_code}

            if doc_id and metadata:
                # Create LangChain Document objects as expected by the store
                docs_to_add.append(Document(page_content=summary_text, metadata=metadata))
                ids_to_add.append(doc_id)

        # --- Step 2: Prepare list of IDs for all documents to be deleted ---
        ids_from_removed = [_get_doc_id_from_change(c) for c in changes if c.change_type == 'removed']
        
        # We also need to delete the old versions of modified items
        ids_from_modified = [_get_doc_id_from_change(c) for c in changes if c.change_type == 'modified']
        
        unique_ids_to_delete = list(set(ids_from_removed + ids_from_modified))
        
        # --- Step 3: Execute DB operations ---
        if unique_ids_to_delete:
            print(f"Deleting {len(unique_ids_to_delete)} old/removed summaries from vector store.")
            vector_store.delete_summaries(unique_ids_to_delete)
        
        if docs_to_add:
            print(f"Adding/updating {len(docs_to_add)} summaries in vector store.")
            vector_store.add_documents(documents=docs_to_add, ids=ids_to_add)
        
        print("--- Vector Ingestion Node Completed Successfully ---")
        return {**state, "ingestion_status": "success"}

    except Exception as e:
        error_message = f"An error occurred during vector store ingestion: {e}"
        print(error_message)
        return {**state, "ingestion_status": "error", "error_message": str(e)}

