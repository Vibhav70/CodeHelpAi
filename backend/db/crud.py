from sqlalchemy.orm import Session
# Import your SQLAlchemy models (the file you wrote)
from backend.db import db_models 
# Import your Pydantic models (for type hinting and data validation)
import backend.schemas as pydantic_models 

#-------------------------USER CRUD FUNCTIONS-------------------------#

def get_user_by_username(db: Session, username: str):
    """Retrieve a single user by their username."""
    return db.query(db_models.User).filter(db_models.User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    """Retrieve a single user by their ID."""
    return db.query(db_models.User).filter(db_models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve a list of all users."""
    return db.query(db_models.User).offset(skip).limit(limit).all()

def create_user(db: Session, username: str, hashed_password: str):
    """
    Create a new user in the database.
    Note: The role will default to 'user' as defined in the db_models.py.
    The create_admin.py script is the only place that should set the 'admin' role.
    """
    db_user = db_models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Delete a user from the database by their ID."""
    db_user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# --- QueryHistory CRUD Functions ---

def get_user_queries(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """
    Retrieve all query history records for a specific user.
    Orders by the most recent timestamp first.
    """
    return db.query(db_models.QueryHistory)\
             .filter(db_models.QueryHistory.user_id == user_id)\
             .order_by(db_models.QueryHistory.timestamp.desc())\
             .offset(skip)\
             .limit(limit)\
             .all()

# def create_user_query(db: Session, query: pydantic_models.QueryHistoryCreate):
#     """
#     Create and store a new QueryHistory record.
#     """
#     # Create a SQLAlchemy model instance from the Pydantic model data
#     db_query = db_models.QueryHistory(
#         question=query.question,
#         answer=query.answer,
#         user_id=query.user_id,
#         project_id=query.project_id
#     )
#     db.add(db_query)
#     db.commit()
#     db.refresh(db_query)
#     return db_query


#-------------------------PROJECT CRUD FUNCTIONS (NEW)-------------------------#

def create_project(db: Session, project: pydantic_models.ProjectCreate, user_id: int):
    """Create a new project for a specific user."""
    db_project = db_models.Project(**project.model_dump(), user_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_project(db: Session, project_id: int, user_id: int):
    """Retrieve a single project, ensuring it belongs to the specified user."""
    return db.query(db_models.Project).filter(
        db_models.Project.id == project_id,
        db_models.Project.user_id == user_id
    ).first()

def get_projects_by_user(db: Session, user_id: int):
    """Retrieve all projects for a specific user."""
    return db.query(db_models.Project).filter(db_models.Project.user_id == user_id).all()


#-------------------------QUERY HISTORY CRUD FUNCTIONS (UPDATED)-------------------------#

def create_user_query(db: Session, query: pydantic_models.QueryHistoryCreate):
    """Create and store a new QueryHistory record."""
    db_query = db_models.QueryHistory(**query.model_dump())
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query

def get_history_by_project(db: Session, project_id: int, user_id: int):
    """Retrieve all query history for a specific project, ensuring user ownership."""
    return db.query(db_models.QueryHistory).filter(
        db_models.QueryHistory.project_id == project_id,
        db_models.QueryHistory.user_id == user_id
    ).order_by(db_models.QueryHistory.timestamp.asc()).all()
