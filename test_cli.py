from cli import classify_line

def test_error_line():
    assert classify_line("ERROR: database crashed") == "ERROR"

def test_warning_line():
    assert classify_line("WARNING: low disk space") == "WARNING"

def test_info_line():
    assert classify_line("INFO: server started") == "INFO"