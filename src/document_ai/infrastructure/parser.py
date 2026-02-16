# type: ignore
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image

import torch
from transformers import AutoModel, AutoTokenizer

from document_ai.application.ports.parser import IParserService


class DeepseekOCRParser(IParserService):
    def __init__(self) -> None:
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        model_name = "deepseek-ai/DeepSeek-OCR-2"

        # Model
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, trust_remote_code=True
        )
        model = AutoModel.from_pretrained(
            model_name, trust_remote_code=True, use_safetensors=True
        )
        self.model = model.eval().cuda().to(torch.bfloat16)
        self.prompt = "<image>\n<|grounding|>Convert the document to markdown. "

        # Directories
        self.output_dir = "output_dir/"
        self.figurer_dir = "images/"

        # Artifacts
        self.page_with_boxes_path = "result_with_boxes.jpg"
        self.markdown_path = "result.mmd"

    def parse(self, page_img: Image.Image) -> tuple[str, Image, list[Image]]:
        with TemporaryDirectory() as tempdir:
            image_path = os.path.join(tempdir, "image.png")
            output_dir = os.path.join(tempdir, self.output_dir)
            with open(image_path, "wb") as f:
                page_img.save(f)

            _ = self.model.infer(
                self.tokenizer,
                prompt=self.prompt,
                image_file=image_path,
                output_path=output_dir,
                base_size=1024,
                image_size=768,
                crop_mode=True,
                save_results=True,
            )

            markdown_path = os.path.join(output_dir, self.markdown_path)
            page_with_boxes_path = os.path.join(output_dir, self.page_with_boxes_path)
            figure_dir = os.path.join(output_dir, self.figurer_dir)

            with open(markdown_path, "r") as f:
                markdown = f.read()
            with open(page_with_boxes_path, "rb") as f:
                page_with_boxes_img = Image.open(f).copy()
            figure_imgs: list[Image.Image] = []
            for figure_path in Path(figure_dir).iterdir():
                with figure_path.open("rb") as f:
                    figure_imgs.append(Image.open(f).copy())

            return markdown, page_with_boxes_img, figure_imgs
