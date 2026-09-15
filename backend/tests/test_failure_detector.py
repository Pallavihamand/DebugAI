from app.testing.failure_detector import detect_failures


def test_detect_failures():
    test_result = {
        "status": "failed",
        "stdout": (
            "temp_test_project\\test_bug.py:2:ZeroDivisionError\n"
            "FAILED temp_test_project/test_bug.py::test_division "
            "- ZeroDivisionError: division by zero"
        )
    }

    failures = detect_failures(test_result)

    assert len(failures) == 1

    assert failures[0]["test"] == (
        "temp_test_project/test_bug.py::test_division"
    )

    assert failures[0]["error_type"] == "ZeroDivisionError"

    assert failures[0]["error_message"] == (
        "ZeroDivisionError: division by zero"
    )

    assert failures[0]["file"] == (
        "temp_test_project\\test_bug.py"
    )

    assert failures[0]["line"] == 2


def test_no_failures_when_tests_pass():
    test_result = {
        "status": "passed",
        "stdout": "1 passed"
    }

    failures = detect_failures(test_result)

    assert failures == []
def test_detect_assertion_error():
    test_result = {
        "status": "failed",
        "stdout": (
            "temp_test_project\\test_bug.py:5: AssertionError\n"
            "FAILED temp_test_project/test_bug.py::test_result "
            "- AssertionError: 10 != 20"
        )
    }

    failures = detect_failures(test_result)

    assert len(failures) == 1

    assert failures[0]["test"] == (
        "temp_test_project/test_bug.py::test_result"
    )

    assert failures[0]["error_type"] == "AssertionError"

    assert failures[0]["error_message"] == (
        "AssertionError: 10 != 20"
    )

    assert failures[0]["file"] == (
        "temp_test_project\\test_bug.py"
    )

    assert failures[0]["line"] == 5
def test_detect_multiple_failures():
    test_result = {
        "status": "failed",
        "stdout": (
            "project\\test_math.py:3:ZeroDivisionError\n"
            "project\\test_user.py:7:KeyError\n"
            "FAILED project/test_math.py::test_division "
            "- ZeroDivisionError: division by zero\n"
            "FAILED project/test_user.py::test_user "
            "- KeyError: 'name'"
        )
    }

    failures = detect_failures(test_result)

    assert len(failures) == 2

    assert failures[0]["error_type"] == "ZeroDivisionError"
    assert failures[0]["file"] == "project\\test_math.py"
    assert failures[0]["line"] == 3

    assert failures[1]["error_type"] == "KeyError"
    assert failures[1]["file"] == "project\\test_user.py"
    assert failures[1]["line"] == 7