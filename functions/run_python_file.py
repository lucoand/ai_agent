import os
import subprocess

def run_python_file(working_directory: str, file_path: str):
    try:
        working_directory_abs = os.path.abspath(working_directory)
    except Exception as e:
        return f'Error: Could not resolve absolute path to "{working_directory}": {e}'
    try:
        file_path_abs = os.path.abspath(os.path.join(working_directory, file_path))
    except Exception as e:
        return f'Error: Could not resolve absolute path to "{file_path}": {e}'
    if not file_path_abs.startswith(working_directory_abs + os.sep):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(file_path_abs):
        return f'Error: File "{file_path}" not found.'

    if not file_path_abs.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    directory = os.path.dirname(file_path_abs)
    file = os.path.basename(file_path_abs)

    try:
        result = subprocess.run(
            ["python", file],
            cwd=directory,
            timeout=30,
            capture_output=True,
            text=True
        )
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
    retval = ""
    if result.stdout == "" and result.stderr == "":
        retval += "No output produced.\n"
    else:
        retval += f"STDOUT: {result.stdout}\n"
        retval += f"STDERR: {result.stderr}\n"
    if result.returncode != 0:
        retval += f"Process exited with code {result.returncode}\n"
    return retval

