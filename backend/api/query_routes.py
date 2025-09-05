from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Import the LangGraph applications
from backend import graph_incremental2 as incremental_app
from backend.graph_query import query_app

# Import auth, DB, and CRUD functions
from backend.core.auth_utils import get_current_user
from backend.db.database import get_db
from backend.crud import project_crud
from backend.db import crud as history_crud
from backend.db import db_models
from backend import schemas as pydantic_models
from backend.vectorstore.ingest import ingest_summaries_to_vector_store

# --- Pydantic Models for Request Bodies ---

class IngestRequest(BaseModel):
    directory: str

class AskRequest(BaseModel):
    question: str

class UploadResponse(BaseModel):
    message: str
    ingested: int

# --- API Router for Project-Specific Actions ---
router = APIRouter(
    prefix="/api/projects/{project_id}",
    dependencies=[Depends(get_current_user)] # Protect all routes
)

# --- Ingestion Endpoint ---
@router.post("/ingest")
async def run_project_ingestion(
    project_id: int,
    request: IngestRequest,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    """
    Triggers the full, end-to-end incremental ingestion pipeline for a project.
    This includes code diffing, summarization, and vector store updates.
    """
    # 1. Verify the project exists and the user has access
    project = project_crud.get_project(db, project_id=project_id, user_id=current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or you do not have access.")

    try:
        # 2. Invoke the incremental ingestion graph
        inputs = {"project_id": project_id, "directory": request.directory}
        final_state = await incremental_app.ainvoke(inputs)
        
        # Extract the final status from the graph's output
        ingestion_status = final_state.get("vector_ingestion_status", "unknown")
        
        return {
            "message": f"Ingestion pipeline completed for project '{project.name}'.",
            "status": ingestion_status
        }

    except Exception as e:
        error_detail = f"An error occurred during the ingestion pipeline: {e}"
        print(error_detail)
        raise HTTPException(status_code=500, detail=error_detail)


# --- Query Endpoint ---
@router.post("/ask")
async def ask_question(
    project_id: int,
    request: AskRequest,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    """
    Receives a question for a specific project, runs it through the RAG pipeline,
    and logs the interaction to the project's history.
    """
    # 1. Verify the project exists and the user has access
    project = project_crud.get_project(db, project_id=project_id, user_id=current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or you do not have access.")

    if query_app is None:
        raise HTTPException(
            status_code=500,
            detail="RAG query graph is not available. Check server logs."
        )

    try:
        # 2. Invoke the graph with the project_id and question
        inputs = {"project_id": project_id, "question": request.question}
        final_state = await query_app.ainvoke(inputs)
        answer = final_state.get("answer", "Could not generate an answer.")

        # 3. Log the history with the project_id
        history_data = pydantic_models.QueryHistoryCreate(
            question=request.question,
            answer=answer,
            user_id=current_user.id,
            project_id=project_id
        )
        history_crud.create_user_query(db=db, query=history_data)

        return {"answer": answer}

    except Exception as e:
        error_detail = f"An error occurred during query graph execution: {e}"
        print(error_detail)
        raise HTTPException(status_code=500, detail=error_detail)


# --- Upload saved summaries to vector DB ---
@router.post("/upload-summaries", response_model=UploadResponse)
async def upload_project_summaries(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    """
    Reads saved summaries for the project from project_data/<id>/summaries_db.json
    and uploads them into the project's vector database index.
    """
    # Verify access
    project = project_crud.get_project(db, project_id=project_id, user_id=current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or you do not have access.")

    try:
        ingested = ingest_summaries_to_vector_store(project_id)
        return UploadResponse(message=f"Uploaded summaries to vector DB for project '{project.name}'.", ingested=ingested)
    except Exception as e:
        error_detail = f"Failed to upload summaries to vector DB: {e}"
        print(error_detail)
        raise HTTPException(status_code=500, detail=error_detail)

