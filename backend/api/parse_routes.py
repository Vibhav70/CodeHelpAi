from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import os

# To make imports work correctly, run the app from the `backend` directory.
from backend.nodes.parser_node import parser_node
from backend.parser.models import FileParseResult

router = APIRouter()

class ParseRequest(BaseModel):
    """Defines the expected JSON body for a parse request."""
    dir: str

@router.post("/parse", response_model=List[FileParseResult])
def parse_directory(request: ParseRequest):
    """
    Endpoint to parse all Python files in a given directory.

    It receives a directory path, validates it, and then runs the parser_node
    to scan and parse all .py files within it.
    """
    # Basic security check: ensure the path exists and is a directory
    if not os.path.isdir(request.dir):
        raise HTTPException(status_code=404, detail=f"Directory not found: {request.dir}")
    
    # Run the full parsing process on the directory
    results = parser_node(request.dir)
    return results