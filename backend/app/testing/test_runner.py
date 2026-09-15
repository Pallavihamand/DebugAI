import subprocess
import sys
import time
from pathlib import Path


def run_tests(project_path: str, timeout: int = 60):
    path = Path(project_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Project path does not exist: {project_path}"
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

        return {
            "status": "passed" if result.returncode == 0 else "failed",
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