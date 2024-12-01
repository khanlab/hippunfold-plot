import ast
import inspect
import os

def get_function_docstrings(module):
    functions = [obj for name, obj in inspect.getmembers(module) if inspect.isfunction(obj)]
    docstrings = {}
    for func in functions:
        docstrings[func.__name__] = inspect.getdoc(func)
    return docstrings

def update_readme(readme_path, docstrings):
    with open(readme_path, 'r') as file:
        lines = file.readlines()

    start_functions = lines.index("## 🛠️ Functions\n")
    end_functions = lines.index("## 🧪 Testing\n")

    new_lines = lines[:start_functions + 2]
    for func_name, docstring in docstrings.items():
        new_lines.append(f"### `{func_name}`\n\n")
        new_lines.append("```python\n")
        new_lines.append(f"{docstring}\n")
        new_lines.append("```\n\n")

    new_lines.extend(lines[end_functions:])

    with open(readme_path, 'w') as file:
        file.writelines(new_lines)

if __name__ == "__main__":
    import plotting
    readme_path = 'README.md'
    docstrings = get_function_docstrings(plotting)
    update_readme(readme_path, docstrings)