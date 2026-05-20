from pathlib import Path

from app.schemas import Claim

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SECTION_TITLES = {
    "supported": "Supported Claims",
    "partial": "Partial Claims",
    "unsupported": "Unsupported Claims",
}


def _render_source_path(source_path: str, project_root: Path = PROJECT_ROOT) -> str:
    source = Path(source_path)
    try:
        rendered = source.resolve().relative_to(project_root.resolve())
    except ValueError:
        try:
            rendered = source.relative_to(project_root)
        except ValueError:
            return source.name
    return rendered.as_posix()


def build_markdown_report(claims: list[Claim]) -> str:
    lines = [
        "# TraceOps Evidence Demo Report",
        "",
        "This report uses fake demo data and keeps source provenance visible.",
        "",
    ]

    for label, title in SECTION_TITLES.items():
        lines.append(f"## {title}")
        section_claims = [claim for claim in claims if claim.label == label]
        if not section_claims:
            lines.extend(["", "No claims in this section.", ""])
            continue

        for claim in section_claims:
            lines.append(f"- **{claim.statement}**")
            lines.append(f"  - Rationale: {claim.rationale}")
            if claim.source_paths:
                lines.append("  - Sources:")
                for source_path in claim.source_paths:
                    lines.append(f"    - `{_render_source_path(source_path)}`")
            else:
                lines.append("  - Sources: No source evidence found.")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_report(output_path: str | Path, claims: list[Claim]) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    report = build_markdown_report(claims)
    path.write_text(report, encoding="utf-8")
    return report
