from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

# --- Project-specific Imports ---
from backend.db.database import get_db
from backend.crud import project_crud
from backend.core import auth_utils
from backend.db import db_models

# Import the compiled LangGraph application
from backend.graph_incremental2 import incremental_ingestion_app

# --- Pydantic Models for API Request ---

class IngestRequest(BaseModel):
    """Request body for the project ingestion endpoint."""
    project_name: str
    directory: str

# --- API Router Initialization ---

router = APIRouter(
    prefix="/api",
    tags=["Ingestion"],
    dependencies=[Depends(auth_utils.get_current_user)]
)

# --- API Endpoint ---

@router.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
async def run_ingestion_for_project(
    request: IngestRequest,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth_utils.get_current_user)
):
    """
    Triggers the incremental ingestion pipeline for a project.
    If a project with the given name doesn't exist, it will be created.
    """
    # 1. Find the project by name for the current user.
    # Note: This assumes a `get_project_by_name` function exists in your CRUD file.
    project = project_crud.get_project_by_name(db, name=request.project_name, user_id=current_user.id)

    # 2. If the project doesn't exist, create it.
    if not project:
        print(f"Project '{request.project_name}' not found. Creating a new one.")
        project_data = {"name": request.project_name, "description": "Auto-created during ingestion."}
        project = project_crud.create_user_project(db=db, project_data=project_data, user_id=current_user.id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create a new project."
            )

    # 3. Define the initial state to start the graph
    initial_state = {
        "project_id": project.id,
        "directory": request.directory
    }

    # 4. Asynchronously invoke the LangGraph application
    try:
        await incremental_ingestion_app.ainvoke(initial_state)
    except Exception as e:
        print(f"Error invoking ingestion graph for project {project.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start ingestion process: {e}"
        )

    return {"message": f"Ingestion process started for project '{project.name}' (ID: {project.id})."}

