from pathlib import Path

from app.testing.project_scanner import scan_project
from app.testing.test_runner import run_tests
from app.testing.failure_detector import detect_failures


def test_testing_pipeline(tmp_path):
    # Create a small temporary project
    project = Path(tmp_path)

    # Create requirements.txt
    (project / "requirements.txt").write_text("pytest")

    # Create a simple passing test
    test_file = project / "test_sample.py"

    test_file.write_text(
        """
def test_sample():
    assert 1 + 1 == 2
"""
    )

    # Step 1: Scan the temporary project
    scan_result = scan_project(str(project))

    assert scan_result["language"] == "Python"
    assert scan_result["test_files"] == 1
    assert scan_result["has_requirements"] is True

    # Step 2: Run tests
    test_result = run_tests(str(project))

    assert test_result["status"] == "passed"
    assert test_result["return_code"] == 0

    # Step 3: Detect failures
    failures = detect_failures(test_result)

    assert failures == []


def test_testing_pipeline_detects_real_failure(tmp_path):
    # Create a temporary project
    project = Path(tmp_path)

    # Create requirements.txt
    (project / "requirements.txt").write_text("pytest")

    # Create an intentionally failing test
    test_file = project / "test_bug.py"

    test_file.write_text(
        """
def test_division():
    number = 10 / 0
    assert number == 5
"""
    )

    # Step 1: Scan the project
    scan_result = scan_project(str(project))

    assert scan_result["language"] == "Python"
    assert scan_result["test_files"] == 1
    assert scan_result["has_requirements"] is True

    # Step 2: Run the real pytest test
    test_result = run_tests(str(project))

    assert test_result["status"] == "failed"
    assert test_result["return_code"] != 0

    # Step 3: Detect the real failure
    failures = detect_failures(test_result)

    # DebugAI should detect one failure
    assert len(failures) == 1

    # Verify extracted information
    assert failures[0]["error_type"] == "ZeroDivisionError"

    assert failures[0]["error_message"] == (
        "ZeroDivisionError: division by zero"
    )

    assert failures[0]["file"] == "test_bug.py"

    assert failures[0]["line"] == 3


def test_testing_pipeline_detects_multiple_real_failures(tmp_path):
    # Create temporary project
    project = Path(tmp_path)

    # Create requirements.txt
    (project / "requirements.txt").write_text("pytest")

    # Create first failing test
    math_test = project / "test_math.py"

    math_test.write_text(
        """
def test_division():
    number = 10 / 0
    assert number == 5
"""
    )

    # Create second failing test
    user_test = project / "test_user.py"

    user_test.write_text(
        """
def test_user():
    user = {}
    assert user["name"] == "Pallavi"
"""
    )

    # Step 1: Scan project
    scan_result = scan_project(str(project))

    assert scan_result["language"] == "Python"
    assert scan_result["test_files"] == 2

    # Step 2: Run real pytest
    test_result = run_tests(str(project))

    assert test_result["status"] == "failed"
    assert test_result["return_code"] != 0

    # Step 3: Detect failures
    failures = detect_failures(test_result)

    # We expect two failures
    assert len(failures) == 2

    # First failure
    assert failures[0]["error_type"] == "ZeroDivisionError"
    assert failures[0]["file"] == "test_math.py"
    assert failures[0]["line"] == 3

    # Second failure
    assert failures[1]["error_type"] == "KeyError"
    assert failures[1]["file"] == "test_user.py"
    assert failures[1]["line"] == 4