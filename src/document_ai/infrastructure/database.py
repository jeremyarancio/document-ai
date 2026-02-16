from pathlib import Path
import duckdb
from document_ai.application.ports.database import IDBService
from document_ai.domain.document import (
    DocumentId,
    Figure,
    Markdown,
    Page,
    StoredDocument,
)
from document_ai.infrastructure.schemas.database import DocumentSchema


class DuckDBService(IDBService):
    def __init__(
        self,
        db_path: Path,
        document_table_name: str,
        markdown_table_name: str,
        figure_table_name: str,
        page_table_name: str,
    ) -> None:
        self.con = duckdb.connect(database=db_path)
        self.document_table_name = document_table_name
        self.markdown_table_name = markdown_table_name
        self.figure_table_name = figure_table_name
        self.page_table_name = page_table_name

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

    def get_all_documents(self) -> list[StoredDocument]:
        rows = self.con.execute(
            f"SELECT id, filename, storagePath FROM {self.document_table_name}"
        ).fetchall()
        return [
            StoredDocument(
                name=row[1],
                pdf_url="",
                storage_path=Path(row[2]),
                id_=DocumentId(row[0]),
            )
            for row in rows
        ]

    def add_markdowns(self, markdowns: list[Markdown]) -> None:
        try:
            self.con.begin()
            self.con.executemany(
                f"""INSERT INTO {self.markdown_table_name} VALUES (?, ?)""",
                [
                    (
                        md.page_id,
                        md.content,
                    )
                    for md in markdowns
                ],
            )
            self.con.commit()
        except Exception:
            self.con.rollback()
            raise

    def add_pages(self, pages: list[Page]) -> None:
        try:
            self.con.begin()
            self.con.executemany(
                f"""INSERT INTO {self.page_table_name} VALUES (?, ?, ?)""",
                [
                    (
                        page.id_,
                        page.document_id,
                        page.n,
                    )
                    for page in pages
                ],
            )
            self.con.commit()
        except Exception:
            self.con.rollback()
            raise

    def add_figures(self, figures: list[Figure]) -> None:
        try:
            self.con.begin()
            self.con.executemany(
                f"""INSERT INTO {self.figure_table_name} VALUES (?, ?, ?)""",
                [(figure.id_, figure.page_id, figure.n) for figure in figures],
            )
            self.con.commit()
        except Exception:
            self.con.rollback()
            raise
