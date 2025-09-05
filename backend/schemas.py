
# from pydantic import BaseModel, Field, ConfigDict
# from datetime import datetime
# from typing import List, Optional


# # --- Project Schemas ---
# class ProjectBase(BaseModel):
#     name: str
#     description: Optional[str] = None

# class ProjectCreate(ProjectBase):
#     pass

# class Project(ProjectBase):
#     id: int
#     user_id: int
#     created_at: datetime

#     class Config:
#         orm_mode = True



# # --- Pydantic Models for Query History ---

# class QueryHistoryBase(BaseModel):
#     """Base model for query history, used for input and basic output."""
#     question: str
#     answer: str

# class QueryHistoryCreate(QueryHistoryBase):
#     """Model used specifically for creating a new history record in the DB."""
#     user_id: int
#     project_id: int

# class QueryHistory(QueryHistoryBase):
#     """
#     Model for representing a full query history record when reading from the API.
#     Includes all database fields.
#     """
#     id: int
#     user_id: int
#     timestamp: datetime
#     project_id: int

#     class Config:
#         # This allows Pydantic to read data from ORM models (like SQLAlchemy)
#         orm_mode = True


# # --- Pydantic Models for User ---

# class UserBase(BaseModel):
#     """Base model for a user, containing the username."""
#     username: str

# class UserCreate(UserBase):
#     """Model used for creating a new user, requires a password."""
#     password: str

# class User(UserBase):
#     """
#     Model for representing a full user record when reading from the API.
#     It includes the user's ID and their associated query history.
#     The password is not included for security.
#     """
#     id: int
#     created_at: datetime
#     history: List[QueryHistory] = []
#     projects: List[Project] = []
#     model_config = ConfigDict(from_attributes=True)

#     # class Config:
#     #     orm_mode = True

# # --- Pydantic Models for Authentication Tokens ---

# class Token(BaseModel):
#     """Model for the JWT access token returned on login."""
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     """Model for the data encoded within the JWT."""
#     username: Optional[str] = None


# backend/models.py

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# --- Pydantic Models for Project ---

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# --- Pydantic Models for Query History ---

class QueryHistoryBase(BaseModel):
    """Base model for query history, used for input and basic output."""
    question: str
    answer: str

class QueryHistoryCreate(QueryHistoryBase):
    """Model used specifically for creating a new history record in the DB."""
    user_id: int
    project_id: int # <-- This is the crucial, correct field.

class QueryHistory(QueryHistoryBase):
    """
    Model for representing a full query history record when reading from the API.
    Includes all database fields.
    """
    id: int
    user_id: int
    project_id: int
    timestamp: datetime

    class Config:
        orm_mode = True


# --- Pydantic Models for User ---

class UserBase(BaseModel):
    """Base model for a user, containing the username."""
    username: str

class UserCreate(UserBase):
    """Model used for creating a new user, requires a password."""
    password: str

class User(UserBase):
    """
    Model for representing a full user record when reading from the API.
    It includes the user's ID and their associated query history.
    The password is not included for security.
    """
    id: int
    created_at: datetime
    history: List[QueryHistory] = []
    projects: List[Project] = []

    class Config:
        orm_mode = True

# --- Pydantic Models for Authentication Tokens ---

class Token(BaseModel):
    """Model for the JWT access token returned on login."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Model for the data encoded within the JWT."""
    username: Optional[str] = None

