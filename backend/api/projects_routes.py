from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.db import crud, db_models
import backend.schemas as pydantic_models
from backend.core.auth_utils import get_current_user
from backend.db.database import get_db
# Placeholder for the vector store deletion logic
# from ..vectorstore.store import delete_vector_store_for_project

router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=pydantic_models.Project, status_code=status.HTTP_201_CREATED)
def create_new_project(
    project: pydantic_models.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    """Create a new project for the currently logged-in user."""
    return crud.create_project(db=db, project=project, user_id=current_user.id)

@router.get("/", response_model=List[pydantic_models.Project])
def read_user_projects(
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    """List all projects for the currently logged-in user."""
    return crud.get_projects_by_user(db=db, user_id=current_user.id)

@router.get("/{project_id}", response_model=pydantic_models.Project)
def read_single_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    """Retrieve details for a specific project."""
    db_project = crud.get_project(db=db, project_id=project_id, user_id=current_user.id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.put("/{project_id}", response_model=pydantic_models.Project)
def update_existing_project(
    project_id: int,
    project: pydantic_models.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    """Update a project's name and/or description."""
    db_project = crud.update_project(db=db, project_id=project_id, project_update=project, user_id=current_user.id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    """Delete a project and its associated vector data."""
    deleted_project = crud.delete_project(db=db, project_id=project_id, user_id=current_user.id)
    if deleted_project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # --- IMPORTANT ---
    # Here you would call a function to delete the associated vector store.
    # This is a placeholder for that logic.
    # delete_vector_store_for_project(project_id)
    # -----------------

    return