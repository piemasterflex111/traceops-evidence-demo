from pathlib import Path

from scripts.check_public_safety import find_public_safety_violations, main


def test_public_safety_script_blocks_forbidden_terms(tmp_path):
    blocked_word = "SECRET" + "_COMPANY_ALPHA"
    sample = tmp_path / "unsafe.md"
    sample.write_text(f"This contains {blocked_word}.", encoding="utf-8")

    violations = find_public_safety_violations(tmp_path)

    assert violations
    assert violations[0].path == sample
    assert violations[0].term == blocked_word


def test_public_safety_script_skips_outputs_directory(tmp_path):
    blocked_word = "PRIVATE" + "_JOB_DESCRIPTION"
    outputs = tmp_path / "outputs"
    outputs.mkdir()
    (outputs / "generated.md").write_text(blocked_word, encoding="utf-8")

    assert find_public_safety_violations(tmp_path) == []


def test_public_safety_main_returns_zero_for_clean_tree(tmp_path):
    (tmp_path / "safe.md").write_text("Demo Manufacturing Company only.", encoding="utf-8")

    assert main([str(tmp_path)]) == 0


def test_public_safety_scanner_skips_private_prompt_and_term_files(tmp_path):
    blocked_word = "REAL" + "_INTERVIEW_NOTE"
    (tmp_path / ".private_sensitive_terms.txt").write_text(blocked_word, encoding="utf-8")
    (tmp_path / "CODEX_PUBLIC_DEMO_PROMPT.md").write_text(blocked_word, encoding="utf-8")

    assert find_public_safety_violations(tmp_path) == []
