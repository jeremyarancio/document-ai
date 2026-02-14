from pathlib import Path

import httpx

from document_ai.application.ports.storage import IStorageService
from document_ai.domain.document import Document, StoredDocument


class LocalStorageService(IStorageService):
    def __init__(self, dir: Path) -> None:
        if not dir.is_dir():
            raise ValueError(f"Not a directory: {str(dir)}")

        self.dir = dir
        self.doc_dir = dir / "documents"
        self.page_dir = dir / "pages"
        self.page_with_boxes_dir = dir / "pages_with_boxes"
        self.fig_dir = dir / "figures"

        self.doc_dir.mkdir(exist_ok=True, parents=True)
        self.page_dir.mkdir(exist_ok=True, parents=True)
        self.page_with_boxes_dir.mkdir(exist_ok=True, parents=True)
        self.fig_dir.mkdir(exist_ok=True, parents=True)

    def store_documents(self, documents: list[Document]) -> list[StoredDocument]:
        stored_documents: list[StoredDocument] = []
        for document in documents:
            filename = document.name.lower() + ".pdf"
            response = httpx.get(document.pdf_url, follow_redirects=True)
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
