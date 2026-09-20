FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000} & while true; do python -m bot.main; sleep 3; done"]
