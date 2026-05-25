from fastapi.testclient import TestClient

from app.agent_contract import get_agent_integration_contract
from app.main import app


def test_agent_contract_documents_public_safe_backend_boundary():
    contract = get_agent_integration_contract()

    assert contract["public_safe"] is True
    assert contract["current_repo_mode"] == "deterministic_fake_data_demo"
    assert contract["required_agent_endpoint"]["path"] == "/agents/job-fit/run"
    assert "risk_flags" in contract["required_agent_endpoint"]["response_fields"]
    assert "Validate model output against a schema before showing it in the UI" in contract["non_negotiable_controls"]


def test_agent_contract_route_exposes_same_contract():
    client = TestClient(app)

    response = client.get("/agent/contract")

    assert response.status_code == 200
    payload = response.json()
    assert payload == get_agent_integration_contract()
    assert payload["intended_agent_backend"]["execution_policy"] == (
        "Python orchestrator controls tools; model returns structured JSON only"
    )
