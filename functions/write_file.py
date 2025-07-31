import os

def write_file(working_directory, file_path, content):
    try:
        # Normalize paths
        working_directory = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Validate boundary
        if not file_path.startswith(working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Write content to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}" 