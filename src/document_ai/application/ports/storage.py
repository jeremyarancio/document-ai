from abc import ABC

from document_ai.domain.document import Document


class IStorageService(ABC):
    def store_documents(self, documents: list[Document]) -> None:
        raise NotImplementedError
