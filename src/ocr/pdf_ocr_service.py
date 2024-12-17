from typing import BinaryIO, Optional
from function_timer import debug_timer
from pdf_to_image.i_pdf_to_image_service import IPdfToImageService
from ocr.i_ocr_service import IOcrService
from ocr.ocr_service_response_dto import (
    OcrServiceResponseItemInSinglePage,
    OcrServiceResponseItemInSingleItem,
)
from pdf_to_image.pdf_to_image_service import PdfToImageService
import uuid
import os
from PIL import Image
import json


"""
I was trying to call the ocrmac library functions directly in fastAPI application, but it was not working.
Therefore, I had to create a separate python file to call the ocrmac library functions.
"""


class PdfOcrService(IOcrService):

    def __init__(self, pdf_to_image_service: Optional[IPdfToImageService] = None):
        self.pdf_to_image_service = pdf_to_image_service or PdfToImageService()

    def perform_request(
        self, file: BinaryIO, prefer_language: Optional[list[str]] = None
    ) -> list[OcrServiceResponseItemInSinglePage]:
        images = self.pdf_to_image_service.convert_pdf_to_image(file)

        self.temp_folder_path = self._generate_temp_folder_directory()
        self.ocr_result_path = self._get_ocr_result_path()

        self._create_temp_folder()

        self._save_images_in_temp_folder(images)

        self._delagate_ocr_service(prefer_language=prefer_language)

        ocr_result = self._get_ocr_result()

        self._delete_temp_folder()

        return ocr_result

    @debug_timer
    def _delagate_ocr_service(
        self,
        prefer_language: Optional[list[str]],
    ) -> None:
        # Get the absolute path of this file
        current_file_path = os.path.abspath(__file__)
        os.system(
            f'python {current_file_path} {self.temp_folder_path} {self.ocr_result_path} {" ".join(prefer_language or [])}'
        )

    @debug_timer
    def _generate_temp_folder_directory(self) -> str:
        return f"/tmp/{uuid.uuid4()}"

    @debug_timer
    def _create_temp_folder(self) -> None:
        if not os.path.exists("/tmp"):
            os.makedirs("/tmp")
        os.makedirs(self.temp_folder_path)

    @debug_timer
    def _save_images_in_temp_folder(self, images: list[Image.Image]) -> None:
        for index, image in enumerate(images):
            image.save(f"{self.temp_folder_path}/page_{index+1:05}.png")

    @debug_timer
    def _delete_temp_folder(self) -> None:
        for file_name in os.listdir(self.temp_folder_path):
            file_path = os.path.join(self.temp_folder_path, file_name)
            os.remove(file_path)
        os.rmdir(self.temp_folder_path)

    @debug_timer
    def _get_ocr_result_path(self) -> str:
        return f"{self.temp_folder_path}/output.json"

    @debug_timer
    def _get_ocr_result(self) -> list[OcrServiceResponseItemInSinglePage]:
        with open(self.ocr_result_path, "r") as f:
            return [
                OcrServiceResponseItemInSinglePage(**recognized_text)
                for recognized_text in json.load(f)
            ]


class OcrServiceStartFromTerminal:

    @debug_timer
    def start(self):
        # Do OCR
        if len(sys.argv) < 3:
            print(
                "Usage: python mac_ocr.py <folder_path> <output_path> <language_preference(optional)>"
            )
            sys.exit(1)

        folder_path = sys.argv[1]
        output_path = sys.argv[2]
        language_preference = sys.argv[3:]

        # Get all image paths inside the folder path
        image_paths = self._get_image_paths_under_folder(folder_path)

        recognized_texts = list()

        print(image_paths)

        for index, image_path in enumerate(image_paths):
            # Perform OCR on the image
            annotations = self._single_page_ocr(
                image_path, language_preference=language_preference
            )

            recognized_texts.append(
                OcrServiceResponseItemInSinglePage(
                    page_number=index + 1,
                    result=annotations,
                    raw_text=" ".join([annotation.text for annotation in annotations]),
                )
            )

        self._save_output_as_json(output_path, recognized_texts)

    @debug_timer
    def _save_output_as_json(
        self,
        output_path: str,
        recognized_texts: list[OcrServiceResponseItemInSinglePage],
    ):
        with open(output_path, "w") as f:
            f.write(
                json.dumps(
                    [
                        recognized_text.model_dump()
                        for recognized_text in recognized_texts
                    ]
                )
            )

    @debug_timer
    def _get_image_paths_under_folder(self, folder_path: str):
        return sorted(
            [
                os.path.join(folder_path, file_name)
                for file_name in os.listdir(folder_path)
                if file_name.endswith((".png", ".jpg"))
            ]
        )

    @debug_timer
    def _single_page_ocr(
        self, image_path: str, language_preference: list[str]
    ) -> list[OcrServiceResponseItemInSingleItem]:

        annotations = None

        if ocrmac.LIVETEXT_AVAILABLE:
            annotations = ocrmac.OCR(
                image_path,
                framework="livetext",
                recognition_level="accurate",
                language_preference=language_preference,
            ).recognize()
        else:
            annotations = ocrmac.OCR(
                image_path,
                recognition_level="accurate",
                language_preference=language_preference,
            ).recognize()

        return [
            OcrServiceResponseItemInSingleItem(
                text=annotation[0], confidence=annotation[1], bounding_box=annotation[2]
            )
            for annotation in annotations
        ]


if __name__ == "__main__":
    import sys
    from ocrmac import ocrmac

    OcrServiceStartFromTerminal().start()
