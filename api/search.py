from __future__ import annotations

from api.content import ContentStore
from api.models import ManifestTopic, SearchResult, TopicFrontmatter

SNIPPET_RADIUS = 60


def _snippet(text: str, query: str) -> str:
    lowered = text.lower()
    position = lowered.find(query)
    if position == -1:
        return " ".join(text[: SNIPPET_RADIUS * 2].split())
    start = max(0, position - SNIPPET_RADIUS)
    end = min(len(text), position + len(query) + SNIPPET_RADIUS)
    snippet = " ".join(text[start:end].split())
    prefix = "…" if start > 0 else ""
    suffix = "…" if end < len(text) else ""
    return f"{prefix}{snippet}{suffix}"


def _best_snippet(
    topic: ManifestTopic, meta: TopicFrontmatter, body: str, query: str
) -> str:
    if query in body.lower():
        return _snippet(body, query)
    if query in topic.title.lower():
        return _snippet(topic.title, query)
    for keyword in meta.keywords:
        if query in keyword.lower():
            return _snippet(keyword, query)
    return _snippet(body, query)


def search(store: ContentStore, query: str, limit: int = 30) -> list[SearchResult]:
    normalized = query.strip().lower()
    if not normalized:
        return []

    results: list[SearchResult] = []
    for topic, meta, body, textbook_id, textbook_title in store.iter_topics():
        haystack = " ".join([topic.title, " ".join(meta.keywords), body]).lower()
        if normalized not in haystack:
            continue
        results.append(
            SearchResult(
                topic_id=topic.id,
                title=topic.title,
                textbook=textbook_id,
                textbook_title=textbook_title,
                snippet=_best_snippet(topic, meta, body, normalized),
            )
        )
        if len(results) >= limit:
            break
    return results
