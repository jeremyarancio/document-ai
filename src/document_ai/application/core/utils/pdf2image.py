from pathlib import Path
from typing import Iterator
from PIL.Image import Image

import pypdfium2 as pdfium


def convert_pdf_to_images(filepath: Path) -> Iterator[Image]:
    pdf = pdfium.PdfDocument(filepath)
    return [page.render(scale=2).to_pil() for page in pdf]
