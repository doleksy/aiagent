import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite a file with the specified content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    target = os.path.join(working_directory, file_path)
    target_abs = os.path.abspath(target)

    working_abs = os.path.abspath(working_directory)

    if not target_abs.startswith(working_abs):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(os.path.dirname(target_abs)):
        try:
            os.makedirs(os.path.dirname(target_abs))
        except FileExistsError as e:
            return f"Error: creating {target_abs}: {e}"
        

    try:
        with open(target_abs, "w") as f:
            f.write(content)
    except OSError as e:
        return f"Error: file writing error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

if __name__ == "__main__":
    print(write_file("../calculator", "blah/dolek.txt", "blah"))
