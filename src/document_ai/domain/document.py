from dataclasses import dataclass, field
from pathlib import Path
from typing import NewType
from uuid import UUID, uuid4


DocumentId = NewType("DocumentId", UUID)


@dataclass
class Document:
    name: str
    pdf_url: str


@dataclass
class StoredDocument(Document):
    storage_path: Path
    id_: DocumentId = field(default_factory=lambda: DocumentId(uuid4()))
