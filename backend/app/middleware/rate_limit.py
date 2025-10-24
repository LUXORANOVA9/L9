"""
Rate Limiting Middleware - Prevents API abuse
"""

import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from app.core.config import settings
from app.core.redis_client import redis_client

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to implement rate limiting using Redis.
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        Check rate limit before processing request.
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/ready", "/live"]:
            return await call_next(request)
        
        # Get client identifier (IP address or API key)
        client_id = self._get_client_id(request)
        
        # Check rate limit
        try:
            allowed, remaining = await self._check_rate_limit(client_id)
            
            if not allowed:
                return JSONResponse(
                    status_code=HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "error": {
                            "code": 429,
                            "message": "Rate limit exceeded. Please try again later.",
                            "retry_after": 60
                        }
                    },
                    headers={
                        "X-RateLimit-Limit": str(settings.RATE_LIMIT_PER_MINUTE),
                        "X-RateLimit-Remaining": "0",
                        "Retry-After": "60"
                    }
                )
            
            # Process request
            response = await call_next(request)
            
            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_PER_MINUTE)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            
            return response
            
        except Exception as e:
            logger.error(f"Rate limiting error: {str(e)}")
            # Allow request on error (fail open)
            return await call_next(request)
    
    def _get_client_id(self, request: Request) -> str:
        """
        Get client identifier from request.
        """
        # Try to get API key from header
        api_key = request.headers.get(settings.API_KEY_HEADER)
        if api_key:
            return f"api_key:{api_key}"
        
        # Fall back to IP address
        client_ip = request.client.host if request.client else "unknown"
        return f"ip:{client_ip}"
    
    async def _check_rate_limit(self, client_id: str) -> tuple[bool, int]:
        """
        Check if client has exceeded rate limit.
        
        Returns:
            (allowed, remaining): Whether request is allowed and remaining count
        """
        try:
            # Initialize Redis client if needed
            if not redis_client._client:
                await redis_client.connect()
            
            # Check rate limit
            return await redis_client.rate_limit_check(
                key=client_id,
                limit=settings.RATE_LIMIT_PER_MINUTE,
                window=60  # 1 minute window
            )
        except Exception as e:
            logger.error(f"Rate limit check failed: {str(e)}")
            # Allow on error
            return True, settings.RATE_LIMIT_PER_MINUTE
