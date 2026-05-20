# Architecture

TraceOps Evidence Demo is a small Python workflow with four steps:

1. `app.evidence_loader` reads fake markdown evidence and the fake role description.
2. `app.requirement_mapper` extracts role requirement bullets and matches simple keywords against evidence files.
3. `app.claim_policy` labels each requirement as supported, partial, or unsupported.
4. `app.report_writer` writes `outputs/demo_report.md` with source paths next to supported claims.

`app.main` exposes the same workflow through FastAPI routes:

- `GET /health`
- `GET /demo/evidence`
- `POST /demo/report`

The project intentionally uses deterministic keyword matching so the behavior is easy to audit.
