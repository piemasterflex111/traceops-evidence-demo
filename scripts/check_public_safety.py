from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

# Public-safe placeholder terms. These prove the scanner works without exposing
# real company, recruiter, or interview names in the public repository.
PUBLIC_FORBIDDEN_TERMS = [
    "SECRET_COMPANY_ALPHA",
    "PRIVATE_RECRUITER_NAME",
    "REAL_INTERVIEW_NOTE",
    "PRIVATE_JOB_DESCRIPTION",
]

PRIVATE_TERMS_FILE = ROOT / ".private_sensitive_terms.txt"

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


def load_terms() -> list[str]:
    terms = list(PUBLIC_FORBIDDEN_TERMS)

    if PRIVATE_TERMS_FILE.exists():
        private_terms = [
            line.strip()
            for line in PRIVATE_TERMS_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        terms.extend(private_terms)

    return sorted(set(terms), key=str.lower)


def should_scan(path: Path) -> bool:
    rel = path.relative_to(ROOT)

    if rel.name in SKIP_FILES:
        return False

    if any(part in SKIP_DIRS for part in rel.parts):
        return False

    if path.suffix.lower() not in TEXT_SUFFIXES:
        return False

    return True


def main() -> int:
    terms = load_terms()
    failures: list[tuple[str, str]] = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        if not should_scan(path):
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")
        lower_text = text.lower()

        for term in terms:
            if term.lower() in lower_text:
                failures.append((str(path.relative_to(ROOT)), term))

    if failures:
        print("Public safety scan failed:")
        for file_path, term in failures:
            print(f"- {file_path}: blocked term '{term}'")
        return 1

    print("Public safety scan passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())