import json
from datetime import datetime
from typing import Dict, Any, List
from .models import ExperienceLog

class RachmaninovActor:
    def __init__(self, log_path: str = "rachmaninov_logs.json"):
        self.log_path = log_path

    def record_action(self, 
                      goal_id: str, 
                      action_text: str, 
                      grade: float, 
                      rationale: str,
                      scores: Dict[str, float]) -> None:
        """Record a completed action with its grade and rationale."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "goal_id": goal_id,
            "action_text": action_text,
            "grade": grade,
            "rationale": rationale,
            "scores": scores
        }
        
        # Load existing logs
        logs = self._load_logs()
        logs.append(entry)
        
        # Save updated logs
        with open(self.log_path, "w") as f:
            json.dump(logs, f, indent=2)

    def _load_logs(self) -> List[Dict[str, Any]]:
        try:
            with open(self.log_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def compute_stats(self) -> Dict[str, Any]:
        """Compute performance stats based on historical logs."""
        logs = self._load_logs()
        if not logs:
            return {}
        
        avg_grade = sum(l["grade"] for l in logs) / len(logs)
        
        # Stagnant goals: 3+ consecutive grades < 0.35
        # (Simplified logic for now)
        stagnant = []
        # ... logic to identify stagnant goals
        
        return {
            "overall_avg": avg_grade,
            "total_actions": len(logs),
            "stagnant_goals": stagnant
        }
