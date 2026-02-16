from abc import ABC, abstractmethod
from PIL.Image import Image

from document_ai.domain.document import Document, Figure, Page, StoredDocument


class IStorageService(ABC):
    @abstractmethod
    def store_documents(self, documents: list[Document]) -> list[StoredDocument]:
        raise NotImplementedError

    @abstractmethod
    def store_figure_imgs(
        self, figures: list[Figure], figure_imgs: list[Image]
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def store_page_with_boxes_imgs(
        self, pages: list[Page], page_with_boxes_imgs: list[Image]
    ) -> None:
        raise NotImplementedError
