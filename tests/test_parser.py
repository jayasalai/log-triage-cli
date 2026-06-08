from logtriage.parser import parse_line

def test_parses_valid_line():
    record = parse_line("2026-06-05 09:14:02 ERROR database connection failed")
    assert record.level == "ERROR"
    assert record.timestamp == "2026-06-05 09:14:02"
    assert record.message == "database connection failed"

def test_parses_warning():
    record = parse_line("2026-06-05 09:15:10 WARNING disk space running low")
    assert record.level == "WARNING"
    assert record.message == "disk space running low"

def test_unrecognised_line_returns_none_level():
    record = parse_line("this is not a valid log line")
    assert record.level is None
    assert record.message == "this is not a valid log line"