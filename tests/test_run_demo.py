import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


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


def test_fastapi_demo_routes_return_200_and_public_safe_content():
    client = TestClient(app)

    for method, path in [
        ("get", "/health"),
        ("get", "/"),
        ("get", "/evidence"),
        ("get", "/report"),
        ("post", "/demo/report"),
    ]:
        response = getattr(client, method)(path)
        text = response.text

        assert response.status_code == 200
        assert "C:" + "\\" not in text
        assert "C:" + "/" not in text
        assert "AIWork" not in text
        assert "Users" not in text
