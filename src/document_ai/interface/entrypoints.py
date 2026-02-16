from document_ai.application.document import DocumentService
from document_ai.application.parse import ParserService
from document_ai.interface import dependencies
from document_ai.settings import get_settings

settings = get_settings()


def download_arxiv_papers() -> None:
    DocumentService.download_documents(
        query=settings.source.query,
        limit=settings.source.limit,
        docsource_service=dependencies.get_docsource_service(),
        storage_service=dependencies.get_storage_service(
            storage_dir=settings.storage.dir
        ),
        database_service=dependencies.get_db_service(
            db_path=settings.db.path,
            document_table_name=settings.db.document_table_name,
            figure_table_name=settings.db.figure_table_name,
            markdown_table_name=settings.db.markdown_table_name,
            page_table_name=settings.db.page_table_name,
        ),
    )


def parse_documents() -> None:
    ParserService.parse_documents(
        storage_service=dependencies.get_storage_service(
            storage_dir=settings.storage.dir
        ),
        database_service=dependencies.get_db_service(
            db_path=settings.db.path,
            document_table_name=settings.db.document_table_name,
            figure_table_name=settings.db.figure_table_name,
            markdown_table_name=settings.db.markdown_table_name,
            page_table_name=settings.db.page_table_name,
        ),
        parser_service=dependencies.get_parser(),
    )
