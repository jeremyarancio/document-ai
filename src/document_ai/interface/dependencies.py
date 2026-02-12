from pathlib import Path
from document_ai.infrastructure.docsource import ArxivDocumentSourceService
from document_ai.infrastructure.storage import LocalStorageService
from document_ai.settings import get_settings

settings = get_settings()


def get_docsource_service():
    return ArxivDocumentSourceService()


def get_storage_service(storage_dir: Path):
    return LocalStorageService(dir=storage_dir)
