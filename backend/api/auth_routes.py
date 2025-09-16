from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.core import auth_utils
from backend.db.database import get_db

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Handles user login and returns a JWT access token.
    This endpoint is used by both regular users and admins.
    """
    user = auth_utils.authenticate_user(
        db,
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_utils.create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}