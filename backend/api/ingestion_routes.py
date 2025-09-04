# backend/api/ingestion_routes.py

from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel

# Import the graph constructor and auth utilities
from backend.graph_incremental2 import build_incremental_graph
from backend.core.auth_utils import get_current_user
from backend.db.db_models import User

# --- Pydantic Model for the Request Body ---
class IngestRequest(BaseModel):
    directory: str

# --- API Router Initialization ---
router = APIRouter(
    prefix="/summarize",
    dependencies=[Depends(get_current_user)] # Protect this endpoint
)

# --- Pre-compile the graph on startup ---
try:
    ingestion_app = build_incremental_graph()
except Exception as e:
    print(f"Error compiling ingestion graph on startup: {e}")
    ingestion_app = None

# --- API Endpoint ---
@router.post("/run")
async def run_incremental_ingestion( # <-- Changed to async def
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
        
        # Run the graph asynchronously using ainvoke
        final_state = await ingestion_app.ainvoke(inputs) # <-- Changed to await ainvoke
        
        changes = final_state.get("changes", [])
        
        return {
            "message": f"Ingestion run complete for user {current_user.username}.",
            "detected_changes": len(changes),
            "changes": [change.dict() for change in changes] # Convert Pydantic models to dicts for JSON
        }
    except Exception as e:
        # Be specific about the error in the response for easier debugging
        error_detail = f"An error occurred during graph execution: {type(e).__name__} - {e}"
        print(error_detail)
        raise HTTPException(
            status_code=500,
            detail=error_detail
        )
