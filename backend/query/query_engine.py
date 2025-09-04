from typing import List, Dict, Any

# Import the VectorStore class (not an instance)
from backend.vectorstore.store import VectorStore

def search_relevant_summaries(project_id: int, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Searches the vector store for a given project for code summaries that are
    most relevant to the user's query.
    """
    print(f"--- Searching summaries for project_id '{project_id}' relevant to query: '{query}' ---")
    
    # 1. Instantiate the VectorStore for the specific project
    vector_store = VectorStore(project_id=project_id)
    
    # 2. Use the search method of the project-specific instance
    results = vector_store.search(query, top_k=top_k)
    
    print(f"Found {len(results)} relevant summaries.")
    return results

def format_context_for_llm(search_results: List[Dict[str, Any]]) -> str:
    """
    Formats the search results into a single string to be used as
    context for the language model.
    """
    if not search_results:
        return "No relevant context found in the codebase for this question."

    context_str = "Here is some relevant context from the codebase summaries:\n\n"
    for result in search_results:
        metadata = result['metadata']
        context_str += f"--- Context from file: {metadata.get('source', 'N/A')} ---\n"
        context_str += f"Type: {metadata.get('type', 'N/A')}\n"
        
        # Add class name if it's a method
        if metadata.get('type') == 'method':
            context_str += f"Class: {metadata.get('class', 'N/A')}\n"
            
        context_str += f"Name: {metadata.get('name', 'N/A')}\n"
        context_str += f"Summary: {result['text']}\n"
        context_str += "---\n\n"
        
    return context_str

