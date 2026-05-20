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


def test_map_requirements_records_matching_source_paths():
    requirements = ["Python automation", "hardware station"]
    evidence = [
        EvidenceSource(
            source_path="data/demo_evidence/sample_python_tooling_notes.md",
            title="Python notes",
            content="Created Python automation around validation checks.",
        )
    ]

    mapped = map_requirements_to_evidence(requirements, evidence)

    assert mapped[0].status == "supported"
    assert mapped[0].source_paths == ["data/demo_evidence/sample_python_tooling_notes.md"]
    assert mapped[1].status == "unsupported"
    assert mapped[1].source_paths == []


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
