from typing import BinaryIO
from pdf2image import convert_from_bytes, convert_from_path
from PIL import Image
from pdf_to_image.i_pdf_to_image_service import IPdfToImageService


class PdfToImageService(IPdfToImageService):
    def convert_pdf_to_image(self, pdf_file: BinaryIO) -> list[Image.Image]:
        return convert_from_bytes(pdf_file.read())
