from backend.parser.models import FunctionInfo
from backend.summarizer.models import FunctionSummary
from backend.summarizer.llm_utils import summarize_code_with_llm

# This is the specific question we'll ask the LLM for each function.
# The main system prompt is now handled inside the llm_node.
QUESTION = "Summarize the following Python function in one or two sentences."

def summarize_function(func_info: FunctionInfo, code_text: str) -> FunctionSummary:
    """
    Generates a summary for a single function using its source code by
    calling the real LLM service.

    Args:
        func_info: A Pydantic model containing the function's name
                   and docstring.
        code_text: The raw string of the function's source code.

    Returns:
        A FunctionSummary object containing the original metadata and the
        newly generated summary from the Gemini API.
    """
    # Call the updated utility, passing the specific question for this context.
    summary_text = summarize_code_with_llm(
        code_text=code_text,
        question=QUESTION
    )

    # Combine the original info with the new summary into a structured object.
    return FunctionSummary(
        name=func_info.name,
        docstring=func_info.docstring,
        summary_text=summary_text
    )