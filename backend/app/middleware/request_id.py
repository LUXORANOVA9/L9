"""
Request ID Middleware - Adds unique request ID to each request
"""

import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add a unique request ID to each request.
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        Add request ID to request state and response headers.
        """
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Add to request state
        request.state.request_id = request_id
        
        # Process request
        response = await call_next(request)
        
        # Add to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response
