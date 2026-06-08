from logtriage.parser import parse_line
from logtriage.classifier import classify

def test_error_severity():
    record = parse_line("2026-06-05 09:16:45 ERROR database connection failed")
    result = classify(record)
    assert result.severity == "error"

def test_warning_severity():
    record = parse_line("2026-06-05 09:15:10 WARNING disk space running low")
    result = classify(record)
    assert result.severity == "warning"

def test_database_category():
    record = parse_line("2026-06-05 09:16:45 ERROR database connection failed")
    result = classify(record)
    assert result.category == "database"