import json
import os
from typing import List, Dict, Any

# Import the VectorStore class, which we will now instantiate per project
from backend.vectorstore.store import VectorStore

def format_summaries_for_ingestion(db_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Transforms the raw summaries from the JSON DB into the format
    required by the VectorStore, which is a list of dicts, each
    with 'text' and 'metadata'.
    """
    formatted_docs = []

    # Process function summaries
    for key, summary_text in db_data.get("functions", {}).items():
        try:
            file_path, func_name = key.split("::")
            formatted_docs.append({
                "text": summary_text,
                "metadata": {
                    "source": file_path,
                    "type": "function",
                    "name": func_name
                }
            })
        except ValueError:
            print(f"Skipping malformed function key: {key}")

    # Process class summaries
    for key, summary_text in db_data.get("classes", {}).items():
        try:
            file_path, class_name = key.split("::")
            formatted_docs.append({
                "text": summary_text,
                "metadata": {
                    "source": file_path,
                    "type": "class",
                    "name": class_name
                }
            })
        except ValueError:
            print(f"Skipping malformed class key: {key}")
            
    # Process method summaries
    for key, summary_text in db_data.get("methods", {}).items():
        try:
            file_path, class_name, method_name = key.split("::")
            formatted_docs.append({
                "text": summary_text,
                "metadata": {
                    "source": file_path,
                    "type": "method",
                    "class": class_name,
                    "name": method_name
                }
            })
        except ValueError:
            print(f"Skipping malformed method key: {key}")

    return formatted_docs

def ingest_summaries_to_vector_store(project_id: int):
    """
    The main function to run the full ingestion process for a specific project.
    1. Loads the summaries from the project-specific JSON file.
    2. Formats them for the vector store.
    3. Adds them to the project-specific FAISS index.
    """
    print(f"--- Starting ingestion for project ID: {project_id} ---")
    
    # Construct the path to the project-specific summaries database
    summaries_db_path = f"project_data/{project_id}/summaries_db.json"
    
    if not os.path.exists(summaries_db_path):
        print(f"Error: Summaries database not found for project {project_id} at {summaries_db_path}. Aborting.")
        return

    try:
        with open(summaries_db_path, "r") as f:
            summaries_data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading summaries database for project {project_id}: {e}. Aborting.")
        return

    # Format the loaded data
    documents_to_add = format_summaries_for_ingestion(summaries_data)

    if not documents_to_add:
        print(f"No valid summaries found to ingest for project {project_id}.")
        return

    # Instantiate the VectorStore for the specific project
    vector_store = VectorStore(project_id=project_id)
    
    # Add the documents to the project's vector store instance
    vector_store.add_summaries(documents_to_add)

    print(f"--- Ingestion complete for project {project_id}. Added {len(documents_to_add)} summaries. ---")

# import json
# import os
# from typing import List, Dict, Any

# # Import the singleton instance of our vector store
# from backend.vectorstore.store import VectorStore

# # Define the path to the source of our summaries
# SUMMARIES_DB_PATH = "summaries_db.json"

# def format_summaries_for_ingestion(db_data: Dict[str, Any]) -> List[Dict[str, Any]]:
#     """
#     Transforms the raw summaries from the JSON DB into the format
#     required by the VectorStore, which is a list of dicts, each
#     with 'text' and 'metadata'.
#     """
#     formatted_docs = []

#     # Process function summaries
#     for key, summary_text in db_data.get("functions", {}).items():
#         try:
#             file_path, func_name = key.split("::")
#             formatted_docs.append({
#                 "text": summary_text,
#                 "metadata": {
#                     "source": file_path,
#                     "type": "function",
#                     "name": func_name
#                 }
#             })
#         except ValueError:
#             print(f"Skipping malformed function key: {key}")

#     # Process class summaries
#     for key, summary_text in db_data.get("classes", {}).items():
#         try:
#             file_path, class_name = key.split("::")
#             formatted_docs.append({
#                 "text": summary_text,
#                 "metadata": {
#                     "source": file_path,
#                     "type": "class",
#                     "name": class_name
#                 }
#             })
#         except ValueError:
#             print(f"Skipping malformed class key: {key}")
            
#     # Process method summaries
#     for key, summary_text in db_data.get("methods", {}).items():
#         try:
#             file_path, class_name, method_name = key.split("::")
#             formatted_docs.append({
#                 "text": summary_text,
#                 "metadata": {
#                     "source": file_path,
#                     "type": "method",
#                     "class": class_name,
#                     "name": method_name
#                 }
#             })
#         except ValueError:
#             print(f"Skipping malformed method key: {key}")

#     return formatted_docs

# def ingest_summaries_to_vector_store():
#     """
#     The main function to run the full ingestion process.
#     1. Loads the summaries from the JSON file.
#     2. Formats them for the vector store.
#     3. Adds them to the FAISS index.
#     """
#     print("--- Starting ingestion of summaries into vector store ---")
#     if not os.path.exists(SUMMARIES_DB_PATH):
#         print(f"Error: Summaries database not found at {SUMMARIES_DB_PATH}. Aborting.")
#         return

#     try:
#         with open(SUMMARIES_DB_PATH, "r") as f:
#             summaries_data = json.load(f)
#     except (json.JSONDecodeError, IOError) as e:
#         print(f"Error reading summaries database: {e}. Aborting.")
#         return

#     # Format the loaded data
#     documents_to_add = format_summaries_for_ingestion(summaries_data)

#     if not documents_to_add:
#         print("No valid summaries found to ingest.")
#         return

#     VectorStore.add_summaries(documents_to_add)

#     print(f"--- Ingestion complete. Added {len(documents_to_add)} summaries to the vector store. ---")

