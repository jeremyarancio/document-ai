from pathlib import Path
from document_ai.application.ports.database import IDBService
from document_ai.application.ports.docsource import IDocumentSourceService
from document_ai.application.ports.storage import IStorageService
from document_ai.infrastructure.database import DuckDBService
from document_ai.infrastructure.docsource import ArxivDocumentSourceService
from document_ai.infrastructure.storage import LocalStorageService


def get_docsource_service() -> IDocumentSourceService:
    return ArxivDocumentSourceService()


def get_storage_service(storage_dir: Path) -> IStorageService:
    return LocalStorageService(dir=storage_dir)


def get_db_service(db_path: Path, document_table_name: str) -> IDBService:
    return DuckDBService(db_path=db_path, document_table_name=document_table_name)
