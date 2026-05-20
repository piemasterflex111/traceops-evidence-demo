# Usage

## Install

```powershell
python -m pip install -e ".[test]"
```

## Run The App

```powershell
python -m uvicorn app.main:app --reload
```

Open the local server and use:

- `GET /`
- `GET /health`
- `GET /evidence`
- `GET /report`
- `POST /demo/report`

## Run The Demo

```powershell
python scripts/run_demo.py
```

The script writes `outputs/demo_report.md`.

## Run Tests

```powershell
python -m pytest -q
python scripts/check_public_safety.py
```

## Inspect The Generated Report

Compare:

- generated report: `outputs/demo_report.md`
- committed example: `docs/examples/demo_report_example.md`

Generated output stays out of Git. The committed example is refreshed from a clean demo run.
