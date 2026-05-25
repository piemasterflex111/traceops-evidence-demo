from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

API_ROUTES = [
    ("GET", "/api/applications"),
    ("GET", "/api/applications/{application_id}"),
    ("GET", "/api/evidence"),
    ("GET", "/api/dashboard/summary"),
    ("GET", "/api/dashboard/prep-actions"),
    ("GET", "/api/applications/{application_id}/interview-packet"),
    ("GET", "/api/applications/{application_id}/gaps"),
]

APPLICATION_STATUS = {"tracking", "applied", "interviewing", "offer", "closed"}
POLICY_STATUS = {"allowed", "blocked", "needs_review"}
CLASSIFICATIONS = {"supported", "partial", "unsupported"}
MATCH_STRENGTH = {"strong", "moderate", "weak", "none"}
RISK_LEVEL = {"low", "medium", "high"}
GAP_STATUS = {"open", "in_progress", "addressed"}
REQUIREMENT_PRIORITY = {"must", "should", "nice"}
DEMO_TAGS = {"aerospace-test-automation", "fintech-backend-platform"}

FORBIDDEN_RESPONSE_TERMS = [
    "SECRET" + "_COMPANY_ALPHA",
    "PRIVATE" + "_RECRUITER_NAME",
    "REAL" + "_INTERVIEW_NOTE",
    "PRIVATE" + "_JOB_DESCRIPTION",
    "ABSOLUTE" + "_LOCAL_PATH_EXAMPLE",
    "C:" + "\\",
    "C:" + "/",
    "AIWork",
    "Users",
]


def assert_public_safe_json(payload):
    text = str(payload)
    for term in FORBIDDEN_RESPONSE_TERMS:
        assert term not in text


def test_root_page_lists_all_routes_with_methods_and_browser_guidance():
    response = client.get("/")

    assert response.status_code == 200
    html = response.text
    for method, path in [
        ("GET", "/health"),
        *API_ROUTES,
        ("GET", "/"),
        ("GET", "/evidence"),
        ("GET", "/report"),
        ("GET", "/demo/evidence"),
        ("POST", "/demo/report"),
    ]:
        assert method in html
        assert path in html

    assert "POST-only" in html
    assert "Swagger" in html
    assert "PowerShell" in html
    assert "curl" in html
    assert 'href="/api/applications"' in html
    assert 'href="/api/evidence"' in html
    assert 'href="/demo/report"' not in html


def test_api_routes_are_registered():
    registered = {
        (method, route.path)
        for route in app.routes
        for method in (route.methods or set())
    }

    for method, path in API_ROUTES:
        assert (method, path) in registered


def test_known_application_ids_work_for_scoped_endpoints():
    for application_id in ["aerospace-test-automation", "fintech-backend-platform"]:
        for suffix in ["", "/interview-packet", "/gaps"]:
            response = client.get(f"/api/applications/{application_id}{suffix}")
            assert response.status_code == 200
            assert_public_safe_json(response.json())


def test_applications_endpoint_returns_contract_list():
    response = client.get("/api/applications")

    assert response.status_code == 200
    payload = response.json()
    assert_public_safe_json(payload)
    assert isinstance(payload, list)
    assert payload

    for application in payload:
        assert {"id", "company", "role", "status", "createdAt"} <= set(application)
        assert application["status"] in APPLICATION_STATUS
        if "demo" in application:
            assert application["demo"] in DEMO_TAGS


def test_application_detail_endpoint_returns_contract_shape():
    application_id = "aerospace-test-automation"
    response = client.get(f"/api/applications/{application_id}")

    assert response.status_code == 200
    payload = response.json()
    assert_public_safe_json(payload)
    assert {"application", "requirements", "evidence", "matrix", "topEvidenceIds"} <= set(payload)
    assert payload["application"]["id"] == application_id
    assert payload["application"]["status"] in APPLICATION_STATUS

    evidence_ids = {item["id"] for item in payload["evidence"]}
    assert set(payload["topEvidenceIds"]) <= evidence_ids

    for requirement in payload["requirements"]:
        assert {"id", "applicationId", "text", "category", "priority"} <= set(requirement)
        assert requirement["applicationId"] == application_id
        assert requirement["priority"] in REQUIREMENT_PRIORITY

    for evidence in payload["evidence"]:
        assert {"id", "title", "source", "domain", "policyStatus", "provenance"} <= set(evidence)
        assert evidence["policyStatus"] in POLICY_STATUS

    for cell in payload["matrix"]:
        assert {"requirementId", "evidenceIds", "classification", "matchStrength", "riskLevel", "safeClaimBlocked"} <= set(cell)
        assert cell["classification"] in CLASSIFICATIONS
        assert cell["matchStrength"] in MATCH_STRENGTH
        assert cell["riskLevel"] in RISK_LEVEL
        assert isinstance(cell["safeClaimBlocked"], bool)
        assert set(cell["evidenceIds"]) <= evidence_ids
        if "bestEvidenceId" in cell:
            assert cell["bestEvidenceId"] in evidence_ids


def test_unknown_application_returns_404_for_application_scoped_endpoints():
    for path in [
        "/api/applications/missing-application",
        "/api/applications/missing-application/interview-packet",
        "/api/applications/missing-application/gaps",
    ]:
        response = client.get(path)
        assert response.status_code == 404
        assert_public_safe_json(response.json())


def test_evidence_endpoint_returns_contract_list():
    response = client.get("/api/evidence")

    assert response.status_code == 200
    payload = response.json()
    assert_public_safe_json(payload)
    assert isinstance(payload, list)
    assert payload

    for evidence in payload:
        assert {"id", "title", "source", "domain", "policyStatus", "provenance"} <= set(evidence)
        assert evidence["policyStatus"] in POLICY_STATUS


def test_dashboard_summary_endpoint_returns_contract_shape():
    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200
    payload = response.json()
    assert_public_safe_json(payload)
    assert {
        "activeInterviews",
        "highestRiskGap",
        "nextAction",
        "strongestTestAutomationEvidenceId",
        "strongestBackendEvidenceSummary",
    } <= set(payload)
    assert isinstance(payload["activeInterviews"], int)


def test_dashboard_prep_actions_endpoint_returns_contract_list():
    response = client.get("/api/dashboard/prep-actions")

    assert response.status_code == 200
    payload = response.json()
    assert_public_safe_json(payload)
    assert isinstance(payload, list)
    assert payload
    for action in payload:
        assert {"label", "detail"} <= set(action)


def test_interview_packet_endpoint_returns_contract_shape():
    application_id = "aerospace-test-automation"
    response = client.get(f"/api/applications/{application_id}/interview-packet")

    assert response.status_code == 200
    payload = response.json()
    assert_public_safe_json(payload)
    assert {
        "applicationId",
        "roleSummary",
        "whyThisRoleFits",
        "topEvidenceIds",
        "topRisks",
        "honestGapAnswers",
        "likelyQuestions",
        "openingAnswer",
        "questionsToAsk",
        "followUpEmail",
        "practicePriority",
        "copyableAnswers",
    } <= set(payload)
    assert payload["applicationId"] == application_id
    assert {"focus"} <= set(payload["practicePriority"])
    for answer in payload["honestGapAnswers"]:
        assert {"gap", "answer"} <= set(answer)
    for answer in payload["copyableAnswers"]:
        assert {"label", "text"} <= set(answer)


def test_gaps_endpoint_returns_contract_list():
    application_id = "aerospace-test-automation"
    response = client.get(f"/api/applications/{application_id}/gaps")

    assert response.status_code == 200
    payload = response.json()
    assert_public_safe_json(payload)
    assert isinstance(payload, list)
    assert payload
    for gap in payload:
        assert {
            "id",
            "applicationId",
            "gap",
            "severity",
            "whyItMatters",
            "studyTask",
            "proofTask",
            "safeFraming",
            "status",
        } <= set(gap)
        assert gap["applicationId"] == application_id
        assert gap["severity"] in RISK_LEVEL
        assert gap["status"] in GAP_STATUS
