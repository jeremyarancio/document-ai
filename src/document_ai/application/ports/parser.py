from abc import ABC, abstractmethod
from pathlib import Path
from PIL.Image import Image


class IParserService(ABC):
    @abstractmethod
    def parse(self, page: Image, dir: Path) -> tuple[str, Image, list[Image]]:
        raise NotImplementedError
