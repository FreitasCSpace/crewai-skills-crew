import os
import subprocess
from pathlib import Path
from crewai.tools import BaseTool
from pydantic import Field


class BashTool(BaseTool):
    name: str = "bash"
    description: str = (
        "Execute any bash command or multiline script. "
        "Working directory is the project root. "
        "Write all output files to ./output/ — that directory always exists. "
        "Returns stdout, stderr, and exit_code. "
        "exit_code 0 = success. Non-zero = failure — read stderr, fix it, retry."
    )
    timeout: int = Field(default=120)

    def _run(self, command: str) -> str:
        # Ensure ./output/ exists (CrewHub symlinks this to artifact storage)
        Path("output").mkdir(exist_ok=True)
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env={**os.environ},
            )
            parts = []
            if result.stdout.strip():
                parts.append(result.stdout.strip())
            if result.stderr.strip():
                parts.append(f"[stderr]\n{result.stderr.strip()}")
            parts.append(f"[exit_code: {result.returncode}]")
            return "\n".join(parts)
        except subprocess.TimeoutExpired:
            return f"[error] Timed out after {self.timeout}s — break into smaller steps."
        except Exception as e:
            return f"[error] {type(e).__name__}: {e}"
