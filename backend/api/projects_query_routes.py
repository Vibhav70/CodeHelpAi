from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Import your project-specific modules
from backend.db.database import get_db
from backend.db import crud
from backend.core import auth_utils
from backend.db import db_models
from backend import schemas as pydantic_models
from backend.graph_query import create_query_graph # Import the RAG graph

router = APIRouter(
    prefix="/api/projects/{project_id}",
    tags=["Project Actions"],
    dependencies=[Depends(auth_utils.get_current_user)]
)

# Compile the RAG graph when the router is initialized
query_app = create_query_graph()

@router.post("/ask", response_model=pydantic_models.QueryHistory)
async def ask_project_question(
    project_id: int,
    request: pydantic_models.QueryHistoryBase, # Use a simple model for the question
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth_utils.get_current_user)
):
    """
    Receives a question for a project, gets an answer from the RAG pipeline,
    and saves the conversation to the history.
    """
    project = crud.get_project(db, project_id=project_id, user_id=current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    # Invoke the RAG graph to get an answer
    inputs = {"project_id": project_id, "question": request.question}
    final_state = await query_app.ainvoke(inputs)
    answer = final_state.get("answer", "Could not generate an answer.")

    # Save the new question and answer to the history
    history_to_create = pydantic_models.QueryHistoryCreate(
        question=request.question,
        answer=answer,
        user_id=current_user.id,
        project_id=project_id
    )
    new_history_entry = crud.create_user_query(db=db, query=history_to_create)
    return new_history_entry


@router.get("/history", response_model=List[pydantic_models.QueryHistory])
def get_project_conversation_history(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth_utils.get_current_user)
):
    """
    Retrieves the full conversation history for a specific project.
    """
    project = crud.get_project(db, project_id=project_id, user_id=current_user.id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
        
    return crud.get_history_by_project(db, project_id=project_id, user_id=current_user.id)

