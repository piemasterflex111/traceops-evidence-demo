from pathlib import Path
from collections import Counter

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


def _render_source_list(source_paths: list[str]) -> list[str]:
    return sorted({_render_source_path(source_path) for source_path in source_paths})


def build_markdown_report(
    claims: list[Claim],
    evidence_sources: list[str] | None = None,
    role_source: str | None = None,
) -> str:
    counts = Counter(claim.label for claim in claims)
    rendered_sources = _render_source_list(evidence_sources or [])
    lines = [
        "# TraceOps Evidence Demo Report",
        "",
        "This report uses fake demo data and keeps source provenance visible for review.",
        "",
        "## Input Summary",
        "",
        f"- Role description: `{_render_source_path(role_source) if role_source else 'not provided'}`",
        f"- Evidence sources loaded: {len(rendered_sources)}",
        f"- Requirements reviewed: {len(claims)}",
        "",
        "## Evidence Sources",
        "",
    ]

    if rendered_sources:
        for source_path in rendered_sources:
            lines.append(f"- `{source_path}`")
    else:
        lines.append("- No evidence sources were loaded.")
    lines.extend(
        [
            "",
            "## Decision Summary",
            "",
            f"- Supported claims: {counts['supported']}",
            f"- Partial claims: {counts['partial']}",
            f"- Unsupported claims: {counts['unsupported']}",
            "",
        ]
    )

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

    lines.extend(
        [
            "## Review Notes",
            "",
            "- Supported claims have direct source evidence and source paths.",
            "- Partial claims have at least one weak or incomplete source.",
            "- Unsupported claims remain visible and are not promoted.",
            "",
            "## Source Provenance",
            "",
            "All source paths are repo-relative and use forward slashes.",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_report(
    output_path: str | Path,
    claims: list[Claim],
    evidence_sources: list[str] | None = None,
    role_source: str | None = None,
) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    report = build_markdown_report(claims, evidence_sources, role_source)
    path.write_text(report, encoding="utf-8")
    return report
