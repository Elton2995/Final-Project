import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.database import engine, Base
from app.core.dependencies import get_current_user
from app.api import (
    auth, users, complaints, requests, feedback, 
    reports, notifications, settings as settings_routes,
    admin
)
from app.middleware.auth import AuthMiddleware
from app.utils.exceptions import (
    AppException,
    app_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    generic_exception_handler
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import (
    auth, users, complaints, requests, feedback, 
    reports, notifications, settings, admin
)

# ... (rest of the file remains the same)

# API Router - Using routers folder
api_prefix = settings.API_PREFIX

# Public routes (no authentication required)
app.include_router(auth.router, prefix=api_prefix)

# Protected routes (authentication required)
app.include_router(users.router, prefix=api_prefix)
app.include_router(complaints.router, prefix=api_prefix)
app.include_router(requests.router, prefix=api_prefix)
app.include_router(feedback.router, prefix=api_prefix)
app.include_router(reports.router, prefix=api_prefix)
app.include_router(notifications.router, prefix=api_prefix)
app.include_router(settings.router, prefix=api_prefix)
app.include_router(admin.router, prefix=api_prefix)

# Setup logging
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Starting ServiceDesk Backend...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"API Prefix: {settings.API_PREFIX}")
    
    # Create upload directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Create database tables
    async with engine.begin() as conn:
        # In production, use Alembic migrations instead
        # await conn.run_sync(Base.metadata.create_all)
        pass
    
    yield
    
    # Shutdown
    logger.info("Shutting down ServiceDesk Backend...")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Customer Service Information System for Small Service-Based Businesses",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Auth Middleware
app.add_middleware(AuthMiddleware)

# Exception Handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Static files
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# API Router
api_prefix = settings.API_PREFIX

# Public routes (no authentication required)
app.include_router(auth.router, prefix=api_prefix, tags=["Authentication"])

# Protected routes (authentication required)
app.include_router(users.router, prefix=api_prefix, tags=["Users"])
app.include_router(complaints.router, prefix=api_prefix, tags=["Complaints"])
app.include_router(requests.router, prefix=api_prefix, tags=["Service Requests"])
app.include_router(feedback.router, prefix=api_prefix, tags=["Feedback"])
app.include_router(reports.router, prefix=api_prefix, tags=["Reports"])
app.include_router(notifications.router, prefix=api_prefix, tags=["Notifications"])
app.include_router(settings_routes.router, prefix=api_prefix, tags=["Settings"])
app.include_router(admin.router, prefix=api_prefix, tags=["Administration"])

# Health Check Endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "documentation": "/api/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )