from pathlib import Path


def scan_project(project_path: str):
    path = Path(project_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Project path does not exist: {project_path}"
        )

    # Folders that should not be scanned
    excluded_dirs = {
        "venv",
        ".venv",
        "__pycache__",
        ".git",
        "node_modules",
        ".pytest_cache",
    }

    python_files = []

    for file in path.rglob("*.py"):
        # Check whether any parent folder is excluded
        if any(part in excluded_dirs for part in file.parts):
            continue

        python_files.append(file)

    test_files = [
        file
        for file in python_files
        if file.name.startswith("test_")
        or file.name.endswith("_test.py")
    ]

    requirements_file = path / "requirements.txt"

    return {
        "project_path": str(path),
        "language": "Python" if python_files else "Unknown",
        "python_files": len(python_files),
        "test_files": len(test_files),
        "tests": [str(file) for file in test_files],
        "has_requirements": requirements_file.exists(),
    }