import time
import logging
from fastapi import Request

logger = logging.getLogger("app")

async def logging_middleware(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        f"RequestID:{request.state.request_id} "
        f"{request.method} {request.url.path} "
        f"{response.status_code}"
    )

    return response