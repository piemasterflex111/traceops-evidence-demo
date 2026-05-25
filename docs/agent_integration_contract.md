# Agent Integration Contract

This document defines the public-safe boundary between the current deterministic TraceOps Evidence Demo and a future private Qwen/vLLM agent backend.

The public repository intentionally stays fake-data only. The private backend can use real resume notes, job descriptions, recruiter context, or interview preparation material, but that private data must not be committed here.

## Current Public Repo Mode

```text
TraceOps Evidence Demo
  -> fake role description
  -> fake evidence markdown
  -> deterministic requirement mapping
  -> claim policy classification
  -> markdown report generation
  -> public-safety scan
```

This repo proves the evidence-governance pattern without requiring private data or external model calls.

## Future Private Agent Backend

```text
Lovable / React UI
  -> FastAPI agent backend
  -> Python orchestrator
  -> Qwen served by vLLM
  -> deterministic tools
  -> schema validation
  -> database run history
  -> human review
  -> markdown export
```

The model should not directly control the system. Python should own the workflow and call the model only for bounded structured outputs.

## Required Agent Endpoint

```http
POST /agents/job-fit/run
```

### Request Fields

```json
{
  "company": "string",
  "role_title": "string",
  "job_description": "string",
  "resume_text": "string",
  "evidence_notes": "string"
}
```

### Response Fields

```json
{
  "run_id": 1,
  "match_score": 0,
  "strong_matches": [],
  "weak_matches": [],
  "missing_skills": [],
  "risk_flags": [],
  "suggested_resume_bullets": [],
  "suggested_interview_talking_points": [],
  "next_actions": []
}
```

## Non-Negotiable Controls

1. Validate model output against a schema before showing it in the UI.
2. Save an input snapshot and output snapshot for each run.
3. Keep unsupported claims visible instead of rewriting them as strengths.
4. Store API keys, private evidence, and model configuration outside the browser.
5. Export markdown only after human review.
6. Keep the public repository fake-data safe.

## Why This Contract Matters

Without this boundary, the project can look like a static demo.

With this boundary, the project shows a stronger backend workflow pattern:

```text
messy input
  -> requirement extraction
  -> evidence matching
  -> claim policy
  -> structured output
  -> review state
  -> exportable artifact
```

That is the reusable pattern for job-fit analysis, validation planning, failure triage, and engineering worklog generation.

## Completion Sequence

1. Keep this public repo deterministic and fake-data safe.
2. Build the private Qwen/vLLM FastAPI agent backend separately.
3. Connect the UI companion to the private backend through this contract.
4. Add run history, markdown export, and review states.
5. Document screenshots and test evidence in the public repo without private data.
