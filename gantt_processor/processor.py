# Gantt Processor - Reads raw events and maps to goals
# Processes data from uberwiki/wiki/gantt/raw_events.jsonl
# Outputs to uberwiki/wiki/gantt/processed/YYYY-MM-DD.json

import json
import os
from datetime import datetime
from pathlib import Path

def load_goals():
    """Load user goals from goals.json"""
    goals_file = Path("/home/gio/uber-wiki/wiki/gantt/goals.json")
    if not goals_file.exists():
        return {}
    with open(goals_file) as f:
        return json.load(f)

def load_raw_events():
    """Load raw events from raw_events.jsonl"""
    raw_file = Path("/home/gio/uber-wiki/wiki/gantt/raw_events.jsonl")
    events = []
    if raw_file.exists():
        with open(raw_file) as f:
            for line in f:
                events.append(json.loads(line.strip()))
    return events

def process_events(events, goals):
    """Process events and assign to goals"""
    result = []
    for event in events:
        # Simple rule: assign based on source
        goal_id = "other"  # default
        if event["source"] == "git":
            goal_id = "development"
        elif event["source"] == "calendar" and "meeting" in event["data"].get("title", ""):
            goal_id = "communication"

        result.append({
            "timestamp": event["timestamp"],
            "duration": event["data"].get("duration", 30),
            "activity": event["activity_type"],
            "goal_id": goal_id,
            "goal_name": goals.get(goal_id, {}).get("name", goal_id)
        })
    return result

def save_daily_file(data):
    """Save processed data to daily file"""
    today = datetime.now().strftime("%Y-%m-%d")
    processed_dir = Path("/home/gio/uber-wiki/wiki/gantt/processed")
    output_file = processed_dir / f"{today}.json"

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    goals = load_goals()
    events = load_raw_events()
    processed = process_events(events, goals)
    save_daily_file(processed)
    print(f"Processed {len(events)} events. Saved to {datetime.now().strftime('%Y-%m-%d')}.json")
