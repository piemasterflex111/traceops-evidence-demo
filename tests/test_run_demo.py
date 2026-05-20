import subprocess
import sys
from pathlib import Path


def test_run_demo_script_executes_from_repo_root():
    root = Path(__file__).resolve().parents[1]

    result = subprocess.run(
        [sys.executable, "scripts/run_demo.py"],
        cwd=root,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Wrote report:" in result.stdout
