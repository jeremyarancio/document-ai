from abc import ABC, abstractmethod
from PIL.Image import Image

from document_ai.domain.document import Document, StoredDocument


class IStorageService(ABC):
    @abstractmethod
    def store_documents(self, documents: list[Document]) -> list[StoredDocument]:
        raise NotImplementedError

    @abstractmethod
    def store_markdowns(self, markdowns: list[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def store_figures(self, pages_figures: list[list[Image]]) -> None:
        raise NotImplementedError

    @abstractmethod
    def store_pages_with_boxes(self, pages_with_boxes: list[Image]) -> None:
        raise NotImplementedError
