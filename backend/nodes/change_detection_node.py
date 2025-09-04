# import json
# import os
# from typing import List, Dict, Any, TypedDict

# # Import the core components
# from backend.parser.scanner import scan_python_files
# from backend.parser.parser import parse_file
# from backend.parser.hasher import create_hashes_from_parse_result
# from backend.diffing.code_change_detector import detect_changes, ChangedItem

# # Define the path for storing the state of our codebase hashes
# HASH_FILE_PATH = "code_hashes.json"

# # --- LangGraph State Definition ---
# class GraphState(TypedDict):
#     """
#     Represents the state of our graph.
#     - directory: The input directory to scan.
#     - changes: The list of detected changes to be processed by the next node.
#     """
#     directory: str
#     changes: List[ChangedItem]
#     summaries: List[Dict[str, Any]] 


# # --- Helper functions for state management (from ingestion_service) ---
# def _load_old_hashes() -> Dict[str, Any]:
#     """Loads the previously stored hashes from the JSON file."""
#     if not os.path.exists(HASH_FILE_PATH):
#         return {}
#     try:
#         with open(HASH_FILE_PATH, "r") as f:
#             return json.load(f)
#     except (json.JSONDecodeError, IOError):
#         return {}

# def _save_new_hashes(hashes: Dict[str, Any]):
#     """Saves the latest set of hashes to the JSON file."""
#     try:
#         with open(HASH_FILE_PATH, "w") as f:
#             json.dump(hashes, f, indent=2)
#     except IOError as e:
#         print(f"Error saving hashes to {HASH_FILE_PATH}: {e}")


# # --- The LangGraph Node ---
# def change_detection_node(state: GraphState) -> GraphState:
#     """
#     A LangGraph node that orchestrates the entire change detection process.
#     """
#     print("--- Change Detection Node Triggered ---")
#     directory = state['directory']
#     if not directory or not os.path.isdir(directory):
#         print("Error: Directory not provided or does not exist in state.")
#         return {**state, "changes": []}

#     # 1. Load the last known state
#     old_hashes = _load_old_hashes()
#     print(f"Loaded hashes for {len(old_hashes)} files from previous run.")

#     # 2. Scan and parse the codebase to generate new hashes
#     python_files = scan_python_files(directory)
#     new_hashes = {}
#     for file_path in python_files:
#         try:
#             parsed_result = parse_file(file_path)
#             file_hash_dict = create_hashes_from_parse_result(parsed_result)
#             new_hashes[file_path] = file_hash_dict
#         except Exception as e:
#             print(f"Could not parse or hash file {file_path}: {e}")
#             continue
#     print(f"Generated new hashes for {len(new_hashes)} files.")

#     # 3. Compare old and new hashes to find what changed
#     changes = detect_changes(old_hashes, new_hashes)
#     print(f"Detected {len(changes)} granular changes.")

#     # 4. Save the new state for the next run
#     _save_new_hashes(new_hashes)
#     print(f"Saved new hashes to {HASH_FILE_PATH}.")

#     # 5. Update the state with the list of changes
#     return {**state, "changes": changes}
import json
import os
from typing import List, Dict, Any, TypedDict, Union

# Import the core components using absolute paths from the 'backend' root
from backend.parser.scanner import scan_python_files
from backend.parser.parser import parse_file
from backend.parser.hasher import create_hashes_from_parse_result
from backend.diffing.code_change_detector import detect_changes, ChangedItem
from backend.summarizer.models import FunctionSummary, ClassSummary, MethodSummary

# --- LangGraph State Definition ---
class GraphState(TypedDict):
    """
    Represents the state of our graph.
    - project_id: The ID of the project being processed.
    - directory: The input directory to scan.
    - changes: The list of detected changes for the next node.
    - summaries: The list of generated summaries.
    """
    project_id: int
    directory: str
    changes: List[ChangedItem]
    summaries: List[Union[FunctionSummary, ClassSummary, MethodSummary]]

# --- Helper functions for project-specific state management ---
def _load_project_hashes(hashes_file_path: str) -> Dict[str, Any]:
    """Loads the previously stored hashes for a specific project."""
    if not os.path.exists(hashes_file_path):
        return {}
    try:
        with open(hashes_file_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def _save_project_hashes(hashes_file_path: str, hashes: Dict[str, Any]):
    """Saves the latest set of hashes for a specific project."""
    try:
        with open(hashes_file_path, "w") as f:
            json.dump(hashes, f, indent=2)
    except IOError as e:
        print(f"Error saving hashes to {hashes_file_path}: {e}")

# --- The LangGraph Node ---
async def change_detection_node(state: GraphState) -> Dict:
    """
    A LangGraph node that orchestrates project-specific change detection.
    """
    print("--- Change Detection Node Triggered ---")
    project_id = state.get("project_id")
    directory = state.get("directory")

    if not project_id:
        raise ValueError("Error: project_id not found in graph state.")
    if not directory or not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not provided or does not exist.")
        return {"changes": []}

    # Define the project-specific path for storing hashes
    project_data_dir = f"project_data/{project_id}"
    os.makedirs(project_data_dir, exist_ok=True)
    hashes_file_path = os.path.join(project_data_dir, "code_hashes.json")

    # 1. Load the last known state for this specific project
    old_hashes = _load_project_hashes(hashes_file_path)
    print(f"Loaded hashes for {len(old_hashes)} files for project {project_id}.")

    # 2. Scan and parse the codebase to generate new hashes
    python_files = scan_python_files(directory)
    new_hashes = {}
    for file_path in python_files:
        try:
            parsed_result = parse_file(file_path)
            file_hash_dict = create_hashes_from_parse_result(parsed_result)
            new_hashes[file_path] = file_hash_dict
        except Exception as e:
            print(f"Could not parse or hash file {file_path}: {e}")
            continue
    print(f"Generated new hashes for {len(new_hashes)} files.")

    # 3. Compare old and new hashes to find what changed
    changes = detect_changes(old_hashes, new_hashes)
    print(f"Detected {len(changes)} granular changes for project {project_id}.")

    # 4. Save the new state for the next run
    _save_project_hashes(hashes_file_path, new_hashes)
    print(f"Saved new hashes for project {project_id} to {hashes_file_path}.")

    # 5. Return the dictionary of changes to update the graph's state
    return {"changes": changes}