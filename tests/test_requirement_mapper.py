from app.evidence_loader import load_evidence_files, load_role_description
from app.main import DATA_DIR, ROLE_PATH
from app.requirement_mapper import extract_requirements, map_requirements_to_evidence
from app.schemas import EvidenceSource


def test_extract_requirements_uses_role_bullets_as_reviewable_items():
    role_text = """
# Demo Firmware Validation Engineer

Requirements:
- Python automation for validation workflows.
- Hardware test station debugging.
"""

    requirements = extract_requirements(role_text)

    assert requirements == [
        "Python automation for validation workflows",
        "Hardware test station debugging",
    ]


def test_demo_requirement_extraction_returns_expected_keys():
    role = load_role_description(ROLE_PATH)

    requirements = extract_requirements(role.content)

    assert "Python automation for validation workflows" in requirements
    assert "Telemetry log review and evidence summaries" in requirements
    assert "Validation station bring-up and fixture lane debugging" in requirements
    assert "Production database ownership" in requirements


def test_supported_requirements_require_direct_source_evidence():
    role = load_role_description(ROLE_PATH)
    evidence = load_evidence_files(DATA_DIR)

    mapped = map_requirements_to_evidence(extract_requirements(role.content), evidence)
    by_requirement = {match.requirement: match for match in mapped}

    claim = by_requirement["Python automation for validation workflows"]
    assert claim.status == "supported"
    assert claim.source_paths == ["data/demo_evidence/python_automation_notes.md"]


def test_partial_matches_include_weak_source_paths():
    requirements = ["Python automation validation workflows"]
    evidence = [
        EvidenceSource(
            source_path="data/demo_evidence/sample_python_tooling_notes.md",
            title="Python notes",
            content="Created Python automation utilities.",
        )
    ]

    mapped = map_requirements_to_evidence(requirements, evidence)

    assert mapped[0].status == "partial"
    assert mapped[0].source_paths == ["data/demo_evidence/sample_python_tooling_notes.md"]


def test_unsupported_requirements_have_no_sources_and_are_not_promoted():
    requirements = ["Production database ownership"]
    evidence = [
        EvidenceSource(
            source_path="data/demo_evidence/unsupported_claim_examples.md",
            title="Unsupported claim examples",
            content=(
                "Unsupported review item: ownership claim was requested, "
                "but no source evidence was found."
            ),
        )
    ]

    mapped = map_requirements_to_evidence(requirements, evidence)

    assert mapped[0].status == "unsupported"
    assert mapped[0].source_paths == []
