import os

def get_files_info(working_directory, directory="."):
    try:
        path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(path, directory))
        valid_target_dir = os.path.commonpath([path, target_dir]) == path
        
        if not valid_target_dir:
            raise ValueError(f'Cannot list "{directory}" as it is outside the permitted working directory')
        
        if not os.path.isdir(target_dir):
            raise ValueError(f'"{directory}" is not a directory')

        results = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(item_path)
            try:
                size = os.path.getsize(item_path)
            except OSError:
                size = 0
            results.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
        
        return "\n".join(results)

    except Exception as e:
        return f"Error: {e}"