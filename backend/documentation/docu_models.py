from sqlalchemy.orm import Session
from backend.db import db_models
from backend import schemas as pydantic_models

def create_or_update_documentation(
    db: Session, 
    project_id: int, 
    content: str
) -> db_models.ProjectDocumentation:
    """
    Creates new documentation for a project or updates it if it already exists.
    """
    # Check if documentation for this project already exists
    db_doc = db.query(db_models.ProjectDocumentation).filter(
        db_models.ProjectDocumentation.project_id == project_id
    ).first()

    if db_doc:
        db_doc.content = content
    else:
        # Create new documentation
        db_doc = db_models.ProjectDocumentation(
            content=content, 
            project_id=project_id
        )
        db.add(db_doc)
    
    db.commit()
    db.refresh(db_doc)
    return db_doc

def get_documentation_by_project(
    db: Session, 
    project_id: int
) -> db_models.ProjectDocumentation:
    """Retrieves the documentation for a specific project."""
    return db.query(db_models.ProjectDocumentation).filter(
        db_models.ProjectDocumentation.project_id == project_id
    ).first()
