from PIL.Image import Image

from document_ai.application.core.utils import pdf2image
from document_ai.application.ports.database import IDBService
from document_ai.application.ports.parser import IParserService
from document_ai.application.ports.storage import IStorageService
from document_ai.domain.document import Figure, Markdown, Page


class ParserService:
    @staticmethod
    def parse_documents(
        storage_service: IStorageService,
        database_service: IDBService,
        parser_service: IParserService,
    ) -> None:
        documents = database_service.get_all_documents()
        for document in documents:
            # We save data and images respectively in db and storage per document iteration
            pages: list[Page] = []
            markdowns: list[Markdown] = []
            figures: list[Figure] = []

            page_with_boxes_imgs: list[Image] = []
            figure_imgs: list[Image] = []

            page_imgs = pdf2image.convert_pdf_to_images(filepath=document.storage_path)

            for page_n, page_img in enumerate(page_imgs):
                content, page_with_boxes_img, page_figure_imgs = parser_service.parse(
                    page_img=page_img
                )

                # Entities -> DB
                page = Page(document_id=document.id_, n=page_n)
                pages.append(page)
                markdowns.append(Markdown(page_id=page.id_, content=content))
                figures.extend(
                    [
                        Figure(page_id=page.id_, n=figure_n)
                        for figure_n, _ in enumerate(page_figure_imgs)
                    ]
                )
                # Images -> Storage
                page_with_boxes_imgs.append(page_with_boxes_img)
                figure_imgs.extend(page_figure_imgs)

            database_service.add_pages(pages=pages)
            database_service.add_markdowns(markdowns=markdowns)

            storage_service.store_page_with_boxes_imgs(
                pages=pages, page_with_boxes_imgs=page_with_boxes_imgs
            )
            if figure_imgs:
                database_service.add_figures(figures=figures)
                storage_service.store_figure_imgs(
                    figures=figures, figure_imgs=figure_imgs
                )
