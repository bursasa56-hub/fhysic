from pathlib import Path

from scripts.validate_content import check


def test_check_accepts_valid_content(content_dir: Path) -> None:
    assert check(content_dir) == 0


def test_check_rejects_broken_content(tmp_path: Path) -> None:
    (tmp_path / "manifest.json").write_text('{"textbooks": []}', encoding="utf-8")
    assert check(tmp_path) == 0

    (tmp_path / "manifest.json").write_text("not json", encoding="utf-8")
    assert check(tmp_path) == 1


def test_check_rejects_missing_file(tmp_path: Path) -> None:
    (tmp_path / "manifest.json").write_text(
        '{"textbooks": [{"id": "t", "title": "T", "author": "A", "grades":'
        ' [{"id": 7, "title": "7", "sections": [{"id": "s", "title": "S",'
        ' "topics": [{"id": "t-7-x", "title": "X", "file": "missing.md"}]}]}]}]}',
        encoding="utf-8",
    )
    assert check(tmp_path) == 1
