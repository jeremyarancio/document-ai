from pathlib import Path
from tempfile import TemporaryDirectory
from PIL.Image import Image

from document_ai.application.core.utils import pdf2image
from document_ai.application.ports.database import IDBService
from document_ai.application.ports.parser import IParserService
from document_ai.application.ports.storage import IStorageService


class ParserService:
    @staticmethod
    def parse_documents(
        storage_service: IStorageService,
        database_service: IDBService,
        parser_service: IParserService,
    ) -> None:
        markdowns: list[str] = []
        pages_with_boxes: list[Image] = []
        pages_figures: list[list[Image]] = []

        documents = database_service.get_all_documents()
        for document in documents:
            pages = pdf2image.convert_pdf_to_images(filepath=document.storage_path)
            for page in pages:
                with TemporaryDirectory() as tempdir:
                    tempdir_ = Path(tempdir)
                    markdown, page_with_boxes, figures = parser_service.parse(
                        page=page, dir=tempdir_
                    )
                    markdowns.append(markdown)
                    pages_with_boxes.append(page_with_boxes)
                    pages_figures.append(figures)
        storage_service.store_markdowns(markdowns=markdowns)
        storage_service.store_figures(pages_figures=pages_figures)
        storage_service.store_pages_with_boxes(pages_with_boxes=pages_with_boxes)
