import os
import sys
from typing import Callable
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

functions: dict[str, Callable] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

working_directory = "./calculator"

def call_function(function_call_part: types.FunctionCall, verbose=False):
    if function_call_part.name is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name="None",
                    response={"error": f"Function name cannot be type: None"}
                )
            ]
        )
    function_name = function_call_part.name
    if function_call_part.args is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"{function_name} arguments cannot by type: None"}
                )
            ]
        )
    args = function_call_part.args
    output = f"Calling function: {function_name}"
    if verbose:
        output += f"({args})"
    print(output)
    if function_call_part.name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ]
        )
    args["working_directory"] = working_directory
    result = functions[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result}
            )
        ]
    )


load_dotenv()
if len(sys.argv) < 2:
    print("ERROR: Requires 1 argument")
    print('Usage: python3 main.py "What is python?"')
    exit(1)
user_prompt = sys.argv[1]
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons, however if you need to access the working directory itself please use "." to reference it.
"""
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",

            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of the specified file, constrained to the working directory.  Limited to the first 10,000 characters in the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory."
            )
        }
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to the specified file within the working directory, and creates the file and any necessary subdirectories if needed.  If the file already exists, it will be overwritten. 'file_path' must be listed first.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written into the file pointed to by 'file_path'."
            )
        }
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file.  Must be a .py file to be able to run.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be run, relative to the working directory."
            )
        }
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

verbose = False
if len(sys.argv) > 2:
    if sys.argv[2] == "--verbose":
        verbose = True

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

model_name = "gemini-2.0-flash-001"

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

prompt_tokens = ""
response_tokens = ""
MAX_ITER = 20

for i in range(MAX_ITER):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    if response.usage_metadata is not None:
        prompt_tokens = str(response.usage_metadata.prompt_token_count)
        response_tokens = str(response.usage_metadata.candidates_token_count)

    if response.candidates is not None:
        for candidate in response.candidates:
            if candidate.content is not None:
                messages.append(candidate.content)
    else:
        prompt_tokens = "0"
        response_tokens = "0"

    if verbose == True:
        print(f"User prompt: {user_prompt}\n")

    if response.function_calls is not None:
        function_call_part = response.function_calls[0]
        function_call_result = call_function(function_call_part, verbose)
        if function_call_result.parts is None:
            raise RuntimeError("Error: function_call_part.parts was type None.")
        if len(function_call_result.parts) < 1:
            raise RuntimeError("Error: function_call_result has no parts.")
        if function_call_result.parts[0].function_response is None:
            raise RuntimeError("Error: function_call_result.parts[0].function_response was type None.")
        if function_call_result.parts[0].function_response.response is None:
            raise RuntimeError("Error: function_call_result.parts[0].function_response.response was type None.")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        messages.append(function_call_result)
    else: 
        print("Final Response:")
        print(response.text)
        break
    if verbose:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

