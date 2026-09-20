from fastapi.testclient import TestClient


def test_search_returns_results(client: TestClient) -> None:
    response = client.get("/api/search", params={"q": "гипотеза"})

    assert response.status_code == 200
    body = response.json()
    assert body["query"] == "гипотеза"
    assert [r["topic_id"] for r in body["results"]] == [
        "book-a-7-chto-izuchaet-fizika"
    ]
    assert body["results"][0]["textbook"] == "book-a"
    assert body["results"][0]["textbook_title"] == "Физика. 7–9 классы"
    assert "snippet" in body["results"][0]


def test_search_without_query_returns_empty(client: TestClient) -> None:
    response = client.get("/api/search")

    assert response.status_code == 200
    assert response.json() == {"query": "", "results": []}
