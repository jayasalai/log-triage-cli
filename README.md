# Log Triage CLI

A command-line tool that reads a log file and classifies each line as ERROR, WARNING, or INFO. Outputs a JSON summary.

## Setup
python3 -m venv venv
source venv/bin/activate
pip install pytest

## How to run
python cli.py sample.log

## How to run tests
pytest