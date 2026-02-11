from abc import ABC

from document_ai.domain.document import Document


class IStorageService(ABC):
    @staticmethod
    def store_documents(documents: list[Document]) -> None:
        raise NotImplementedError
