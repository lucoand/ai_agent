import os

def write_file(working_directory: str, file_path: str, content: str):
    # if file_path.startswith("/") or ".." in file_path:
    #     return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        working_directory_abs = os.path.abspath(working_directory)
    except Exception as e:
        return f'Error: Could not resolve absolute path to working directory "{working_directory}": {e}'
    try:
        path = os.path.abspath(os.path.join(working_directory, file_path))
    except Exception as e:
        return f'Error: Could not resolve absolute path to {file_path}'
    if not path.startswith(working_directory_abs + os.sep):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # if "/" in file_path:
    #     parts = file_path.split("/")
    #     temp_path = working_directory_abs
    #     for part in parts[:-1]:
    #         temp_path = os.path.join(temp_path, part)
    #     if not os.path.exists(temp_path):
    #         try:
    #             os.makedirs(temp_path)
    #         except Exception as e:
    #             return f'Error: Could not make directory "{temp_path}": {e}'
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except Exception as e:
        return f'Error: Could not make directory "{os.path.dirname(path)}": {e}'

    try:
        with open(path, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error: Could not write file "{path}": {e}'
    
    return f'Successfully wrote to "{path}" ({len(content)} characters written)'
