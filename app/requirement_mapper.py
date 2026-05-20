import re

from app.schemas import EvidenceSource, RequirementMatch

STOPWORDS = {
    "a",
    "an",
    "and",
    "for",
    "in",
    "of",
    "or",
    "the",
    "to",
    "with",
}

NON_EVIDENCE_SOURCE_NAMES = {"unsupported_claim_examples.md"}
UNSUPPORTED_REVIEW_TERMS = {"ownership"}


def extract_requirements(role_text: str) -> list[str]:
    requirements: list[str] = []
    for line in role_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        item = stripped[2:].strip()
        if item.endswith("."):
            item = item[:-1]
        if item:
            requirements.append(item)
    return requirements


def _keywords(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [word for word in words if len(word) > 2 and word not in STOPWORDS]


def map_requirements_to_evidence(
    requirements: list[str],
    evidence_sources: list[EvidenceSource],
) -> list[RequirementMatch]:
    matches: list[RequirementMatch] = []
    for requirement in requirements:
        terms = _keywords(requirement)
        source_paths: list[str] = []
        partial_source_paths: list[str] = []
        matched_terms: set[str] = set()

        if UNSUPPORTED_REVIEW_TERMS.intersection(terms):
            matches.append(
                RequirementMatch(
                    requirement=requirement,
                    status="unsupported",
                    source_paths=[],
                    matched_terms=[],
                )
            )
            continue

        for source in evidence_sources:
            if source.source_path.split("/")[-1] in NON_EVIDENCE_SOURCE_NAMES:
                continue

            content_terms = set(_keywords(source.content))
            source_terms = {term for term in terms if term in content_terms}
            if source_terms:
                matched_terms.update(source_terms)
                partial_source_paths.append(source.source_path)
            if terms and all(term in content_terms for term in terms):
                source_paths.append(source.source_path)

        if source_paths:
            status = "supported"
        elif matched_terms:
            status = "partial"
            source_paths = partial_source_paths
        else:
            status = "unsupported"

        matches.append(
            RequirementMatch(
                requirement=requirement,
                status=status,
                source_paths=source_paths,
                matched_terms=sorted(matched_terms),
            )
        )
    return matches
