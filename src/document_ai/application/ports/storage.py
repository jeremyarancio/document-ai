from abc import ABC, abstractmethod

from document_ai.domain.document import Document, StoredDocument


class IStorageService(ABC):
    @abstractmethod
    def store_documents(self, documents: list[Document]) -> list[StoredDocument]:
        raise NotImplementedError

    @abstractmethod
    def pull_documents(self) -> list[StoredDocument]:
        raise NotImplementedError
