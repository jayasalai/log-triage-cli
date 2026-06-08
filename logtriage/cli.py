"""Command-line entry point for log triage."""

import argparse
import json
import sys

from . import __version__
from .classifier import SEVERITY_ORDER, classify_all, summarize
from .parser import parse_lines

def _read_input(path: str) -> list[str]:
    if path == "-":
        return sys.stdin.readlines()
    with open(path, "r", encoding="utf-8") as handle:
        return handle.readlines()

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="logtriage",
        description="Read a log file, classify each line, emit a JSON report.",
    )
    parser.add_argument("path", help="Path to a log file.")
    parser.add_argument(
        "--min-severity",
        choices=list(SEVERITY_ORDER),
        default="info",
        help="Only include entries at or above this severity.",
    )
    parser.add_argument("--pretty", action="store_true", help="Indent the JSON output.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser

def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        raw_lines = _read_input(args.path)
    except FileNotFoundError:
        print(f"error: no such file: {args.path}", file=sys.stderr)
        return 2
    classifications = classify_all(parse_lines(raw_lines))
    threshold = SEVERITY_ORDER[args.min_severity]
    filtered = [c for c in classifications if SEVERITY_ORDER[c.severity] >= threshold]
    report = summarize(filtered)
    text = json.dumps(report, indent=2 if args.pretty else None)
    print(text)
    return 1 if report["worst_severity"] in ("error", "critical") else 0

def main() -> None:
    raise SystemExit(run())

if __name__ == "__main__":
    main()