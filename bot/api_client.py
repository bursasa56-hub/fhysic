from __future__ import annotations

import httpx


class ApiClient:
    def __init__(self, base_url: str, client: httpx.AsyncClient | None = None) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = client or httpx.AsyncClient(
            base_url=self._base_url,
            timeout=10,
        )

    async def get_grades(self) -> list[dict]:
        response = await self._client.get("/api/grades")
        response.raise_for_status()
        return response.json()["grades"]

    async def search(self, query: str) -> list[dict]:
        response = await self._client.get("/api/search", params={"q": query})
        response.raise_for_status()
        return response.json()["results"]

    async def aclose(self) -> None:
        await self._client.aclose()
