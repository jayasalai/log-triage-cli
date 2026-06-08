"""Parse raw log lines into structured records."""

import re
from dataclasses import dataclass

_LINE_RE = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>[A-Z]+)\s+"
    r"(?P<message>.*)$"
)

KNOWN_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

@dataclass
class LogRecord:
    """One parsed log line."""
    raw: str
    timestamp: str | None
    level: str | None
    message: str

def parse_line(line: str) -> LogRecord:
    """Parse a single line. Always returns a record."""
    line = line.rstrip("\n")
    match = _LINE_RE.match(line)
    if not match:
        return LogRecord(raw=line, timestamp=None, level=None, message=line.strip())
    level = match.group("level").upper()
    if level not in KNOWN_LEVELS:
        return LogRecord(raw=line, timestamp=None, level=None, message=line.strip())
    return LogRecord(
        raw=line,
        timestamp=match.group("timestamp"),
        level=level,
        message=match.group("message").strip(),
    )

def parse_lines(lines: list[str]) -> list[LogRecord]:
    """Parse many lines, skipping blank ones."""
    return [parse_line(line) for line in lines if line.strip()]