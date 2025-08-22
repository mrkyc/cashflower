import time
from collections import defaultdict

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# In-memory store for request timestamps.
request_counts = defaultdict(list)

# Configuration
RATE_LIMIT_DURATION_SECONDS = 60  # 1 minute
RATE_LIMIT_REQUESTS = 1000  # requests per minute per session_id

IP_WHITELIST = {"127.0.0.1", "172.18.0.3"}


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to limit the number of requests per session ID.
    Bypasses the limit for clients on the IP_WHITELIST.
    """

    async def dispatch(self, request: Request, call_next):
        # Bypass rate limiting for whitelisted IPs (internal services)
        if request.client and request.client.host in IP_WHITELIST:
            return await call_next(request)

        session_id = request.headers.get("x-session-id")

        if session_id:
            current_time = time.time()

            # Filter out requests older than the defined duration
            request_timestamps = request_counts[session_id]
            valid_requests = [
                t
                for t in request_timestamps
                if t > current_time - RATE_LIMIT_DURATION_SECONDS
            ]

            if len(valid_requests) >= RATE_LIMIT_REQUESTS:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": f"Too many requests for session {session_id}. Please try again later."
                    },
                )

            valid_requests.append(current_time)
            request_counts[session_id] = valid_requests

        response = await call_next(request)
        return response
