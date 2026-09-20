from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

import frontmatter
from pydantic import ValidationError

from api.models import (
    GradeNode,
    Manifest,
    ManifestGrade,
    ManifestSection,
    ManifestTopic,
    PartNode,
    SectionNode,
    Textbook,
    TextbookDetail,
    TextbookSummary,
    TopicDetail,
    TopicFrontmatter,
    TopicNode,
)

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"

RETELING_MARKER = "<!-- пересказ -->"


class ContentError(Exception):
    pass


def split_variants(text: str) -> tuple[str, str | None]:
    if RETELING_MARKER in text:
        body, retelling = text.split(RETELING_MARKER, 1)
        return body.strip(), retelling.strip()
    return text.strip(), None


def load_manifest(path: Path) -> Manifest:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ContentError(f"manifest not found: {path}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ContentError(f"invalid manifest json: {exc}") from exc
    try:
        return Manifest.model_validate(data)
    except ValidationError as exc:
        raise ContentError(f"invalid manifest: {exc}") from exc


def parse_topic_file(path: Path) -> tuple[TopicFrontmatter, str]:
    try:
        post = frontmatter.load(path)
    except FileNotFoundError as exc:
        raise ContentError(f"topic file not found: {path}") from exc
    try:
        meta = TopicFrontmatter.model_validate(post.metadata)
    except ValidationError as exc:
        raise ContentError(f"invalid frontmatter in {path}: {exc}") from exc
    return meta, post.content


def _section_groups(
    grade: ManifestGrade,
) -> list[tuple[str | None, str | None, list[ManifestSection]]]:
    if grade.parts:
        return [(part.id, part.title, part.sections) for part in grade.parts]
    return [(None, None, grade.sections)]


class ContentStore:
    def __init__(self, content_dir: Path = CONTENT_DIR) -> None:
        self.content_dir = Path(content_dir)
        self.manifest = load_manifest(self.content_dir / "manifest.json")
        self._textbooks: dict[str, Textbook] = {}
        self._topics: dict[str, ManifestTopic] = {}
        self._meta: dict[str, TopicFrontmatter] = {}
        self._bodies: dict[str, str] = {}
        self._retellings: dict[str, str] = {}
        self._order: dict[str, list[str]] = {}
        self._topic_textbook: dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        for textbook in self.manifest.textbooks:
            if textbook.id in self._textbooks:
                raise ContentError(f"duplicate textbook id: {textbook.id}")
            self._textbooks[textbook.id] = textbook
            order: list[str] = []
            for grade in textbook.grades:
                for _, _, sections in _section_groups(grade):
                    for section in sections:
                        for topic in section.topics:
                            if topic.id in self._topics:
                                raise ContentError(f"duplicate topic id: {topic.id}")
                            meta, body = parse_topic_file(
                                self.content_dir / topic.file
                            )
                            if meta.textbook != textbook.id:
                                raise ContentError(
                                    f"frontmatter textbook mismatch in {topic.file}: "
                                    f"{meta.textbook} != {textbook.id}"
                                )
                            self._topics[topic.id] = topic
                            self._meta[topic.id] = meta
                            body, retelling = split_variants(body)
                            self._bodies[topic.id] = body
                            if retelling:
                                self._retellings[topic.id] = retelling
                            self._topic_textbook[topic.id] = textbook.id
                            order.append(topic.id)
            self._order[textbook.id] = order

    def textbooks(self) -> list[TextbookSummary]:
        return [
            TextbookSummary(
                id=textbook.id,
                title=textbook.title,
                author=textbook.author,
                grades=[grade.id for grade in textbook.grades],
            )
            for textbook in self.manifest.textbooks
        ]

    @staticmethod
    def _section_node(section: ManifestSection) -> SectionNode:
        return SectionNode(
            id=section.id,
            title=section.title,
            topics=[TopicNode(id=t.id, title=t.title) for t in section.topics],
        )

    def _grade_node(self, grade: ManifestGrade) -> GradeNode:
        if grade.parts:
            return GradeNode(
                id=grade.id,
                title=grade.title,
                parts=[
                    PartNode(
                        id=part.id,
                        title=part.title,
                        sections=[self._section_node(s) for s in part.sections],
                    )
                    for part in grade.parts
                ],
            )
        return GradeNode(
            id=grade.id,
            title=grade.title,
            sections=[self._section_node(s) for s in grade.sections],
        )

    def textbook(self, textbook_id: str) -> TextbookDetail | None:
        textbook = self._textbooks.get(textbook_id)
        if textbook is None:
            return None
        return TextbookDetail(
            id=textbook.id,
            title=textbook.title,
            author=textbook.author,
            grades=[self._grade_node(grade) for grade in textbook.grades],
        )

    def tree(self) -> list[TextbookDetail]:
        details = []
        for textbook in self.manifest.textbooks:
            detail = self.textbook(textbook.id)
            if detail is not None:
                details.append(detail)
        return details

    def topic(self, topic_id: str) -> TopicDetail | None:
        if topic_id not in self._topics:
            return None
        textbook_id = self._topic_textbook[topic_id]
        order = self._order[textbook_id]
        index = order.index(topic_id)
        prev_id = order[index - 1] if index > 0 else None
        next_id = order[index + 1] if index < len(order) - 1 else None
        meta = self._meta[topic_id]
        return TopicDetail(
            id=topic_id,
            title=self._topics[topic_id].title,
            textbook=textbook_id,
            textbook_title=self._textbooks[textbook_id].title,
            grade=meta.grade,
            section=meta.section,
            body=self._bodies[topic_id],
            retelling=self._retellings.get(topic_id),
            prev=prev_id,
            next=next_id,
        )

    def iter_topics(
        self,
    ) -> Iterator[tuple[ManifestTopic, TopicFrontmatter, str, str, str]]:
        for textbook_id, order in self._order.items():
            textbook_title = self._textbooks[textbook_id].title
            for topic_id in order:
                yield (
                    self._topics[topic_id],
                    self._meta[topic_id],
                    self._bodies[topic_id],
                    textbook_id,
                    textbook_title,
                )

    def __len__(self) -> int:
        return len(self._topics)
