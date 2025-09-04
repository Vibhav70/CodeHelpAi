from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import Dict, Any

from backend.db import crud, db_models
from backend.core.auth_utils import get_current_user
from backend.db.database import get_db
from graph_incremental import create_incremental_ingestion_graph
from graph_query import create_query_graph

# Build graphs on startup
incremental_graph = create_incremental_ingestion_graph()
query_graph = create_query_graph()

router = APIRouter(
    prefix="/api/projects/{project_id}",
    tags=["Project Actions"],
    dependencies=[Depends(get_current_user)]
)

def get_project_and_verify_owner(project_id: int, db: Session, current_user: db_models.User):
    """Helper to get a project and verify the current user owns it."""
    project = crud.get_project(db, project_id=project_id, user_id=current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or you do not have permission")
    return project

@router.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
async def run_project_ingestion(
    project_id: int,
    directory: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    """
    Run the incremental ingestion and summarization pipeline for a specific project.
    """
    get_project_and_verify_owner(project_id, db, current_user)

    initial_state = {"project_id": project_id, "directory": directory}
    
    # Asynchronously invoke the ingestion graph.
    await incremental_graph.ainvoke(initial_state)

    return {"message": f"Ingestion process started for project {project_id}."}

@router.post("/ask", response_model=Dict[str, Any])
async def ask_project_question(
    project_id: int,
    question: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    """
    Ask a question about the codebase of a specific project.
    """
    get_project_and_verify_owner(project_id, db, current_user)

    initial_state = {"project_id": project_id, "question": question}
    final_state = await query_graph.ainvoke(initial_state)
    answer = final_state.get("answer", "Could not generate an answer.")
    
    # Log the query to the user's general history
    crud.create_user_query(db, user_id=current_user.id, question=question, answer=answer)
    
    return {"answer": answer}
