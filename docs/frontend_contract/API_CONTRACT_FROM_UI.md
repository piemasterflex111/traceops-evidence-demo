# API Contract From Current UI

This contract is derived from the existing React/TanStack UI and `src/lib/traceops/types.ts`. A future FastAPI backend should return these read models without requiring the frontend to derive policy, classification, risk, or safe-claim state.

All endpoints are read-only `GET` endpoints for the first integration pass.

## Shared Types

```ts
type ApplicationStatus = "tracking" | "applied" | "interviewing" | "offer" | "closed";
type PolicyStatus = "allowed" | "blocked" | "needs_review";
type Classification = "supported" | "partial" | "unsupported";
type MatchStrength = "strong" | "moderate" | "weak" | "none";
type RiskLevel = "low" | "medium" | "high";
type GapStatus = "open" | "in_progress" | "addressed";
type RequirementPriority = "must" | "should" | "nice";
type DemoTag = "aerospace-test-automation" | "fintech-backend-platform";
```

Public-safe constraint for every endpoint: public/demo responses must not include real company names, recruiter names, private interview details, private slugs, or production claims that are not supported by policy-approved evidence.

## GET /api/applications

Purpose: list tracked applications for the dashboard and applications table.

Frontend screens: `/`, `/applications`.

Expected response shape:

```json
[
  {
    "id": "aerospace-test-automation",
    "company": "Aerospace Manufacturing Automation Co.",
    "role": "Test Automation Engineer",
    "status": "interviewing",
    "createdAt": "2026-05-12T00:00:00Z",
    "demo": "aerospace-test-automation",
    "interviewTime": "Upcoming technical screen",
    "primaryFitTheme": "Python test automation...",
    "topRisk": "PLC/Siemens depth",
    "nextAction": "Practice the multi-channel..."
  }
]
```

Required fields:

- `id: string`
- `company: string`
- `role: string`
- `status: ApplicationStatus`
- `createdAt: string` ISO date/time string

Optional fields:

- `demo?: DemoTag`
- `interviewTime?: string`
- `primaryFitTheme?: string`
- `topRisk?: string`
- `nextAction?: string`

Enum/status fields:

- `status`: `tracking`, `applied`, `interviewing`, `offer`, `closed`
- `demo`: public demo tag when applicable

Public-safe constraints:

- In public mode, `id` must be an anonymized slug.
- `company` and `role` must be public-safe display strings.
- `interviewTime` must remain generic unless private mode is explicitly enabled later.

## GET /api/applications/{application_id}

Purpose: return the complete application detail read model: overview, requirements, evidence library available to that application, matrix cells, and top evidence references.

Frontend screens: `/applications/$applicationId`, also loaded by `/applications/$applicationId/interview-packet` and `/applications/$applicationId/gaps` for page headers and evidence lookups.

Expected response shape:

```json
{
  "application": {
    "id": "aerospace-test-automation",
    "company": "Aerospace Manufacturing Automation Co.",
    "role": "Test Automation Engineer",
    "status": "interviewing",
    "createdAt": "2026-05-12T00:00:00Z"
  },
  "requirements": [
    {
      "id": "req-h-py",
      "applicationId": "aerospace-test-automation",
      "text": "Python test automation",
      "category": "technical",
      "priority": "must",
      "extractedFrom": "job-description"
    }
  ],
  "evidence": [
    {
      "id": "ev-rs232",
      "title": "Python serial telemetry logger",
      "source": "Aerospace manufacturing/test environment",
      "domain": "python-automation",
      "policyStatus": "allowed",
      "provenance": "career/aerospace-mfg/serial-logger"
    }
  ],
  "matrix": [
    {
      "requirementId": "req-h-py",
      "evidenceIds": ["ev-rs232"],
      "bestEvidenceId": "ev-rs232",
      "classification": "supported",
      "matchStrength": "strong",
      "riskLevel": "low",
      "safeClaimBlocked": false,
      "safeTalkingPoint": "Wrote Python that...",
      "gapNote": "Single-script scope..."
    }
  ],
  "topEvidenceIds": ["ev-rs232"]
}
```

Required fields:

- `application: Application`
- `requirements: Requirement[]`
- `evidence: Evidence[]`
- `matrix: MatrixCell[]`
- `topEvidenceIds: string[]`

Required `Requirement` fields:

- `id: string`
- `applicationId: string`
- `text: string`
- `category: string`
- `priority: RequirementPriority`

Optional `Requirement` fields:

- `extractedFrom?: string`

Required `Evidence` fields:

- `id: string`
- `title: string`
- `source: string`
- `domain: string`
- `policyStatus: PolicyStatus`
- `provenance: string`

Optional `Evidence` fields:

- `sourceUrl?: string`
- `summary?: string`
- `bestFit?: string`
- `riskNote?: string`

Required `MatrixCell` fields:

- `requirementId: string`
- `evidenceIds: string[]`
- `classification: Classification`
- `matchStrength: MatchStrength`
- `riskLevel: RiskLevel`
- `safeClaimBlocked: boolean`

Optional `MatrixCell` fields:

- `bestEvidenceId?: string`
- `safeTalkingPoint?: string`
- `gapNote?: string`
- `rationale?: string`

Enum/status fields:

- Application, policy, classification, match, risk, and priority enums listed under shared types.

Public-safe constraints:

- Matrix cells must be backend-provided or demo-data-provided. React should not infer claim safety.
- If `safeClaimBlocked` is true, omit `safeTalkingPoint` or keep it non-claiming.
- `evidenceIds`, `bestEvidenceId`, and `topEvidenceIds` must reference evidence included in `evidence` or be intentionally absent.

## GET /api/evidence

Purpose: return the evidence library for dashboard counts, recent evidence, evidence filtering, and policy badge rendering.

Frontend screens: `/`, `/evidence`.

Expected response shape:

```json
[
  {
    "id": "ev-traceops",
    "title": "TraceOps Evidence Operations",
    "source": "TraceOps project",
    "sourceUrl": "https://example.invalid/public-demo",
    "domain": "internal-tools",
    "policyStatus": "allowed",
    "provenance": "projects/traceops",
    "summary": "FastAPI evidence-governance app...",
    "bestFit": "Internal tools / Python backend / AI workflow systems",
    "riskNote": "Project/tool proof, not direct career production experience."
  }
]
```

Required fields:

- `id: string`
- `title: string`
- `source: string`
- `domain: string`
- `policyStatus: PolicyStatus`
- `provenance: string`

Optional fields:

- `sourceUrl?: string`
- `summary?: string`
- `bestFit?: string`
- `riskNote?: string`

Enum/status fields:

- `policyStatus`: `allowed`, `blocked`, `needs_review`

Public-safe constraints:

- `source`, `provenance`, and `sourceUrl` must not reveal private employers, contacts, hidden repos, private slugs, or private interview context in public mode.
- Blocked evidence can be listed, but must not be used for safe claims.

## GET /api/dashboard/summary

Purpose: return dashboard-level summary values that the UI should display without recalculating from private logic.

Frontend screen: `/`.

Expected response shape:

```json
{
  "activeInterviews": 2,
  "highestRiskGap": "Java/Spring/AWS production backend depth",
  "nextAction": "Practice role-specific answer and honest gap framing",
  "strongestTestAutomationEvidenceId": "ev-16ch",
  "strongestBackendEvidenceSummary": "FastAPI / SQLAlchemy / workflow automation projects"
}
```

Required fields:

- `activeInterviews: number`
- `highestRiskGap: string`
- `nextAction: string`
- `strongestTestAutomationEvidenceId: string`
- `strongestBackendEvidenceSummary: string`

Optional fields:

- None currently consumed by the UI.

Enum/status fields:

- None.

Public-safe constraints:

- Summary text must be public-safe and non-private.
- `strongestTestAutomationEvidenceId` should reference an item returned by `GET /api/evidence`.
- Do not expose internal ranking logic or unsupported production claims.

## GET /api/dashboard/prep-actions

Purpose: return short dashboard action cards.

Frontend screen: `/`.

Expected response shape:

```json
[
  {
    "label": "Backend role",
    "detail": "Prepare honest Java/Spring/AWS gap answer."
  }
]
```

Required fields:

- `label: string`
- `detail: string`

Optional fields:

- None currently consumed by the UI.

Enum/status fields:

- None.

Public-safe constraints:

- Keep actions generic in public mode.
- Do not include private recruiter names, exact interview timing, or private company identifiers.

## GET /api/applications/{application_id}/interview-packet

Purpose: return a complete interview-prep packet for one application.

Frontend screen: `/applications/$applicationId/interview-packet`.

Expected response shape:

```json
{
  "applicationId": "aerospace-test-automation",
  "roleSummary": "Test Automation Engineer at ...",
  "whyThisRoleFits": ["Direct manufacturing-test experience..."],
  "topEvidenceIds": ["ev-16ch", "ev-rs232"],
  "topRisks": ["PLC/Siemens depth..."],
  "honestGapAnswers": [
    {
      "gap": "PLC / Siemens depth",
      "answer": "I haven't owned a Siemens or PLC stack in production..."
    }
  ],
  "likelyQuestions": ["Walk me through a test station..."],
  "openingAnswer": "I'm a Python-first engineer...",
  "questionsToAsk": ["What does a good week look like..."],
  "followUpEmail": "Subject: Thanks for the conversation...",
  "practicePriority": {
    "focus": "Practice multi-channel station story first.",
    "note": "This is your strongest evidence..."
  },
  "copyableAnswers": [
    {
      "label": "30-second version",
      "text": "Python-first engineer...",
      "context": "Short version for recruiter screens..."
    }
  ]
}
```

Required fields:

- `applicationId: string`
- `roleSummary: string`
- `whyThisRoleFits: string[]`
- `topEvidenceIds: string[]`
- `topRisks: string[]`
- `honestGapAnswers: { gap: string; answer: string }[]`
- `likelyQuestions: string[]`
- `openingAnswer: string`
- `questionsToAsk: string[]`
- `followUpEmail: string`
- `practicePriority: { focus: string; note?: string }`
- `copyableAnswers: { label: string; text: string; context?: string }[]`

Optional fields:

- `practicePriority.note?: string`
- `copyableAnswers[].context?: string`

Enum/status fields:

- None directly, but `topEvidenceIds` must align with evidence policy state.

Public-safe constraints:

- Follow-up emails must use placeholders such as `[Name]`, not recruiter names.
- Do not include exact private interview dates/times.
- Opening answers and copyable answers must not overstate blocked or unsupported evidence.
- `topEvidenceIds` should reference evidence from `GET /api/applications/{application_id}`.

## GET /api/applications/{application_id}/gaps

Purpose: return gap tracker rows for one application.

Frontend screen: `/applications/$applicationId/gaps`.

Expected response shape:

```json
[
  {
    "id": "gap-be-java",
    "applicationId": "fintech-backend-platform",
    "gap": "Java / Spring production backend depth",
    "severity": "high",
    "whyItMatters": "Role title explicitly includes Java...",
    "studyTask": "Learn Spring Boot controller/service/repository structure...",
    "proofTask": "Build a tiny Java/Spring REST API...",
    "safeFraming": "My strongest recent backend work is Python/FastAPI...",
    "status": "open"
  }
]
```

Required fields:

- `id: string`
- `applicationId: string`
- `gap: string`
- `severity: RiskLevel`
- `whyItMatters: string`
- `studyTask: string`
- `proofTask: string`
- `safeFraming: string`
- `status: GapStatus`

Optional fields:

- None currently consumed by the UI.

Enum/status fields:

- `severity`: `low`, `medium`, `high`
- `status`: `open`, `in_progress`, `addressed`

Public-safe constraints:

- Gap wording must be honest and public-safe.
- `safeFraming` must not claim unsupported experience.
- Do not expose private interview feedback or private employer identifiers.
