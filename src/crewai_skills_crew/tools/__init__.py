from crewai_skills_crew.tools.list_skills_tool import ListSkillsTool
from crewai_skills_crew.tools.load_skill_tool import LoadSkillTool
from crewai_skills_crew.tools.bash_tool import BashTool

AGENT_TOOLS = [ListSkillsTool(), LoadSkillTool(), BashTool()]
