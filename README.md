# TraceOps Evidence Demo

TraceOps Evidence Demo is a public-safe Python/FastAPI project that demonstrates evidence ingestion, source provenance, claim labeling, and markdown reporting.

## What It Demonstrates

Engineering teams often need to connect a requirement to the evidence that supports it. This demo loads fake markdown evidence, maps a fake role description to those sources, and writes a report that separates supported, partial, and unsupported claims.

## What It Does Not Include

- No LLM integration.
- No screenshots.
- No private databases.
- No private tracker exports.
- No real company, recruiter, interview, or job-description data.

## Install

```powershell
python -m pip install -e ".[test]"
```

## Run The Demo

```powershell
python scripts/run_demo.py
```

The generated report is written to `outputs/demo_report.md`.

## Run Tests

```powershell
python -m pytest -q
python scripts/check_public_safety.py
```

## FastAPI Routes

```powershell
python -m uvicorn app.main:app --reload
```

- `GET /health`
- `GET /demo/evidence`
- `POST /demo/report`

## Source Provenance

Each loaded evidence file keeps its file path. Supported claims include those paths in the report so a reviewer can trace a statement back to the fake source that supports it.

## Unsupported Claims

Unsupported claims are flagged instead of presented as proven. This keeps the report useful for review: it shows both what the evidence supports and what still needs evidence.

## Public Data Safety

All included data is fake demo data. The safety script scans public text files for blocked private identifiers and fails if one is found.
