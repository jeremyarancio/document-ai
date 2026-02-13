from uuid import UUID
from pydantic import BaseModel

from document_ai.domain.document import StoredDocument


class DocumentSchema(BaseModel):
    id_: UUID
    filename: str
    storage_path: str

    @classmethod
    def from_stored_document(cls, document: StoredDocument) -> "DocumentSchema":
        return cls(
            id_=document.id_,
            filename=document.name,
            storage_path=str(document.storage_path),
        )
