from typing import Annotated
from pydantic import BaseModel, HttpUrl, Field, AfterValidator

from document_ai.domain.document import Document


class _Link(BaseModel):
    link: Annotated[HttpUrl, Field(validation_alias="@href")]
    mime_type: Annotated[str, Field(validation_alias="@type")]


def _ensure_pdf_exists(links: list[_Link]) -> list[_Link]:
    if not any(link.mime_type == "application/pdf" for link in links):
        raise ValueError("At least one link must have mime_type 'application/pdf'")
    return links


class _Entry(BaseModel):
    title: str
    links: Annotated[
        list[_Link],
        Field(validation_alias="link"),
        AfterValidator(_ensure_pdf_exists),
    ]


class Feed(BaseModel):
    entries: Annotated[list[_Entry], Field(validation_alias="entry")]


class ArxivDocuments(BaseModel):
    feed: Feed

    def to_documents(self) -> list[Document]:
        """We ensure there is a pdf_url link when pulling the data"""
        return [
            Document(
                name=entry.title,
                pdf_url=str(link.link),
            )
            for entry in self.feed.entries
            for link in entry.links
        ]
