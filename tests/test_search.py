from api.content import ContentStore
from api.search import search


def test_search_matches_title() -> None:
    store = ContentStore()
    assert search(store, "движение")


def test_search_matches_keyword() -> None:
    store = ContentStore()
    assert search(store, "гипотеза")


def test_search_matches_body() -> None:
    store = ContentStore()
    assert search(store, "половине цены деления")


def test_search_is_case_insensitive() -> None:
    store = ContentStore()
    assert search(store, "ФИЗИКА")


def test_search_empty_query_returns_nothing() -> None:
    store = ContentStore()
    assert search(store, "   ") == []


def test_search_result_has_textbook() -> None:
    store = ContentStore()
    results = search(store, "движение")

    assert results
    for result in results:
        assert result.textbook
        assert result.textbook_title


def test_search_snippet_contains_query() -> None:
    store = ContentStore()
    results = search(store, "траектория")

    assert any("траектор" in result.snippet.lower() for result in results)


def test_search_keyword_snippet_contains_query() -> None:
    store = ContentStore()
    results = search(store, "гипотеза")

    assert any("гипотез" in result.snippet.lower() for result in results)
