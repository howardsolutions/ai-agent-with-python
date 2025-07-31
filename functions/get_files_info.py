import os
from google.genai import types

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

def get_files_info(working_directory, directory="."):
    try:
        # Normalize paths
        working_directory = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, directory))

        # Validate boundary
        if not target_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Validate it's a directory
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        # Build result string
        result_lines = []
        for entry in os.listdir(target_path):
            entry_path = os.path.join(target_path, entry)
            is_dir = os.path.isdir(entry_path)
            file_size = os.path.getsize(entry_path)
            result_lines.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: {str(e)}"
