from typing import List, Optional, Dict
from .models import DomainDef, ActionDomain, ActionMode, ScoreAxis

PRAXIS_ONTOLOGY: Dict[str, DomainDef] = {
    "Body & Fitness": DomainDef(ActionDomain.HEAL, ActionMode.LIFT, ScoreAxis.PHYSICAL, "reps", ["gym", "lift", "workout", "sport", "exercise"]),
    "Rest & Recovery": DomainDef(ActionDomain.HEAL, ActionMode.REST, ScoreAxis.PHYSICAL, "hours", ["sleep", "rest", "nap", "recovery"]),
    "Mental Balance": DomainDef(ActionDomain.HEAL, ActionMode.REST, ScoreAxis.PSYCHOLOGICAL, "min", ["meditation", "journal", "breathe", "calm"]),
    "Environment & Home": DomainDef(ActionDomain.CONSTRUCT, ActionMode.CREATE, ScoreAxis.PSYCHOLOGICAL, "tasks", ["home", "clean", "organize", "repair"]),
    "Health & Longevity": DomainDef(ActionDomain.HEAL, ActionMode.WALK, ScoreAxis.PHYSICAL, "steps", ["walk", "outside", "doctor", "pharmacy"]),
    "Financial Security": DomainDef(ActionDomain.FABRICATE, ActionMode.WORK, ScoreAxis.ECONOMIC, "€", ["bank", "budget", "finance", "invoice", "spreadsheet"]),
    "Friendship & Social": DomainDef(ActionDomain.BOND, ActionMode.REST, ScoreAxis.PSYCHOLOGICAL, "contacts", ["friend", "call", "meet", "social", "message"]),
    "Romance & Intimacy": DomainDef(ActionDomain.BOND, ActionMode.REST, ScoreAxis.PSYCHOLOGICAL, "quality-time", ["partner", "date", "intimacy", "together"]),
    "Community & Contribution": DomainDef(ActionDomain.BOND, ActionMode.CREATE, ScoreAxis.PSYCHOLOGICAL, "hours", ["volunteer", "community", "contribute", "teach"]),
    "Career & Craft": DomainDef(ActionDomain.FABRICATE, ActionMode.WORK, ScoreAxis.INTELLECTUAL, "deliverables", ["desk", "ide", "code", "work", "project", "office"]),
    "Wealth & Assets": DomainDef(ActionDomain.FABRICATE, ActionMode.WORK, ScoreAxis.ECONOMIC, "€", ["invest", "trading", "portfolio", "asset", "crypto"]),
    "Gaming & Esports": DomainDef(ActionDomain.STUDY, ActionMode.CREATE, ScoreAxis.INTELLECTUAL, "hours", ["game", "esports", "ranked", "practice", "stream"]),
    "Impact & Legacy": DomainDef(ActionDomain.CONSTRUCT, ActionMode.CREATE, ScoreAxis.INTELLECTUAL, "projects", ["write", "publish", "launch", "build", "create"]),
    "Spirit & Purpose": DomainDef(ActionDomain.STUDY, ActionMode.LEARN, ScoreAxis.PSYCHOLOGICAL, "pages", ["read", "philosophy", "reflect", "meaning", "purpose"]),
}

def resolve_domain(domain_str: str) -> Optional[DomainDef]:
    if domain_str in PRAXIS_ONTOLOGY:
        return PRAXIS_ONTOLOGY[domain_str]
    
    domain_lower = domain_str.lower()
    for key, defn in PRAXIS_ONTOLOGY.items():
        primary = key.lower().split("&")[0].strip()
        if primary in domain_lower:
            return defn
    return None

def enrich_goals_prompt(goals: List[dict]) -> str:
    lines = []
    for g in goals:
        name = g.get("name", "Unknown")
        domain = g.get("domain", "")
        progress = g.get("progress", 0.0)
        
        defn = resolve_domain(domain)
        if defn:
            tag = f"[{defn.ayuDomain.value}/{defn.defaultMode.value} → {defn.scoreAxis.value} +{defn.unit}]"
        else:
            tag = "[GENERAL]"
        
        lines.append(f"• \"{name}\" {tag} progress={int(progress * 100)}%")
    return "\n".join(lines)

VISUAL_HINTS: Dict[str, str] = {
    "dumbbell": "Body & Fitness",
    "barbell": "Body & Fitness",
    "weights": "Body & Fitness",
    "squat": "Body & Fitness",
    "bench press": "Body & Fitness",
    "laptop": "Career & Craft",
    "coding": "Career & Craft",
    "money": "Financial Security",
    "book": "Spirit & Purpose",
    "meditation": "Mental Balance",
}