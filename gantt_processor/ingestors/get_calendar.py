# Ingest calendar events from system calendar
# Stores raw events in uberwiki/wiki/gantt/raw_events.jsonl

import json
from datetime import datetime

# This is a placeholder - we would integrate with actual calendar API
# For now, generate sample data for testing

def main():
    # Read existing raw_events
    raw_file = "/home/gio/uber-wiki/wiki/gantt/raw_events.jsonl"
    with open(raw_file, 'a') as f:
        event = {
            "timestamp": datetime.now().isoformat(),
            "source": "calendar",
            "activity_type": "calendar_event",
            "data": {"title": "Sample Meeting", "duration": 60}
        }
        f.write(json.dumps(event) + "\n")

if __name__ == "__main__":
    main()
