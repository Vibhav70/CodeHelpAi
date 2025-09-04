import os
from typing import List

def scan_python_files(base_path: str) -> List[str]:
    """
    Recursively scans a directory for Python (.py) files.

    It ignores directories named '__pycache__', 'venv', and any hidden directories
    (those starting with a dot).

    Args:
        base_path: The absolute or relative path to the directory to scan.

    Returns:
        A list of absolute paths to all found Python files.
    """
    python_files = []
    # Ensure the base_path is absolute to build correct absolute paths for found files
    abs_base_path = os.path.abspath(base_path)
    
    # Common directories to ignore
    ignored_dirs = {'__pycache__', 'venv'}

    for root, dirnames, filenames in os.walk(abs_base_path, topdown=True):
        # Exclude specific directories from traversal
        # We modify dirnames in-place to prevent os.walk from visiting them
        dirnames[:] = [d for d in dirnames if d not in ignored_dirs and not d.startswith('.')]

        for filename in filenames:
            if filename.endswith(".py"):
                # Construct the full absolute path and add it to the list
                file_path = os.path.join(root, filename)
                python_files.append(file_path)

    return python_files


# For testing if it is scanning or not


# if __name__ == '__main__':
#     # You can run this script directly to test its functionality
#     # Replace '.' with the path to your project directory if needed
#     project_path = '.'
#     found_files = scan_python_files(project_path)
#     print(f"Found {len(found_files)} Python files:")
#     for f in found_files:
#         print(f)