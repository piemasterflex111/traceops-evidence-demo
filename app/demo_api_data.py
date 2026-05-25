from copy import deepcopy

from fastapi import HTTPException


APPLICATIONS = [
    {
        "id": "aerospace-test-automation",
        "company": "Demo Manufacturing Company",
        "role": "Demo Test Automation Engineer",
        "status": "interviewing",
        "createdAt": "2026-05-12T00:00:00Z",
        "demo": "aerospace-test-automation",
        "interviewTime": "Upcoming technical screen",
        "primaryFitTheme": "Python test automation for validation workflow tooling",
        "topRisk": "PLC and station-integration depth",
        "nextAction": "Practice the validation station story with supported evidence only",
    },
    {
        "id": "fintech-backend-platform",
        "company": "Demo Manufacturing Company",
        "role": "Demo Firmware Validation Engineer",
        "status": "tracking",
        "createdAt": "2026-05-14T00:00:00Z",
        "demo": "fintech-backend-platform",
        "interviewTime": "Generic prep window",
        "primaryFitTheme": "FastAPI workflow tooling and reviewable evidence reports",
        "topRisk": "Java and cloud backend depth",
        "nextAction": "Frame backend strengths as Python and FastAPI demo work",
    },
]

EVIDENCE = [
    {
        "id": "ev-python-automation",
        "title": "Python validation workflow notes",
        "source": "Demo Evidence Source",
        "sourceUrl": "https://example.invalid/traceops-demo/python-automation",
        "domain": "python-automation",
        "policyStatus": "allowed",
        "provenance": "data/demo_evidence/python_automation_notes.md",
        "summary": "Fake notes describing Python scripts for parsing logs and building reviewable summaries.",
        "bestFit": "Python automation, evidence review, and repeatable internal tooling patterns.",
        "riskNote": "Demo evidence only; it does not claim live production ownership.",
    },
    {
        "id": "ev-validation-station",
        "title": "Demo validation station workflow",
        "source": "Demo Validation Station",
        "sourceUrl": "https://example.invalid/traceops-demo/validation-station",
        "domain": "test-validation",
        "policyStatus": "allowed",
        "provenance": "data/demo_evidence/validation_station_notes.md",
        "summary": "Fake station notes covering test steps, observed signals, and reportable outcomes.",
        "bestFit": "Manufacturing test workflow, validation review, and source-backed discussion.",
        "riskNote": "Station details are intentionally generic fake demo data.",
    },
    {
        "id": "ev-fastapi-reporting",
        "title": "FastAPI evidence report demo",
        "source": "TraceOps Evidence Demo",
        "sourceUrl": "https://example.invalid/traceops-demo/fastapi-reporting",
        "domain": "internal-tools",
        "policyStatus": "allowed",
        "provenance": "app/main.py",
        "summary": "FastAPI demo that maps requirements to evidence, classifications, and markdown reports.",
        "bestFit": "Internal tools, Python backend patterns, and reviewable report generation.",
        "riskNote": "Project evidence; safe framing should avoid production deployment claims.",
    },
    {
        "id": "ev-unsupported-claims",
        "title": "Unsupported claim examples",
        "source": "Demo Evidence Source",
        "domain": "claim-review",
        "policyStatus": "blocked",
        "provenance": "data/demo_evidence/unsupported_claim_examples.md",
        "summary": "Fake examples used to show claims that should not become safe talking points.",
        "bestFit": "Public safety review and unsupported-claim handling.",
        "riskNote": "Blocked evidence is visible for review but not used as support.",
    },
]

APPLICATION_DETAILS = {
    "aerospace-test-automation": {
        "application": APPLICATIONS[0],
        "requirements": [
            {
                "id": "req-auto-python",
                "applicationId": "aerospace-test-automation",
                "text": "Python test automation",
                "category": "technical",
                "priority": "must",
                "extractedFrom": "demo-role-description",
            },
            {
                "id": "req-validation-workflow",
                "applicationId": "aerospace-test-automation",
                "text": "Validation station workflow review",
                "category": "domain",
                "priority": "must",
                "extractedFrom": "demo-role-description",
            },
            {
                "id": "req-plc-depth",
                "applicationId": "aerospace-test-automation",
                "text": "PLC integration depth",
                "category": "technical",
                "priority": "should",
                "extractedFrom": "demo-role-description",
            },
        ],
        "evidence": [EVIDENCE[0], EVIDENCE[1], EVIDENCE[3]],
        "matrix": [
            {
                "requirementId": "req-auto-python",
                "evidenceIds": ["ev-python-automation"],
                "bestEvidenceId": "ev-python-automation",
                "classification": "supported",
                "matchStrength": "strong",
                "riskLevel": "low",
                "safeClaimBlocked": False,
                "safeTalkingPoint": "Built Python demo automation that parses evidence inputs and produces reviewable summaries.",
                "gapNote": "Keep scope tied to demo evidence and avoid production claims.",
                "rationale": "The evidence directly supports Python automation in a validation workflow.",
            },
            {
                "requirementId": "req-validation-workflow",
                "evidenceIds": ["ev-validation-station"],
                "bestEvidenceId": "ev-validation-station",
                "classification": "supported",
                "matchStrength": "moderate",
                "riskLevel": "medium",
                "safeClaimBlocked": False,
                "safeTalkingPoint": "Can discuss validation workflow structure using fake station notes and source-backed outcomes.",
                "gapNote": "The station context is generic demo data.",
                "rationale": "The fake station notes match the workflow requirement but omit hardware-specific depth.",
            },
            {
                "requirementId": "req-plc-depth",
                "evidenceIds": ["ev-unsupported-claims"],
                "bestEvidenceId": "ev-unsupported-claims",
                "classification": "unsupported",
                "matchStrength": "none",
                "riskLevel": "high",
                "safeClaimBlocked": True,
                "gapNote": "Do not claim PLC ownership from the current demo evidence.",
                "rationale": "Blocked examples show what not to claim.",
            },
        ],
        "topEvidenceIds": ["ev-python-automation", "ev-validation-station"],
    },
    "fintech-backend-platform": {
        "application": APPLICATIONS[1],
        "requirements": [
            {
                "id": "req-fastapi-backend",
                "applicationId": "fintech-backend-platform",
                "text": "Python backend workflow tooling",
                "category": "technical",
                "priority": "must",
                "extractedFrom": "demo-role-description",
            },
            {
                "id": "req-java-cloud",
                "applicationId": "fintech-backend-platform",
                "text": "Java and cloud backend depth",
                "category": "technical",
                "priority": "should",
                "extractedFrom": "demo-role-description",
            },
        ],
        "evidence": [EVIDENCE[2], EVIDENCE[3]],
        "matrix": [
            {
                "requirementId": "req-fastapi-backend",
                "evidenceIds": ["ev-fastapi-reporting"],
                "bestEvidenceId": "ev-fastapi-reporting",
                "classification": "supported",
                "matchStrength": "strong",
                "riskLevel": "low",
                "safeClaimBlocked": False,
                "safeTalkingPoint": "Built a FastAPI demo that exposes reviewable evidence and report endpoints.",
                "gapNote": "Describe it as demo project work, not deployed service ownership.",
                "rationale": "The public repo contains the FastAPI implementation pattern.",
            },
            {
                "requirementId": "req-java-cloud",
                "evidenceIds": ["ev-unsupported-claims"],
                "bestEvidenceId": "ev-unsupported-claims",
                "classification": "partial",
                "matchStrength": "weak",
                "riskLevel": "high",
                "safeClaimBlocked": True,
                "gapNote": "Practice honest framing around non-Python backend gaps.",
                "rationale": "The demo supports backend workflow thinking but not Java or cloud depth.",
            },
        ],
        "topEvidenceIds": ["ev-fastapi-reporting"],
    },
}

INTERVIEW_PACKETS = {
    "aerospace-test-automation": {
        "applicationId": "aerospace-test-automation",
        "roleSummary": "Demo Test Automation Engineer role focused on Python automation and validation workflow review.",
        "whyThisRoleFits": [
            "Python automation evidence maps directly to the must-have test automation requirement.",
            "The fake validation station notes support a source-backed discussion of test workflow structure.",
        ],
        "topEvidenceIds": ["ev-python-automation", "ev-validation-station"],
        "topRisks": ["PLC integration depth is not supported by the current demo evidence."],
        "honestGapAnswers": [
            {
                "gap": "PLC integration depth",
                "answer": "I would frame this as a learning area and keep my supported examples focused on Python automation and validation workflow review.",
            }
        ],
        "likelyQuestions": [
            "Walk through how the demo validation workflow turns evidence into a reviewable report.",
            "How would you keep unsupported claims out of an interview answer?",
        ],
        "openingAnswer": "I work best on Python-first validation workflow tools where evidence, requirements, and claims stay traceable.",
        "questionsToAsk": [
            "Which validation workflow outputs are reviewed most often by engineers?",
            "Where do unsupported or partial claims create the most review overhead?",
        ],
        "followUpEmail": "Subject: Thanks for the conversation\n\nHi [Name],\n\nThank you for discussing the demo validation workflow. I appreciated learning more about the role requirements and the evidence review process.\n\nBest,\n[Your Name]",
        "practicePriority": {
            "focus": "Practice the Python automation and validation station story first.",
            "note": "Those are the strongest supported evidence areas for this demo application.",
        },
        "copyableAnswers": [
            {
                "label": "30-second version",
                "text": "I build Python workflow tools that keep requirements, evidence, and claim classification reviewable.",
                "context": "Short version for an initial screen.",
            }
        ],
    },
    "fintech-backend-platform": {
        "applicationId": "fintech-backend-platform",
        "roleSummary": "Demo Firmware Validation Engineer role framed around backend workflow tooling and honest gap handling.",
        "whyThisRoleFits": [
            "The FastAPI demo supports Python backend workflow discussion.",
            "The report writer shows traceable requirement-to-evidence output.",
        ],
        "topEvidenceIds": ["ev-fastapi-reporting"],
        "topRisks": ["Java and cloud backend depth are partial or unsupported in this demo."],
        "honestGapAnswers": [
            {
                "gap": "Java and cloud backend depth",
                "answer": "My strongest backend evidence here is Python and FastAPI demo work, so I would not present it as Java or cloud experience.",
            }
        ],
        "likelyQuestions": [
            "How does the API keep policy and classification decisions out of the frontend?",
            "What would you test before wiring this backend to a UI?",
        ],
        "openingAnswer": "This demo shows how I structure small FastAPI tools around traceable read models and public-safe evidence.",
        "questionsToAsk": [
            "Which read models should the backend own instead of the frontend?",
            "How are partial and unsupported claims reviewed in the workflow?",
        ],
        "followUpEmail": "Subject: Thanks for the conversation\n\nHi [Name],\n\nThank you for reviewing the demo backend workflow. I appreciated the discussion about traceable evidence and safe claim framing.\n\nBest,\n[Your Name]",
        "practicePriority": {
            "focus": "Practice the FastAPI evidence report walkthrough.",
            "note": "Keep Java and cloud depth framed as a current gap.",
        },
        "copyableAnswers": [
            {
                "label": "Backend version",
                "text": "My strongest backend example here is a FastAPI demo that returns reviewable evidence and dashboard read models.",
                "context": "Use when asked about backend project scope.",
            }
        ],
    },
}

GAPS = {
    "aerospace-test-automation": [
        {
            "id": "gap-plc-depth",
            "applicationId": "aerospace-test-automation",
            "gap": "PLC integration depth",
            "severity": "high",
            "whyItMatters": "The demo role may value station integration beyond Python automation.",
            "studyTask": "Review basic PLC terminology and how it connects to validation station workflows.",
            "proofTask": "Add a fake demo note that explains where PLC signals would enter the validation workflow.",
            "safeFraming": "My supported evidence is Python automation and validation workflow review; PLC depth is a current gap.",
            "status": "open",
        },
        {
            "id": "gap-hardware-specifics",
            "applicationId": "aerospace-test-automation",
            "gap": "Hardware-specific station details",
            "severity": "medium",
            "whyItMatters": "The public demo intentionally avoids private or hardware-specific details.",
            "studyTask": "Prepare a generic explanation of station inputs, outputs, and review artifacts.",
            "proofTask": "Create a fake station checklist under demo evidence if more detail is needed.",
            "safeFraming": "I can discuss the workflow pattern without claiming private station specifics.",
            "status": "in_progress",
        },
    ],
    "fintech-backend-platform": [
        {
            "id": "gap-java-cloud",
            "applicationId": "fintech-backend-platform",
            "gap": "Java and cloud backend depth",
            "severity": "high",
            "whyItMatters": "The current evidence supports Python and FastAPI, not Java or cloud operations.",
            "studyTask": "Review Spring Boot controller, service, and repository structure at a demo level.",
            "proofTask": "Build a tiny fake-data REST API if Java evidence becomes necessary.",
            "safeFraming": "My strongest backend evidence here is Python and FastAPI demo work.",
            "status": "open",
        }
    ],
}

PREP_ACTIONS = [
    {
        "label": "Validation role",
        "detail": "Practice the Python automation answer and the honest PLC gap frame.",
    },
    {
        "label": "Backend role",
        "detail": "Prepare the FastAPI demo walkthrough and avoid unsupported cloud claims.",
    },
]

DASHBOARD_SUMMARY = {
    "activeInterviews": 1,
    "highestRiskGap": "PLC integration depth",
    "nextAction": "Practice role-specific answers with source-backed evidence only",
    "strongestTestAutomationEvidenceId": "ev-python-automation",
    "strongestBackendEvidenceSummary": "FastAPI demo endpoints and markdown evidence report workflow",
}


def list_applications() -> list[dict[str, object]]:
    return deepcopy(APPLICATIONS)


def list_evidence() -> list[dict[str, object]]:
    return deepcopy(EVIDENCE)


def get_application_detail(application_id: str) -> dict[str, object]:
    if application_id not in APPLICATION_DETAILS:
        raise HTTPException(status_code=404, detail="Application not found")
    return deepcopy(APPLICATION_DETAILS[application_id])


def get_interview_packet(application_id: str) -> dict[str, object]:
    if application_id not in INTERVIEW_PACKETS:
        raise HTTPException(status_code=404, detail="Application not found")
    return deepcopy(INTERVIEW_PACKETS[application_id])


def get_gaps(application_id: str) -> list[dict[str, object]]:
    if application_id not in GAPS:
        raise HTTPException(status_code=404, detail="Application not found")
    return deepcopy(GAPS[application_id])


def get_dashboard_summary() -> dict[str, object]:
    return deepcopy(DASHBOARD_SUMMARY)


def list_prep_actions() -> list[dict[str, str]]:
    return deepcopy(PREP_ACTIONS)
