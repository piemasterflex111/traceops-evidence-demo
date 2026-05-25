# TraceOps API Contract

## Project Purpose

TraceOps Evidence Demo is a public-safe FastAPI backend that demonstrates an evidence workflow for interview preparation and portfolio review. It uses fake demo data to show how applications, requirements, evidence, claim safety, interview packets, and gap tracking can be returned as auditable read models.

All included data is fake/demo-safe. The API must not expose real company names, recruiter names, personal interview details, private slugs, local machine paths, or unsupported production claims.

## Route Table

| Method | Path | Purpose | Browser-openable |
| --- | --- | --- | --- |
| GET | `/health` | Health check for local verification. | Yes |
| GET | `/api/applications` | List public-safe demo applications. | Yes |
| GET | `/api/applications/{application_id}` | Return application overview, requirements, evidence, matrix, and top evidence IDs. | Yes |
| GET | `/api/evidence` | List public-safe evidence records. | Yes |
| GET | `/api/dashboard/summary` | Return dashboard summary fields. | Yes |
| GET | `/api/dashboard/prep-actions` | Return dashboard prep action cards. | Yes |
| GET | `/api/applications/{application_id}/interview-packet` | Return an interview packet for one demo application. | Yes |
| GET | `/api/applications/{application_id}/gaps` | Return gap tracker rows for one demo application. | Yes |
| GET | `/` | Human-readable route index and demo overview. | Yes |
| GET | `/evidence` | Legacy evidence inventory endpoint. | Yes |
| GET | `/report` | Plain-text markdown report preview. | Yes |
| GET | `/demo/evidence` | Legacy demo evidence endpoint. | Yes |
| POST | `/demo/report` | Generate the demo report output. | No; POST-only |

POST routes are not intended for the browser address bar. Use Swagger, PowerShell, curl, or client code.

## Endpoint Contracts

### GET /health

Purpose: confirm the local server is running.

Response:

```json
{
  "status": "ok"
}
```

Required fields:

- `status: "ok"`

### GET /api/applications

Purpose: list demo applications for dashboards and selection screens.

Response:

```json
[
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
    "nextAction": "Practice the validation station story with supported evidence only"
  }
]
```

Required fields:

- `id: string`
- `company: string`
- `role: string`
- `status: "tracking" | "applied" | "interviewing" | "offer" | "closed"`
- `createdAt: string`

Optional fields:

- `demo: string`
- `interviewTime: string`
- `primaryFitTheme: string`
- `topRisk: string`
- `nextAction: string`

### GET /api/applications/{application_id}

Purpose: return the full application detail read model used by a frontend role-fit screen.

Response:

```json
{
  "application": {},
  "requirements": [],
  "evidence": [],
  "matrix": [],
  "topEvidenceIds": []
}
```

Required top-level fields:

- `application: object`
- `requirements: array`
- `evidence: array`
- `matrix: array`
- `topEvidenceIds: array`

Requirement fields:

- Required: `id`, `applicationId`, `text`, `category`, `priority`
- Optional: `extractedFrom`
- `priority`: `must`, `should`, or `nice`

Evidence fields:

- Required: `id`, `title`, `source`, `domain`, `policyStatus`, `provenance`
- Optional: `sourceUrl`, `summary`, `bestFit`, `riskNote`
- `policyStatus`: `allowed`, `blocked`, or `needs_review`

Matrix cell fields:

- Required: `requirementId`, `evidenceIds`, `classification`, `matchStrength`, `riskLevel`, `safeClaimBlocked`
- Optional: `bestEvidenceId`, `safeTalkingPoint`, `gapNote`, `rationale`
- `classification`: `supported`, `partial`, or `unsupported`
- `matchStrength`: `strong`, `moderate`, `weak`, or `none`
- `riskLevel`: `low`, `medium`, or `high`

### GET /api/evidence

Purpose: list the demo evidence library.

Response:

```json
[
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
    "riskNote": "Demo evidence only; it does not claim live production ownership."
  }
]
```

Required fields:

- `id`, `title`, `source`, `domain`, `policyStatus`, `provenance`

Optional fields:

- `sourceUrl`, `summary`, `bestFit`, `riskNote`

### GET /api/dashboard/summary

Purpose: return dashboard headline values without requiring the frontend to derive safety state.

Response:

```json
{
  "activeInterviews": 1,
  "highestRiskGap": "PLC integration depth",
  "nextAction": "Practice role-specific answers with source-backed evidence only",
  "strongestTestAutomationEvidenceId": "ev-python-automation",
  "strongestBackendEvidenceSummary": "FastAPI demo endpoints and markdown evidence report workflow"
}
```

Required fields:

- `activeInterviews: number`
- `highestRiskGap: string`
- `nextAction: string`
- `strongestTestAutomationEvidenceId: string`
- `strongestBackendEvidenceSummary: string`

### GET /api/dashboard/prep-actions

Purpose: return short action cards for the dashboard.

Response:

```json
[
  {
    "label": "Validation role",
    "detail": "Practice the Python automation answer and the honest PLC gap frame."
  }
]
```

Required fields:

- `label: string`
- `detail: string`

### GET /api/applications/{application_id}/interview-packet

Purpose: return a public-safe interview packet for one demo application.

Response:

```json
{
  "applicationId": "aerospace-test-automation",
  "roleSummary": "Demo Test Automation Engineer role focused on Python automation and validation workflow review.",
  "whyThisRoleFits": [],
  "topEvidenceIds": [],
  "topRisks": [],
  "honestGapAnswers": [],
  "likelyQuestions": [],
  "openingAnswer": "I work best on Python-first validation workflow tools where evidence, requirements, and claims stay traceable.",
  "questionsToAsk": [],
  "followUpEmail": "Subject: Thanks for the conversation...",
  "practicePriority": {
    "focus": "Practice the Python automation and validation station story first.",
    "note": "Those are the strongest supported evidence areas for this demo application."
  },
  "copyableAnswers": []
}
```

Required fields:

- `applicationId`
- `roleSummary`
- `whyThisRoleFits`
- `topEvidenceIds`
- `topRisks`
- `honestGapAnswers`
- `likelyQuestions`
- `openingAnswer`
- `questionsToAsk`
- `followUpEmail`
- `practicePriority`
- `copyableAnswers`

Nested fields:

- `honestGapAnswers[]`: `gap`, `answer`
- `practicePriority`: `focus`; optional `note`
- `copyableAnswers[]`: `label`, `text`; optional `context`

### GET /api/applications/{application_id}/gaps

Purpose: return gap tracker rows for one demo application.

Response:

```json
[
  {
    "id": "gap-plc-depth",
    "applicationId": "aerospace-test-automation",
    "gap": "PLC integration depth",
    "severity": "high",
    "whyItMatters": "The demo role may value station integration beyond Python automation.",
    "studyTask": "Review basic PLC terminology and how it connects to validation station workflows.",
    "proofTask": "Add a fake demo note that explains where PLC signals would enter the validation workflow.",
    "safeFraming": "My supported evidence is Python automation and validation workflow review; PLC depth is a current gap.",
    "status": "open"
  }
]
```

Required fields:

- `id`
- `applicationId`
- `gap`
- `severity`
- `whyItMatters`
- `studyTask`
- `proofTask`
- `safeFraming`
- `status`

Enums:

- `severity`: `low`, `medium`, or `high`
- `status`: `open`, `in_progress`, or `addressed`

## Unknown Application IDs

Unknown application IDs return HTTP 404 for application-scoped API endpoints:

- `GET /api/applications/{application_id}`
- `GET /api/applications/{application_id}/interview-packet`
- `GET /api/applications/{application_id}/gaps`

Expected response body:

```json
{
  "detail": "Application not found"
}
```

## How To Verify Locally

Start the server:

```powershell
python -m uvicorn app.main:app --reload
```

Check core endpoints:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/api/applications
Invoke-RestMethod http://127.0.0.1:8000/api/evidence
Invoke-RestMethod http://127.0.0.1:8000/api/dashboard/summary
```

Run automated checks:

```powershell
python -m pytest -q
python scripts/check_public_safety.py
python scripts/smoke_api.py
```

## How To Explain This In An Interview

This backend is a small, demo-safe evidence workflow. It separates evidence records, role requirements, classification decisions, interview packet content, and gap tracking into explicit API read models. The goal is auditability: a frontend can render useful interview-prep screens without inventing claims, deriving risk state, or exposing private data.
