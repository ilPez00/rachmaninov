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
        """Hybrid search: llmwiki (semantic) -> grep (fallback)."""
        search_path = self.root / (project if project else "")
        
        # 1. Try llmwiki (Rust binary for semantic/BM25)
        if self._is_llmwiki_available():
            try:
                cmd = ["llmwiki", "search", query, "--wiki-root", str(search_path)]
                output = subprocess.check_output(cmd).decode()
                # Parse llmwiki output format
                return self._parse_llmwiki(output)
            except Exception:
                pass

        # 2. Fallback: Python grep-based ranking
        results = []
        try:
            cmd = ["grep", "-ril", query, str(search_path)]
            files = subprocess.check_output(cmd).decode().splitlines()
            for path in files[:5]: # Top 5 files
                content = Path(path).read_text()
                # Extract 200-char dense snippet around match
                snippet = self._extract_snippet(content, query)
                results.append(f"[{Path(path).name}] {snippet}")
        except subprocess.CalledProcessError:
            pass
            
        return results

    def _is_llmwiki_available(self) -> bool:
        from shutil import which
        return which("llmwiki") is not None

    def _parse_llmwiki(self, output: str) -> List[str]:
        """Convert llmwiki stdout to dense context blocks."""
        # Simple extraction of paths and snippets
        lines = output.splitlines()
        results = []
        for line in lines:
            if line.startswith("[") and "]" in line:
                results.append(line.strip())
        return results[:3]

    def _extract_snippet(self, content: str, query: str) -> str:
        """Find query in text and return context window."""
        idx = content.lower().find(query.lower())
        if idx == -1: return content[:200]
        start = max(0, idx - 100)
        end = min(len(content), idx + 100)
        return "..." + content[start:end].replace("\n", " ") + "..."

    def sync(self, remote: Optional[str] = None):
        """Version control the knowledge base."""
        subprocess.run(["git", "add", "."], cwd=self.root)
        subprocess.run(["git", "commit", "-m", "chore: auto-sync wiki"], cwd=self.root)
        if remote:
            subprocess.run(["git", "push", "origin", "main"], cwd=self.root)