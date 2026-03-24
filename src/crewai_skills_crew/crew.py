"""CrAI Skills Crew — one agent, any task, skills discovered at runtime."""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .tools import AGENT_TOOLS


@CrewBase
class CrewaiSkillsCrew:
    """One agent that dynamically discovers and loads skills to complete any task."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def executor(self) -> Agent:
        return Agent(
            config=self.agents_config["executor"],
            tools=AGENT_TOOLS,
            allow_delegation=False,
            verbose=True,
        )

    @task
    def execute_task(self) -> Task:
        return Task(config=self.tasks_config["execute_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
