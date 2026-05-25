from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse

from app.agent_contract import get_agent_integration_contract
from app.claim_policy import classify_matches
from app.evidence_loader import load_evidence_files, load_role_description
from app.report_writer import build_markdown_report, write_report
from app.requirement_mapper import extract_requirements, map_requirements_to_evidence
from scripts.check_public_safety import find_public_safety_violations

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
    evidence_paths = [source.source_path for source in evidence]
    report = write_report(output_path, claims, evidence_paths, role.source_path)
    return {
        "evidence_count": len(evidence),
        "requirement_count": len(requirements),
        "claim_count": len(claims),
        "output_path": "outputs/demo_report.md",
        "requirements": requirements,
        "claims": claims,
        "evidence": evidence,
        "report": report,
    }


def _build_result_without_writing() -> dict[str, object]:
    evidence = load_evidence_files(DATA_DIR)
    role = load_role_description(ROLE_PATH)
    requirements = extract_requirements(role.content)
    matches = map_requirements_to_evidence(requirements, evidence)
    claims = classify_matches(matches)
    report = build_markdown_report(
        claims,
        [source.source_path for source in evidence],
        role.source_path,
    )
    return {
        "evidence": evidence,
        "requirements": requirements,
        "claims": claims,
        "report": report,
    }


def _claim_count(claims: list[object], label: str) -> int:
    return sum(1 for claim in claims if getattr(claim, "label") == label)


def _html_page(title: str, body: str) -> HTMLResponse:
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; line-height: 1.45; max-width: 960px; }}
    code {{ background: #f2f2f2; padding: 0.1rem 0.25rem; }}
    section {{ border-top: 1px solid #ddd; padding-top: 1rem; margin-top: 1rem; }}
    .status {{ font-weight: 700; text-transform: capitalize; }}
  </style>
</head>
<body>
{body}
</body>
</html>"""
    return HTMLResponse(html)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    result = _build_result_without_writing()
    claims = result["claims"]
    violations = find_public_safety_violations(PROJECT_ROOT)
    body = f"""
<h1>TraceOps Evidence Demo</h1>
<p>A fake-data validation workflow that maps role requirements to source-backed evidence.</p>
<section>
  <h2>Decision Summary</h2>
  <ul>
    <li>Supported claims: {_claim_count(claims, "supported")}</li>
    <li>Partial claims: {_claim_count(claims, "partial")}</li>
    <li>Unsupported claims: {_claim_count(claims, "unsupported")}</li>
  </ul>
</section>
<section>
  <h2>Public Safety</h2>
  <p>{'passed' if not violations else 'review required'}</p>
</section>
<section>
  <h2>Routes</h2>
  <ul>
    <li><code>/evidence</code></li>
    <li><code>/report</code></li>
    <li><code>/demo/report</code></li>
    <li><code>/agent/contract</code></li>
  </ul>
</section>
"""
    return _html_page("TraceOps Evidence Demo", body)


@app.get("/evidence")
def evidence_inventory() -> dict[str, object]:
    role = load_role_description(ROLE_PATH)
    evidence = load_evidence_files(DATA_DIR)
    return {
        "role_source": role.source_path,
        "requirements": extract_requirements(role.content),
        "evidence": [
            {"source_path": source.source_path, "title": source.title}
            for source in evidence
        ],
    }


@app.get("/report", response_class=PlainTextResponse)
def report_preview() -> str:
    result = _build_result_without_writing()
    return str(result["report"])


@app.get("/demo/evidence")
def demo_evidence() -> dict[str, object]:
    return evidence_inventory()


@app.post("/demo/report")
def demo_report() -> dict[str, object]:
    result = run_workflow()
    return {
        "output_path": result["output_path"],
        "claim_count": result["claim_count"],
        "requirement_count": result["requirement_count"],
        "evidence_count": result["evidence_count"],
    }


@app.get("/agent/contract")
def agent_contract() -> dict[str, object]:
    return get_agent_integration_contract()
