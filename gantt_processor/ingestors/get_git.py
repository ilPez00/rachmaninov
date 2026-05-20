# Ingest git commits from repository history
# Stores raw events in uberwiki/wiki/gantt/raw_events.jsonl

import json
import subprocess
from datetime import datetime

def main():
    # This is a placeholder - we would parse git log
    # For now, generate sample data for testing
    raw_file = "/home/gio/uber-wiki/wiki/gantt/raw_events.jsonl"
    with open(raw_file, 'a') as f:
        event = {
            "timestamp": datetime.now().isoformat(),
            "source": "git",
            "activity_type": "git_commit",
            "data": {"message": "Example commit", "files": ["app.py"]}
        }
        f.write(json.dumps(event) + "\n")

if __name__ == "__main__":
    main()
