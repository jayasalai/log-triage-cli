# Log Triage CLI

A command-line tool that reads a log file, classifies each line by 
severity and category, and outputs a JSON report.

## Setup
python3 -m venv venv
source venv/bin/activate
pip install pytest

## How to run
python -m logtriage.cli sample_logs/app.log --pretty

## How to run tests
pytest