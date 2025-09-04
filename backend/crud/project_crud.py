from sqlalchemy.orm import Session
from backend.db import db_models
import backend.schemas as pydantic_models

# --- Project CRUD Functions ---

def get_project_by_name(db: Session, name: str, user_id: int):
    """Retrieve a single project by its name for a specific user."""
    return db.query(db_models.Project).filter(
        db_models.Project.name == name,
        db_models.Project.user_id == user_id
    ).first()

def create_user_project(db: Session, project_data: dict, user_id: int):
    """Create a new project for a user from a dictionary."""
    db_project = db_models.Project(
        name=project_data['name'],
        description=project_data.get('description'),
        user_id=user_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def create_project(db: Session, project: pydantic_models.ProjectCreate, user_id: int):
    """Create a new project in the database for a specific user."""
    db_project = db_models.Project(**project.model_dump(), user_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_project(db: Session, project_id: int, user_id: int):
    """Retrieve a single project by its ID, ensuring it belongs to the user."""
    return db.query(db_models.Project).filter(
        db_models.Project.id == project_id,
        db_models.Project.user_id == user_id
    ).first()

def get_projects_by_user(db: Session, user_id: int):
    """Retrieve all projects owned by a specific user."""
    return db.query(db_models.Project).filter(db_models.Project.user_id == user_id).all()

def update_project(db: Session, project_id: int, project_update: pydantic_models.ProjectCreate, user_id: int):
    """Update a project's name and description."""
    db_project = get_project(db, project_id, user_id)
    if db_project:
        db_project.name = project_update.name
        db_project.description = project_update.description
        db.commit()
        db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int, user_id: int):
    """Delete a project from the database."""
    db_project = get_project(db, project_id, user_id)
    if db_project:
        db.delete(db_project)
        db.commit()
        return db_project
    return None

