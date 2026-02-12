import os

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        work_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(work_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([work_dir_abs, abs_file_path]) == work_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            f'Error: "{file_path}" is not a directory'

        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f"File reading error: {e}"