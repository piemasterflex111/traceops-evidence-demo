# Architecture

TraceOps Evidence Demo is a small deterministic workflow. It is designed so a reviewer can follow a requirement from the fake role description to source evidence and the final report.

## FastAPI App

`app.main` exposes the demo workflow:

- `GET /` shows a simple HTML summary.
- `GET /health` returns a health response.
- `GET /evidence` returns role requirements and evidence inventory.
- `GET /report` returns a markdown report preview.
- `POST /demo/report` writes `outputs/demo_report.md`.

## Evidence Loader

`app.evidence_loader` reads markdown files from `data/demo_evidence/`. It returns repo-relative source paths so reports and API responses do not expose local machine paths.

## Requirement Extractor

`app.requirement_mapper.extract_requirements` reads bullet items from the fake role description. Each bullet becomes a reviewable requirement.

## Mapper

`app.requirement_mapper.map_requirements_to_evidence` compares requirement keywords against fake evidence sources. It ignores the unsupported-claim examples as source evidence because that file exists to test negative review cases.

## Claim Policy

`app.claim_policy` converts mapping results into supported, partial, or unsupported claims. Partial claims require at least one source. Unsupported claims always have no sources and remain visible for review.

## Report Writer

`app.report_writer` writes markdown with an input summary, evidence source list, decision counts, claim sections, review notes, and source provenance rules.

## Safety Scanner

`scripts/check_public_safety.py` scans public text files for fake blocked placeholder terms. It skips generated outputs, virtual environments, caches, private prompt files, and private sensitive-term files.

## Tests

The pytest suite covers evidence loading, requirement extraction, mapping, claim policy, report output, FastAPI routes, demo execution, and scanner failure modes.
