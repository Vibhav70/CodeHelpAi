import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from backend.summarizer.models import FileSummary

# --- LLM Initialization ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_output_tokens=500 # Increased token limit for larger JSON output
)

# --- JSON Parser Setup ---
# We create a parser that expects a JSON output matching our FileSummary model.
parser = JsonOutputParser(pydantic_object=FileSummary)

# --- Prompt Template for JSON Output ---
# The prompt now includes instructions for the JSON format.
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert code assistant. Your task is to provide a comprehensive JSON summary "
            "of the given Python file. Analyze the file's overall purpose, its classes, and its functions. "
            "Provide a concise, high-level summary for each component. "
            "Format your response as a JSON object that strictly follows this schema:\n"
            "{format_instructions}",
        ),
        ("human", "Summarize the following Python file:\n\n```python\n{code_context}\n```"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# --- LangChain Chain Definition ---
chain = prompt | llm | parser

def get_structured_llm_summary(file_path: str, code_context: str) -> dict:
    """
    Invokes the LLM chain to get a structured JSON summary for a code file.

    Args:
        file_path: The path to the file being summarized.
        code_context: The full source code of the file.

    Returns:
        A dictionary matching the FileSummary Pydantic model.
    """
    print(f"--- Calling Gemini API for structured summary of {os.path.basename(file_path)} ---")
    try:
        response = chain.invoke({"code_context": code_context})
        return response
    except Exception as e:
        print(f"LLM call failed for {file_path}: {e}")
        return {
            "file_path": file_path,
            "summary_text": "Error: Could not generate summary.",
            "class_summaries": [],
            "function_summaries": [],
        }