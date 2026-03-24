#!/usr/bin/env python
"""
main.py — standard crewAI entry points: run, train, replay, test.

Usage:
  crewai run            → interactive prompt for your task
  python -m crewai_skills_crew.main "your task here"

Examples:
  python -m crewai_skills_crew.main "generate 10 employee records as JSON, validate, write a summary"
  python -m crewai_skills_crew.main "create a CSV of 20 products and compute avg price per category"
"""

import sys
import warnings
import traceback
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def _ensure_dirs():
    """Create workspace/ and output/ at project root if they don't exist."""
    root = Path(__file__).resolve().parent.parent.parent
    (root / "workspace").mkdir(exist_ok=True)
    (root / "output").mkdir(exist_ok=True)


def _check_env():
    """Validate that the required API key is set."""
    import os
    provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
    if provider == "anthropic" and not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set. Copy .env.example → .env and add your key.")
        sys.exit(1)
    if provider == "openai" and not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not set. Copy .env.example → .env and add your key.")
        sys.exit(1)


def run():
    """
    Run the crew — primary entry point.
    Accepts a task from CLI args or prompts interactively.
    """
    try:
        _check_env()
        _ensure_dirs()

        if len(sys.argv) > 1:
            goal = " ".join(sys.argv[1:]).strip()
        else:
            goal = input("Enter your task: ").strip()

        if not goal:
            print("ERROR: Empty task.")
            sys.exit(1)

        from crewai_skills_crew.crew import build_crew

        print(f"\n{'═' * 60}")
        print(f"  TASK: {goal[:54]}{'...' if len(goal) > 54 else ''}")
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'═' * 60}\n")

        result = build_crew(goal).kickoff()

        print(f"\n{'═' * 60}")
        print("  DONE")
        print(f"{'═' * 60}")
        print(result)

        root = Path(__file__).resolve().parent.parent.parent
        files = [f for f in (root / "workspace").rglob("*") if f.is_file()]
        if files:
            print("\nFiles in workspace:")
            for f in sorted(files):
                print(f"  {f.relative_to(root)}  ({f.stat().st_size:,} bytes)")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}")
        print(traceback.format_exc())
        sys.exit(1)


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        _check_env()
        _ensure_dirs()

        from crewai_skills_crew.crew import build_crew

        goal = "generate sample data, validate it, and write a summary report"
        n_iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 5
        filename = sys.argv[2] if len(sys.argv) > 2 else "training_results.pkl"

        print(f"\nTraining for {n_iterations} iterations...")
        build_crew(goal).train(
            n_iterations=n_iterations, filename=filename,
            inputs={"goal": goal}
        )
        print(f"\nTraining complete → {filename}")

    except Exception as e:
        raise Exception(f"Training error: {e}")


def replay():
    """
    Replay crew execution from a specific task.
    """
    try:
        from crewai_skills_crew.crew import build_crew

        task_id = sys.argv[1] if len(sys.argv) > 1 else None
        if not task_id:
            print("Usage: replay <task_id>")
            sys.exit(1)

        build_crew("replay").replay(task_id=task_id)

    except Exception as e:
        raise Exception(f"Replay error: {e}")


def test():
    """
    Test the crew and generate performance metrics.
    """
    try:
        _check_env()
        _ensure_dirs()

        from crewai_skills_crew.crew import build_crew

        goal = "generate sample data, validate it, and write a summary report"
        n_iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 3
        eval_llm = sys.argv[2] if len(sys.argv) > 2 else "gpt-4"

        print(f"\nTesting for {n_iterations} iterations...")
        build_crew(goal).test(
            n_iterations=n_iterations, openai_model_name=eval_llm,
            inputs={"goal": goal}
        )
        print("\nTesting complete.")

    except Exception as e:
        raise Exception(f"Test error: {e}")


if __name__ == "__main__":
    run()
