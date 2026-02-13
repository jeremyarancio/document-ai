from pathlib import Path
import duckdb
from document_ai.application.ports.database import IDBService
from document_ai.domain.document import StoredDocument
from document_ai.infrastructure.schemas.database import DocumentSchema


class DuckDBService(IDBService):
    def __init__(self, db_path: Path, document_table_name: str) -> None:
        self.con = duckdb.connect(database=db_path)
        self.document_table_name = document_table_name

    def add_documents(self, documents: list[StoredDocument]) -> None:
        document_schemas = [
            DocumentSchema.from_stored_document(document) for document in documents
        ]
        try:
            self.con.begin()
            self.con.executemany(
                f"""INSERT INTO {self.document_table_name} VALUES (?, ?, ?)""",
                [
                    (
                        doc.id_,
                        doc.filename,
                        doc.storage_path,
                    )
                    for doc in document_schemas
                ],
            )
            self.con.commit()
        except Exception:
            self.con.rollback()
            raise
