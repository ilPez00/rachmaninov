import asyncio
import sys
import json
import argparse
from .planner import RachmaninovPlanner
from .actor import RachmaninovActor
from .ontology_personal import PersonalOntology
from .wiki import UberWiki, WikiPage

from .dream import RachmaninovDreamEngine

async def plan_cmd(args):
    planner = RachmaninovPlanner()
    try:
        with open(args.goals, "r") as f:
            goals = json.load(f)
    except Exception as e:
        print(f"Error loading goals: {e}")
        return

    context = args.context or "Working on PC, terminal active."
    proposals = await planner.propose_actions(goals, context)
    print(json.dumps(proposals, indent=2))

async def dream_cmd(args):
    engine = RachmaninovDreamEngine()
    try:
        with open(args.goals, "r") as f:
            goals = json.load(f)
    except Exception as e:
        print(f"Error loading goals: {e}")
        return

    print("[*] Dreaming variations for stalled goals...")
    dreams = await engine.generate_dreams(goals)
    if not dreams:
        print("[!] No stalled goals found or no dreams generated.")
    for d in dreams:
        print(f"[{d.type}] For {d.source_goal_id}: {d.content}")

def act_cmd(args):
    # ... existing
    actor = RachmaninovActor()
    scores = {
        "physical": args.physical,
        "economic": args.economic,
        "intellectual": args.intellectual,
        "psychological": args.psychological
    }
    actor.record_action(args.goal_id, args.text, args.grade, args.rationale, scores)
    print("Action recorded successfully.")

def learn_cmd(args):
    po = PersonalOntology()
    po.learn_entity(args.name, args.category, args.description)
    print(f"Learned entity: {args.name}")

def wiki_ingest_cmd(args):
    wiki = UberWiki()
    page = WikiPage(path="", title=args.title, content=args.content, project=args.project)
    wiki.ingest(page)
    print("Ingested into UberWiki.")

def mcp_serve(args):
    from .mcp import mcp
    mcp.run()

def main():
    parser = argparse.ArgumentParser(description="Rachmaninov Standalone Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Plan command
    p_plan = subparsers.add_parser("plan", help="Propose actions based on goals")
    p_plan.add_argument("--goals", required=True, help="Path to goals.json")
    p_plan.add_argument("--context", help="Current user context")

    # Act command
    p_act = subparsers.add_parser("act", help="Record and grade an action")
    p_act.add_argument("--goal-id", required=True)
    p_act.add_argument("--text", required=True)
    p_act.add_argument("--grade", type=float, required=True)
    p_act.add_argument("--rationale", required=True)
    p_act.add_argument("--physical", type=float, default=0.0)
    p_act.add_argument("--economic", type=float, default=0.0)
    p_act.add_argument("--intellectual", type=float, default=0.0)
    p_act.add_argument("--psychological", type=float, default=0.0)

    # Dream command
    p_dream = subparsers.add_parser("dream", help="Generate variations for stalled goals")
    p_dream.add_argument("--goals", required=True, help="Path to goals.json")

    # Learn command
    p_learn = subparsers.add_parser("learn", help="Learn personal entity")
    p_learn.add_argument("--name", required=True)
    p_learn.add_argument("--category", choices=["Project", "Person", "Tool", "Concept"], required=True)
    p_learn.add_argument("--description", default="")

    # Wiki command
    p_wiki = subparsers.add_parser("wiki", help="Manage UberWiki")
    p_wiki.add_argument("--title", required=True)
    p_wiki.add_argument("--content", required=True)
    p_wiki.add_argument("--project", default="default")

    # MCP command
    subparsers.add_parser("mcp", help="Start MCP server")

    args = parser.parse_args()

    if args.command == "plan":
        asyncio.run(plan_cmd(args))
    elif args.command == "act":
        act_cmd(args)
    elif args.command == "dream":
        asyncio.run(dream_cmd(args))
    elif args.command == "learn":
        learn_cmd(args)
    elif args.command == "wiki":
        wiki_ingest_cmd(args)
    elif args.command == "mcp":
        mcp_serve(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
