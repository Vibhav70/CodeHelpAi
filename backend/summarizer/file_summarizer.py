import os
from backend.parser.models import FileParseResult
from backend.summarizer.models import FileSummary
from backend.llm.llm_node import get_structured_llm_summary

def summarize_file_in_one_shot(file_parse_result: FileParseResult) -> FileSummary:
    """
    Generates a complete summary for a file in a single LLM call.

    This function reads the entire content of a source file and sends it to the
    LLM, requesting a single structured JSON response containing summaries for
    the file, its classes, and its functions.

    Args:
        file_parse_result: The parsed structure of the file.

    Returns:
        A FileSummary object populated with data from the LLM.
    """
    try:
        with open(file_parse_result.file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
    except Exception as e:
        print(f"Error reading file {file_parse_result.file_path}: {e}")
        return FileSummary(
            file_path=file_parse_result.file_path,
            summary_text="Error: Could not read file content.",
            class_summaries=[],
            function_summaries=[],
        )

    # Make the single API call for the entire file.
    summary_dict = get_structured_llm_summary(
        file_path=file_parse_result.file_path,
        code_context=file_content
    )

    # Convert the dictionary response back into a Pydantic model.
    return FileSummary(**summary_dict)
