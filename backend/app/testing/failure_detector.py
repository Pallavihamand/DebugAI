import re


def detect_failures(test_result: dict):
    """
    Extract structured failure information from pytest results.
    """

    failures = []

    if test_result["status"] != "failed":
        return failures

    output = test_result.get("stdout", "")

    # Match traceback locations:
    # project\test_math.py:3:ZeroDivisionError
    location_pattern = r"^(.+?\.py):(\d+):\s*([A-Za-z_][\w.]*)$"

    locations = {}

    for line in output.splitlines():
        line = line.strip()

        location_match = re.match(location_pattern, line)

        if location_match:
            file_path = location_match.group(1)
            line_number = int(location_match.group(2))
            error_type = location_match.group(3)

            locations[file_path.replace("\\", "/")] = {
                "file": file_path,
                "line": line_number,
                "error_type": error_type
            }

    # Match pytest short summary
    failure_pattern = r"FAILED (.+?)(?:\s+-\s+(.+))?$"

    for line in output.splitlines():
        match = re.match(failure_pattern, line.strip())

        if not match:
            continue

        test_name = match.group(1)
        error_message = match.group(2) or "Test failed"

        error_type = "Unknown"

        if ":" in error_message:
            error_type = error_message.split(":", 1)[0].strip()

        test_file = test_name.split("::")[0]

        failure = {
            "test": test_name,
            "error_type": error_type,
            "error_message": error_message,
            "file": test_file,
            "line": None,
            "traceback": output
        }

        normalized_test_file = test_file.replace("\\", "/")

        if normalized_test_file in locations:
            location = locations[normalized_test_file]

            failure["error_type"] = location["error_type"]
            failure["file"] = location["file"]
            failure["line"] = location["line"]

        failures.append(failure)

    if not failures:
        failures.append({
            "test": "Unknown",
            "error_type": "Unknown",
            "error_message": "Test execution failed.",
            "file": None,
            "line": None,
            "traceback": output
        })

    return failures