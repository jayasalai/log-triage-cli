import argparse
import json

def classify_line(line):
    if "ERROR" in line:
        return "ERROR"
    elif "WARNING" in line:
        return "WARNING"
    else:
        return "INFO"

def triage_logs(filename):
    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    with open(filename, 'r') as f:
        for line in f:
            label = classify_line(line.strip())
            counts[label] += 1
    return counts

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Triage log files')
    parser.add_argument('filename', help='Path to log file')
    args = parser.parse_args()
    result = triage_logs(args.filename)
    print(json.dumps(result, indent=2))