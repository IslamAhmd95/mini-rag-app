from typing import Optional

from fastapi.responses import JSONResponse


def json_response(message: str, status: int = 200, data: Optional[dict] = None) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content= {
            "message": message,
            **(data or {})
        }
    )