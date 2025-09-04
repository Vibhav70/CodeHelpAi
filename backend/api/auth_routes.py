# backend/api/auth_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.core import auth, auth_utils
from backend.db import db_models as db_models
from backend.db.database import get_db, engine

# Create database tables if they don't exist
db_models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/auth")


# --- Pydantic Models for Request Bodies ---
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# --- API Endpoints ---
@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(db_models.User).filter(db_models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = auth.get_password_hash(user.password)
    new_user = db_models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User {user.username} created successfully."}



# def login_for_access_token(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(db_models.User).filter(db_models.User.username == user.username).first()
#     if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = auth.create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
# 2. CHANGE THE FUNCTION SIGNATURE TO THIS
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # 3. ACCESS USERNAME AND PASSWORD FROM THE FORM DATA
    user = auth_utils.authenticate_user(
        db,
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create and return the token
    access_token = auth_utils.create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}