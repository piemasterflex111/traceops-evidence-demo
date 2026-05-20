from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.main import OUTPUT_PATH, run_workflow  # noqa: E402


def main() -> int:
    result = run_workflow(Path(OUTPUT_PATH))
    print(f"Wrote report: {result['output_path']}")
    print(f"Evidence files: {result['evidence_count']}")
    print(f"Requirements: {result['requirement_count']}")
    print(f"Claims: {result['claim_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
