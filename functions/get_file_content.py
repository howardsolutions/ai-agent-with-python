import os
import sys

# Add the parent directory to the path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MAX_FILE_CONTENT_LENGTH

def get_file_content(working_directory, file_path):
    try:
        # Normalize paths
        working_directory = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Validate boundary
        if not file_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if file exists
        if not os.path.isfile(file_path):
            return f'Error: File "{file_path}" does not exist'

        # Read file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Check if content needs truncation
            if len(content) > MAX_FILE_CONTENT_LENGTH:
                truncated_content = content[:MAX_FILE_CONTENT_LENGTH]
                return truncated_content + f'\n[...File "{file_path}" truncated at {MAX_FILE_CONTENT_LENGTH} characters]'
            else:
                return content

    except Exception as e:
        return f"Error: {str(e)}"
