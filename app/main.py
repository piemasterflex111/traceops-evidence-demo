from pathlib import Path

from fastapi import FastAPI

from app.claim_policy import classify_matches
from app.evidence_loader import load_evidence_files, load_role_description
from app.report_writer import write_report
from app.requirement_mapper import extract_requirements, map_requirements_to_evidence

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "demo_evidence"
ROLE_PATH = DATA_DIR / "sample_role_description.md"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "demo_report.md"

app = FastAPI(title="TraceOps Evidence Demo")


def run_workflow(output_path: Path = OUTPUT_PATH) -> dict[str, object]:
    evidence = load_evidence_files(DATA_DIR)
    role = load_role_description(ROLE_PATH)
    requirements = extract_requirements(role.content)
    matches = map_requirements_to_evidence(requirements, evidence)
    claims = classify_matches(matches)
    report = write_report(output_path, claims)
    return {
        "evidence_count": len(evidence),
        "requirement_count": len(requirements),
        "claim_count": len(claims),
        "output_path": str(output_path),
        "report": report,
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/demo/evidence")
def demo_evidence() -> dict[str, object]:
    role = load_role_description(ROLE_PATH)
    evidence = load_evidence_files(DATA_DIR)
    return {
        "role_source": role.source_path,
        "evidence": [
            {"source_path": source.source_path, "title": source.title}
            for source in evidence
        ],
    }


@app.post("/demo/report")
def demo_report() -> dict[str, object]:
    result = run_workflow()
    return {
        "output_path": result["output_path"],
        "claim_count": result["claim_count"],
        "requirement_count": result["requirement_count"],
    }
