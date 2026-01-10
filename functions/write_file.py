import os

def write_file(working_directory, file_path, content):
    try:
        path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(path, file_path))
        valid_target_file = os.path.commonpath([path, target_file]) == path
        
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
            
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
