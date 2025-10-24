"""
Timing Middleware - Measures request processing time
"""

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to measure and log request processing time.
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        Measure request processing time and add to response headers.
        """
        # Record start time
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Add to response headers (in milliseconds)
        response.headers["X-Process-Time"] = f"{process_time * 1000:.2f}ms"
        
        return response
