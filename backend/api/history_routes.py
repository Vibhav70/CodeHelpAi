
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from backend.core.auth_utils import get_current_user
from backend.db import db_models
from backend.db.database import get_db

router = APIRouter()

# --- Pydantic Model for Response ---
class HistoryItem(BaseModel):
    id: int
    question: str
    answer: str
    timestamp: datetime

    class Config:
        orm_mode = True

# --- API Endpoint ---
@router.get("/history", response_model=List[HistoryItem])
def get_user_history(
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    """
    Retrieves the query history for the currently logged-in user.
    """
    history = (
        db.query(db_models.QueryHistory)
        .filter(db_models.QueryHistory.user_id == current_user.id)
        .order_by(db_models.QueryHistory.timestamp.desc())
        .all()
    )
    return history