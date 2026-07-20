from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import traceback

from app.core.config import settings

logger = logging.getLogger(__name__)

class AppException(Exception):
    """Custom application exception."""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        errors: list = None
    ):
        self.message = message
        self.status_code = status_code
        self.errors = errors or []
        super().__init__(message)

async def app_exception_handler(request: Request, exc: AppException):
    """Handle custom application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "errors": exc.errors,
            "status_code": exc.status_code
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation exceptions."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(f"Validation error: {errors}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation error",
            "errors": errors,
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY
        }
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """Handle generic exceptions."""
    error_id = f"{int(time.time())}-{hash(exc) % 10000}"
    
    logger.error(f"Unhandled exception [{error_id}]: {exc}")
    logger.error(traceback.format_exc())
    
    # In production, don't expose internal error details
    if settings.ENVIRONMENT == "production":
        message = "An internal error occurred. Please try again later."
    else:
        message = str(exc)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": message,
            "error_id": error_id,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )