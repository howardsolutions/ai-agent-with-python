import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=[]):
    try:
        # Normalize paths
        working_directory = os.path.abspath(working_directory)
        absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Validate boundary
        if not absolute_file_path.startswith(working_directory):
            return f'Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if file exists
        if not os.path.isfile(absolute_file_path):
            return f'File "{file_path}" not found.'

        # Check if file is a Python file
        if not absolute_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Execute the Python file
        result = subprocess.run(
            [sys.executable, absolute_file_path] + args,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Format output
        output_parts = []
        
        if result.stdout:
            output_parts.append(f"STDOUT: {result.stdout}")
        
        if result.stderr:
            output_parts.append(f"STDERR: {result.stderr}")
        
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        
        if not output_parts:
            return "No output produced."
        
        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: executing Python file: Timeout after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"
