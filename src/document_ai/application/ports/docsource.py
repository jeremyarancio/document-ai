from abc import ABC

from document_ai.domain.document import Document


class IDocumentSourceService(ABC):
    def pull_documents(self, query: str, limit: int) -> list[Document]:
        raise NotImplementedError
