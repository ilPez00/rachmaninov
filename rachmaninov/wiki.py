import os
import subprocess
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional
from .models import WikiPage

class UberWiki:
    """Local, project-aware knowledge store with Git sync."""

    def __init__(self, root: str = "~/.rachmaninov/wiki"):
        self.root = Path(root).expanduser()
        self.root.mkdir(parents=True, exist_ok=True)
        self._ensure_git()

    def _ensure_git(self):
        if not (self.root / ".git").exists():
            subprocess.run(["git", "init"], cwd=self.root, capture_output=True)

    def ingest(self, page: WikiPage):
        project_dir = self.root / page.project
        project_dir.mkdir(exist_ok=True)
        
        file_path = project_dir / f"{page.title.lower().replace(' ', '_')}.md"
        
        content = "---\n"
        content += yaml.dump(page.frontmatter)
        content += "---\n\n"
        content += page.content
        
        file_path.write_text(content)
        return file_path

    def search(self, query: str, project: Optional[str] = None) -> List[str]:
        """Simple grep-based search across markdown files."""
        results = []
        search_path = self.root / (project if project else "")
        
        try:
            # Recursive grep for query in .md files
            cmd = ["grep", "-ril", query, str(search_path)]
            output = subprocess.check_output(cmd).decode().splitlines()
            for path in output[:3]: # Top 3 results
                results.append(Path(path).read_text())
        except subprocess.CalledProcessError:
            pass
            
        return results

    def sync(self, remote: Optional[str] = None):
        """Version control the knowledge base."""
        subprocess.run(["git", "add", "."], cwd=self.root)
        subprocess.run(["git", "commit", "-m", "chore: auto-sync wiki"], cwd=self.root)
        if remote:
            subprocess.run(["git", "push", "origin", "main"], cwd=self.root)