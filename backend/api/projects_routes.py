from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Import your project-specific modules
from backend.db.database import get_db
from backend.crud import project_crud
from backend.core import auth_utils
from backend.db import db_models
from backend import schemas as pydantic_models

router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"],
    dependencies=[Depends(auth_utils.get_current_user)] # Protect all routes in this file
)

@router.post("/", response_model=pydantic_models.Project)
def create_project_for_user(
    project: pydantic_models.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth_utils.get_current_user)
):
    """
    Create a new project for the currently authenticated user.
    """
    # Use .model_dump() for Pydantic v2
    return project_crud.create_project(db=db, project=project, user_id=current_user.id)


@router.get("/", response_model=List[pydantic_models.Project])
def read_user_projects(
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth_utils.get_current_user)
):
    """
    Retrieve all projects for the currently authenticated user.
    """
    projects = project_crud.get_projects_by_user(db, user_id=current_user.id)
    return projects

