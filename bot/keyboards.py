from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


def search_keyboard(webapp_url: str, results: list[dict]) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text=f"{result['title']} · {result['textbook_title']}",
                web_app=WebAppInfo(url=f"{webapp_url}?topic={result['topic_id']}"),
            )
        ]
        for result in results
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def open_app_keyboard(webapp_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть конспекты",
                    web_app=WebAppInfo(url=webapp_url),
                )
            ]
        ]
    )
