from abc import ABC, abstractmethod
from typing import BinaryIO
from PIL import Image


class IPdfToImageService(ABC):
    @abstractmethod
    def convert_pdf_to_image(self, pdf_file: BinaryIO) -> list[Image.Image]: ...
