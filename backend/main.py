from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from backend.api import parse_routes, diff_routes, summary_routes, query_routes, auth_routes, history_routes
from backend.api import ingestion_routes, auth_routes, query_routes, project_routes2, admin_routes
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
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include the new routers. All routes will be available under the /api prefix.
# For example, the parse endpoint will be at http://localhost:8000/api/parse
# app.include_router(parse_routes.router, prefix="/api", tags=["Parsing"])
# app.include_router(diff_routes.router, prefix="/api", tags=["Diffing"])
# app.include_router(summary_routes.router, prefix="/api", tags=["Summarize"])
app.include_router(query_routes.router, prefix="/api", tags=["Query"])
app.include_router(auth_routes.router)
app.include_router(admin_routes.router)
# app.include_router(history_routes.router, prefix="/api", tags=["History"])
# app.include_router(ingestion_routes.router, prefix='/api', tags=["Summarize & Ingest"])
# app.include_router(summarize_changes.router, prefic="/api", tags=["summarize_changes"])
app.include_router(project_routes2.router)

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
