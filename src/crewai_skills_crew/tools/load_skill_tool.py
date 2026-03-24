from pathlib import Path
from crewai.tools import BaseTool

SKILLS_DIR = Path(__file__).parent.parent / "skills"


class LoadSkillTool(BaseTool):
    name: str = "load_skill"
    description: str = (
        "Load full instructions for a skill by name. "
        "Input: skill name as a plain string (e.g. 'run_python'). "
        "Read the instructions carefully before executing."
    )

    def _run(self, skill_name: str) -> str:
        skill_name = skill_name.strip().replace("/", "").replace("..", "").replace(" ", "_")
        path = SKILLS_DIR / f"{skill_name}.md"
        if not path.exists():
            available = [p.stem for p in sorted(SKILLS_DIR.glob("*.md"))]
            return f"Skill '{skill_name}' not found. Available: {', '.join(available)}"
        return f"=== SKILL: {skill_name} ===\n\n{path.read_text(encoding='utf-8')}"
