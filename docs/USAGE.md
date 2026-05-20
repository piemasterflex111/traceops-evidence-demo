# Usage

Install test dependencies:

```powershell
python -m pip install -e ".[test]"
```

Run the demo workflow:

```powershell
python scripts/run_demo.py
```

Run the FastAPI app:

```powershell
python -m uvicorn app.main:app --reload
```

Run verification:

```powershell
python -m pytest -q
python scripts/check_public_safety.py
python scripts/run_demo.py
```
