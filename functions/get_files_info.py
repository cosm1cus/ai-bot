import os

def get_files_info(working_directory, directory="."):
    try:
        work_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(work_dir_abs, directory))
        valid_target_dir = os.path.commonpath([work_dir_abs, target_dir]) == work_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            f'Error: "{directory}" is not a directory'

        dir_items = os.listdir(target_dir)
        contents = []

        for i in dir_items:
            name = i
            size = os.path.getsize(os.path.join(target_dir, i))
            is_dir = os.path.isdir(os.path.join(target_dir, i))
            record = f"- {name}: file_size={size} bytes, is_dir={is_dir}"
            contents.append(record)

        return "\n".join(contents)
    except Exception as e:
        return f"Error listing files: {e}"