import logging
import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        try:
            response = await call_next(request)
            duration = time.time() - start
            logger.info(
                "%s %s %s %.2fs",
                request.method,
                request.url.path,
                response.status_code,
                duration,
            )
            return response
        except Exception:
            duration = time.time() - start
            logger.exception(
                "%s %s failed after %.2fs",
                request.method,
                request.url.path,
                duration,
            )
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error"},
            )
