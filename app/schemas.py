from dataclasses import dataclass, field


@dataclass(frozen=True)
class EvidenceSource:
    source_path: str
    title: str
    content: str


@dataclass(frozen=True)
class RoleDescription:
    source_path: str
    content: str


@dataclass(frozen=True)
class RequirementMatch:
    requirement: str
    status: str
    source_paths: list[str] = field(default_factory=list)
    matched_terms: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Claim:
    requirement: str
    label: str
    statement: str
    rationale: str
    source_paths: list[str] = field(default_factory=list)
