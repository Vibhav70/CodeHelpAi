# backend/api/ingestion_routes.py

from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel

# Import the graph constructor and auth utilities
from backend.graph_incremental import create_incremental_ingestion_graph
from backend.core.auth_utils import get_current_user
from backend.db.db_models import User

# --- Pydantic Model for the Request Body ---
class IngestRequest(BaseModel):
    directory: str

# --- API Router Initialization ---
router = APIRouter(
    prefix="/api/ingestion",
    tags=["Ingestion"],
    dependencies=[Depends(get_current_user)] # Protect this endpoint
)

# --- Pre-compile the graph on startup ---
try:
    ingestion_app = create_incremental_ingestion_graph()
except Exception as e:
    print(f"Error compiling ingestion graph on startup: {e}")
    ingestion_app = None

# --- API Endpoint ---
@router.post("/run")
def run_incremental_ingestion(
    request: IngestRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Triggers the incremental ingestion and change detection graph.
    """
    if ingestion_app is None:
        raise HTTPException(
            status_code=500,
            detail="Ingestion graph is not available. Check server logs."
        )
    
    try:
        # The initial state for the graph
        inputs = {"directory": request.directory}
        
        # Run the graph. The final state will contain the list of changes.
        final_state = ingestion_app.invoke(inputs)
        
        changes = final_state.get("changes", [])
        
        return {
            "message": f"Ingestion run complete for user {current_user.username}.",
            "detected_changes": len(changes),
            "changes": [change.dict() for change in changes] # Convert Pydantic models to dicts for JSON
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during graph execution: {e}"
        )
