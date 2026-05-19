import asyncio
import subprocess
import json
from typing import List, Dict, Any
from .ontology import resolve_domain, enrich_goals_prompt
from .ontology_personal import PersonalOntology
from .wiki import UberWiki
from .models import ProposedAction

SYSTEM_PROMPT = """You are Rachmaninov — action-proposal engine. 
Global Ontology: {goals_context}
Personal Ontology (User Symbols): {personal_context}
Relevant History (UberWiki): {wiki_context}

Current User Context: {user_context}

Output ONLY a JSON array of specific proposed actions."""

class RachmaninovPlanner:
    def __init__(self, model: str = "opencode/deepseek-v4-flash-free"):
        self.model = model
        self.personal = PersonalOntology()
        self.wiki = UberWiki()

    async def propose_actions(self, goals: List[dict], user_context: str) -> List[Dict[str, Any]]:
        # 0. Learn new entities from context
        self.personal.learn_from_context(user_context)

        # 1. Map command to personal entities
        personal_matches = self.personal.map_command(user_context)
        personal_context = ", ".join([f"{e.name} ({e.category})" for e in personal_matches]) or "None"
        
        # 2. Search UberWiki for project-specific data
        project_hint = next((e.name for e in personal_matches if e.category == "Project"), None)
        wiki_results = self.wiki.search(user_context, project=project_hint)
        wiki_context = "\n---\n".join(wiki_results) or "No relevant history."

        goals_context = enrich_goals_prompt(goals)
        prompt = SYSTEM_PROMPT.format(
            goals_context=goals_context, 
            personal_context=personal_context,
            wiki_context=wiki_context[:1000], # Cap history size
            user_context=user_context
        )
        
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
