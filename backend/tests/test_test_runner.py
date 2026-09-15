from pathlib import Path

from app.testing.test_runner import run_tests


def test_run_tests_when_tests_pass(tmp_path):
    project = Path(tmp_path)

    test_file = project / "test_sample.py"

    test_file.write_text(
        """
def test_sample():
    assert 1 + 1 == 2
"""
    )

    result = run_tests(str(project))

    assert result["status"] == "passed"
    assert result["return_code"] == 0
    assert result["duration"] >= 0


def test_run_tests_when_test_fails(tmp_path):
    project = Path(tmp_path)

    test_file = project / "test_bug.py"

    test_file.write_text(
        """
def test_division():
    number = 10 / 0
    assert number == 5
"""
    )

    result = run_tests(str(project))

    assert result["status"] == "failed"
    assert result["return_code"] == 1
    assert "ZeroDivisionError" in result["stdout"]


def test_run_tests_when_no_tests_exist(tmp_path):
    project = Path(tmp_path)

    result = run_tests(str(project))

    assert result["status"] == "no_tests"
    assert result["return_code"] == 5


def test_run_tests_when_project_does_not_exist(tmp_path):
    project = tmp_path / "does_not_exist"

    try:
        run_tests(str(project))
        assert False
    except FileNotFoundError:
        assert True


def test_run_tests_when_path_is_file(tmp_path):
    project_file = tmp_path / "project.txt"

    project_file.write_text("not a project")

    try:
        run_tests(str(project_file))
        assert False
    except NotADirectoryError:
        assert True