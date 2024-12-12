from typing import Optional
from pydantic import BaseModel


class OcrServerResponseDTO(BaseModel):
    data: list["OcrServiceResponseItemInSinglePage"]
    code: str


class OcrServiceResponseItemInSingleItem(BaseModel):
    text: str
    bounding_box: tuple[float, float, float, float]
    confidence: Optional[float] = None


class OcrServiceResponseItemInSinglePage(BaseModel):
    page_number: int
    result: list["OcrServiceResponseItemInSingleItem"]
