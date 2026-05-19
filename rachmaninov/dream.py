import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from .models import Dream, ScoreAxis
from .wiki import UberWiki
from .actor import RachmaninovActor

DREAM_PROMPT = """You are Rachmaninov's Dream Engine. 
The user has a stalled goal: "{goal_name}" (ID: {goal_id})
Recent performance has been poor (stagnation detected).

Successful patterns from similar domains (UberWiki):
{wiki_context}

Your task is to "dream" a virtual variation of this goal. 
Type: {dream_type}
- SIMULATION: A hypothetical future scenario where the goal is achieved.
- VARIATION: A slightly different approach or a pivot.
- CROSS_POLLINATION: Combine this goal with another successful pattern.

Output ONLY a JSON object:
{{
  "content": "The synthesized dream/variation text",
  "rationale": "Why this might work"
}}
"""

class RachmaninovDreamEngine:
    def __init__(self, model: str = "opencode/deepseek-v4-flash-free"):
        self.model = model
        self.cache_path = Path("~/.rachmaninov/dream_cache.json").expanduser()
        self.actor = RachmaninovActor()
        self.wiki = UberWiki()

    async def generate_dreams(self, goals: List[dict]) -> List[Dream]:
        """Identify stalled goals and generate dream variations."""
        stats = self.actor.compute_stats()
        # Stagnant goals logic (placeholder: goals with progress < 0.2 and not recently updated)
        stagnant = [g for g in goals if g.get("progress", 0) < 0.2]
        
        new_dreams = []
        for goal in stagnant:
            # 1. Search Wiki for context
            wiki_results = self.wiki.search(goal["name"])
            wiki_context = "\n---\n".join(wiki_results) or "No relevant history."
            
            # 2. Pick a dream type
            dream_type = "VARIATION" # In a real implementation, this would cycle
            
            # 3. Call AI to synthesize
            prompt = DREAM_PROMPT.format(
                goal_name=goal["name"],
                goal_id=goal["id"],
                wiki_context=wiki_context,
                dream_type=dream_type
            )
            
            cmd = [
                "opencode", "run",
                "--model", self.model,
                "--dangerously-skip-permissions",
                prompt
            ]
            
            try:
                process = await asyncio.create_subprocess_exec(
                    *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
                )
                stdout, _ = await process.communicate()
                result = stdout.decode().strip()
                
                if "{" in result and "}" in result:
                    json_str = result[result.find("{"):result.rfind("}")+1]
                    dream_data = json.loads(json_str)
                    
                    new_dreams.append(Dream(
                        id=f"dream_{goal['id']}_{int(datetime.now().timestamp())}",
                        type=dream_type,
                        source_goal_id=goal["id"],
                        content=dream_data["content"],
                        timestamp=datetime.now().isoformat(),
                        metadata={"rationale": dream_data.get("rationale")}
                    ))
            except Exception as e:
                print(f"Error generating dream for {goal['id']}: {e}")
                
        # Save to cache
        self._save_dreams(new_dreams)
        return new_dreams

    def load_active_dreams(self) -> List[Dream]:
        if not self.cache_path.exists():
            return []
        try:
            data = json.loads(self.cache_path.read_text())
            return [Dream(**d) for d in data if not d.get("dismissed", False)]
        except Exception:
            return []

    def _save_dreams(self, dreams: List[Dream]):
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        # Merge with existing
        existing = self.load_active_dreams()
        merged = [vars(d) for d in existing + dreams]
        self.cache_path.write_text(json.dumps(merged, indent=2))

    def build_context_block(self) -> str:
        dreams = self.load_active_dreams()
        if not dreams:
            return ""
        
        lines = ["[DREAM PROPOSALS]"]
        for d in dreams[:3]: # Show top 3
            lines.append(f"• ({d.type}) For {d.source_goal_id}: {d.content}")
        lines.append("[/DREAM PROPOSALS]")
        return "\n".join(lines)