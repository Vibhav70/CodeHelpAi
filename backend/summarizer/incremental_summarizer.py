from parser.parser import parse_file
from summarizer.file_summarizer import summarize_file
from summarizer.models import FileSummary

def summarize_changes(changed_files: list[str]) -> list[FileSummary]:
    """
    Parses and summarizes a list of changed files.

    This function is a key part of the incremental processing pipeline.
    It takes a list of file paths (e.g., from the diffing node),
    re-parses each file to get its current AST structure, and then
    generates a new summary for it.

    Args:
        changed_files: A list of absolute file paths for files that
                       have been added or modified.

    Returns:
        A list of FileSummary objects, one for each processed file.
    """
    all_summaries = []
    for file_path in changed_files:
        try:
            # 1. Parse the file to get its current structure.
            parse_result = parse_file(file_path)

            # 2. Generate a new, complete summary for the parsed file.
            file_summary = summarize_file(parse_result)

            all_summaries.append(file_summary)
        except Exception as e:
            # In a production system, you'd want more robust logging here.
            print(f"Error processing file {file_path}: {e}")
            continue

    return all_summaries