import os

def write_file(working_directory, file_path, content):
    try:
        work_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(work_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([work_dir_abs, abs_file_path]) == work_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        with open(abs_file_path, "w") as f:
             f.write(content)
             return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"File writing error: {e}"
