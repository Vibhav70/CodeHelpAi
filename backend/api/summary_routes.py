from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict

# Import the main LangGraph application builder
from backend.graph_incremental2 import build_incremental_graph

# Import auth, DB, and CRUD functions
from backend.core.auth_utils import get_current_user
from backend.db.database import get_db
from backend.crud import project_crud
from backend.db import db_models

# --- Pydantic Model for the Ingestion Request Body ---
class IngestionRequest(BaseModel):
    directory: str

# --- API Router for Project-Specific Actions ---
router = APIRouter(
    prefix="/api/projects",
    tags=["Project Actions"],
    dependencies=[Depends(get_current_user)]
)

# --- Compile the LangGraph application on startup for efficiency ---
try:
    incremental_ingestion_app = build_incremental_graph()
    print("--- Incremental Ingestion Graph compiled successfully. ---")
except Exception as e:
    print(f"CRITICAL: Failed to compile incremental ingestion graph on startup: {e}")
    incremental_ingestion_app = None

# --- Ingestion Endpoint ---
@router.post("/{project_id}/ingest")
async def run_project_ingestion(
    project_id: int,
    request: IngestionRequest,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    """
    Triggers the full, end-to-end incremental ingestion pipeline for a project.
    This includes:
    1. Detecting granular code changes.
    2. Summarizing new/modified code.
    3. Saving summaries to a persistent JSON file.
    4. Updating the project's vector database with the changes.
    """
    # 1. Verify the project exists and the user has access.
    project = project_crud.get_project(db, project_id=project_id, user_id=current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or you do not have access.")

    if incremental_ingestion_app is None:
        raise HTTPException(
            status_code=500,
            detail="Ingestion pipeline is not available. Check server logs for errors."
        )

    try:
        # 2. Define the initial state to start the graph.
        initial_state = {
            "project_id": project_id,
            "directory": request.directory,
        }

        # 3. Asynchronously invoke the LangGraph pipeline.
        print(f"--- Starting ingestion pipeline for project: {project.name} (ID: {project_id}) ---")
        final_state = await incremental_ingestion_app.ainvoke(initial_state)

        # 4. Return a success response based on the final state of the graph.
        ingestion_status = final_state.get("vector_ingest_status", "unknown")
        change_count = len(final_state.get("changes", []))
        
        return {
            "message": f"Ingestion pipeline completed for project '{project.name}'.",
            "status": ingestion_status,
            "changes_detected": change_count
        }

    except Exception as e:
        error_detail = f"An error occurred during the ingestion pipeline: {e}"
        print(f"ERROR: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)

