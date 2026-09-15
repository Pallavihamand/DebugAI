from app.testing.project_scanner import scan_project


def test_scan_project():
    result = scan_project(".")

    assert "project_path" in result
    assert "language" in result
    assert "python_files" in result
    assert "test_files" in result