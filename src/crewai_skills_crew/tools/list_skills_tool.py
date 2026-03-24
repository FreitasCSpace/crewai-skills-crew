from pathlib import Path
from crewai.tools import BaseTool

SKILLS_DIR = Path(__file__).parent.parent / "skills"


class ListSkillsTool(BaseTool):
    name: str = "list_skills"
    description: str = (
        "List all available skills with short descriptions. "
        "Always call this first before starting any task."
    )

    def _run(self) -> str:
        skill_files = sorted(SKILLS_DIR.glob("*.md"))
        if not skill_files:
            return "No skills found in skills/ directory."
        lines = ["Available skills:\n"]
        for path in skill_files:
            lines.append(f"  - {path.stem}: {self._describe(path)}")
        return "\n".join(lines)

    def _describe(self, path: Path) -> str:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
            for i, line in enumerate(lines):
                if line.strip().lower() == "## purpose":
                    for c in lines[i + 1: i + 5]:
                        c = c.strip()
                        if c and not c.startswith("#"):
                            return c[:120]
            for line in lines:
                s = line.strip()
                if s and not s.startswith("#"):
                    return s[:120]
        except Exception as e:
            return f"(error: {e})"
        return "(no description)"
