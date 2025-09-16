
from pydantic import BaseModel
from typing import List, Optional

class FunctionSummary(BaseModel):
    """
    Stores the generated summary for a single function.
    """
    file_path: str
    function_name: str
    summary: str
    source_code: str 

class ClassSummary(BaseModel):
    """
    Stores the generated summary for a single class.
    This could be expanded to include method summaries in the future.
    """
    file_path: str
    class_name: str
    summary: str
    source_code: str 

class MethodSummary(BaseModel):
    """
    Stores the generated summary for a method within a class.
    """
    file_path: str
    class_name: str
    method_name: str
    summary: str
    source_code: str 
