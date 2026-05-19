import asyncio
import subprocess
import json
from typing import List, Dict, Any
from .ontology import resolve_domain, enrich_goals_prompt
from .models import ProposedAction

SYSTEM_PROMPT = """You are Rachmaninov — action-proposal engine. Not an assistant.
Your task is to take a user's goals and context, then propose specific, high-impact actions for the day.

Goals with ontology tags (domain/mode/scoreAxis already resolved — do NOT change them):
{goals_context}

User Context:
{user_context}

Output ONLY a JSON array of proposed actions:
[
  {{
    "id": "goal_id",
    "action_text": "Specific action to take",
    "duration_min": 30,
    "scope": "SMALL/MEDIUM/LARGE"
  }}
]
"""

class RachmaninovPlanner:
    def __init__(self, model: str = "opencode/deepseek-v4-flash-free"):
        self.model = model

    async def propose_actions(self, goals: List[dict], user_context: str) -> List[Dict[str, Any]]:
        goals_context = enrich_goals_prompt(goals)
        prompt = SYSTEM_PROMPT.format(goals_context=goals_context, user_context=user_context)
        
        cmd = [
            "opencode", "run",
            "--model", self.model,
            "--dangerously-skip-permissions",
            prompt
        ]
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            result = stdout.decode().strip()
            
            # Extract JSON
            if "[" in result and "]" in result:
                json_str = result[result.find("["):result.rfind("]")+1]
                proposals = json.loads(json_str)
                
                # Enrich proposals with ontology data
                enriched = []
                for p in proposals:
                    goal_id = p.get("id")
                    goal = next((g for g in goals if g["id"] == goal_id), None)
                    if goal:
                        defn = resolve_domain(goal["domain"])
                        if defn:
                            p.update({
                                "ayuDomain": defn.ayuDomain.value,
                                "mode": defn.defaultMode.value,
                                "scoreAxis": defn.scoreAxis.value,
                                "unit": defn.unit
                            })
                    enriched.append(p)
                return enriched
        except Exception as e:
            print(f"Error proposing actions: {e}")
            return []
        return []
