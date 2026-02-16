from abc import ABC, abstractmethod
from PIL.Image import Image


class IParserService(ABC):
    @abstractmethod
    def parse(self, page_img: Image) -> tuple[str, Image, list[Image]]:
        raise NotImplementedError
