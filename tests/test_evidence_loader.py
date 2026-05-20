from pathlib import Path

from app.evidence_loader import load_evidence_files, load_role_description


def test_load_evidence_files_reads_markdown_sources_with_provenance(tmp_path):
    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir()
    (evidence_dir / "notes.md").write_text("Built station checks.", encoding="utf-8")
    (evidence_dir / "role.md").write_text("Role text.", encoding="utf-8")

    sources = load_evidence_files(evidence_dir, role_filename="role.md")

    assert len(sources) == 1
    assert sources[0].source_path == str(evidence_dir / "notes.md")
    assert sources[0].content == "Built station checks."


def test_load_role_description_reads_requested_file(tmp_path):
    role_file = tmp_path / "sample_role_description.md"
    role_file.write_text("Role requires Python validation tooling.", encoding="utf-8")

    role = load_role_description(role_file)

    assert role.source_path == str(role_file)
    assert "Python validation tooling" in role.content
