"""
crew.py
-------
One agent. Any task. Skills discovered and loaded at runtime.

The agent receives the goal, discovers available skills via list_skills,
loads whatever it needs via load_skill, executes via bash, and loops
until the task is fully done.
"""

import os
from crewai import Agent, Crew, Task, Process, LLM
from crewai_skills_crew.tools import AGENT_TOOLS


BACKSTORY = """
You are a capable, methodical executor with access to a library of skills.

For every task, follow this loop — no exceptions:

1. Call list_skills — see what you have available
2. Identify which skill(s) are relevant to the job
3. Call load_skill — read the full instructions for each relevant skill
4. Execute using bash, following the skill instructions exactly
5. Read every output:
   - exit_code 0 = success, move on
   - Non-zero = failure — read stderr, fix the problem, try again
6. Is the task fully done?
   - YES → report your results clearly
   - NO  → load the next skill and continue
7. Keep looping until done

Rules you never break:
- Always list_skills before starting anything new
- Always load_skill before executing — never guess syntax or flags
- Never stop early — keep going until the task is complete and verified
- If something fails, fix it and retry — one failure is not the end
- All files go in ./workspace — use relative paths only
"""


def build_llm() -> LLM:
    provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))

    if provider == "anthropic":
        return LLM(
            model=os.getenv("LLM_MODEL", "claude-sonnet-4-20250514"),
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            temperature=temperature,
        )
    elif provider == "openai":
        return LLM(
            model=os.getenv("LLM_MODEL", "gpt-4o"),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=temperature,
        )
    else:
        raise ValueError(f"Unknown LLM_PROVIDER='{provider}'. Use 'anthropic' or 'openai'.")


def build_crew(goal: str) -> Crew:
    agent = Agent(
        role="General Purpose Executor",
        goal="Complete any task given to you using the available skills and bash.",
        backstory=BACKSTORY,
        tools=AGENT_TOOLS,
        llm=build_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=25,
    )

    task = Task(
        description=(
            f"Complete the following task fully and correctly:\n\n"
            f"{goal}\n\n"
            f"Start by calling list_skills to see what you have available. "
            f"Then load the relevant skills and execute. "
            f"Keep going until the task is done and all outputs are verified."
        ),
        expected_output=(
            "A clear summary of what was done, what files were created, "
            "and confirmation that the task is complete."
        ),
        agent=agent,
    )

    return Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )
