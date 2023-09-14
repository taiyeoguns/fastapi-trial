import logging
from http import HTTPStatus

from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def custom_http_exception_handler(request, exc):
    logger.exception(exc)
    return await http_exception_handler(request, exc)


async def validation_exception_handler(request, exc):
    logger.exception(exc)
    return JSONResponse({"message": str(exc)}, HTTPStatus.BAD_REQUEST)


async def unhandled_exception_handler(request, exc):
    logger.exception(exc)
    return JSONResponse(
        {"message": "Server error occurred"},
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )
