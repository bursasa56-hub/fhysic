from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import MenuButtonWebApp, WebAppInfo

from bot.api_client import ApiClient
from bot.config import Settings
from bot.handlers import router


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = Settings()
    bot = Bot(
        settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    api = ApiClient(settings.api_base_url)
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="Конспекты",
            web_app=WebAppInfo(url=settings.webapp_url),
        )
    )
    try:
        await dispatcher.start_polling(
            bot,
            api=api,
            webapp_url=settings.webapp_url,
        )
    finally:
        await api.aclose()


if __name__ == "__main__":
    asyncio.run(main())
