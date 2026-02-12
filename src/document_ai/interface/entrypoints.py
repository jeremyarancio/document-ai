from document_ai.application.document import DocumentService
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
    )


if __name__ == "__main__":
    download_arxiv_papers()
