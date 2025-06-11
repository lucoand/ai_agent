import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
if len(sys.argv) < 2:
    print("ERROR: Requires 1 argument")
    print('Usage: python3 main.py "What is python?"')
    exit(1)
user_prompt = sys.argv[1]
system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

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

response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt)
)
if response.usage_metadata is not None:
    prompt_tokens = str(response.usage_metadata.prompt_token_count)
    response_tokens = str(response.usage_metadata.candidates_token_count)
else:
    prompt_tokens = "0"
    response_tokens = "0"

if verbose == True:
    print(f"User prompt: {user_prompt}\n")

print(response.text)
if verbose == True:
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")

