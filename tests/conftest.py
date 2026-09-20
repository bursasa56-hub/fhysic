import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.content import ContentStore
from api.main import app, get_store

MANIFEST = {
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
                                },
                                {
                                    "id": "book-a-7-fizicheskie-velichiny",
                                    "title": "Физические величины",
                                    "file": "book-a/07/vvedenie/02.md",
                                },
                            ],
                        }
                    ],
                },
                {
                    "id": 8,
                    "title": "8 класс",
                    "sections": [
                        {
                            "id": "teplovye",
                            "title": "Тепловые явления",
                            "topics": [
                                {
                                    "id": "book-a-8-teplota",
                                    "title": "Количество теплоты",
                                    "file": "book-a/08/teplovye/01.md",
                                }
                            ],
                        }
                    ],
                },
            ],
        },
        {
            "id": "book-b",
            "title": "Физика. 10–11 классы",
            "author": "Б. Автор",
            "grades": [
                {
                    "id": 10,
                    "title": "10 класс",
                    "sections": [
                        {
                            "id": "mehanika",
                            "title": "Механика",
                            "topics": [
                                {
                                    "id": "book-b-10-kinematika",
                                    "title": "Кинематика",
                                    "file": "book-b/10/mehanika/01.md",
                                }
                            ],
                        }
                    ],
                }
            ],
        },
        {
            "id": "book-c",
            "title": "Физика. 8 класс (в двух частях)",
            "author": "В. Автор",
            "grades": [
                {
                    "id": 8,
                    "title": "8 класс",
                    "parts": [
                        {
                            "id": "chast-1",
                            "title": "Часть 1",
                            "sections": [
                                {
                                    "id": "kinematika",
                                    "title": "Кинематика",
                                    "topics": [
                                        {
                                            "id": "book-c-8-dvizhenie",
                                            "title": "Движение",
                                            "file": "book-c/08/chast-1/kinematika/01.md",
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            "id": "chast-2",
                            "title": "Часть 2",
                            "sections": [
                                {
                                    "id": "teplovye",
                                    "title": "Тепловые явления",
                                    "topics": [
                                        {
                                            "id": "book-c-8-teplota",
                                            "title": "Теплота",
                                            "file": "book-c/08/chast-2/teplovye/01.md",
                                        }
                                    ],
                                }
                            ],
                        },
                    ],
                }
            ],
        },
    ]
}

TOPICS = {
    "book-a/07/vvedenie/01.md": (
        "---\ntitle: Что изучает физика\ntextbook: book-a\ngrade: 7\n"
        "section: vvedenie\norder: 1\nkeywords: [физика, гипотеза]\n---\n\n"
        "Физика изучает явления. $s = vt$\n\n"
        "<!-- пересказ -->\n\n"
        "Кратко: физика изучает явления природы.\n"
    ),
    "book-a/07/vvedenie/02.md": (
        "---\ntitle: Физические величины\ntextbook: book-a\ngrade: 7\n"
        "section: vvedenie\norder: 2\nkeywords: [измерение]\n---\n\n"
        "Цена деления прибора.\n"
    ),
    "book-a/08/teplovye/01.md": (
        "---\ntitle: Количество теплоты\ntextbook: book-a\ngrade: 8\n"
        "section: teplovye\norder: 1\nkeywords: [теплота]\n---\n\n"
        "$Q = cm\\Delta t$\n"
    ),
    "book-b/10/mehanika/01.md": (
        "---\ntitle: Кинематика\ntextbook: book-b\ngrade: 10\n"
        "section: mehanika\norder: 1\nkeywords: [движение]\n---\n\n"
        "Механическое движение.\n"
    ),
    "book-c/08/chast-1/kinematika/01.md": (
        "---\ntitle: Движение\ntextbook: book-c\ngrade: 8\n"
        "section: kinematika\norder: 1\nkeywords: [движение]\n---\n\n"
        "Путь и скорость.\n"
    ),
    "book-c/08/chast-2/teplovye/01.md": (
        "---\ntitle: Теплота\ntextbook: book-c\ngrade: 8\n"
        "section: teplovye\norder: 1\nkeywords: [теплота]\n---\n\n"
        "Количество теплоты.\n"
    ),
}


@pytest.fixture
def content_dir(tmp_path: Path) -> Path:
    for relative, text in TOPICS.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    (tmp_path / "manifest.json").write_text(
        json.dumps(MANIFEST, ensure_ascii=False), encoding="utf-8"
    )
    return tmp_path


@pytest.fixture
def store(content_dir: Path) -> ContentStore:
    return ContentStore(content_dir)


@pytest.fixture
def client(store: ContentStore) -> TestClient:
    app.dependency_overrides[get_store] = lambda: store
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
