from sqlalchemy.orm import Session
# Import your SQLAlchemy models (the file you wrote)
from backend.db import db_models 
# Import your Pydantic models (for type hinting and data validation)
import backend.schemas as pydantic_models 

# --- User CRUD Functions (You likely have these already) ---

def get_user_by_username(db: Session, username: str):
    return db.query(db_models.User).filter(db_models.User.username == username).first()

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

def create_user_query(db: Session, query: pydantic_models.QueryHistoryCreate):
    """
    Create and store a new QueryHistory record.
    """
    # Create a SQLAlchemy model instance from the Pydantic model data
    db_query = db_models.QueryHistory(
        question=query.question,
        answer=query.answer,
        user_id=query.user_id,
        project_id=query.project_id
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query