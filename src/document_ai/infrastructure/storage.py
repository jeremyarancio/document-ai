from pathlib import Path

import httpx
from PIL.Image import Image

from document_ai.application.ports.storage import IStorageService
from document_ai.domain.document import Document, Figure, Page, StoredDocument


class LocalStorageService(IStorageService):
    def __init__(self, dir: Path) -> None:
        if not dir.is_dir():
            raise ValueError(f"Not a directory: {str(dir)}")

        self.dir = dir
        self.doc_dir = dir / "documents"
        self.page_with_boxes_dir = dir / "pages_with_boxes"
        self.fig_dir = dir / "figures"

        self.doc_dir.mkdir(exist_ok=True, parents=True)
        self.page_with_boxes_dir.mkdir(exist_ok=True, parents=True)
        self.fig_dir.mkdir(exist_ok=True, parents=True)

    def store_documents(self, documents: list[Document]) -> list[StoredDocument]:
        stored_documents: list[StoredDocument] = []
        for document in documents:
            filename = document.name.lower() + ".pdf"
            response = httpx.get(
                document.pdf_url, follow_redirects=True
            )  # NOTE: It should be out of the Storage Responsibility
            filepath = self.doc_dir / filename
            with filepath.open("wb") as f:
                f.write(response.content)
            stored_documents.append(
                StoredDocument(
                    name=filename,
                    pdf_url=document.pdf_url,
                    storage_path=filepath,
                )
            )
        return stored_documents

    def store_figure_imgs(
        self, figures: list[Figure], figure_imgs: list[Image]
    ) -> None:
        for figure, figure_img in zip(figures, figure_imgs, strict=True):
            filepath = self.fig_dir / (str(figure.id_) + ".png")
            with filepath.open("wb") as f:
                figure_img.save(f)

    def store_page_with_boxes_imgs(
        self, pages: list[Page], page_with_boxes_imgs: list[Image]
    ) -> None:
        for page, page_with_boxes_img in zip(pages, page_with_boxes_imgs, strict=True):
            filepath = self.page_with_boxes_dir / (str(page.id_) + ".png")
            with filepath.open("wb") as f:
                page_with_boxes_img.save(f)
