import hashlib
from .models import FileParseResult

def hash_string(content: str) -> str:
    """
    Generates a SHA256 hash for a given string content.
    """
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def create_hashes_from_parse_result(parse_result: FileParseResult) -> dict:
    """
    Creates a nested dictionary of hashes for each component in a parsed file.

    The structure will be:
    {
        "functions": { "func_name": "hash_of_func_source" },
        "classes": {
            "ClassName": {
                "source_hash": "hash_of_class_source",
                "methods": { "method_name": "hash_of_method_source" }
            }
        }
    }
    """
    file_hashes = {
        "functions": {},
        "classes": {}
    }

    # Hash top-level functions
    for func in parse_result.functions:
        file_hashes["functions"][func.name] = hash_string(func.source_code)

    # Hash classes and their methods
    for cls in parse_result.classes:
        class_details = {
            "source_hash": hash_string(cls.source_code),
            "methods": {}
        }
        for method in cls.methods:
            class_details["methods"][method.name] = hash_string(method.source_code)
        
        file_hashes["classes"][cls.name] = class_details

    return file_hashes