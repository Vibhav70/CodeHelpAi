import json
import os
from typing import Dict, Any

from .change_detection_node import GraphState

# --- Helper functions for project-specific summary management ---

def _get_summary_db_path(project_id: int) -> str:
    """Constructs the file path for a project's summary database."""
    project_data_dir = f"project_data/{project_id}"
    os.makedirs(project_data_dir, exist_ok=True)
    return os.path.join(project_data_dir, "summaries_db.json")

def _load_project_summaries(db_path: str) -> Dict[str, Any]:
    """Loads the summary database for a specific project."""
    if not os.path.exists(db_path):
        return {"functions": {}, "classes": {}, "methods": {}}
    try:
        with open(db_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"functions": {}, "classes": {}, "methods": {}}

def _save_project_summaries(db_path: str, summaries: Dict[str, Any]):
    """Saves the summary database for a specific project."""
    try:
        with open(db_path, "w") as f:
            json.dump(summaries, f, indent=2)
    except IOError as e:
        print(f"Error saving summaries to {db_path}: {e}")

def _get_unique_id(summary_dict: Dict[str, Any]) -> str:
    """Creates a unique identifier for a summary dictionary."""
    if 'method_name' in summary_dict:
        return f"{summary_dict['file_path']}::{summary_dict['class_name']}::{summary_dict['method_name']}"
    elif 'class_name' in summary_dict:
        return f"{summary_dict['file_path']}::{summary_dict['class_name']}"
    else:
        return f"{summary_dict['file_path']}::{summary_dict['function_name']}"

# --- The LangGraph Node ---

async def ingest_updates_node(state: GraphState) -> None:
    """
    An async LangGraph node that saves the generated summaries to a project-specific JSON file.
    """
    print("--- Ingestion Node Triggered ---")
    project_id = state.get("project_id")
    summaries = state.get("summaries", [])
    changes = state.get("changes", [])

    if not project_id:
        raise ValueError("Error: project_id not found in graph state.")

    db_path = _get_summary_db_path(project_id)
    summary_db = _load_project_summaries(db_path)

    # Handle removed items
    for change in changes:
        if change.change_type == 'removed':
            unique_id = f"{change.file_path}::{change.item_name}"
            if change.item_type == 'method':
                # Note: This requires a more complex lookup if class name isn't in ChangedItem
                # For now, we assume simple cases.
                pass 
            elif change.item_type == 'class' and unique_id in summary_db['classes']:
                del summary_db['classes'][unique_id]
            elif change.item_type == 'function' and unique_id in summary_db['functions']:
                del summary_db['functions'][unique_id]
    
    # Handle added/modified items
    for summary in summaries:
        # Convert Pydantic model to dict if it's not already
        summary_dict = summary if isinstance(summary, dict) else summary.dict()
        unique_id = _get_unique_id(summary_dict)
        
        if 'method_name' in summary_dict:
            summary_db['methods'][unique_id] = summary_dict
        elif 'class_name' in summary_dict:
            summary_db['classes'][unique_id] = summary_dict
        else:
            summary_db['functions'][unique_id] = summary_dict

    _save_project_summaries(db_path, summary_db)
    total_items = len(summary_db['functions']) + len(summary_db['classes']) + len(summary_db['methods'])
    print(f"Summaries database for project {project_id} updated. Total items: {total_items}.")
    
    # This node doesn't need to return anything to the state
    return {}
