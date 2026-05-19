import asyncio
import sys
import json
import argparse
from .planner import RachmaninovPlanner
from .actor import RachmaninovActor

async def plan(args):
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

def act(args):
    actor = RachmaninovActor()
    scores = {
        "physical": args.physical,
        "economic": args.economic,
        "intellectual": args.intellectual,
        "psychological": args.psychological
    }
    actor.record_action(args.goal_id, args.text, args.grade, args.rationale, scores)
    print("Action recorded successfully.")

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

    args = parser.parse_args()

    if args.command == "plan":
        asyncio.run(plan(args))
    elif args.command == "act":
        act(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
