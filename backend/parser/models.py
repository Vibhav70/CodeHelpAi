from pydantic import BaseModel
from typing import List, Optional

class FunctionInfo(BaseModel):
    """
    Represents a single function, including its full source code.
    """
    name: str
    docstring: Optional[str] = None
    source_code: str 

class ClassInfo(BaseModel):
    """
    Represents a single class, its methods, and its full source code.
    """
    name: str
    docstring: Optional[str] = None
    source_code: str 
    methods: List[FunctionInfo]

class FileParseResult(BaseModel):
    """
    Represents the complete parsed structure of a single Python file.
    """
    file_path: str
    classes: List[ClassInfo]
    functions: List[FunctionInfo]