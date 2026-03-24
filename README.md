# crewai-skills-crew

One agent. Any task. Skills loaded at runtime.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env        # add your API key
```

## Usage

```bash
# via crewAI CLI
crewai run

# via entry point
crewai_skills_crew

# via python directly
python -m crewai_skills_crew.main "your task here"
```

## Examples

```bash
python -m crewai_skills_crew.main "generate 10 employee records as JSON, validate every field, write a summary"
python -m crewai_skills_crew.main "clone https://github.com/owner/repo and summarise the last 10 commits"
python -m crewai_skills_crew.main "create a CSV of 20 products with name/price/category and compute avg price per category"
python -m crewai_skills_crew.main "read all .py files in ./workspace and find any syntax errors"
```

## How it works

```
python -m crewai_skills_crew.main "task"
      │
      ▼
  One agent
      │
      ├── list_skills        → what do I have?
      ├── load_skill(X)      → how do I do this?
      ├── bash(command)      → do it
      ├── evaluate output
      ├── load_skill(Y)      → need something else?
      ├── bash(command)      → do it
      └── loop until done
```

The agent discovers skills at runtime — no hardcoded workflows.

## Project Structure

```
crewai-skills-crew/
├── pyproject.toml        ← project config + entry points
├── .env.example          ← template for API keys
├── README.md
├── src/
│   └── crewai_skills_crew/
│       ├── __init__.py
│       ├── main.py       ← entry points: run, train, replay, test
│       ├── crew.py       ← one agent, one task, built from goal
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── bash_tool.py
│       │   ├── list_skills_tool.py
│       │   └── load_skill_tool.py
│       └── skills/
│           ├── file_ops.md
│           ├── run_python.md
│           ├── git_ops.md
│           └── ...
├── workspace/            ← agent file output (gitignored)
└── output/               ← reports (gitignored)
```

## Adding a skill

Drop a `.md` file in `src/crewai_skills_crew/skills/`:

```markdown
# Skill: your_skill

## Purpose
One sentence.

## When to use
When is this skill the right choice.

## How to execute
Bash commands with examples.

## Output contract
What stdout/exit_code mean.

## Evaluate output
How to know it worked. What to do if it didn't.
```

Agent discovers it automatically on next run — no registration needed.

## Switch LLM

```bash
# Claude (default)
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...

# GPT-4o
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```
