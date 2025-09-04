# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel, Field
# from typing import Dict, List

# from backend.parser.scanner import scan_python_files
# from backend.nodes.parser_node import parser_node
# from backend.nodes.summary_node import summary_node
# from backend.graph_incremental import build_graph, GraphState
# from backend.summarizer.models import FileSummary

# # Define the router for summary-related endpoints
# router = APIRouter()

# # --- Pydantic Models for Request Bodies ---

# class SummarizeRequest(BaseModel):
#     """Defines the JSON body for the /summarize endpoint."""
#     directory: str = Field(..., alias="dir", description="The absolute path to the directory to summarize.")

# class SummarizeChangesRequest(BaseModel):
#     """Defines the JSON body for the /summarize-changes endpoint."""
#     old_hashes: Dict[str, str]
#     directory: str = Field(..., alias="dir", description="The absolute path to the directory to scan for changes.")

# # --- API Endpoints ---

# @router.post("/summarize", response_model=List[FileSummary])
# async def summarize_directory(request: SummarizeRequest):
#     """
#     Performs a full summarization of all Python files in a directory.
#     This is a "from-scratch" operation that does not use the incremental graph.
#     """
#     try:
#         # 1. Find all Python files in the target directory.
#         # all_files = scan_python_files(request.directory)
#         # if not all_files:
#         #     return []

#         # 2. Parse all the files.
#         parsed_files = parser_node(request.directory)

#         # 3. Summarize the parsed files.
#         summaries = summary_node(parsed_files)

#         return summaries
#     except Exception as e:
#         # Provide a meaningful error response if something goes wrong.
#         raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


# @router.post("/summarize_changes", response_model=List[FileSummary])
# async def summarize_changes(request: SummarizeChangesRequest):
#     """
#     Runs the incremental summarization graph to process only changed files.
#     """
#     try:
#         # 1. Build the incremental processing graph.
#         app = build_graph()

#         # 2. Define the initial state for the graph invocation.
#         initial_state: GraphState = {
#             "old_hashes": request.old_hashes,
#             "new_dir": request.directory,
#             "changed_files": {},
#             "parsed_files": [],
#             "summaries": []
#         }

#         # 3. Invoke the graph and get the final state.
#         final_state = app.invoke(initial_state)

#         # 4. Return the summaries from the final state.
#         return final_state.get("summaries", [])
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred during incremental summarization: {e}")
