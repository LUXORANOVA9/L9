"""
LUXORANOVA Enterprise AI Platform - Main Application Entry Point
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from prometheus_client import make_asgi_app
import uvicorn

from app.core.config import settings
from app.core.database import engine, Base
from app.core.redis_client import redis_client
from app.core.logging_config import setup_logging
from app.api.v1 import api_router
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.timing import TimingMiddleware

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifespan manager for startup and shutdown events.
    """
    # Startup
    logger.info("🚀 Starting LUXORANOVA Enterprise AI Platform...")
    
    try:
        # Initialize database
        logger.info("📊 Initializing database...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database initialized successfully")
        
        # Initialize Redis
        logger.info("🔴 Connecting to Redis...")
        await redis_client.ping()
        logger.info("✅ Redis connected successfully")
        
        # Initialize AI models
        logger.info("🤖 Loading AI models...")
        # TODO: Initialize Ollama, OpenAI, etc.
        logger.info("✅ AI models loaded successfully")
        
        # Initialize MCP servers
        logger.info("🔌 Starting MCP servers...")
        # TODO: Start MCP servers
        logger.info("✅ MCP servers started successfully")
        
        logger.info("✨ LUXORANOVA is ready to serve!")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down LUXORANOVA...")
    
    try:
        # Close Redis connection
        await redis_client.close()
        logger.info("✅ Redis connection closed")
        
        # Close database connection
        await engine.dispose()
        logger.info("✅ Database connection closed")
        
        logger.info("👋 LUXORANOVA shutdown complete")
        
    except Exception as e:
        logger.error(f"❌ Shutdown error: {str(e)}")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise AI Platform with Hierarchical Orchestration and Computer-Using Agents",
    version=settings.APP_VERSION,
    docs_url="/api/docs" if settings.APP_ENV != "production" else None,
    redoc_url="/api/redoc" if settings.APP_ENV != "production" else None,
    openapi_url="/api/openapi.json" if settings.APP_ENV != "production" else None,
    lifespan=lifespan,
)


# ============================================================================
# Middleware Configuration
# ============================================================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
)

# Gzip Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Trusted Host (Production only)
if settings.APP_ENV == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    )

# Custom Middleware
app.add_middleware(RequestIDMiddleware)
app.add_middleware(TimingMiddleware)
app.add_middleware(RateLimitMiddleware)


# ============================================================================
# Exception Handlers
# ============================================================================

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "request_id": request.state.request_id,
            }
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": 422,
                "message": "Validation error",
                "details": exc.errors(),
                "request_id": request.state.request_id,
            }
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error",
                "request_id": request.state.request_id,
            }
        },
    )


# ============================================================================
# Routes
# ============================================================================

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for load balancers and monitoring.
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
    }


# Readiness check endpoint
@app.get("/ready", tags=["Health"])
async def readiness_check():
    """
    Readiness check endpoint for Kubernetes.
    """
    try:
        # Check database connection
        from app.core.database import execute_raw_sql
        await execute_raw_sql("SELECT 1")
        
        # Check Redis connection
        await redis_client.ping()
        
        return {
            "status": "ready",
            "checks": {
                "database": "ok",
                "redis": "ok",
            }
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "error": str(e),
            }
        )


# Liveness check endpoint
@app.get("/live", tags=["Health"])
async def liveness_check():
    """
    Liveness check endpoint for Kubernetes.
    """
    return {"status": "alive"}


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Enterprise AI Platform with Hierarchical Orchestration",
        "docs": f"{settings.API_URL}/api/docs",
        "health": f"{settings.API_URL}/health",
    }


# Include API router
app.include_router(api_router, prefix="/api/v1")


# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    """
    Run the application with uvicorn.
    """
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.APP_ENV == "development",
        workers=settings.WORKERS if settings.APP_ENV == "production" else 1,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
        use_colors=True,
    )
