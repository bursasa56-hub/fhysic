from bot.handlers import parse_search_query


def test_parse_search_query_strips_command() -> None:
    assert parse_search_query("/search сила трения") == "сила трения"


def test_parse_search_query_without_argument_is_empty() -> None:
    assert parse_search_query("/search") == ""
