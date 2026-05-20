from app.claim_policy import classify_claim
from app.schemas import RequirementMatch


def test_supported_claim_requires_direct_evidence():
    match = RequirementMatch(
        requirement="Python automation",
        status="supported",
        source_paths=["data/demo_evidence/sample_python_tooling_notes.md"],
        matched_terms=["python", "automation"],
    )

    claim = classify_claim(match)

    assert claim.label == "supported"
    assert "Supported by demo evidence" in claim.rationale


def test_unsupported_claim_is_flagged_instead_of_presented_as_proven():
    match = RequirementMatch(
        requirement="firmware release ownership",
        status="unsupported",
        source_paths=[],
        matched_terms=[],
    )

    claim = classify_claim(match)

    assert claim.label == "unsupported"
    assert claim.statement.startswith("Unsupported")
    assert claim.source_paths == []


def test_partial_claim_requires_at_least_one_source():
    match = RequirementMatch(
        requirement="Python automation",
        status="partial",
        source_paths=[],
        matched_terms=["python"],
    )

    claim = classify_claim(match)

    assert claim.label == "unsupported"
    assert claim.statement.startswith("Unsupported")
    assert claim.source_paths == []


def test_partial_claim_lists_weak_source_evidence():
    match = RequirementMatch(
        requirement="Python automation validation workflows",
        status="partial",
        source_paths=["data/demo_evidence/sample_python_tooling_notes.md"],
        matched_terms=["python", "automation"],
    )

    claim = classify_claim(match)

    assert claim.label == "partial"
    assert claim.source_paths == ["data/demo_evidence/sample_python_tooling_notes.md"]


def test_unsupported_claim_is_not_promoted_when_matched_terms_are_present():
    match = RequirementMatch(
        requirement="Production firmware ownership",
        status="unsupported",
        source_paths=["data/demo_evidence/unsupported_claim_examples.md"],
        matched_terms=["firmware", "ownership"],
    )

    claim = classify_claim(match)

    assert claim.label == "unsupported"
    assert claim.source_paths == []
