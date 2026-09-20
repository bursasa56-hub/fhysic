from pathlib import Path

import pytest

from api.content import ContentError, ContentStore


def test_store_loads_repo_content() -> None:
    store = ContentStore()

    assert len(store) == 177
    textbook_ids = [textbook.id for textbook in store.textbooks()]
    assert "peryshkin" in textbook_ids
    assert "myakishev" in textbook_ids
    assert "gendenshtein" in textbook_ids
    assert "kasyanov" in textbook_ids
    assert "panebrattsev" in textbook_ids
    by_id = {textbook.id: textbook for textbook in store.textbooks()}
    assert by_id["peryshkin"].grades == [7, 8, 9]
    assert by_id["myakishev"].grades == [10, 11]
    assert by_id["gendenshtein"].grades == [7, 8, 9]
    assert by_id["kasyanov"].grades == [10, 11]
    assert by_id["panebrattsev"].grades == [7, 8, 9]


def test_textbooks_ordered_by_grade_range() -> None:
    store = ContentStore()

    grade_ranges = [
        (min(textbook.grades), max(textbook.grades))
        for textbook in store.textbooks()
    ]
    assert grade_ranges == sorted(grade_ranges, key=lambda pair: pair[0])


def test_textbook_returns_grade_tree() -> None:
    store = ContentStore()

    textbook = store.textbook("peryshkin")

    assert textbook is not None
    assert textbook.title == "Физика. 7–9 классы"
    assert [grade.id for grade in textbook.grades] == [7, 8, 9]
    assert textbook.grades[0].sections[0].topics[0].id == (
        "peryshkin-7-chto-izuchaet-fizika"
    )


def test_unknown_textbook_returns_none() -> None:
    store = ContentStore()
    assert store.textbook("nope") is None


def test_topic_returns_body_and_neighbours() -> None:
    store = ContentStore()

    topic = store.topic("peryshkin-7-fizicheskie-velichiny")

    assert topic is not None
    assert topic.textbook == "peryshkin"
    assert topic.textbook_title == "Физика. 7–9 классы"
    assert topic.grade == 7
    assert topic.section == "vvedenie"
    assert "Цена деления" in topic.body
    assert topic.prev == "peryshkin-7-nablyudeniya-opyty"
    assert topic.next == "peryshkin-7-tochnost-pogreshnost"


def test_first_topic_has_no_prev_and_last_no_next() -> None:
    store = ContentStore()

    assert store.topic("peryshkin-7-chto-izuchaet-fizika").prev is None
    assert store.topic("peryshkin-9-vselennaya").next is None


def test_unknown_topic_returns_none() -> None:
    store = ContentStore()
    assert store.topic("does-not-exist") is None


def test_missing_topic_file_raises(tmp_path: Path) -> None:
    (tmp_path / "manifest.json").write_text(
        '{"textbooks": [{"id": "t", "title": "T", "author": "A", "grades":'
        ' [{"id": 7, "title": "7", "sections": [{"id": "s", "title": "S",'
        ' "topics": [{"id": "t-7-x", "title": "X", "file": "missing.md"}]}]}]}]}',
        encoding="utf-8",
    )
    with pytest.raises(ContentError):
        ContentStore(tmp_path)


def test_duplicate_topic_id_raises(tmp_path: Path) -> None:
    topic_file = tmp_path / "a.md"
    topic_file.write_text(
        "---\ntitle: A\ntextbook: t\ngrade: 7\nsection: s\norder: 1\n---\n\nBody\n",
        encoding="utf-8",
    )
    (tmp_path / "manifest.json").write_text(
        '{"textbooks": [{"id": "t", "title": "T", "author": "A", "grades":'
        ' [{"id": 7, "title": "7", "sections": [{"id": "s", "title": "S",'
        ' "topics": [{"id": "dup", "title": "A", "file": "a.md"},'
        ' {"id": "dup", "title": "B", "file": "a.md"}]}]}]}]}',
        encoding="utf-8",
    )
    with pytest.raises(ContentError):
        ContentStore(tmp_path)


def test_textbook_mismatch_raises(tmp_path: Path) -> None:
    topic_file = tmp_path / "a.md"
    topic_file.write_text(
        "---\ntitle: A\ntextbook: other\ngrade: 7\nsection: s\norder: 1\n---\n\nBody\n",
        encoding="utf-8",
    )
    (tmp_path / "manifest.json").write_text(
        '{"textbooks": [{"id": "t", "title": "T", "author": "A", "grades":'
        ' [{"id": 7, "title": "7", "sections": [{"id": "s", "title": "S",'
        ' "topics": [{"id": "t-7-a", "title": "A", "file": "a.md"}]}]}]}]}',
        encoding="utf-8",
    )
    with pytest.raises(ContentError):
        ContentStore(tmp_path)
