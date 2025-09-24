from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from backend.parser.parser import FileParseResult

# --- Models to structure the change detection results ---

class ChangedItem(BaseModel):
    """Represents a single detected change."""
    file_path: str
    item_type: str  # e.g., 'function', 'class', 'method'
    item_name: str
    change_type: str # 'added', 'removed', 'modified'
    class_name: Optional[str] = None # The crucial field for methods

# --- The Main Diffing Logic ---

def detect_changes(
    old_hashes: Dict[str, Any], 
    new_hashes: Dict[str, Any],
    parsed_file_results: Dict[str, FileParseResult] # Accept the 3rd argument
) -> List[ChangedItem]:
    """
    Compares two sets of nested file hashes to detect granular changes.
    """
    changes: List[ChangedItem] = []
    
    all_file_paths = set(old_hashes.keys()) | set(new_hashes.keys())

    for file_path in all_file_paths:
        old_file_hash = old_hashes.get(file_path)
        new_file_hash = new_hashes.get(file_path)

        if not old_file_hash and new_file_hash:
            # Case 1: File was added
            for func_name in new_file_hash["functions"]:
                changes.append(ChangedItem(file_path=file_path, item_type='function', item_name=func_name, change_type='added'))
            for class_name, class_data in new_file_hash.get("classes", {}).items():
                changes.append(ChangedItem(file_path=file_path, item_type='class', item_name=class_name, change_type='added'))
                for method_name in class_data.get("methods", {}):
                    changes.append(ChangedItem(file_path=file_path, item_type='method', item_name=method_name, change_type='added', class_name=class_name))
            continue

        if not new_file_hash and old_file_hash:
            # Case 2: File was removed
            for func_name in old_file_hash["functions"]:
                changes.append(ChangedItem(file_path=file_path, item_type='function', item_name=func_name, change_type='removed'))
            for class_name, class_data in old_file_hash.get("classes", {}).items():
                changes.append(ChangedItem(file_path=file_path, item_type='class', item_name=class_name, change_type='removed'))
                for method_name in class_data.get("methods", {}):
                    changes.append(ChangedItem(file_path=file_path, item_type='method', item_name=method_name, change_type='removed', class_name=class_name))
            continue

        # Case 3: File exists in both, check for modifications
        _compare_item_hashes(changes, file_path, 'function', old_file_hash.get("functions", {}), new_file_hash.get("functions", {}))
        _compare_class_hashes(changes, file_path, old_file_hash.get("classes", {}), new_file_hash.get("classes", {}))

    return changes

def _compare_item_hashes(changes: List[ChangedItem], file_path: str, item_type: str, old_items: Dict, new_items: Dict, class_name: Optional[str] = None):
    """Helper to compare simple key-value hash dictionaries, now aware of class context."""
    old_names = set(old_items.keys())
    new_names = set(new_items.keys())

    for name in new_names - old_names:
        changes.append(ChangedItem(file_path=file_path, item_type=item_type, item_name=name, change_type='added', class_name=class_name))
    
    for name in old_names - new_names:
        changes.append(ChangedItem(file_path=file_path, item_type=item_type, item_name=name, change_type='removed', class_name=class_name))

    for name in old_names & new_names:
        if old_items[name] != new_items[name]:
            changes.append(ChangedItem(file_path=file_path, item_type=item_type, item_name=name, change_type='modified', class_name=class_name))

def _compare_class_hashes(changes: List[ChangedItem], file_path: str, old_classes: Dict, new_classes: Dict):
    """Helper to compare the more complex class hash dictionaries."""
    old_names = set(old_classes.keys())
    new_names = set(new_classes.keys())

    for name in new_names - old_names:
        changes.append(ChangedItem(file_path=file_path, item_type='class', item_name=name, change_type='added'))
        for method_name in new_classes[name].get('methods', {}):
             changes.append(ChangedItem(file_path=file_path, item_type='method', item_name=method_name, change_type='added', class_name=name))
    
    for name in old_names - new_names:
        changes.append(ChangedItem(file_path=file_path, item_type='class', item_name=name, change_type='removed'))
        for method_name in old_classes[name].get('methods', {}):
             changes.append(ChangedItem(file_path=file_path, item_type='method', item_name=method_name, change_type='removed', class_name=name))

    for name in old_names & new_names:
        old_class = old_classes[name]
        new_class = new_classes[name]
        if old_class['source_hash'] != new_class['source_hash']:
            changes.append(ChangedItem(file_path=file_path, item_type='class', item_name=name, change_type='modified'))
        
        # Pass the class name down to the method comparison
        _compare_item_hashes(
            changes, 
            file_path, 
            'method', 
            old_class.get('methods', {}), 
            new_class.get('methods', {}),
            class_name=name
        )