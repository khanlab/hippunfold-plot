import ast
import inspect
import os
from pdoc.docstrings import numpy as numpy_docstring_to_markdown



def get_function_docstrings(module, function_names=None):
    """
    Get docstrings for specific functions in a module or all functions if no names are specified.

    Args:
        module: The module object containing the functions.
        function_names (list of str, optional): List of function names to retrieve docstrings for. 
                                                If None, retrieves all functions.

    Returns:
        dict: A dictionary mapping function names to their docstrings.
    """
    # Get all functions in the module
    functions = [obj for name, obj in inspect.getmembers(module) if inspect.isfunction(obj)]
    
    docstrings = {}
    for func in functions:
        # If a list of function names is provided, filter functions
        if function_names is None or func.__name__ in function_names:
            docstrings[func.__name__] = numpy_docstring_to_markdown(inspect.getdoc(func))
    
    return docstrings

def update_readme(readme_path, docstrings):
    with open(readme_path, 'r') as file:
        lines = file.readlines()

    start_functions = lines.index("## 🛠️ Functions\n")
    end_functions = lines.index("## 🧪 Testing\n")

    new_lines = lines[:start_functions + 2]
    for func_name, docstring in docstrings.items():
        new_lines.append(f"### `{func_name}`\n\n")
        new_lines.append(f"{docstring}\n")

    new_lines.extend(lines[end_functions:])

    with open(readme_path, 'w') as file:
        file.writelines(new_lines)

if __name__ == "__main__":
    import hippunfold_plot.plotting as plotting
    readme_path = 'README.md'
    docstrings = get_function_docstrings(plotting,['plot_hipp_surf'])
    update_readme(readme_path, docstrings)
