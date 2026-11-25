"""Gives every request an ID, logs it, and records API usage."""

import logging
import time
import uuid

from fastapi import Request, Response

from genericfinder.api.errors import problem_response
from genericfinder.db.models import ApiRequest
from genericfinder.logging_setup import request_id_ctx

logger = logging.getLogger("genericfinder.http")


async def request_context(request: Request, call_next) -> Response:
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:16]
    token = request_id_ctx.set(request_id)
    start = time.perf_counter()
    response = None

    try:
        try:
            response = await call_next(request)
        except Exception:
            logger.exception("unhandled error")
            response = problem_response(
                request, 500, "Something went wrong on our side. Quote the request ID."
            )

        return response

    finally:
        latency_ms = round((time.perf_counter() - start) * 1000)

        if response is not None:
            response.headers["X-Request-ID"] = request_id

            try:
                async with request.app.state.sessionmaker() as session:
                    session.add(
                        ApiRequest(
                            request_id=request_id,
                            method=request.method,
                            path=request.url.path[:255],
                            status_code=response.status_code,
                            latency_ms=latency_ms,
                        )
                    )
                    await session.commit()
            except Exception:
                logger.exception("failed to record API request")

            logger.info(
                "request finished",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status": response.status_code,
                    "duration_ms": latency_ms,
                },
            )

        request_id_ctx.reset(token)
