from typing import Optional
from pydantic import BaseModel


class OcrServiceResponseDTO(BaseModel):
    data: list["OcrServiceResponseItemInSinglePage"]
    code: str

    class Example:
        example = {
            "code": "Success",
            "data": [
                {
                    "page_number": 1,
                    "result": [
                        {
                            "text": "@",
                            "bounding_box": [
                                0.06173561335193551,
                                0.9115374795934997,
                                0.03287361574752628,
                                0.03378002497240513,
                            ],
                            "confidence": 1,
                        },
                        {
                            "text": "ocrmac",
                            "bounding_box": [
                                0.09937716347350677,
                                0.9121470714196308,
                                0.1922706798649284,
                                0.035327076500950065,
                            ],
                            "confidence": 1,
                        },
                        {
                            "text": "FastAPI",
                            "bounding_box": [
                                0.781586478592785,
                                0.9217179089103967,
                                0.15863155606397106,
                                0.03156418228312216,
                            ],
                            "confidence": 1,
                        },
                    ],
                    "raw_text": "@ ocrmac FastAPI",
                },
                {
                    "page_number": 2,
                    "result": [
                        {
                            "text": "#",
                            "bounding_box": [
                                0.06177763218219904,
                                0.9117609677143913,
                                0.03425124398678316,
                                0.03518222988302052,
                            ],
                            "confidence": 1,
                        },
                        {
                            "text": "ocrmac",
                            "bounding_box": [
                                0.10113174714452675,
                                0.912252450199557,
                                0.19235377714700289,
                                0.03645169806173153,
                            ],
                            "confidence": 1,
                        },
                        {
                            "text": "FastAPI",
                            "bounding_box": [
                                0.05827067847744357,
                                0.8590116279069767,
                                0.04847638801538564,
                                0.011627906686046519,
                            ],
                            "confidence": 1,
                        },
                    ],
                    "raw_text": "# ocrmac FastAPI",
                },
            ],
        }


class OcrServiceResponseItemInSingleItem(BaseModel):
    text: str
    bounding_box: tuple[float, float, float, float]
    confidence: Optional[float] = None


class OcrServiceResponseItemInSinglePage(BaseModel):
    page_number: int
    result: list["OcrServiceResponseItemInSingleItem"]
    raw_text: str
