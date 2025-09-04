
# from typing import Dict, List, Any

# # Import the main vector_store instance and graph state definitions
# from backend.vectorstore.store import VectorStore
# from backend.nodes.change_detection_node import GraphState, ChangedItem
# from backend.summarizer.models import FunctionSummary, ClassSummary, MethodSummary

# def _get_doc_id(change: ChangedItem) -> str:
#     """Creates a unique, consistent ID for a document based on its metadata."""
#     if change.item_type == 'method':
#         # This requires a lookup to get the class name, which adds complexity.
#         # For a robust implementation, the class name should be part of the ChangedItem.
#         # For now, we'll assume a simpler key for deletion.
#         return f"{change.file_path}::{change.item_name}" # Simplified for now
#     return f"{change.file_path}::{change.item_name}"

# async def vector_ingest_node(state: GraphState) -> Dict:
#     """
#     An incremental LangGraph node that updates the vector store based on
#     detected changes. It adds new summaries, updates modified ones, and
#     removes deleted ones.
#     """
#     print("--- Incremental Vector Ingestion Node Triggered ---")
#     changes = state.get("changes", [])
#     new_summaries = state.get("summaries", [])

#     if not changes and not new_summaries:
#         print("No changes or summaries to process. Skipping vector store update.")
#         return {**state, "ingestion_status": "skipped"}

#     try:
#         # --- Step 1: Identify documents to delete ---
#         ids_to_delete = [_get_doc_id(c) for c in changes if c.change_type == 'removed']
#         if ids_to_delete:
#             print(f"Deleting {len(ids_to_delete)} summaries from vector store.")
#             # We assume a delete method exists on our vector store
#             VectorStore.delete_summaries(ids_to_delete)

#         # --- Step 2: Identify documents to add or update ---
#         docs_to_add_or_update = []
#         for summary_item in new_summaries:
#             # Convert Pydantic model to dict if needed
#             summary_dict = summary_item.dict() if hasattr(summary_item, 'dict') else summary_item
            
#             doc_id, text, metadata = None, None, {}
            
#             if 'method_name' in summary_dict:
#                 metadata = {"source": summary_dict['file_path'], "type": "method", "class": summary_dict['class_name'], "name": summary_dict['method_name']}
#                 doc_id = f"{summary_dict['file_path']}::{summary_dict['class_name']}::{summary_dict['method_name']}"
#             elif 'function_name' in summary_dict:
#                 metadata = {"source": summary_dict['file_path'], "type": "function", "name": summary_dict['function_name']}
#                 doc_id = f"{summary_dict['file_path']}::{summary_dict['function_name']}"
#             elif 'class_name' in summary_dict:
#                 metadata = {"source": summary_dict['file_path'], "type": "class", "name": summary_dict['class_name']}
#                 doc_id = f"{summary_dict['file_path']}::{summary_dict['class_name']}"

#             if doc_id:
#                 # For modified items, we first delete the old version
#                 ids_to_delete.append(doc_id)
#                 docs_to_add_or_update.append({"text": summary_dict['summary'], "metadata": metadata})

#         # Ensure we delete old versions of modified files before adding new ones
#         unique_ids_to_delete = list(set(ids_to_delete))
#         if unique_ids_to_delete:
#             print(f"Deleting {len(unique_ids_to_delete)} old/removed summaries before update.")
#             VectorStore.delete_summaries(unique_ids_to_delete)
        
#         if docs_to_add_or_update:
#             print(f"Adding/updating {len(docs_to_add_or_update)} summaries in vector store.")
#             VectorStore.add_summaries(docs_to_add_or_update)
        
#         print("--- Vector Ingestion Node Completed Successfully ---")
#         return {**state, "ingestion_status": "success"}

#     except Exception as e:
#         error_message = f"An error occurred during vector store ingestion: {e}"
#         print(error_message)
#         return {**state, "ingestion_status": "error", "error_message": str(e)}

from typing import Dict, List, Any

# Import the VectorStore class (not an instance)
from backend.vectorstore.store import VectorStore
# Import the graph state and data models from our updated change detection node
from backend.nodes.change_detection_node import GraphState, ChangedItem
from backend.summarizer.models import FunctionSummary, ClassSummary, MethodSummary

def _get_doc_id(change: ChangedItem) -> str:
    """Creates a unique, consistent ID for a document based on its metadata."""
    # Use the class_name from the ChangedItem for methods to ensure consistency.
    if change.item_type == 'method' and change.class_name:
        return f"{change.file_path}::{change.class_name}::{change.item_name}"
    # Fallback for functions, classes, or if class_name is somehow missing
    return f"{change.file_path}::{change.item_name}"

async def vector_ingest_node(state: GraphState) -> Dict:
    """
    An incremental LangGraph node that updates the vector store based on
    detected changes for a specific project.
    """
    print("--- Incremental Vector Ingestion Node Triggered ---")
    project_id = state.get("project_id")
    changes = state.get("changes", [])
    new_summaries = state.get("summaries", [])

    if not project_id:
        print("Error: project_id not found in state. Skipping vector store update.")
        return {**state, "ingestion_status": "error", "error_message": "Project ID missing."}

    # Instantiate the VectorStore for the specific project
    vector_store = VectorStore(project_id=project_id)

    if not changes and not new_summaries:
        print("No changes or summaries to process. Skipping vector store update.")
        return {**state, "ingestion_status": "skipped"}

    try:
        # --- Step 1: Prepare documents to add/update from new summaries ---
        docs_to_add = []
        ids_of_modified_items = []
        for summary_item in new_summaries:
            summary_dict = summary_item.dict() if hasattr(summary_item, 'dict') else summary_item
            
            doc_id, metadata = None, {}
            
            if 'method_name' in summary_dict:
                metadata = {"source": summary_dict['file_path'], "type": "method", "class": summary_dict['class_name'], "name": summary_dict['method_name']}
                doc_id = f"{summary_dict['file_path']}::{summary_dict['class_name']}::{summary_dict['method_name']}"
            elif 'function_name' in summary_dict:
                metadata = {"source": summary_dict['file_path'], "type": "function", "name": summary_dict['function_name']}
                doc_id = f"{summary_dict['file_path']}::{summary_dict['function_name']}"
            elif 'class_name' in summary_dict:
                metadata = {"source": summary_dict['file_path'], "type": "class", "name": summary_dict['class_name']}
                doc_id = f"{summary_dict['file_path']}::{summary_dict['class_name']}"

            if doc_id:
                ids_of_modified_items.append(doc_id)
                docs_to_add.append({"text": summary_dict['summary'], "metadata": metadata})

        # --- Step 2: Prepare list of all documents to be deleted ---
        # This includes items explicitly marked as 'removed' from the change detector...
        ids_from_removed = [_get_doc_id(c) for c in changes if c.change_type == 'removed']
        # ...and the old versions of items that were modified.
        unique_ids_to_delete = list(set(ids_from_removed + ids_of_modified_items))
        
        # --- Step 3: Execute DB operations ---
        if unique_ids_to_delete:
            print(f"Deleting {len(unique_ids_to_delete)} old/removed summaries from vector store.")
            vector_store.delete_summaries(unique_ids_to_delete)
        
        if docs_to_add:
            print(f"Adding/updating {len(docs_to_add)} summaries in vector store.")
            vector_store.add_summaries(docs_to_add)
        
        print("--- Vector Ingestion Node Completed Successfully ---")
        return {**state, "ingestion_status": "success"}

    except Exception as e:
        error_message = f"An error occurred during vector store ingestion: {e}"
        print(error_message)
        return {**state, "ingestion_status": "error", "error_message": str(e)}

