from pathlib import Path

import httpx

from document_ai.application.ports.storage import IStorageService
from document_ai.domain.document import Document


class LocalStorageService(IStorageService):
    def __init__(self, dir: Path) -> None:
        if not dir.is_dir():
            raise ValueError(f"Not a directory: {str(dir)}")

        self.dir = dir
        self.pdf_dir = dir / "pdfs"
        self.pdf_dir.mkdir(exist_ok=True, parents=True)

    def store_documents(self, documents: list[Document]):
        for document in documents:
            filename = document.name.lower() + ".pdf"
            response = httpx.get(document.pdf_url, follow_redirects=True)
            filepath = self.pdf_dir / filename
            with filepath.open("wb") as f:
                f.write(response.content)
