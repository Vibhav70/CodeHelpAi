# backend/nodes/ingest_updates_node.py

import json
import os
from typing import List, Dict, Any, Union
from pydantic import BaseModel

# Import the state and change definitions
from .change_detection_node import GraphState, ChangedItem
# Import the summary models
from ..summarizer.models import FunctionSummary, ClassSummary, MethodSummary

# Define the path for our "database" of summaries
SUMMARIES_DB_PATH = "summaries_db.json"

def _load_summaries_db() -> Dict[str, Any]:
    """Loads the existing summaries from our JSON database file."""
    if not os.path.exists(SUMMARIES_DB_PATH):
        return {"functions": {}, "classes": {}, "methods": {}}
    try:
        with open(SUMMARIES_DB_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"functions": {}, "classes": {}, "methods": {}}

def _save_summaries_db(db_data: Dict[str, Any]):
    """Saves the updated summaries back to the JSON database file."""
    try:
        with open(SUMMARIES_DB_PATH, "w") as f:
            json.dump(db_data, f, indent=2)
    except IOError as e:
        print(f"Error saving summaries DB to {SUMMARIES_DB_PATH}: {e}")

async def ingest_updates_node(state: GraphState) -> dict:
    """
    An async LangGraph node that updates the persistent summary store based on
    detected changes and new summaries.
    """
    print("--- Ingestion Node Triggered ---")
    changes = state.get("changes", [])
    new_summaries = state.get("summaries", [])
    
    if not new_summaries:
        print("No new summaries to ingest. Skipping update.")
        return {}

    summaries_db = _load_summaries_db()
    
    # --- Step 1: Handle Removed Items ---
    for change in changes:
        if change.change_type == 'removed':
            # This logic remains the same
            if change.item_type == 'function':
                key = f"{change.file_path}::{change.item_name}"
                if key in summaries_db["functions"]: del summaries_db["functions"][key]
            elif change.item_type == 'class':
                key = f"{change.file_path}::{change.item_name}"
                if key in summaries_db["classes"]: del summaries_db["classes"][key]

    # --- Step 2: Handle Added/Modified Items ---
    for summary_item in new_summaries:
        # --- THIS IS THE FIX ---
        # Convert the Pydantic model object to a dictionary to standardize it.
        if isinstance(summary_item, BaseModel):
            summary_dict = summary_item.dict()
        else:
            summary_dict = summary_item # It's already a dict

        # Now, the key-based checks will work correctly.
        if 'method_name' in summary_dict:
            key = f"{summary_dict['file_path']}::{summary_dict['class_name']}::{summary_dict['method_name']}"
            summaries_db["methods"][key] = summary_dict['summary']
        elif 'function_name' in summary_dict:
            key = f"{summary_dict['file_path']}::{summary_dict['function_name']}"
            summaries_db["functions"][key] = summary_dict['summary']
        elif 'class_name' in summary_dict:
            key = f"{summary_dict['file_path']}::{summary_dict['class_name']}"
            summaries_db["classes"][key] = summary_dict['summary']

    # --- Step 3: Save the updated database ---
    _save_summaries_db(summaries_db)
    
    print(f"Summaries database updated. Total functions: {len(summaries_db['functions'])}, classes: {len(summaries_db['classes'])}.")
    
    return {}
