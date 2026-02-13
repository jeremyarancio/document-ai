from abc import ABC, abstractmethod

from document_ai.domain.document import StoredDocument


class IDBService(ABC):
    @abstractmethod
    def add_documents(self, documents: list[StoredDocument]) -> None:
        raise NotImplementedError
