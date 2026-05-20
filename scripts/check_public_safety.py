from pathlib import Path
import sys
from dataclasses import dataclass

ROOT = Path(__file__).resolve().parents[1]

# Public-safe placeholder terms. These prove the scanner works without exposing
# real company, recruiter, or interview names in the public repository.
PUBLIC_FORBIDDEN_TERMS = [
    "SECRET" + "_COMPANY_ALPHA",
    "PRIVATE" + "_RECRUITER_NAME",
    "REAL" + "_INTERVIEW_NOTE",
    "PRIVATE" + "_JOB_DESCRIPTION",
    "ABSOLUTE" + "_LOCAL_PATH_EXAMPLE",
]

SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".pytest_tmp",
    "outputs",
}

SKIP_FILES = {
    ".private_sensitive_terms.txt",
    "CODEX_PUBLIC_DEMO_PROMPT.md",
}

TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".csv",
}


@dataclass(frozen=True)
class SafetyViolation:
    path: Path
    term: str


def load_terms() -> list[str]:
    return sorted(set(PUBLIC_FORBIDDEN_TERMS), key=str.lower)


def should_scan(path: Path, root: Path = ROOT) -> bool:
    rel = path.relative_to(root)

    if rel.name in SKIP_FILES:
        return False

    if any(part in SKIP_DIRS for part in rel.parts):
        return False

    if path.suffix.lower() not in TEXT_SUFFIXES:
        return False

    return True


def find_public_safety_violations(root: str | Path = ROOT) -> list[SafetyViolation]:
    scan_root = Path(root)
    terms = load_terms()
    failures: list[SafetyViolation] = []

    for path in scan_root.rglob("*"):
        if not path.is_file():
            continue

        if not should_scan(path, scan_root):
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")
        lower_text = text.lower()

        for term in terms:
            if term.lower() in lower_text:
                failures.append(SafetyViolation(path=path, term=term))

    return failures


def main(argv: list[str] | None = None) -> int:
    root = Path(argv[0]) if argv else ROOT
    failures = find_public_safety_violations(root)

    if failures:
        print("Public safety scan failed:")
        for violation in failures:
            file_path = violation.path.relative_to(root)
            print(f"- {file_path}: blocked term '{violation.term}'")
        return 1

    print("Public safety scan passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
