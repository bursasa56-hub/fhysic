from __future__ import annotations

from contextlib import asynccontextmanager
from functools import lru_cache
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.content import CONTENT_DIR, ContentStore
from api.models import (
    SearchResponse,
    TextbookDetail,
    TextbooksResponse,
    TopicDetail,
    TreeResponse,
)
from api.search import search as search_topics

WEB_DIR = Path(__file__).resolve().parent.parent / "web"


@lru_cache
def get_store() -> ContentStore:
    return ContentStore(CONTENT_DIR)


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_store()
    yield


app = FastAPI(title="Physics Notes API", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/textbooks", response_model=TextbooksResponse)
def get_textbooks(store: ContentStore = Depends(get_store)) -> TextbooksResponse:
    return TextbooksResponse(textbooks=store.textbooks())


@app.get("/api/tree", response_model=TreeResponse)
def get_tree(store: ContentStore = Depends(get_store)) -> TreeResponse:
    return TreeResponse(textbooks=store.tree())


@app.get("/api/textbooks/{textbook_id}", response_model=TextbookDetail)
def get_textbook(
    textbook_id: str, store: ContentStore = Depends(get_store)
) -> TextbookDetail:
    textbook = store.textbook(textbook_id)
    if textbook is None:
        raise HTTPException(
            status_code=404, detail=f"textbook not found: {textbook_id}"
        )
    return textbook


@app.get("/api/topics/{topic_id}", response_model=TopicDetail)
def get_topic(topic_id: str, store: ContentStore = Depends(get_store)) -> TopicDetail:
    topic = store.topic(topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail=f"topic not found: {topic_id}")
    return topic


@app.get("/api/search", response_model=SearchResponse)
def search(
    q: str = Query(default=""),
    store: ContentStore = Depends(get_store),
) -> SearchResponse:
    return SearchResponse(query=q, results=search_topics(store, q))


@app.get("/")
def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")
