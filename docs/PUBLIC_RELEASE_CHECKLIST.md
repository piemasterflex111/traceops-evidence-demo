# Public Release Checklist

Before publishing or committing changes, verify:

- No private files are staged.
- No prompt files are staged.
- No generated `outputs/` files are staged.
- No absolute paths appear in public files.
- No real companies, recruiter names, interview notes, or real job descriptions appear.
- Fake demo evidence remains under `data/demo_evidence/`.
- Tests pass with `python -m pytest -q`.
- The safety scan passes with `python scripts/check_public_safety.py`.
- The demo run succeeds with `python scripts/run_demo.py`.
- The committed report example is under `docs/examples/`.
