import os
import sys
import tempfile
import shutil
from unittest.mock import patch

# This setup assumes the standard project structure has been configured
# correctly (e.g., via `pip install -e .` or a conftest.py file).

import pytest

# --- CORRECTED IMPORTS ---
# The import paths are now updated to reflect that 'parser' and 'summarizer'
# are likely sub-packages of the 'backend' package.
from backend.parser.scanner import scan_python_files
from backend.parser.hasher import hash_file
from backend.nodes.parser_node import parser_node
from backend.nodes.summary_node import summary_node
from backend.graph_incremental import build_graph, GraphState

# --- Test Cases ---

# This fixture creates a temporary directory with code files for testing.
@pytest.fixture
def temp_code_dir():
    dir_path = tempfile.mkdtemp()
    file_contents = {
        "module_one.py": (
            "class MyClass:\n"
            '    """A simple test class."""\n'
            "    def method_a(self):\n"
            '        """A test method."""\n'
            "        pass\n"
        ),
        "module_two.py": (
            '"""Top-level module docstring."""\n'
            "def top_level_func():\n"
            '    """A top-level function."""\n'
            "    return True\n"
        ),
    }
    for filename, content in file_contents.items():
        with open(os.path.join(dir_path, filename), "w") as f:
            f.write(content)
    yield dir_path
    shutil.rmtree(dir_path)

# --- CORRECTED PATCH DECORATORS ---
# The patch targets are also updated to point to the correct module paths.
@patch("backend.summarizer.file_summarizer.summarize_file_in_one_shot")
@patch("backend.summarizer.file_summarizer.summarize_file_in_one_shot")
@patch("backend.summarizer.file_summarizer.summarize_file_in_one_shot")
def test_full_summarization(mock_func_llm, mock_class_llm, mock_file_llm, temp_code_dir):
    """
    Tests the full, from-scratch summarization workflow.
    """
    # Arrange
    mock_func_llm.return_value = "This is a mock summary."
    mock_class_llm.return_value = "This is a mock summary."
    mock_file_llm.return_value = "This is a mock summary."

    # Act
    all_files = scan_python_files(temp_code_dir)
    parsed_files = parser_node(all_files)
    summaries = summary_node(parsed_files)

    # Assert
    assert len(summaries) == 2
    assert summaries[0].file_path.endswith("module_one.py")
    assert len(summaries[0].class_summaries) == 1
    assert summaries[0].class_summaries[0].name == "MyClass"
    assert summaries[1].file_path.endswith("module_two.py")
    assert len(summaries[1].function_summaries) == 1
    assert summaries[1].function_summaries[0].name == "top_level_func"
@patch("backend.summarizer.file_summarizer.summarize_file_in_one_shot")
@patch("backend.summarizer.file_summarizer.summarize_file_in_one_shot")
@patch("backend.summarizer.file_summarizer.summarize_file_in_one_shot")
def test_incremental_summarization(mock_func_llm, mock_class_llm, mock_file_llm, temp_code_dir):
    """
    Tests the incremental graph by simulating a file change.
    """
    # Arrange
    mock_func_llm.return_value = "This is an updated mock summary."
    mock_class_llm.return_value = "This is an updated mock summary."
    mock_file_llm.return_value = "This is an updated mock summary."
    
    module_one_path = os.path.join(temp_code_dir, "module_one.py")
    module_two_path = os.path.join(temp_code_dir, "module_two.py")

    old_hashes = {
        module_one_path: hash_file(module_one_path),
        module_two_path: hash_file(module_two_path),
    }

    with open(module_two_path, "a") as f:
        f.write("\n# A new comment to change the hash\n")

    app = build_graph()
    initial_state: GraphState = {
        "old_hashes": old_hashes, "new_dir": temp_code_dir,
        "changed_files": {}, "parsed_files": [], "summaries": []
    }

    # Act
    final_state = app.invoke(initial_state)

    # Assert
    changed_files = final_state["changed_files"]
    summaries = final_state["summaries"]

    assert changed_files["modified"] == [module_two_path]
    assert not changed_files["added"]
    assert not changed_files["removed"]
    
    assert len(summaries) == 1
    assert summaries[0].file_path == module_two_path
