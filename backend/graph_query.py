from typing import TypedDict, List, Dict, Any

from langgraph.graph import StateGraph, END

# --- LLM and LangChain Imports ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# --- Import our custom query engine components ---
from .query.query_engine import search_relevant_summaries, format_context_for_llm

# --- LangGraph State Definition ---
class RAGGraphState(TypedDict):
    """
    Represents the state of our RAG graph.
    - project_id: The ID of the project being queried.
    - question: The user's input question.
    - context: The relevant summaries retrieved from the vector store.
    - answer: The final, LLM-generated answer.
    """
    project_id: int
    question: str
    context: str
    answer: str

# --- LLM Chain for Answer Generation ---
# 1. Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

# 2. Define the prompt for the final answer generation
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert code assistant. Use the following context from the codebase summaries to answer the user's question. If the context doesn't contain the answer, state that you couldn't find the information in the provided summaries."),
    ("human", "Context:\n\n{context}\n\nQuestion: {question}"),
])

# 3. Create the chain
rag_chain = rag_prompt | llm | StrOutputParser()

# --- LangGraph Nodes (Now Asynchronous) ---

async def retrieve_node(state: RAGGraphState) -> RAGGraphState:
    """
    Retrieves relevant context from the vector store based on the question.
    """
    print("--- RAG Graph: Retrieving Context ---")
    project_id = state['project_id']
    question = state['question']
    
    # Search for relevant summaries in the project-specific vector store
    search_results = search_relevant_summaries(project_id, question, top_k=5)
    
    # Format the results into a single context string
    context = format_context_for_llm(search_results)
    
    return {**state, "context": context}

async def generate_node(state: RAGGraphState) -> RAGGraphState:
    """
    Generates an answer using the LLM based on the retrieved context.
    """
    print("--- RAG Graph: Generating Answer ---")
    question = state['question']
    context = state['context']
    
    # Asynchronously generate the answer using the RAG chain
    answer = await rag_chain.ainvoke({"question": question, "context": context})
    
    return {**state, "answer": answer}

# --- Graph Definition ---

def create_query_graph():
    """
    Builds and compiles the LangGraph for the RAG query pipeline.
    """
    workflow = StateGraph(RAGGraphState)

    # Add the nodes to the graph
    workflow.add_node("retriever", retrieve_node)
    workflow.add_node("generator", generate_node)

    # Define the execution flow
    workflow.set_entry_point("retriever")
    workflow.add_edge("retriever", "generator")
    workflow.add_edge("generator", END)

    # Compile the graph
    app = workflow.compile()
    print("Async RAG Query Graph compiled successfully.")
    return app

# Create a single, compiled instance of the graph to be used by the API
query_app = create_query_graph()