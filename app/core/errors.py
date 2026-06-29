from typing import Any
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

class AppError(Exception):
    def __init__(self, status_code: int, message: str, details: Any | None = None) -> None:
        self.status_code = status_code
        self.message = message
        self.details = details

def _app_error_handler(request: Request, exc: AppError):
    return ORJSONResponse(status_code=exc.status_code, content={"error": {"message": exc.message, "details": exc.details}})

def _http_error_handler(request: Request, exc: StarletteHTTPException):
    return ORJSONResponse(status_code=exc.status_code, content={"error": {"message": exc.detail}})

def _validation_error_handler(request: Request, exc: RequestValidationError):
    return ORJSONResponse(status_code=422, content={"error": {"message": "Validation error", "details": exc.errors()}})

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, _app_error_handler)
    app.add_exception_handler(StarletteHTTPException, _http_error_handler)
    app.add_exception_handler(RequestValidationError, _validation_error_handler)
