import os

from google.genai import types

from .config import FILE_CHARACTER_LIMIT

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read from, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    target = os.path.join(working_directory, file_path)
    target_abs = os.path.abspath(target)

    working_abs = os.path.abspath(working_directory)

    if not target_abs.startswith(working_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_abs, "r") as f:
            content_str = f.read(FILE_CHARACTER_LIMIT)
            if len(content_str) == FILE_CHARACTER_LIMIT:
                content_str += f'[...File "{file_path}" trancated at {FILE_CHARACTER_LIMIT} characters]'

            return content_str
    except OSError as e:
        return f"Error: file reading error: {e}"
    
if __name__ == "__main__":
    print(get_file_content("../calculator", "main.py"))
