# tests/test_query.py

import pytest
import tempfile
import os
import shutil
from pathlib import Path

# --- Imports from your project ---
# Adjust these paths if your structure is different
from backend.parser.scanner import scan_python_files
from backend.parser.parser import parse_file
from backend.vectorstore.ingest import ingest_summaries
from backend.query.query_engine import QueryEngine


# --- Mock Implementation of Summarizer ---
# This is a placeholder for the real summarizer to make the test self-contained.
# In a real-world scenario, you might use pytest-mock to patch the real function.
from backend.summarizer.models import FileSummary, ClassSummary, FunctionSummary

def mock_summarize_file(parsed_result) -> FileSummary:
    """A mock summarizer that creates predictable summaries for testing."""
    file_path = parsed_result.file_path
    
    # Create simple summaries based on the parsed info
    func_summaries = [
        FunctionSummary(name=f.name, summary_text=f"This is a summary for the function {f.name}.")
        for f in parsed_result.functions
    ]
    class_summaries = [
        ClassSummary(
            name=c.name,
            summary_text=f"This is a summary for the class {c.name}.",
            method_summaries=[
                FunctionSummary(name=m.name, summary_text=f"A summary for the method {m.name}.")
                for m in c.methods
            ]
        )
        for c in parsed_result.classes
    ]

    return FileSummary(
        file_path=file_path,
        summary_text=f"A summary for the file {os.path.basename(file_path)}.",
        function_summaries=func_summaries,
        class_summaries=class_summaries
    )

# --- Pytest Fixture for Test Environment ---

@pytest.fixture(scope="module")
def sample_repo():
    """Creates a temporary directory with a small Python project for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        
        # Create auth.py
        (root / "auth").mkdir()
        (root / "auth" / "main.py").write_text(
            "class Authenticator:\n"
            "    def login(self, user, password):\n"
            "        print('User logged in')\n"
        )
        
        # Create database.py
        (root / "db").mkdir()
        (root / "db" / "connect.py").write_text(
            "def connect_to_database():\n"
            "    return 'Connected'\n"
        )
        
        yield str(root) # Provide the path to the tests
        
        # Teardown is handled by TemporaryDirectory context manager

# --- Test Function ---

def test_ingest_and_query(sample_repo):
    """
    Tests the full end-to-end flow: ingest a repo and then query it.
    """
    # 1. --- INGESTION PHASE ---
    print(f"\n--- Ingesting sample repo at: {sample_repo} ---")
    
    # Scan, parse, and summarize the files
    python_files = scan_python_files(sample_repo)
    all_summaries = []
    for file_path in python_files:
        parsed_result = parse_file(file_path)
        summary = mock_summarize_file(parsed_result)
        all_summaries.append(summary)
        
    # Ingest the summaries into the vector DB
    ingest_summaries(all_summaries)
    
    print("--- Ingestion complete ---")

    # 2. --- QUERY PHASE ---
    print("\n--- Querying ingested data ---")
    engine = QueryEngine()
    
    # This question should be most similar to the 'login' method summary
    question = "How does a user log in?"
    results = engine.search_summaries(question, top_k=1)
    
    # 3. --- ASSERTION PHASE ---
    print("\n--- Asserting results ---")
    
    # Ensure we got at least one result
    assert len(results) > 0, "Search should return at least one result."
    
    top_result = results[0]
    
    # Ensure the top result has the expected metadata
    assert "metadata" in top_result, "Result should contain metadata."
    
    metadata = top_result["metadata"]
    print(f"Top result metadata: {metadata}")
    
    # Check if the most relevant document is indeed from the auth file
    assert "auth" in metadata.get("file_path", ""), "File path should be related to auth."
    assert metadata.get("symbol_name") == "Authenticator.login", "Symbol name should be the login method."
    
    print("--- Test passed successfully! ---")

