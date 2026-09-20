import json
from pathlib import Path

import pytest

from api.content import ContentError, load_manifest, parse_topic_file

VALID_MANIFEST = {
    "textbooks": [
        {
            "id": "book-a",
            "title": "Физика. 7–9 классы",
            "author": "А. Автор",
            "grades": [
                {
                    "id": 7,
                    "title": "7 класс",
                    "sections": [
                        {
                            "id": "vvedenie",
                            "title": "Введение",
                            "topics": [
                                {
                                    "id": "book-a-7-chto-izuchaet-fizika",
                                    "title": "Что изучает физика",
                                    "file": "book-a/07/vvedenie/01.md",
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    ]
}

TOPIC_TEXT = """---
title: Что изучает физика
textbook: book-a
grade: 7
section: vvedenie
order: 1
keywords: [физика, явления, опыт]
---

## Что изучает физика

Физика изучает явления природы.
"""


def test_load_manifest_parses_tree(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(VALID_MANIFEST, ensure_ascii=False), encoding="utf-8")

    manifest = load_manifest(path)

    assert len(manifest.textbooks) == 1
    textbook = manifest.textbooks[0]
    assert textbook.id == "book-a"
    assert textbook.grades[0].sections[0].topics[0].id == "book-a-7-chto-izuchaet-fizika"


def test_load_manifest_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(ContentError):
        load_manifest(tmp_path / "missing.json")


def test_load_manifest_invalid_json_raises(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text("{ not json", encoding="utf-8")
    with pytest.raises(ContentError):
        load_manifest(path)


def test_load_manifest_invalid_shape_raises(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps({"textbooks": [{"id": "book-a"}]}), encoding="utf-8")
    with pytest.raises(ContentError):
        load_manifest(path)


def test_parse_topic_file_splits_frontmatter(tmp_path: Path) -> None:
    path = tmp_path / "topic.md"
    path.write_text(TOPIC_TEXT, encoding="utf-8")

    meta, body = parse_topic_file(path)

    assert meta.title == "Что изучает физика"
    assert meta.textbook == "book-a"
    assert meta.grade == 7
    assert meta.keywords == ["физика", "явления", "опыт"]
    assert body.startswith("## Что изучает физика")
    assert "---" not in body
