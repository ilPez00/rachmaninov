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
class PersonalEntity:
    name: str
    category: str  # Project, Person, Tool, Concept
    description: str = ""
    associations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WikiPage:
    path: str
    title: str
    content: str
    frontmatter: Dict[str, Any] = field(default_factory=dict)
    project: str = "default"
