from app.schemas import Claim, RequirementMatch

VALID_LABELS = {"supported", "partial", "unsupported"}


def classify_claim(match: RequirementMatch) -> Claim:
    if match.status not in VALID_LABELS:
        status = "unsupported"
    else:
        status = match.status

    if status == "supported" and match.source_paths:
        return Claim(
            requirement=match.requirement,
            label="supported",
            statement=f"Supported: {match.requirement}",
            rationale="Supported by demo evidence with source provenance.",
            source_paths=match.source_paths,
        )

    if status == "partial" and match.source_paths:
        return Claim(
            requirement=match.requirement,
            label="partial",
            statement=f"Partial: {match.requirement}",
            rationale=(
                "Some requirement terms appear in demo evidence, but no single "
                "source supports the full requirement."
            ),
            source_paths=match.source_paths,
        )

    return Claim(
        requirement=match.requirement,
        label="unsupported",
        statement=f"Unsupported: {match.requirement}",
        rationale="No matching demo evidence was found.",
        source_paths=[],
    )


def classify_matches(matches: list[RequirementMatch]) -> list[Claim]:
    return [classify_claim(match) for match in matches]
