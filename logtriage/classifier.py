"""Classify parsed records by severity and category."""

from dataclasses import dataclass
from .parser import LogRecord

SEVERITY_ORDER = {"info": 0, "warning": 1, "error": 2, "critical": 3}

_LEVEL_TO_SEVERITY = {
    "DEBUG": "info", "INFO": "info", "WARNING": "warning",
    "ERROR": "error", "CRITICAL": "critical",
}

_CATEGORY_KEYWORDS = [
    ("auth", ("unauthorized", "forbidden", "login", "permission", "token")),
    ("database", ("database", "sql", "deadlock", "query", "connection refused")),
    ("network", ("timeout", "timed out", "connection reset", "unreachable", "dns")),
    ("disk", ("disk", "no space", "quota", "inode", "read-only file system")),
    ("memory", ("out of memory", "oom", "memoryerror", "heap")),
]

@dataclass
class Classification:
    severity: str
    category: str
    record: LogRecord

def _severity_for(record: LogRecord) -> str:
    if record.level and record.level in _LEVEL_TO_SEVERITY:
        return _LEVEL_TO_SEVERITY[record.level]
    text = record.message.lower()
    if any(w in text for w in ("error", "fail", "exception", "traceback")):
        return "error"
    return "info"

def _category_for(record: LogRecord) -> str:
    text = record.message.lower()
    for name, keywords in _CATEGORY_KEYWORDS:
        if any(k in text for k in keywords):
            return name
    return "uncategorized"

def classify(record: LogRecord) -> Classification:
    return Classification(_severity_for(record), _category_for(record), record)

def classify_all(records: list[LogRecord]) -> list[Classification]:
    return [classify(r) for r in records]

def summarize(items: list[Classification]) -> dict:
    by_severity, by_category = {}, {}
    for it in items:
        by_severity[it.severity] = by_severity.get(it.severity, 0) + 1
        by_category[it.category] = by_category.get(it.category, 0) + 1
    worst = "info"
    for it in items:
        if SEVERITY_ORDER[it.severity] > SEVERITY_ORDER[worst]:
            worst = it.severity
    return {
        "total_lines": len(items),
        "worst_severity": worst if items else None,
        "by_severity": by_severity,
        "by_category": by_category,
        "entries": [
            {
                "timestamp": c.record.timestamp,
                "level": c.record.level,
                "severity": c.severity,
                "category": c.category,
                "message": c.record.message,
            }
            for c in items
        ],
    }