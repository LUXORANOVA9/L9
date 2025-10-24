"""
LUXORANOVA API v1
"""

from fastapi import APIRouter

# Create main API router
api_router = APIRouter()

# TODO: Import and include routers when implemented
# from app.api.v1 import auth, agents, tasks, workflows, users
# api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# api_router.include_router(agents.router, prefix="/agents", tags=["Agents"])
# api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
# api_router.include_router(workflows.router, prefix="/workflows", tags=["Workflows"])
# api_router.include_router(users.router, prefix="/users", tags=["Users"])

@api_router.get("/")
async def api_root():
    """API v1 root endpoint."""
    return {
        "version": "1.0.0",
        "status": "active",
        "message": "LUXORANOVA API v1 - Coming Soon"
    }
