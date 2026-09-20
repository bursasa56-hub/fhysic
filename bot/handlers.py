from __future__ import annotations

import httpx
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from bot.api_client import ApiClient
from bot.keyboards import open_app_keyboard, search_keyboard

router = Router()


def parse_search_query(text: str) -> str:
    return text.partition(" ")[2].strip()


@router.message(CommandStart())
async def start(message: Message, webapp_url: str) -> None:
    await message.answer(
        "Привет! Здесь краткие конспекты по физике по школьным учебникам.\n"
        "Открой приложение и выбери учебник:",
        reply_markup=open_app_keyboard(webapp_url),
    )


@router.message(Command("search"))
async def search(message: Message, api: ApiClient, webapp_url: str) -> None:
    query = parse_search_query(message.text or "")
    if not query:
        await message.answer("Напиши так: /search сила")
        return
    try:
        results = await api.search(query)
    except httpx.HTTPError:
        await message.answer("Сервис временно недоступен, попробуй позже.")
        return
    if not results:
        await message.answer("Ничего не найдено.")
        return
    await message.answer("Найдено:", reply_markup=search_keyboard(webapp_url, results))
