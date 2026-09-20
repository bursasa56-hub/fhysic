from bot.keyboards import open_app_keyboard, search_keyboard


def test_search_keyboard_uses_topic_id() -> None:
    keyboard = search_keyboard(
        "https://example.com",
        [
            {
                "topic_id": "sila",
                "title": "Сила",
                "textbook_title": "Физика. 7–9 классы",
                "snippet": "…",
            }
        ],
    )

    button = keyboard.inline_keyboard[0][0]
    assert button.web_app.url == "https://example.com?topic=sila"
    assert "Сила" in button.text
    assert "Физика" in button.text


def test_open_app_keyboard() -> None:
    keyboard = open_app_keyboard("https://example.com")

    assert keyboard.inline_keyboard[0][0].web_app.url == "https://example.com"
