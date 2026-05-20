from app.evidence_loader import load_evidence_files, load_role_description
from app.main import DATA_DIR, ROLE_PATH


def test_demo_evidence_files_load_with_repo_relative_provenance():
    sources = load_evidence_files(DATA_DIR)
    source_paths = {source.source_path for source in sources}

    assert len(sources) >= 4
    assert "data/demo_evidence/validation_station_notes.md" in source_paths
    assert "data/demo_evidence/python_automation_notes.md" in source_paths
    assert "data/demo_evidence/firmware_log_review_notes.md" in source_paths
    assert "data/demo_evidence/unsupported_claim_examples.md" in source_paths
    assert all("\\" not in source.source_path for source in sources)
    assert all(":" not in source.source_path for source in sources)


def test_role_description_loads_from_demo_data():
    role = load_role_description(ROLE_PATH)

    assert role.source_path == "data/demo_evidence/sample_role_description.md"
    assert "Demo Firmware Validation Engineer" in role.content
    assert "Production database ownership" in role.content
