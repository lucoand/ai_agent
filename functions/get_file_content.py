import os

def get_file_content(working_directory: str, file_path: str):
    # if file_path.startswith("/") or ".." in file_path:
    #     return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        working_directory_abs = os.path.abspath(working_directory)
    except Exception as e:
        return f'Error: Count not resolve path to "{working_directory}: {e}'
    try:
        path = os.path.abspath(os.path.join(working_directory, file_path))
    except Exception as e:
        return f'Error: Could not resolve path to {file_path}'
    if not path.startswith(working_directory_abs + os.sep):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(path):
        return f'Error: File not found or is not a regular file: "{path}"'
    MAX_CHARS = 10000

    try:
        with open(path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    except Exception as e:
        return f'Error: Could not open file "{path}": {e}'
    f.close()

    if len(file_content_string) == MAX_CHARS:
        file_content_string += f'\n[...File "{path}" truncated at 10000 characters]'

    return file_content_string
