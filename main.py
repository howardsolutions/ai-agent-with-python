import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

# Checking for argument passed in for the prompt
if len(sys.argv) < 1:
    print("No argument passed.")
    sys.exit(1)

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    
    user_prompt = sys.argv[1]
      
    # ROLES 
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    system_prompt = """
            You are a helpful AI coding agent.

            When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

            - List files and directories

            All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
            """
    
    # Function Declarations
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    generate_content = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    
    # Check for function calls
    if generate_content.candidates[0].content.parts[0].function_call:
        function_call_part = generate_content.candidates[0].content.parts[0].function_call
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(generate_content.text)
    
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {generate_content.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {generate_content.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
