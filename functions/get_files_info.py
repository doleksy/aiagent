import os

def get_files_info(working_directory, directory="."):
    print(f"wd: {working_directory}, dir: {directory}")
    
    target = os.path.join(working_directory, directory)
    target_abs = os.path.abspath(target)
    print(f"target: {target_abs}")

    working_abs = os.path.abspath(working_directory)
    print(f"working: {working_abs}")

    if not target_abs.startswith(working_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_abs):
        return f'Error: "{directory}" is not a directory'

    print(os.listdir(target_abs))
    contents_str = ""
    for entry in os.listdir(target_abs):
        entry_abs = os.path.join(target_abs, entry)
        contents_str += f"- {entry}: file_size={os.path.getsize(entry_abs)} bytes, is_dir={os.path.isdir(entry_abs)}\n"

    return contents_str

if __name__ == "__main__":
    print(get_files_info("../calculator", "."))
