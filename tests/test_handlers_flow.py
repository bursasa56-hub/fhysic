from bot.handlers import search, start


class FakeApi:
    def __init__(self, results=None) -> None:
        self._results = results or []

    async def search(self, query: str) -> list[dict]:
        return self._results


class FakeMessage:
    def __init__(self, text: str = "") -> None:
        self.text = text
        self.answers: list[tuple[str, object]] = []

    async def answer(self, text: str, reply_markup=None) -> None:
        self.answers.append((text, reply_markup))


async def test_start_sends_open_app_button() -> None:
    message = FakeMessage()

    await start(message, webapp_url="https://example.com")

    assert len(message.answers) == 1
    button = message.answers[0][1].inline_keyboard[0][0]
    assert button.web_app.url == "https://example.com"


async def test_search_without_query_asks_for_one() -> None:
    message = FakeMessage(text="/search")

    await search(message, api=FakeApi(results=[]), webapp_url="https://example.com")

    assert "Напиши так" in message.answers[0][0]


async def test_search_with_no_results() -> None:
    message = FakeMessage(text="/search ззз")

    await search(message, api=FakeApi(results=[]), webapp_url="https://example.com")

    assert message.answers[0][0] == "Ничего не найдено."


async def test_search_with_results_builds_webapp_buttons() -> None:
    message = FakeMessage(text="/search сила")
    api = FakeApi(
        results=[
            {
                "topic_id": "sila",
                "title": "Сила",
                "textbook_title": "Физика. 7–9 классы",
                "snippet": "…",
            }
        ]
    )

    await search(message, api=api, webapp_url="https://example.com")

    button = message.answers[0][1].inline_keyboard[0][0]
    assert button.web_app.url == "https://example.com?topic=sila"
