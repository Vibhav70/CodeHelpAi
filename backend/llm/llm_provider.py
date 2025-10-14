# backend/llm_provider.py
import os
from dotenv import load_dotenv

# --- Imports for Google Gemini ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from backend.summarizer.models import FileSummary # Assuming this is the correct path

# Load environment variables from .env file at the project root
load_dotenv()

# --- 1. General Purpose LLM for Q&A ---

def get_llm():
    """
    Initializes and returns a general-purpose LangChain LLM provider for Q&A.

    This function loads the Google API key and initializes the ChatGoogleGenerativeAI
    model, which is suitable for the RAG (Retrieval-Augmented Generation) query node.

    Returns:
        An instance of the ChatGoogleGenerativeAI model.
    """
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")

    # Initialize the Gemini model with a low temperature for factual, consistent answers
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.1)
    return llm

# --- 2. Specialized LLM Chain for Structured Summarization ---

def get_summarization_chain():
    """
    Initializes and returns a specialized LangChain chain for code summarization.

    This function sets up a Google Gemini model with a prompt and a JSON output
    parser to ensure the output strictly matches the `FileSummary` Pydantic model.

    Returns:
        A LangChain runnable chain object.
    """
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")

    # Initialize the Gemini model for structured output
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        max_output_tokens=500
    )

    # Create a parser that expects a JSON output matching our FileSummary model
    parser = JsonOutputParser(pydantic_object=FileSummary)

    # Create the prompt template with instructions for the JSON format
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

    # Define the full LangChain chain
    chain = prompt | llm | parser
    return chain