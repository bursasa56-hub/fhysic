from __future__ import annotations

from pydantic import BaseModel, Field


class ManifestTopic(BaseModel):
    id: str
    title: str
    file: str


class ManifestSection(BaseModel):
    id: str
    title: str
    topics: list[ManifestTopic]


class ManifestPart(BaseModel):
    id: str
    title: str
    sections: list[ManifestSection]


class ManifestGrade(BaseModel):
    id: int
    title: str
    sections: list[ManifestSection] = Field(default_factory=list)
    parts: list[ManifestPart] = Field(default_factory=list)


class Textbook(BaseModel):
    id: str
    title: str
    author: str
    grades: list[ManifestGrade]


class Manifest(BaseModel):
    textbooks: list[Textbook]


class TopicFrontmatter(BaseModel):
    title: str
    textbook: str
    grade: int
    section: str
    order: int
    keywords: list[str] = Field(default_factory=list)


class TopicNode(BaseModel):
    id: str
    title: str


class SectionNode(BaseModel):
    id: str
    title: str
    topics: list[TopicNode]


class PartNode(BaseModel):
    id: str
    title: str
    sections: list[SectionNode]


class GradeNode(BaseModel):
    id: int
    title: str
    sections: list[SectionNode] = Field(default_factory=list)
    parts: list[PartNode] = Field(default_factory=list)


class TextbookSummary(BaseModel):
    id: str
    title: str
    author: str
    grades: list[int]


class TextbooksResponse(BaseModel):
    textbooks: list[TextbookSummary]


class TextbookDetail(BaseModel):
    id: str
    title: str
    author: str
    grades: list[GradeNode]


class TreeResponse(BaseModel):
    textbooks: list[TextbookDetail]


class TopicDetail(BaseModel):
    id: str
    title: str
    textbook: str
    textbook_title: str
    grade: int
    section: str
    body: str
    retelling: str | None = None
    prev: str | None
    next: str | None


class SearchResult(BaseModel):
    topic_id: str
    title: str
    textbook: str
    textbook_title: str
    snippet: str


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
