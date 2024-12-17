from typing import Optional
from fastapi import Request, FastAPI, UploadFile
from fastapi.responses import JSONResponse

from ocr.image_ocr_service import ImageOcrService
from ocr.pdf_ocr_service import PdfOcrService
from ocr.ocr_service_response_dto import OcrServiceResponseDTO

app = FastAPI()


@app.get("/health")
def health():
    return JSONResponse(status_code=200, content={"status": "ok"})


@app.post(
    "/ocr",
    responses={
        200: {
            "description": "Success Request",
            "content": {
                "application/json": {"example": OcrServiceResponseDTO.Example.example}
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "code": "Fail",
                        "detail": "Error Message",
                    }
                }
            },
        },
    },
)
def ocr(
    files: list[UploadFile],
    langugae_preference: Optional[list[str]] = None,
):
    try:
        images = []
        for file in files:
            if _is_pdf(file):
                ocr_service = PdfOcrService()
                ocr_result = ocr_service.perform_request(file.file, langugae_preference)

                return JSONResponse(
                    status_code=200,
                    content={
                        "code": "Success",
                        "data": [
                            response_item.model_dump() for response_item in ocr_result
                        ],
                    },
                )

            elif _is_image(file):
                images.append(file.file)

            else:
                return JSONResponse(
                    status_code=400,
                    content={"code": "Fail", "detail": "Invalid File Type"},
                )

        ocr_service = ImageOcrService()
        ocr_result = ocr_service.perform_request(images, langugae_preference)
        return JSONResponse(
            status_code=200,
            content={
                "code": "Success",
                "data": [response_item.model_dump() for response_item in ocr_result],
            },
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"code": "Fail", "detail": str(e)})


def _is_pdf(file: UploadFile) -> bool:
    return file.filename.endswith(".pdf")


def _is_image(file: UploadFile) -> bool:
    return file.filename.endswith((".png", ".jpg", ".jpeg"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
