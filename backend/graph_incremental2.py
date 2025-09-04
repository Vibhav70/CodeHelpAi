from typing import TypedDict, List, Dict, Any, Union

from langgraph.graph import StateGraph, END

# --- Import Project-Aware Nodes ---
from backend.nodes.change_detection_node import change_detection_node
from backend.nodes.summarize_changes_node import summarize_changes_node
from backend.nodes.ingest_update_node2 import ingest_updates_node
from backend.nodes.vector_ingest_node import vector_ingest_node

# --- Import Data Models ---
from backend.diffing.code_change_detector import ChangedItem
from backend.summarizer.models import FunctionSummary, ClassSummary, MethodSummary

# --- Graph State Definition ---
# This TypedDict defines the "schema" of the data that flows through the graph.
class GraphState(TypedDict):
    project_id: int
    directory: str
    changes: List[ChangedItem]
    summaries: List[Union[FunctionSummary, ClassSummary, MethodSummary]]

# --- Graph Definition ---

def build_incremental_graph():
    """Builds and compiles the LangGraph for project-specific incremental ingestion."""
    workflow = StateGraph(GraphState)

    # Add all the nodes to the graph
    workflow.add_node("detect_changes", change_detection_node)
    workflow.add_node("summarize_changes", summarize_changes_node)
    workflow.add_node("ingest_text_updates", ingest_updates_node)
    workflow.add_node("ingest_vector_updates", vector_ingest_node)

    # Define the execution flow (edges)
    workflow.set_entry_point("detect_changes")
    workflow.add_edge("detect_changes", "summarize_changes")
    workflow.add_edge("summarize_changes", "ingest_text_updates")
    workflow.add_edge("ingest_text_updates", "ingest_vector_updates")
    workflow.add_edge("ingest_vector_updates", END)

    # Compile the graph into a runnable application
    return workflow.compile()

# --- Create a singleton instance of the compiled graph ---
# This is efficient as the graph is compiled only once when the server starts.
incremental_ingestion_app = build_incremental_graph()
