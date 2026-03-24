# CrewAI Skills Crew

One agent. Any task. Skills discovered and loaded at runtime.

## What it does

A single **General Purpose Executor** agent that dynamically discovers skills from markdown files, loads their instructions, and executes via bash — looping until the task is fully complete.

```
CrewHub sends "goal" input
      │
      ▼
  Executor Agent
      │
      ├── list_skills        → what do I have?
      ├── load_skill(X)      → how do I do this?
      ├── bash(command)      → do it
      ├── evaluate output
      ├── load_skill(Y)      → need something else?
      ├── bash(command)      → do it
      └── loop until done
```

No hardcoded workflows — the agent decides which skills to use based on the goal.

## Inputs

| Input | Description | Example |
|-------|-------------|---------|
| `goal` | The task to complete | `"generate 10 employee records as JSON, validate, write a summary"` |

## Available Skills

Skills are `.md` files in `src/crewai_skills_crew/skills/`. The agent discovers them automatically.

| Skill | Purpose |
|-------|---------|
| `file_ops` | Read, write, copy, move files |
| `run_python` | Execute Python scripts |
| `git_ops` | Git clone, log, diff operations |
| `http_request` | Make HTTP requests via curl |
| `read_file` | Read file contents |
| `write_file` | Write content to files |
| `validate_json` | Validate JSON structure |
| `validate_csv` | Validate CSV structure |
| `validate_data` | General data validation |
| `write_report` | Generate text reports |
| `write_markdown_report` | Generate markdown reports |

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

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env        # add your API key
crewai run
```
