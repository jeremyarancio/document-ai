from pathlib import Path
from tempfile import TemporaryDirectory

from document_ai.application.ports.database import IDBService
from document_ai.application.ports.storage import IStorageService


class ParserService:
    @staticmethod
    def parse_documents(
        storage_service: IStorageService,
        database_service: IDBService,
    ) -> None:
        with TemporaryDirectory() as tempdir:
            tempdir_ = Path(tempdir)
            documents = storage_service.pull_documents()
