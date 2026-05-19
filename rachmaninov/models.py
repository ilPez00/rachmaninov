from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict

class ScoreAxis(Enum):
    PHYSICAL = "physical"
    ECONOMIC = "economic"
    INTELLECTUAL = "intellectual"
    PSYCHOLOGICAL = "psychological"

class ActionDomain(Enum):
    FABRICATE = "FABRICATE"
    STUDY = "STUDY"
    CONSTRUCT = "CONSTRUCT"
    BOND = "BOND"
    HEAL = "HEAL"

class ActionMode(Enum):
    LIFT = "LIFT"
    REST = "REST"
    CREATE = "CREATE"
    WALK = "WALK"
    WORK = "WORK"
    LEARN = "LEARN"

@dataclass
class DomainDef:
    ayuDomain: ActionDomain
    defaultMode: ActionMode
    scoreAxis: ScoreAxis
    unit: str
    contextHints: List[str]

@dataclass
class ProposedAction:
    id: str
    name: str
    domain: str
    ayuDomain: str
    mode: str
    scoreAxis: str
    unit: str
    progress: float = 0.0

@dataclass
class ExperienceLog:
    desire: str
    intent: str = ""
    method: str = ""
    action: str = ""
    effectSummary: str = ""
    effectDetails: str = ""
    outcome: str = ""
    relatedResources: List[str] = field(default_factory=list)
    symbolicAssociations: Dict[str, str] = field(default_factory=dict)
    physicalScore: float = 0.0
    economicScore: float = 0.0
    intellectualScore: float = 0.0
    psychologicalScore: float = 0.0
