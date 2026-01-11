import os
import subprocess
import sys

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Arguments to pass to the Python file",
                ),
                description="Arguments to pass to the Python file",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(path, file_path))
        valid_target_file = os.path.commonpath([path, target_file]) == path
        
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
            
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
            
        command = [sys.executable, target_file]
        if args:
            command.extend(args)
            
        result = subprocess.run(
            command,
            cwd=os.path.dirname(target_file),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
            
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        else:
            if result.stdout:
                output.append(f"STDOUT:\n{result.stdout.strip()}")
            if result.stderr:
                output.append(f"STDERR:\n{result.stderr.strip()}")
                
        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"
