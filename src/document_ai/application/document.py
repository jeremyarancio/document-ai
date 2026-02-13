from document_ai.application.core.utils.logger import get_logger
from document_ai.application.ports.database import IDBService
from document_ai.application.ports.docsource import IDocumentSourceService
from document_ai.application.ports.storage import IStorageService

logger = get_logger()


class DocumentService:
    @staticmethod
    def download_documents(
        query: str,
        limit: int,
        docsource_service: IDocumentSourceService,
        storage_service: IStorageService,
        database_service: IDBService,
    ) -> None:
        logger.info("Start pulling documents from external source...")
        documents = docsource_service.pull_documents(query=query, limit=limit)
        logger.info("Storing {} documents to storage...", len(documents))
        stored_documents = storage_service.store_documents(documents=documents)
        logger.info("Store document data into database...")
        database_service.add_documents(documents=stored_documents)
        logger.info("Pull documents finished successfully.")
