"""
MCP Server for Rachmaninov Core.
Enables any agent (Hermes, OpenCode, etc.) to use Rachmaninov locally.
"""

import asyncio
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP

from .planner import RachmaninovPlanner
from .actor import RachmaninovActor
from .wiki import UberWiki, WikiPage
from .ontology_personal import PersonalOntology

mcp = FastMCP("Rachmaninov")

@mcp.tool()
async def plan_day(goals_path: str, context: str) -> str:
    """Propose high-impact actions based on local goals and context."""
    import json
    planner = RachmaninovPlanner()
    with open(goals_path, "r") as f:
        goals = json.load(f)
    proposals = await planner.propose_actions(goals, context)
    return json.dumps(proposals, indent=2)

@mcp.tool()
async def record_action(goal_id: str, text: str, grade: float, rationale: str) -> str:
    """Record a completed action into the PDCA loop."""
    actor = RachmaninovActor()
    actor.record_action(goal_id, text, grade, rationale, {})
    return f"Action recorded for {goal_id}."

@mcp.tool()
async def search_knowledge(query: str, project: str = "default") -> List[str]:
    """Search the local UberWiki for relevant history/data."""
    wiki = UberWiki()
    return wiki.search(query, project=project)

@mcp.tool()
async def learn_term(name: str, category: str, description: str = "") -> str:
    """Add a new term or project to the personal ontology."""
    po = PersonalOntology()
    po.learn_entity(name, category, description)
    return f"Learned {name} as {category}."

if __name__ == "__main__":
    mcp.run()
