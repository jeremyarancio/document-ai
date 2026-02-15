from abc import ABC, abstractmethod
from PIL.Image import Image

from document_ai.domain.document import Markdown


class IParserService(ABC):
    @abstractmethod
    def parse(self, page_img: Image) -> tuple[str, Image, list[Image]]:
        raise NotImplementedError
