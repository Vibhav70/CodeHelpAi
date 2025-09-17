from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import your models, CRUD functions, and security dependencies
from backend.db import db_models, crud
from backend.core import auth_utils
from backend.db.database import get_db
from backend import schemas as pydantic_models

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
    dependencies=[Depends(auth_utils.get_current_admin_user)] # Protect all routes
)

@router.post("/users", response_model=pydantic_models.User)
def create_user_by_admin(
    user_to_create: pydantic_models.UserCreate,
    db: Session = Depends(get_db)
):
    """Admin endpoint to create a new user."""
    db_user = crud.get_user_by_username(db, username=user_to_create.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = auth_utils.get_password_hash(user_to_create.password)
    return crud.create_user(db=db, username=user_to_create.username, hashed_password=hashed_password)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_admin(user_id: int, db: Session = Depends(get_db)):
    """Admin endpoint to delete a user."""
    # (Requires crud.delete_user function)
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id=user_id)
    return {"message": "User deleted successfully"}

@router.get("/users", response_model=List[pydantic_models.User])
def list_users_by_admin(db: Session = Depends(get_db)):
    """Admin endpoint to list all users."""
    # (Requires crud.get_users function)
    return crud.get_users(db)