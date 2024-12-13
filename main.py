from typing import Optional
from fastapi import Request, FastAPI, UploadFile
from fastapi.responses import JSONResponse

from ocr.ocr_service import OcrService
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
    file: UploadFile,
    langugae_preference: Optional[list[str]] = None,
):
    try:
        ocr_service = OcrService()
        ocr_result = ocr_service.perform_request(file.file, langugae_preference)

        return JSONResponse(
            status_code=200,
            content={
                "code": "Success",
                "data": [response_item.model_dump() for response_item in ocr_result],
            },
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"code": "Fail", "detail": str(e)})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
