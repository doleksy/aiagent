import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read from, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                )
            )
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    target = os.path.join(working_directory, file_path)
    target_abs = os.path.abspath(target)

    working_abs = os.path.abspath(working_directory)

    if not target_abs.startswith(working_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_abs):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        full_args = ["python", file_path, *args]
        print(f"cwd: {working_abs}")
        print(f"args={full_args}")
        result = subprocess.run(full_args, capture_output=True, cwd=working_directory, timeout=30)
        output = []
        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output.append(f"STDERR: {result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"

if __name__ == "__main__":
    print(run_python_file("../calculator", "main.py", ["3 + 5"]))
