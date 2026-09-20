import httpx
import pytest

from bot.api_client import ApiClient

GRADES = {
    "grades": [{"id": 7, "title": "7 класс", "sections": []}]
}
SEARCH = {
    "query": "сила",
    "results": [{"topic_id": "sila", "title": "Сила", "snippet": "…"}],
}


def make_client(handler) -> ApiClient:
    transport = httpx.MockTransport(handler)
    raw = httpx.AsyncClient(transport=transport, base_url="http://test")
    return ApiClient("http://test", client=raw)


async def test_get_grades_returns_list() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/grades"
        return httpx.Response(200, json=GRADES)

    client = make_client(handler)
    try:
        grades = await client.get_grades()
    finally:
        await client.aclose()

    assert grades == GRADES["grades"]


async def test_search_passes_query() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["q"] == "сила"
        return httpx.Response(200, json=SEARCH)

    client = make_client(handler)
    try:
        results = await client.search("сила")
    finally:
        await client.aclose()

    assert results == SEARCH["results"]


async def test_search_raises_on_server_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    client = make_client(handler)
    try:
        with pytest.raises(httpx.HTTPStatusError):
            await client.search("сила")
    finally:
        await client.aclose()
