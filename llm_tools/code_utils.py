"""
Miscellaneous small functions and useful snippets whose definitions were moved here so as to 
not clutter or distract from the workhorse code where they are used, or to designate
functions as potentially generally useful outside of this project.
"""

import ast
from pathlib import Path

def extract_functions(source: str) -> list:
    """
    Given a string of source code, extract the names and arguments of all functions defined in that source code.

    1. Parse the source code string into an Abstract Syntax Tree (AST) using the built-in `ast.parse()` function.
    2. Use the built-in `ast.walk()` function to traverse the AST and identify all `FunctionDef` nodes.
    3. For each `FunctionDef` node, extract the name of the function and the names of its arguments using the `node.name` and `node.args.args` attributes, respectively.
    4. Return a list of strings, where each string represents the name of a function followed by a comma-separated list of its arguments.
    """
    functions = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.FunctionDef):
            functions.append(f"{node.name}({', '.join(arg.arg for arg in node.args.args)})")
    return functions


def map_project() -> dict:
    """
    Traverse the current directory and its subdirectories, identifying all files with a `.py` extension and generating a
    mapping from each file name to its relative path, the number of tokens it contains, its docstring (if any), and the
    names and arguments of all functions defined in the file.
    """
    mapping = {}
    #supported_extensions=['.py']
    #for file in Path('.').rglob('*.*'):
    for file in Path('.').rglob('*.py'):
        if not file.is_file():
            continue
        with open(file) as f:
            source = f.read()
        num_tokens = len(source)
        functions = extract_functions(source)
        docstring = ast.get_docstring(ast.parse(source))

        record = f"path: {str(file)}\n" \
                 f"number of tokens: {num_tokens}\n"
        if docstring:
            record += f"docstring: {docstring}\n"
        record += f"functions: {', '.join(functions)}\n"

        mapping[record['path']] = record
    return mapping
