import os
import sys
from typing import Dict, Any, Callable

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

# Checking for argument passed in for the prompt
if len(sys.argv) < 1:
    print("No argument passed.")
    sys.exit(1)

def create_function_mapping(working_directory: str) -> Dict[str, Callable]:
    """Create a mapping of function names to their execution functions."""
    return {
        "get_files_info": lambda args: get_files_info(working_directory, args.get("directory", ".")),
        "get_file_content": lambda args: get_file_content(working_directory, args.get("file_path")),
        "run_python_file": lambda args: run_python_file(working_directory, args.get("file_path"), args.get("args", [])),
        "write_file": lambda args: write_file(working_directory, args.get("file_path"), args.get("content")),
    }

def execute_function_call(function_name: str, function_args: Dict[str, Any], working_directory: str) -> str:
    """Execute a function call based on the function name and arguments."""
    function_mapping = create_function_mapping(working_directory)
    
    if function_name not in function_mapping:
        return f"Error: Unknown function {function_name}"
    
    try:
        return function_mapping[function_name](function_args)
    except Exception as e:
        return f"Error executing function: {str(e)}"

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    
    # Get current working directory for security
    working_directory = os.getcwd()
    
    user_prompt = sys.argv[1]
      
    # ROLES 
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
    
    # Function Declarations
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    generate_content = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    
    # Check for function calls and execute them
    if generate_content.candidates[0].content.parts[0].function_call:
        function_call_part = generate_content.candidates[0].content.parts[0].function_call
        function_name = function_call_part.name
        function_args = function_call_part.args
        
        print(f"Calling function: {function_name}({function_args})")
        
        result = execute_function_call(function_name, function_args, working_directory)
        print(f"Function result: {result}")
    else:
        print(generate_content.text)
    
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {generate_content.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {generate_content.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()