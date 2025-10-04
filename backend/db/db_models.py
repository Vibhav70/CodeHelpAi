
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    role = Column(String, default=UserRole.USER, nullable=False)
    history = relationship("QueryHistory", back_populates="owner")

    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")


class QueryHistory(Base):
    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False) 

    # Relationship to User
    owner = relationship("User", back_populates="history")
    project = relationship("Project", back_populates="query_history")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship back to the User
    owner = relationship("User", back_populates="projects")
    query_history = relationship("QueryHistory", back_populates="project", cascade="all, delete-orphan")
    documentation = relationship("ProjectDocumentation", back_populates="project", cascade="all, delete-orphan",uselist=False )


class ProjectDocumentation(Base):
    __tablename__ = "project_documentation"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False) # Stores the generated Markdown
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, unique=True)
    project = relationship("Project", back_populates="documentation")