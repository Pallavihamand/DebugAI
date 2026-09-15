import subprocess
import sys
import time
from pathlib import Path


def run_tests(project_path: str, timeout: int = 60):
    """
    Run pytest for a project and return structured test execution results.

    Possible statuses:
        passed
        failed
        no_tests
        error
        timeout
    """

    path = Path(project_path)

    # Validate that the project path exists
    if not path.exists():
        raise FileNotFoundError(
            f"Project path does not exist: {project_path}"
        )

    # Validate that the project path is a directory
    if not path.is_dir():
        raise NotADirectoryError(
            f"Project path is not a directory: {project_path}"
        )

    start_time = time.time()

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest"
            ],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        duration = time.time() - start_time

        # pytest return code 0 = all tests passed
        if result.returncode == 0:
            status = "passed"

        # pytest return code 1 = tests failed
        elif result.returncode == 1:
            status = "failed"

        # pytest return code 5 = no tests collected
        elif result.returncode == 5:
            status = "no_tests"

        # Other return codes = pytest/execution error
        else:
            status = "error"

        return {
            "status": status,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration": round(duration, 2)
        }

    except subprocess.TimeoutExpired:

        duration = time.time() - start_time

        return {
            "status": "timeout",
            "return_code": None,
            "stdout": "",
            "stderr": "Test execution timed out.",
            "duration": round(duration, 2)
        }