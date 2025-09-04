
from backend.query.query_engine import QueryEngine
# Import the real LLM provider
from backend.llm.llm_provider import get_llm

def _format_context(search_results: list[dict]) -> str:
    """Formats the search results into a single string for the LLM context."""
    if not search_results:
        return "No relevant context found."
    
    context = ""
    for i, result in enumerate(search_results):
        content = result.get('content', 'No content available.')
        metadata = result.get('metadata', {})
        file = metadata.get('file_path', 'N/A')
        symbol = metadata.get('symbol_name', 'N/A')
        
        context += f"--- Context {i+1} (from {file}, symbol: {symbol}) ---\n"
        context += f"{content}\n\n"
        
    return context.strip()

def query_node(question: str) -> str:
    """
    A LangGraph node that performs the full RAG process.

    It retrieves relevant context from the vector store, constructs a prompt,
    and calls an LLM to generate a final answer to the user's question.

    Args:
        question: The user's natural language question.

    Returns:
        The generated answer from the LLM.
    """
    print(f"--- Query Node Triggered with question: '{question}' ---")
    
    # 1. Search for relevant summaries (Retrieval)
    engine = QueryEngine()
    search_results = engine.search_summaries(question, top_k=3)
    
    # 2. Concatenate results into a context string (Augmentation)
    context = _format_context(search_results)
    
    # 3. Construct the prompt for the LLM
    prompt = (
        "You are a helpful AI assistant for answering questions about a codebase.\n"
        "Please answer the following question based ONLY on the provided context.\n"
        "If the context does not contain the answer, state that you cannot answer.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {question}\n\n"
        "ANSWER:"
    )
    
    # 4. Pass context and question to LLM to generate an answer (Generation)
    print("\n--- Calling Real LLM (Gemini) ---")
    llm = get_llm()
    response = llm.invoke(prompt)
    answer = response.content
    
    print(f"Generated Answer: {answer}")
    return answer
