import re


def detect_failures(test_result: dict):
    """
    Extract structured failure information from pytest results.

    Returns a list of dictionaries containing:
    - test
    - error_type
    - error_message
    - file
    - line
    - traceback
    """

    failures = []

    # If tests did not fail, there is nothing to detect.
    if test_result.get("status") != "failed":
        return failures

    output = test_result.get("stdout", "")

    # ---------------------------------------------------------
    # 1. Extract traceback locations
    # ---------------------------------------------------------
    #
    # Example:
    # test_math.py:3:ZeroDivisionError
    # test_math.py:10:AssertionError
    #
    # We keep ALL locations instead of storing only one location
    # per file.
    # ---------------------------------------------------------

    location_pattern = (
        r"^(.+?\.py):(\d+):\s*([A-Za-z_][\w.]*)$"
    )

    locations = []

    for line in output.splitlines():
        line = line.strip()

        location_match = re.match(
            location_pattern,
            line
        )

        if location_match:
            file_path = location_match.group(1)
            line_number = int(location_match.group(2))
            error_type = location_match.group(3)

            locations.append(
                {
                    "file": file_path,
                    "line": line_number,
                    "error_type": error_type,
                }
            )

    # ---------------------------------------------------------
    # 2. Extract pytest FAILED summary lines
    # ---------------------------------------------------------
    #
    # Example:
    #
    # FAILED test_math.py::test_division
    # - ZeroDivisionError: division by zero
    #
    # ---------------------------------------------------------

    failure_pattern = (
        r"^FAILED (.+?)(?:\s+-\s+(.+))?$"
    )

    for line in output.splitlines():

        match = re.match(
            failure_pattern,
            line.strip()
        )

        if not match:
            continue

        test_name = match.group(1)

        error_message = (
            match.group(2)
            or "Test failed"
        )

        # -----------------------------------------------------
        # 3. Extract error type from error message
        # -----------------------------------------------------

        error_type = "Unknown"

        if ":" in error_message:
            error_type = (
                error_message
                .split(":", 1)[0]
                .strip()
            )

        # -----------------------------------------------------
        # 4. Extract test file
        # -----------------------------------------------------

        test_file = test_name.split("::")[0]

        normalized_test_file = (
            test_file.replace("\\", "/")
        )

        # -----------------------------------------------------
        # 5. Find the matching traceback location
        # -----------------------------------------------------
        #
        # We search through ALL locations instead of using:
        #
        # locations[file] = ...
        #
        # This allows multiple failures from the same file.
        # -----------------------------------------------------

        matching_location = None

        for location in locations:

            normalized_location_file = (
                location["file"]
                .replace("\\", "/")
            )

            if normalized_location_file == normalized_test_file:

                # Match the error type as an additional check.
                if location["error_type"] == error_type:
                    matching_location = location
                    break

        # -----------------------------------------------------
        # 6. Create structured failure
        # -----------------------------------------------------

        failure = {
            "test": test_name,
            "error_type": error_type,
            "error_message": error_message,
            "file": test_file,
            "line": None,
            "traceback": output,
        }

        # -----------------------------------------------------
        # 7. Add traceback information if found
        # -----------------------------------------------------

        if matching_location:

            failure["error_type"] = (
                matching_location["error_type"]
            )

            failure["file"] = (
                matching_location["file"]
            )

            failure["line"] = (
                matching_location["line"]
            )

        failures.append(failure)

    # ---------------------------------------------------------
    # 8. Fallback
    # ---------------------------------------------------------
    #
    # If pytest failed but we could not extract a FAILED line,
    # still return a structured failure.
    # ---------------------------------------------------------

    if not failures:

        failures.append(
            {
                "test": "Unknown",
                "error_type": "Unknown",
                "error_message": "Test execution failed.",
                "file": None,
                "line": None,
                "traceback": output,
            }
        )

    return failures