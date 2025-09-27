from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import your modules
from backend.db.database import get_db
from backend.crud import project_crud
from backend.documentation import docu_models as documentation_crud
from backend.core import auth_utils
from backend.db import db_models
from backend import schemas as pydantic_models
from backend.documentation import generator as documentation_service

router = APIRouter(
    prefix="/api/projects/{project_id}/documentation",
    tags=["Documentation"],
    dependencies=[Depends(auth_utils.get_current_user)]
)

@router.post("/generate", response_model=pydantic_models.ProjectDocumentation)
def generate_and_save_docs(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth_utils.get_current_user),
    project_name: str = None
    
):
    """
    Generates, saves, and returns the full Markdown documentation for a project.
    """
    # 1. Verify project ownership
    project = project_crud.get_project(db, project_id=project_id, user_id=current_user.id, project_name=project_name)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    # 2. Call the documentation service to generate the Markdown
    print(f"--- Generating documentation for project ID: {project_id} ---")
    markdown_content = documentation_service.generate_project_documentation(project_id,project_name=project.name)

    # 3. Save the new/updated documentation to the database
    db_documentation = documentation_crud.create_or_update_documentation(
        db, project_id=project_id, content=markdown_content
    )
    output_file = f"project_data/{project_id}/documentation.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"Documentation saved to: {output_file}")
    
    print(f"--- Documentation for project '{project.name}' saved successfully. ---")
    return db_documentation

@router.get("/", response_model=pydantic_models.ProjectDocumentation)
def get_project_docs(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth_utils.get_current_user)
):
    """
    Retrieves the most recently generated documentation for a project.
    """
    project = project_crud.get_project(db, project_id=project_id, user_id=current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
        
    documentation = documentation_crud.get_documentation_by_project(db, project_id=project_id)
    if not documentation:
        raise HTTPException(status_code=404, detail="No documentation has been generated for this project yet.")
        
    return documentation