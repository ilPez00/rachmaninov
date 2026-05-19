import json
from pathlib import Path
from typing import List, Dict, Any
from .models import PersonalEntity

class PersonalOntology:
    """Tracks per-user symbols and project entities."""

    def __init__(self, path: str = "~/.rachmaninov/personal_ontology.json"):
        self.path = Path(path).expanduser()
        self.entities: Dict[str, PersonalEntity] = self._load()

    def _load(self) -> Dict[str, Any]:
        if self.path.exists():
            data = json.loads(self.path.read_text())
            return {k: PersonalEntity(**v) for k, v in data.items()}
        return {}

    def save(self):
        data = {k: vars(v) for k, v in self.entities.items()}
        self.path.write_text(json.dumps(data, indent=2))

    def map_command(self, command: str) -> List[PersonalEntity]:
        """Identify which personal entities are mentioned in a command."""
        matches = []
        for name, entity in self.entities.items():
            if name.lower() in command.lower():
                matches.append(entity)
        return matches

    def learn_entity(self, name: str, category: str, description: str = ""):
        if name not in self.entities:
            self.entities[name] = PersonalEntity(name, category, description)
            self.save()

    def learn_from_context(self, text: str):
        """Automatically detect potential new entities in text."""
        import re
        # Detect CapitalizedWords that aren't common English (primitive symbol detection)
        words = re.findall(r'\b[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)*\b', text)
        
        common_ignores = {"Aura", "Praxis", "Rachmaninov", "User", "The", "Monday", "Today"}
        
        for word in words:
            if word not in common_ignores and word not in self.entities:
                # Default to Concept or Project based on length/suffix
                category = "Project" if len(word) > 5 else "Concept"
                self.learn_entity(word, category, f"Auto-detected from context: {text[:50]}...")
