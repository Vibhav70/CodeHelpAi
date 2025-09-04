import ast
from typing import List
from .models import ClassInfo, FunctionInfo, FileParseResult
import ast
from typing import List
from .models import ClassInfo, FunctionInfo, FileParseResult


def get_source_segment(source_lines: List[str], node: ast.AST) -> str:
    """
    Extracts the full source code of an AST node from the file's lines.
    AST nodes have `lineno` and `end_lineno` attributes.
    """
    # ast line numbers are 1-indexed, so we subtract 1 for list slicing
    start = node.lineno - 1
    end = node.end_lineno
    return "".join(source_lines[start:end])

def parse_file(file_path: str) -> FileParseResult:
    """
    Parses a Python file and extracts structured information for functions and classes,
    including their full source code.
    """
    with open(file_path, "r", encoding="utf-8") as source_file:
        source_lines = source_file.readlines()
        # Join lines to pass to ast.parse, which expects a single string
        source_code = "".join(source_lines)

    tree = ast.parse(source_code, filename=file_path)

    top_level_functions = []
    classes = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            # This is a top-level function
            func_info = FunctionInfo(
                name=node.name,
                docstring=ast.get_docstring(node),
                source_code=get_source_segment(source_lines, node)
            )
            top_level_functions.append(func_info)

        elif isinstance(node, ast.ClassDef):
            # This is a class
            methods = []
            for method_node in node.body:
                if isinstance(method_node, ast.FunctionDef):
                    method_info = FunctionInfo(
                        name=method_node.name,
                        docstring=ast.get_docstring(method_node),
                        source_code=get_source_segment(source_lines, method_node)
                    )
                    methods.append(method_info)
            
            class_info = ClassInfo(
                name=node.name,
                docstring=ast.get_docstring(node),
                source_code=get_source_segment(source_lines, node),
                methods=methods
            )
            classes.append(class_info)

    return FileParseResult(
        file_path=file_path,
        classes=classes,
        functions=top_level_functions
    )