# TraceOps Evidence Demo: Public Repo Rules

This is a public-safe portfolio repository.

## Hard Privacy Rules

Work inside this repository only. Do not inspect, copy, import, summarize, or migrate files from any other local repo or folder.

Do not use:

- real company names
- recruiter names
- interview notes
- real job descriptions
- personal evidence files
- private screenshots
- private databases
- generated job-tracker reports
- absolute local paths
- usernames
- local machine folder names
- prompt files
- private sensitive-term files

Use fake demo data only.

Allowed fake names:

- Demo Manufacturing Company
- Demo Firmware Validation Engineer
- Demo Test Automation Engineer
- Demo Validation Station
- Demo Evidence Source

## Public Repo Purpose

This repo demonstrates a practical Python/FastAPI internal-tool pattern:

```text
role requirement
-> evidence source
-> claim classification
-> source provenance
-> reviewable report
```

The repo should feel like a small engineering workflow tool, not a toy script and not an inflated product pitch.

## Tone Rules

Use direct engineer-to-engineer language.

Avoid hype. Prefer:

- source-backed
- reviewable
- traceable
- fake demo data
- supported claim
- partial claim
- unsupported claim
- repo-relative path
- validation workflow
- evidence report

## Technical Boundaries

Allowed:

- Python
- FastAPI
- Pydantic
- pytest
- simple HTML/Jinja2
- markdown reports
- fake markdown evidence
- public safety scanner

Not allowed:

- LLM integration
- external APIs
- databases
- private data support
- screenshots copied from another project
- generated outputs committed under outputs/
- prompt files committed to Git
- private sensitive-term files committed to Git

## Required Checks Before Any Commit

Run:

```powershell
python -m pytest -q
python scripts/check_public_safety.py
python scripts/run_demo.py
python scripts/check_public_safety.py
```

Public committed files must not contain:

- absolute paths
- local machine paths
- private names
- usernames
- private prompt files
- private sensitive-term files

Generated outputs belong in outputs/ and should be ignored.

Example report output belongs in docs/examples/.
