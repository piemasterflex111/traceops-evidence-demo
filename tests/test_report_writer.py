from pathlib import Path

from app.report_writer import build_markdown_report, write_report
from app.schemas import Claim


def test_report_writer_includes_source_provenance(tmp_path):
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

    report = build_markdown_report(claims)

    assert "## Supported Claims" in report
    assert "## Unsupported Claims" in report
    assert "data/demo_evidence/sample_python_tooling_notes.md" in report
    assert "No source evidence found" in report

    output_path = tmp_path / "demo_report.md"
    write_report(output_path, claims)
    assert output_path.read_text(encoding="utf-8") == report


def test_report_writer_renders_repo_relative_source_paths():
    absolute_source = (
        Path.cwd()
        / "data"
        / "demo_evidence"
        / "sample_python_tooling_notes.md"
    )
    claims = [
        Claim(
            requirement="Python automation",
            label="supported",
            statement="Supported: Python automation",
            rationale="Supported by demo evidence.",
            source_paths=[str(absolute_source)],
        )
    ]

    report = build_markdown_report(claims)

    assert "data/demo_evidence/sample_python_tooling_notes.md" in report
    assert "C:\\" not in report
    assert "C:/" not in report
    assert "AIWork" not in report
    assert "Users" not in report
