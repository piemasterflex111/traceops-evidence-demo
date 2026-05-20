from pathlib import Path

from app.schemas import EvidenceSource, RoleDescription


def _title_from_markdown(path: Path, content: str) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("_", " ").title()


def load_evidence_files(
    evidence_dir: str | Path,
    role_filename: str = "sample_role_description.md",
) -> list[EvidenceSource]:
    directory = Path(evidence_dir)
    sources: list[EvidenceSource] = []
    for path in sorted(directory.glob("*.md")):
        if path.name == role_filename:
            continue
        content = path.read_text(encoding="utf-8").strip()
        sources.append(
            EvidenceSource(
                source_path=str(path),
                title=_title_from_markdown(path, content),
                content=content,
            )
        )
    return sources


def load_role_description(role_path: str | Path) -> RoleDescription:
    path = Path(role_path)
    return RoleDescription(
        source_path=str(path),
        content=path.read_text(encoding="utf-8").strip(),
    )
