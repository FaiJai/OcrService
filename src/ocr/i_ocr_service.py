from typing import BinaryIO, Optional
from PIL import Image
from abc import ABC, abstractmethod

from ocr.ocr_service_response_dto import (
    OcrServiceResponseItemInSinglePage,
)


class IOcrService(ABC):

    @abstractmethod
    def perform_request(
        self, file: BinaryIO, prefer_language: Optional[list[str]] = None
    ) -> list[OcrServiceResponseItemInSinglePage]: ...
