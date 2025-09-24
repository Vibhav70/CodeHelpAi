from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from backend.api import parse_routes, diff_routes, summary_routes, query_routes, auth_routes, history_routes
from backend.api import ingestion_routes, auth_routes, query_routes, projects_routes, admin_routes,projects_query_routes,summary_routes
from sqlalchemy.orm import Session

from backend.db import db_models
from backend.db.database import engine



db_models.Base.metadata.create_all(bind=engine) # for creating db_models

# Create a FastAPI app instance
app = FastAPI(
    title="CodeHelp API",
    description="API for parsing and analyzing codebases.",
    version="0.1.0",
)

# --- START: ADD THIS FOR TESTING ---
@app.get("/test")
def read_test():
    """A simple test route to confirm the app is running."""
    return {"message": "Test route is working!"}
# --- END: ADD THIS FOR TESTING ---


origins = [
    "http://localhost:5173",  # Default Vite dev server port
    "http://localhost:3000",  # Common React dev server port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)

app.include_router(summary_routes.router)
app.include_router(query_routes.router)
app.include_router(auth_routes.router)
app.include_router(admin_routes.router)
app.include_router(projects_routes.router)

@app.get("/health")
def read_health():
    """
    A simple health check endpoint.
    Returns a JSON response indicating the service is running.
    """
    return {"status": "ok"}

# To run this application:
# 1. Make sure you are in the `backend` directory.
# 2. Run the command: uvicorn main:app --reload

#
# Notes

# ingest endpoint - end to end change detection -> summarization -> vector store update
# upload summaries endpoint - upload summaries to vector store first time
