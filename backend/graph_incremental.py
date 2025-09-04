from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel

# Import all the nodes for the graph
from backend.nodes.change_detection_node import change_detection_node, ChangedItem
from backend.nodes.summarize_changes_node import summarize_changes_node
from backend.nodes.vector_ingest_node import vector_ingest_node

# --- LangGraph State Definition ---
# This defines the "shared memory" that is passed between all the nodes in our graph.
class GraphState(TypedDict):
    project_id: int
    directory: str
    changes: List[ChangedItem]
    summaries: List[Dict[str, Any]]
    # Add status fields to track the outcome of each step
    ingestion_status: str
    vector_ingestion_status: str
    error_message: Optional[str]

# --- Graph Definition ---
from langgraph.graph import StateGraph, END

def build_incremental_ingestion_graph():
    """
    Builds and compiles the complete LangGraph for the incremental ingestion pipeline.
    """
    workflow = StateGraph(GraphState)

    # Add all the nodes to the graph
    workflow.add_node("detect_changes", change_detection_node)
    workflow.add_node("summarize", summarize_changes_node)
    workflow.add_node("ingest_to_vectorstore", vector_ingest_node)

    # Define the execution flow (the edges between the nodes)
    workflow.set_entry_point("detect_changes")
    workflow.add_edge("detect_changes", "summarize")
    workflow.add_edge("summarize", "ingest_to_vectorstore")
    workflow.add_edge("ingest_to_vectorstore", END)

    # Compile the graph into a runnable application
    return workflow.compile()

# Create a single, compiled instance of the graph to be used by the API
incremental_ingestion_app = build_incremental_ingestion_graph()

