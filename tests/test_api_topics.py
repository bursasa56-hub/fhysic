from fastapi.testclient import TestClient


def test_topic_returns_body_and_neighbours(client: TestClient) -> None:
    response = client.get("/api/topics/book-a-7-fizicheskie-velichiny")

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Физические величины"
    assert body["textbook"] == "book-a"
    assert body["textbook_title"] == "Физика. 7–9 классы"
    assert body["grade"] == 7
    assert body["section"] == "vvedenie"
    assert "Цена деления" in body["body"]
    assert body["prev"] == "book-a-7-chto-izuchaet-fizika"
    assert body["next"] == "book-a-8-teplota"


def test_topic_body_has_no_frontmatter(client: TestClient) -> None:
    body = client.get("/api/topics/book-a-7-chto-izuchaet-fizika").json()
    assert "---" not in body["body"]
    assert body["prev"] is None


def test_unknown_topic_returns_404(client: TestClient) -> None:
    response = client.get("/api/topics/nope")

    assert response.status_code == 404
    assert response.json()["detail"] == "topic not found: nope"


def test_topic_returns_retelling(client: TestClient) -> None:
    body = client.get("/api/topics/book-a-7-chto-izuchaet-fizika").json()

    assert body["retelling"] == "Кратко: физика изучает явления природы."
    assert "пересказ" not in body["body"]


def test_topic_without_retelling_returns_none(client: TestClient) -> None:
    body = client.get("/api/topics/book-a-7-fizicheskie-velichiny").json()

    assert body["retelling"] is None
