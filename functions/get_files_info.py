import os
from typing import Optional

def get_files_info(working_directory: str, directory: Optional[str] = None) -> str:
    if directory is None:
        directory = "."
    # if directory.startswith("/") or ".." in directory:
    #     return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    try:
        working_directory_abs = os.path.abspath(working_directory)
    except Exception as e:
        return f'Error: Could not resolve working directory "{working_directory}". {e}'
    try:
        path = os.path.abspath(os.path.join(working_directory, directory))
    except Exception as e:
        return f'Error: Could not resolve "{directory}"'
    # print(path)
    if not path.startswith(working_directory_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(path):
        return f'Error: "{path}" is not a directory'
    try:
        contents = os.listdir(path)
    except Exception as e:
        return f"Error: Could not get contents of directory {path}: {e}"
    results = ""
    for item in contents:
        file_path = os.path.join(path, item)
        try:
            file_size = str(os.path.getsize(file_path))
        except Exception as e:
            return f"Error: Could not get file size for {file_path}: {e}"
        try:
            is_dir = str(os.path.isdir(file_path))
        except Exception as e:
            return f"Error: Could not determine if {file_path}: was a directory or a normal file: {e}"
        results += f"- {item}: file_size={file_size} bytes, is_dir={is_dir}\n"
    return results
