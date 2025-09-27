# import json
# import os
# import re
# from typing import Dict, Any
# from jinja2 import Environment, FileSystemLoader

# # --- Jinja2 Template Setup ---
# # Assumes you have a 'templates' folder in your backend directory
# template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
# env = Environment(
#     loader=FileSystemLoader(template_dir),
#     trim_blocks=True,
#     lstrip_blocks=True
# )
# template = env.get_template("doc_template.md")


# def _format_summary_for_markdown(text: str) -> str:
#     """
#     Properly formats text for Markdown by handling newlines correctly.
#     Converts literal \n sequences to actual newlines and ensures proper line breaks.
#     """
#     if not isinstance(text, str):
#         return ""
    
#     # First, convert any literal \n sequences to actual newlines
#     text = text.replace('\\n', '\n')
    
#     # Then replace single newlines with Markdown hard line breaks (two spaces + newline)
#     # This ensures line breaks are preserved in Markdown rendering
#     return text.replace('\n', '  \n')


# def _clean_markdown_output(content: str) -> str:
#     """
#     Cleans the final Markdown output to ensure consistent and clean formatting.
#     Handles both literal \n sequences and actual newlines properly.
#     """
#     if not isinstance(content, str):
#         return ""
    
#     # Step 1: Convert any remaining literal \n sequences to actual newlines
#     # This handles cases where JSON data might contain escaped newlines
#     content = content.replace('\\n', '\n')
    
#     # Step 2: Normalize different newline formats
#     content = content.replace('\r\n', '\n').replace('\r', '\n')
    
#     # Step 3: Split content by code blocks to process them separately
#     # This preserves code block formatting while cleaning the rest
#     code_block_pattern = r'(```[\w]*\n.*?\n```)'
#     parts = re.split(code_block_pattern, content, flags=re.DOTALL)
    
#     cleaned_parts = []
#     for i, part in enumerate(parts):
#         if i % 2 == 1:  # This is a code block
#             cleaned_parts.append(part)
#         else:  # This is regular content
#             # Clean up excessive whitespace and normalize paragraph breaks
#             # Replace multiple consecutive newlines with double newlines (paragraph breaks)
#             part = re.sub(r'\n{3,}', '\n\n', part)
            
#             # Ensure single isolated newlines become paragraph breaks for better readability
#             # But preserve existing double newlines
#             part = re.sub(r'(?<!\n)\n(?!\n)(?!\s)', '\n\n', part)
            
#             cleaned_parts.append(part)
    
#     # Step 4: Join everything back together and final cleanup
#     final_content = ''.join(cleaned_parts)
    
#     # Remove excessive whitespace at the beginning and end
#     final_content = final_content.strip()
    
#     # Ensure we don't have more than 2 consecutive newlines anywhere
#     final_content = re.sub(r'\n{3,}', '\n\n', final_content)
    
#     return final_content


# def _organize_summaries(summaries_data: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Restructures the flat summary data from the JSON file into a nested
#     dictionary that is organized by file path.
#     """
#     organized_data = {}

#     def get_or_create(keys):
#         node = organized_data
#         for key in keys:
#             node = node.setdefault(key, {})
#         return node

#     # Process classes
#     for key, class_summary in summaries_data.get("classes", {}).items():
#         try:
#             file_path, class_name = key.split("::")
#             class_node = get_or_create([file_path, "classes", class_name])
            
#             # Create a copy to avoid modifying the original data
#             formatted_summary = dict(class_summary)
#             if 'summary' in formatted_summary:
#                 formatted_summary['summary'] = _format_summary_for_markdown(formatted_summary['summary'])
            
#             class_node.update(formatted_summary)
#         except ValueError:
#             print(f"Skipping malformed class key: {key}")

#     # Process methods
#     for key, method_summary in summaries_data.get("methods", {}).items():
#         try:
#             file_path, class_name, _ = key.split("::")
#             class_node = get_or_create([file_path, "classes", class_name])
            
#             # Create a copy to avoid modifying the original data
#             formatted_summary = dict(method_summary)
#             if 'summary' in formatted_summary:
#                 formatted_summary['summary'] = _format_summary_for_markdown(formatted_summary['summary'])
            
#             class_node.setdefault('methods', []).append(formatted_summary)
#         except ValueError:
#             print(f"Skipping malformed method key: {key}")
    
#     # Process functions        
#     for key, func_summary in summaries_data.get("functions", {}).items():
#         try:
#             file_path, _ = key.split("::")
#             file_node = get_or_create([file_path])
            
#             # Create a copy to avoid modifying the original data
#             formatted_summary = dict(func_summary)
#             if 'summary' in formatted_summary:
#                 formatted_summary['summary'] = _format_summary_for_markdown(formatted_summary['summary'])
            
#             file_node.setdefault('functions', []).append(formatted_summary)
#         except ValueError:
#             print(f"Skipping malformed function key: {key}")

#     return organized_data


# def generate_project_documentation(project_id: int, project_name: str) -> str:
#     """
#     Generates a complete Markdown documentation for a project.
#     """
#     summaries_db_path = f"project_data/{project_id}/summaries_db.json"
    
#     if not os.path.exists(summaries_db_path):
#         return f"# Documentation for {project_name}\n\nNo summaries found. Please run the ingestion pipeline first."

#     try:
#         with open(summaries_db_path, "r", encoding="utf-8") as f:
#             summaries_data = json.load(f)
#     except (json.JSONDecodeError, IOError) as e:
#         return f"# Documentation for {project_name}\n\nError: Could not read the summaries database. {str(e)}"

#     try:
#         organized_data = _organize_summaries(summaries_data)
#         markdown_content = template.render(project_name=project_name, files=organized_data)
#         cleaned_content = _clean_markdown_output(markdown_content)

#         output_file = f"project_data/{project_id}/documentation.md"
#         with open(output_file, "w", encoding="utf-8") as f:
#             f.write(cleaned_content)
#         print(f"Documentation saved to: {output_file}")
#         return cleaned_content
#     except Exception as e:
#         return f"# Documentation for {project_name}\n\nError generating documentation: {str(e)}"


import json
import os
import re
from typing import Dict, Any, List, Tuple
from jinja2 import Environment, FileSystemLoader

# Import your LLM chain for summarization, assuming it's in this location
# This reuses the same LLM configuration from your ingestion pipeline
from backend.nodes.summarize_changes_node import summarizer_chain

# --- Jinja2 Template Setup ---
# This points to your 'templates' folder to load the 'doc_template_v2.md'
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
template = env.get_template("doc_template_v2.md")

def _generate_project_summary(all_summaries: List[str]) -> str:
    """
    Makes a final LLM call to generate a high-level summary of the entire project
    based on the summaries of all its files.
    """
    print("--- Generating high-level project summary ---")
    if not all_summaries:
        return "No summary data was available to generate a project overview."

    # Join all individual summaries into a single context block for the LLM
    full_context = "\n\n---\n\n".join(all_summaries)
    
    # A specific prompt designed to synthesize, not just list, the information
    prompt = (
        "You are a principal software architect. Based on the following summaries of individual "
        "code files, write a high-level, executive summary of the entire project. "
        "Describe its main purpose, overall architecture, and how the key components interact. "
        "Do not describe each file individually; synthesize the information into a holistic overview."
    )
    
    try:
        # We reuse the summarizer chain, but provide a more specialized prompt
        # Note: The chain expects a 'code_snippet' key, so we adapt our context to it.
        # A more advanced implementation might have a separate chain for this task.
        response = summarizer_chain.invoke({
            "code_snippet": f"File Summaries:\n{full_context}",
            "system_prompt": prompt
        })
        return response
    except Exception as e:
        print(f"Failed to generate project-level summary: {e}")
        return "Could not generate a high-level project summary due to an API or processing error."


def _organize_summaries(summaries_data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """
    Restructures the flat summary data from the JSON file into a nested dictionary 
    organized by file path, and also returns a flat list of summary texts.
    """
    organized_data = {}
    all_summary_texts = []

    def get_or_create_nested(keys: List[str]) -> Dict:
        node = organized_data
        for key in keys:
            node = node.setdefault(key, {})
        return node

    # Process classes and methods first
    for key, summary_obj in summaries_data.get("classes", {}).items():
        try:
            file_path, class_name = key.split("::")
            class_node = get_or_create_nested([file_path, "classes", class_name])
            class_node.update(summary_obj)
            all_summary_texts.append(f"File '{file_path}' contains a class '{class_name}': {summary_obj.get('summary', '')}")
        except ValueError: continue

    for key, summary_obj in summaries_data.get("methods", {}).items():
        try:
            file_path, class_name, _ = key.split("::")
            class_node = get_or_create_nested([file_path, "classes", class_name])
            class_node.setdefault('methods', []).append(summary_obj)
        except ValueError: continue
            
    # Process standalone functions
    for key, summary_obj in summaries_data.get("functions", {}).items():
        try:
            file_path, func_name = key.split("::")
            file_node = get_or_create_nested([file_path])
            file_node.setdefault('functions', []).append(summary_obj)
            all_summary_texts.append(f"File '{file_path}' contains a function '{func_name}': {summary_obj.get('summary', '')}")
        except ValueError: continue

    return organized_data, all_summary_texts


def generate_project_documentation(project_id: int, project_name: str) -> str:
    """
    Generates a complete, well-formatted Markdown documentation for a project.
    """
    summaries_db_path = f"project_data/{project_id}/summaries_db.json"
    
    if not os.path.exists(summaries_db_path):
        return f"# Documentation for {project_name}\n\nNo summaries found. Please run the ingestion pipeline first."

    try:
        with open(summaries_db_path, "r", encoding="utf-8") as f:
            summaries_data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return f"# Documentation for {project_name}\n\nError: Could not read the summaries database."

    # Organize the data for the template and get the flat list for the meta-summary
    organized_data, all_summaries = _organize_summaries(summaries_data)
    
    # Generate the high-level summary
    # project_summary = _generate_project_summary(all_summaries)    # high level summary generation disabled for now
    
    # Render the final document using the template
    markdown_content = template.render(
        project_name=project_name,
        # project_summary=project_summary,
        files=organized_data
    )
    
    
    return markdown_content.strip()

