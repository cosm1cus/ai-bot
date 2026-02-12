import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        work_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(work_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([work_dir_abs, abs_file_path]) == work_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not abs_file_path.endswith(".py"):
             return f'Error: "{file_path}" is not a Python file'

        command = ["python3", abs_file_path]

        if args:
             command.extend(args)

        file_run = subprocess.run(command, cwd=work_dir_abs, capture_output=True, text=True, timeout=30)

        output = []

        if file_run.returncode != 0:
             output.append(f"Process exited with code {file_run.returncode}")
        if not file_run.stdout or not file_run.stderr:
             output.append(f"No output produced")
        if file_run.stdout:
            output.append(f"STDOUT: \n{file_run.stdout}")
        if file_run.stderr:
            output.append(f"STDERR: \n{file_run.stderr}")

        return '\n'.join(output)
    except Exception as e:
        return f"File execution error {e}"