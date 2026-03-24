#!/usr/bin/env python
"""Entry-point for the CrewAI Skills Crew."""

from .crew import CrewaiSkillsCrew


def run():
    """Run the crew — primary entry point used by CrewHub and CLI."""
    inputs = {
        "goal": "generate 10 employee records as JSON, validate every field, and write a summary report",
    }
    CrewaiSkillsCrew().crew().kickoff(inputs=inputs)


def train():
    """Train the crew for a given number of iterations."""
    import sys
    inputs = {
        "goal": "generate sample data, validate it, and write a summary report",
    }
    n_iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    filename = sys.argv[2] if len(sys.argv) > 2 else "training_results.pkl"
    CrewaiSkillsCrew().crew().train(
        n_iterations=n_iterations, filename=filename, inputs=inputs,
    )


def replay():
    """Replay crew execution from a specific task."""
    import sys
    task_id = sys.argv[1] if len(sys.argv) > 1 else None
    if not task_id:
        print("Usage: replay <task_id>")
        return
    CrewaiSkillsCrew().crew().replay(task_id=task_id)


def test():
    """Test the crew and generate performance metrics."""
    import sys
    inputs = {
        "goal": "generate sample data, validate it, and write a summary report",
    }
    n_iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    eval_llm = sys.argv[2] if len(sys.argv) > 2 else "gpt-4"
    CrewaiSkillsCrew().crew().test(
        n_iterations=n_iterations, openai_model_name=eval_llm, inputs=inputs,
    )


if __name__ == "__main__":
    run()
