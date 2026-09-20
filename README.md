# Конспекты по физике — Telegram Mini App

Telegram-бот с миниаппом для чтения кратких конспектов по физике (7–11 классы).

## Состав

- `api/` — FastAPI: JSON API и статика миниаппа.
- `bot/` — aiogram: команды, навигация, поиск.
- `web/` — миниапп (Telegram WebApp + marked + KaTeX).
- `content/` — конспекты в Markdown + `manifest.json`.

## Локальный запуск

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
copy .env.example .env
.venv\Scripts\python -m uvicorn api.main:app --reload --port 8000
```

Миниапп: http://127.0.0.1:8000/

Бот (в отдельном терминале, нужен `BOT_TOKEN` и HTTPS `WEBAPP_URL`):

```bash
.venv\Scripts\python -m bot.main
```

## Проверка контента

```bash
.venv\Scripts\python -m scripts.validate_content
```

## Тесты

```bash
.venv\Scripts\python -m pytest
```

## Деплой

1. Заполнить `.env` (`BOT_TOKEN`, `WEBAPP_URL=https://<домен>`, `DOMAIN`).
2. Указать A-запись домена на сервер.
3. Запустить:

```bash
docker compose up -d --build
```

Caddy автоматически получит HTTPS-сертификат. `WEBAPP_URL` должен совпадать с доменом.
