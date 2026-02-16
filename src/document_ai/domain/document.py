from dataclasses import dataclass, field
from pathlib import Path
from typing import NewType
from uuid import UUID, uuid4


DocumentId = NewType("DocumentId", UUID)
PageId = NewType("PageId", UUID)
FigureId = NewType("FigureId", UUID)


@dataclass
class Document:
    name: str
    pdf_url: str


@dataclass
class StoredDocument(Document):
    storage_path: Path
    id_: DocumentId = field(default_factory=lambda: DocumentId(uuid4()))


@dataclass
class Markdown:
    page_id: PageId
    content: str


@dataclass
class Page:
    document_id: DocumentId
    n: int
    id_: PageId = field(default_factory=lambda: PageId(uuid4()))


@dataclass
class Figure:
    page_id: PageId
    n: int
    id_: FigureId = field(default_factory=lambda: FigureId(uuid4()))
