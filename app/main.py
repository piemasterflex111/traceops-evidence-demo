from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse

from app.claim_policy import classify_matches
from app.demo_api_data import (
    get_application_detail,
    get_dashboard_summary,
    get_gaps,
    get_interview_packet,
    list_applications,
    list_evidence,
    list_prep_actions,
)
from app.evidence_loader import load_evidence_files, load_role_description
from app.report_writer import build_markdown_report, write_report
from app.requirement_mapper import extract_requirements, map_requirements_to_evidence
from scripts.check_public_safety import find_public_safety_violations

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "demo_evidence"
ROLE_PATH = DATA_DIR / "sample_role_description.md"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "demo_report.md"

app = FastAPI(title="TraceOps Evidence Demo")

ROUTE_CATALOG = [
    {
        "method": "GET",
        "path": "/health",
        "purpose": "Health check for local verification.",
        "browser_openable": True,
    },
    {
        "method": "GET",
        "path": "/api/applications",
        "purpose": "List public-safe demo applications.",
        "browser_openable": True,
    },
    {
        "method": "GET",
        "path": "/api/applications/{application_id}",
        "purpose": "Application detail, requirements, evidence, and matrix.",
        "browser_openable": True,
    },
    {
        "method": "GET",
        "path": "/api/evidence",
        "purpose": "List public-safe demo evidence records.",
        "browser_openable": True,
    },
    {
        "method": "GET",
        "path": "/api/dashboard/summary",
        "purpose": "Dashboard summary read model.",
        "browser_openable": True,
    },
    {
        "method": "GET",
        "path": "/api/dashboard/prep-actions",
        "purpose": "Dashboard prep action cards.",
        "browser_openable": True,
    },
    {
        "method": "GET",
        "path": "/api/applications/{application_id}/interview-packet",
        "purpose": "Interview packet for a demo application.",
        "browser_openable": True,
    },
    {
        "method": "GET",
        "path": "/api/applications/{application_id}/gaps",
        "purpose": "Gap tracker rows for a demo application.",
        "browser_openable": True,
    },
    {
        "method": "GET",
        "path": "/",
        "purpose": "Human-readable route index and demo overview.",
        "browser_openable": True,
    },
    {
        "method": "GET",
        "path": "/evidence",
        "purpose": "Legacy evidence inventory endpoint.",
        "browser_openable": True,
    },
    {
        "method": "GET",
        "path": "/report",
        "purpose": "Plain-text markdown report preview.",
        "browser_openable": True,
    },
    {
        "method": "GET",
        "path": "/demo/evidence",
        "purpose": "Legacy demo evidence endpoint.",
        "browser_openable": True,
    },
    {
        "method": "POST",
        "path": "/demo/report",
        "purpose": "POST-only report generation endpoint.",
        "browser_openable": False,
    },
]


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


def _route_link(path: str) -> str:
    demo_application_id = "aerospace-test-automation"
    return path.replace("{application_id}", demo_application_id)


def _route_rows() -> str:
    rows = []
    for route in ROUTE_CATALOG:
        path = str(route["path"])
        method = str(route["method"])
        purpose = str(route["purpose"])
        if route["browser_openable"]:
            display_path = _route_link(path)
            path_html = f'<a href="{display_path}"><code>{path}</code></a>'
            browser = "Yes"
        else:
            path_html = f"<code>{path}</code>"
            browser = "No; POST-only"
        rows.append(
            "<tr>"
            f"<td><code>{method}</code></td>"
            f"<td>{path_html}</td>"
            f"<td>{purpose}</td>"
            f"<td>{browser}</td>"
            "</tr>"
        )
    return "\n".join(rows)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/applications")
def api_applications() -> list[dict[str, object]]:
    return list_applications()


@app.get("/api/applications/{application_id}")
def api_application_detail(application_id: str) -> dict[str, object]:
    return get_application_detail(application_id)


@app.get("/api/evidence")
def api_evidence() -> list[dict[str, object]]:
    return list_evidence()


@app.get("/api/dashboard/summary")
def api_dashboard_summary() -> dict[str, object]:
    return get_dashboard_summary()


@app.get("/api/dashboard/prep-actions")
def api_dashboard_prep_actions() -> list[dict[str, str]]:
    return list_prep_actions()


@app.get("/api/applications/{application_id}/interview-packet")
def api_interview_packet(application_id: str) -> dict[str, object]:
    return get_interview_packet(application_id)


@app.get("/api/applications/{application_id}/gaps")
def api_application_gaps(application_id: str) -> list[dict[str, object]]:
    return get_gaps(application_id)


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
  <p>Browser-openable GET routes are linked. <code>POST /demo/report</code> is POST-only and must be called from Swagger, PowerShell, curl, or client code. It is not meant to work from the browser address bar.</p>
  <table>
    <thead>
      <tr>
        <th>Method</th>
        <th>Path</th>
        <th>Purpose</th>
        <th>Browser-openable</th>
      </tr>
    </thead>
    <tbody>
      {_route_rows()}
    </tbody>
  </table>
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
