from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_textbooks_returns_summaries(client: TestClient) -> None:
    response = client.get("/api/textbooks")

    assert response.status_code == 200
    body = response.json()
    assert [t["id"] for t in body["textbooks"]] == ["book-a", "book-b", "book-c"]
    assert body["textbooks"][0]["author"] == "А. Автор"
    assert body["textbooks"][0]["grades"] == [7, 8]


def test_textbook_returns_tree_without_bodies(client: TestClient) -> None:
    response = client.get("/api/textbooks/book-a")

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Физика. 7–9 классы"
    assert [grade["id"] for grade in body["grades"]] == [7, 8]
    first_topic = body["grades"][0]["sections"][0]["topics"][0]
    assert first_topic == {
        "id": "book-a-7-chto-izuchaet-fizika",
        "title": "Что изучает физика",
    }
    assert "file" not in first_topic
    assert "body" not in first_topic


def test_unknown_textbook_returns_404(client: TestClient) -> None:
    response = client.get("/api/textbooks/nope")

    assert response.status_code == 404
    assert response.json()["detail"] == "textbook not found: nope"


def test_tree_returns_full_nested_structure(client: TestClient) -> None:
    response = client.get("/api/tree")

    assert response.status_code == 200
    textbooks = response.json()["textbooks"]
    assert [t["id"] for t in textbooks] == ["book-a", "book-b", "book-c"]
    first_topic = textbooks[0]["grades"][0]["sections"][0]["topics"][0]
    assert first_topic == {
        "id": "book-a-7-chto-izuchaet-fizika",
        "title": "Что изучает физика",
    }


def test_textbook_with_parts_exposes_parts(client: TestClient) -> None:
    response = client.get("/api/textbooks/book-c")

    assert response.status_code == 200
    grade = response.json()["grades"][0]
    assert grade["sections"] == []
    assert [part["id"] for part in grade["parts"]] == ["chast-1", "chast-2"]
    assert grade["parts"][0]["sections"][0]["topics"][0]["id"] == "book-c-8-dvizhenie"
