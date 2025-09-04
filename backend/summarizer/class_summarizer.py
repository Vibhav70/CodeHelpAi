from backend.parser.models import ClassInfo
from backend.summarizer.models import ClassSummary
from backend.summarizer.function_summarizer import summarize_function
from backend.summarizer.llm_utils import summarize_code_with_llm

# A specific question to get a high-level overview of a class.
CLASS_QUESTION = "Summarize the following Python class in two to three sentences. Describe its primary role and responsibility."

def summarize_class(class_info: ClassInfo) -> ClassSummary:
    """
    Generates a comprehensive summary for a class by calling the real LLM service.

    Args:
        class_info: A Pydantic model containing the parsed information
                    for the class, including its methods.

    Returns:
        A ClassSummary object containing the high-level class summary
        and a list of summaries for each of its methods.
    """
    # Reconstruct the class definition for the high-level summary.
    reconstructed_class_code = (
        f"class {class_info.name}:\n"
        f'    """{class_info.docstring}"""\n'
        f"    # ... methods and attributes ...\n"
    )

    # Generate the main summary for the class itself using the real LLM.
    class_summary_text = summarize_code_with_llm(
        code_text=reconstructed_class_code,
        question=CLASS_QUESTION
    )

    # Summarize each method within the class.
    method_summaries = []
    for method_info in class_info.methods:
        # NOTE: This is a temporary workaround. The parser does not yet
        # provide the raw source code for each method.
        reconstructed_method_code = (
            f"def {method_info.name}(self, ...):\n"
            f'    """{method_info.docstring}"""\n'
            f"    # ... method body ...\n"
        )
        
        method_summary = summarize_function(
            func_info=method_info,
            code_text=reconstructed_method_code
        )
        method_summaries.append(method_summary)

    # Assemble the final structured summary for the class.
    return ClassSummary(
        name=class_info.name,
        docstring=class_info.docstring,
        summary_text=class_summary_text,
        method_summaries=method_summaries
    )