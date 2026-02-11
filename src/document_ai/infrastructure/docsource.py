import httpx
import xmltodict

from document_ai.application.ports.docsource import IDocumentSourceService
from document_ai.domain.document import Document
from document_ai.infrastructure.schemas.docsource import ArxivDocuments


class ArxivDocumentSourceService(IDocumentSourceService):
    def __init__(self) -> None:
        self.api_url = "https://export.arxiv.org/api/query?search_query=all:{query}&max_results={limit}"

    def pull_documents(self, query: str, limit: int) -> list[Document]:
        url = self.api_url.format(query=query, limit=limit)
        data = httpx.get(url)
        json_data = xmltodict.parse(data.content)
        return ArxivDocuments.model_validate(json_data).to_documents()
