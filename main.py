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
if len(sys.argv) < 2:
    print("Usage: python main.py <prompt> [--verbose]")
    sys.exit(1)

def call_function(function_call_part, verbose=False):
    """Handle the abstract task of calling one of our four functions."""
    function_name = function_call_part.name
    function_args = function_call_part.args
    
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")
    
    # Add working_directory to the arguments
    function_args["working_directory"] = "./calculator"
    
    # Dictionary mapping function names to their actual functions
    function_mapping = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    # Check if function name is valid
    if function_name not in function_mapping:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Call the function with keyword arguments
    try:
        function_result = function_mapping[function_name](**function_args)
        
        # Return types.Content with from_function_response describing the result
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error executing function: {str(e)}"},
                )
            ],
        )

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    
    # Parse command line arguments
    args = sys.argv[1:]
    verbose = "--verbose" in args
    user_prompt = args[0] if args[0] != "--verbose" else args[1]
      
    # Initialize messages list with user prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, you MUST use the available functions to gather information and answer the question. Do not try to answer based on general knowledge alone.

        You can perform the following operations:
        - List files and directories using get_files_info
        - Read file contents using get_file_content
        - Execute Python files with optional arguments using run_python_file
        - Write or overwrite files using write_file

        IMPORTANT: Always use the appropriate functions to explore the codebase and gather information before providing your final answer.

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

    # Main agent loop - limit to 20 iterations to prevent infinite loops
    max_iterations = 20
    for iteration in range(max_iterations):
        try:
            # Generate content with the entire messages list
            generate_content = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
            )
            
            if verbose:
                print(f"Iteration {iteration + 1}: Generated response")
            
            # Add the candidate response to messages
            for candidate in generate_content.candidates:
                messages.append(candidate.content)
            
            # Check if this is a final response (no function call)
            has_function_call = False
            for part in generate_content.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    has_function_call = True
                    break
            
            if not has_function_call:
                # This is the final response, print it and break
                if verbose:
                    print("No function call detected - final response")
                print(generate_content.text)
                break
            
            # Handle function call
            function_call_part = None
            for part in generate_content.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    function_call_part = part.function_call
                    break
            
            if function_call_part:
                # Use call_function to execute the function
                function_call_result = call_function(function_call_part, verbose=verbose)
            
                # Verify the response structure
                if not hasattr(function_call_result.parts[0], 'function_response') or not hasattr(function_call_result.parts[0].function_response, 'response'):
                    raise Exception("Invalid function call result structure")
                
                # Print the result if verbose is set
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                
                # Add the function response to messages
                messages.append(function_call_result)
            
        except Exception as e:
            print(f"Error in iteration {iteration + 1}: {str(e)}")
            break
    
    # Check if we hit the iteration limit
    if iteration == max_iterations - 1:
        print(f"Warning: Reached maximum iterations ({max_iterations})")
    
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {generate_content.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {generate_content.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()