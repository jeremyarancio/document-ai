from abc import ABC, abstractmethod

from document_ai.domain.document import Figure, Markdown, Page, StoredDocument


class IDBService(ABC):
    @abstractmethod
    def add_documents(self, documents: list[StoredDocument]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all_documents(self) -> list[StoredDocument]:
        raise NotImplementedError

    @abstractmethod
    def add_pages(self, pages: list[Page]) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_figures(self, figures: list[Figure]) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_markdowns(self, markdowns: list[Markdown]) -> None:
        raise NotImplementedError
