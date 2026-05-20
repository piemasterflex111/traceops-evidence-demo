from app.report_writer import build_markdown_report, write_report
from app.schemas import Claim


def test_report_writer_includes_review_sections_and_source_provenance(tmp_path):
    claims = [
        Claim(
            requirement="Python automation",
            label="supported",
            statement="Supported: Python automation",
            rationale="Supported by demo evidence.",
            source_paths=["data/demo_evidence/sample_python_tooling_notes.md"],
        ),
        Claim(
            requirement="firmware release ownership",
            label="unsupported",
            statement="Unsupported: firmware release ownership",
            rationale="No matching demo evidence was found.",
            source_paths=[],
        ),
    ]

    report = build_markdown_report(
        claims,
        evidence_sources=["data/demo_evidence/python_automation_notes.md"],
        role_source="data/demo_evidence/sample_role_description.md",
    )

    assert "## Input Summary" in report
    assert "## Evidence Sources" in report
    assert "## Decision Summary" in report
    assert "## Supported Claims" in report
    assert "## Partial Claims" in report
    assert "## Unsupported Claims" in report
    assert "## Review Notes" in report
    assert "## Source Provenance" in report
    assert "data/demo_evidence/sample_python_tooling_notes.md" in report
    assert "No source evidence found" in report

    output_path = tmp_path / "demo_report.md"
    write_report(
        output_path,
        claims,
        evidence_sources=["data/demo_evidence/python_automation_notes.md"],
        role_source="data/demo_evidence/sample_role_description.md",
    )
    assert output_path.read_text(encoding="utf-8") == report


def test_report_writer_renders_repo_relative_source_paths():
    claims = [
        Claim(
            requirement="Python automation",
            label="supported",
            statement="Supported: Python automation",
            rationale="Supported by demo evidence.",
            source_paths=[
                "data/demo_evidence/python_automation_notes.md",
            ],
        )
    ]

    report = build_markdown_report(claims)

    assert "data/demo_evidence/python_automation_notes.md" in report
    assert "C:" + "\\" not in report
    assert "C:" + "/" not in report
    assert "AIWork" not in report
    assert "Users" not in report
