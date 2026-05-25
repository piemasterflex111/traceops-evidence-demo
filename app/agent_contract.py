def get_agent_integration_contract() -> dict[str, object]:
    """Return the public-safe contract for a future LLM-backed agent layer.

    This repository intentionally keeps the public demo deterministic and fake-data only.
    The contract below documents the backend boundary that a Qwen/vLLM agent service
    should satisfy before it is connected to a frontend or a private evidence store.
    """
    return {
        "contract_version": "0.1.0",
        "public_safe": True,
        "current_repo_mode": "deterministic_fake_data_demo",
        "intended_agent_backend": {
            "model_runtime": "Qwen served through vLLM behind a private FastAPI service",
            "execution_policy": "Python orchestrator controls tools; model returns structured JSON only",
            "data_policy": "No private resume, recruiter, company, or interview data in the public repo",
            "review_policy": "Generated claims must remain reviewable before promotion or export",
        },
        "required_agent_endpoint": {
            "method": "POST",
            "path": "/agents/job-fit/run",
            "request_fields": [
                "company",
                "role_title",
                "job_description",
                "resume_text",
                "evidence_notes",
            ],
            "response_fields": [
                "run_id",
                "match_score",
                "strong_matches",
                "weak_matches",
                "missing_skills",
                "risk_flags",
                "suggested_resume_bullets",
                "suggested_interview_talking_points",
                "next_actions",
            ],
        },
        "non_negotiable_controls": [
            "Validate model output against a schema before showing it in the UI",
            "Save an input snapshot and output snapshot for each run",
            "Keep unsupported claims visible instead of rewriting them as strengths",
            "Store API keys and private evidence outside the browser",
            "Export markdown only after human review",
        ],
        "completion_sequence": [
            "Keep this public repo deterministic and fake-data safe",
            "Build the private Qwen/vLLM FastAPI agent backend separately",
            "Connect the UI companion to the private backend through this contract",
            "Add run history, markdown export, and review states",
            "Document screenshots and test evidence in the public repo without private data",
        ],
    }
