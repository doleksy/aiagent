import os

def get_files_info(working_directory, directory="."):
    target = os.path.join(working_directory, directory)
    target_abs = os.path.abspath(target)

    working_abs = os.path.abspath(working_directory)

    if not target_abs.startswith(working_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_abs):
        return f'Error: "{directory}" is not a directory'

    contents_str = ""
    try:
        dir_listing = os.listdir(target_abs)
    except Exception as e:
        return f"Error: in os.listdir({target_abs}): {e}"
    
    for entry in dir_listing:
        entry_abs = os.path.join(target_abs, entry)

        try:
            entry_size = os.path.getsize(entry_abs)
        except OSError as e:
            return f"Error: in os.path.getsize({entry_abs}): {e}"
        
        contents_str += f" - {entry}: file_size={entry_size} bytes, is_dir={os.path.isdir(entry_abs)}\n"

    return contents_str

if __name__ == "__main__":
    print(get_files_info("../calculator", "."))
