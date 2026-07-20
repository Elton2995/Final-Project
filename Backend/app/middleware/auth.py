from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import logging
import re

from app.core.security import decode_token, is_token_expired
from app.core.database import SessionLocal
from app.crud.user import user_crud

logger = logging.getLogger(__name__)

# Public routes that don't require authentication
PUBLIC_PATHS = [
    r"^/$",
    r"^/health$",
    r"^/api/v1/auth/login$",
    r"^/api/v1/auth/register$",
    r"^/api/v1/auth/refresh$",
    r"^/api/docs",
    r"^/api/redoc",
    r"^/api/openapi.json",
    r"^/uploads/",
]

class AuthMiddleware(BaseHTTPMiddleware):
    """Authentication middleware that validates JWT tokens for protected routes."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        """Process the request and validate authentication if required."""
        
        # Skip authentication for public paths
        path = request.url.path
        is_public = any(re.match(pattern, path) for pattern in PUBLIC_PATHS)
        
        if is_public:
            return await call_next(request)
        
        # Check for Authorization header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            # Allow OPTIONS requests (CORS preflight)
            if request.method == "OPTIONS":
                return await call_next(request)
            
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Not authenticated",
                    "message": "Authorization header required"
                }
            )
        
        # Extract token
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise ValueError("Invalid authentication scheme")
        except ValueError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Invalid authentication header",
                    "message": "Authorization header must be 'Bearer <token>'"
                }
            )
        
        # Validate token
        try:
            # Check if token is expired
            if is_token_expired(token):
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "detail": "Token expired",
                        "message": "Please refresh your token"
                    }
                )
            
            # Decode token
            payload = decode_token(token)
            user_id = payload.get("sub")
            
            if not user_id:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "detail": "Invalid token payload",
                        "message": "User ID not found in token"
                    }
                )
            
            # Get user from database
            db = SessionLocal()
            try:
                user = user_crud.get(db, int(user_id))
                
                if not user:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "detail": "User not found",
                            "message": "The user associated with this token no longer exists"
                        }
                    )
                
                if not user.is_active:
                    return JSONResponse(
                        status_code=status.HTTP_403_FORBIDDEN,
                        content={
                            "detail": "User inactive",
                            "message": "Your account has been deactivated"
                        }
                    )
                
                if user.deleted_at:
                    return JSONResponse(
                        status_code=status.HTTP_403_FORBIDDEN,
                        content={
                            "detail": "User deleted",
                            "message": "Your account has been deleted"
                        }
                    )
                
                # Store user in request state for later use
                request.state.user = user
                request.state.user_id = user.id
                request.state.user_role = user.role
                
            finally:
                db.close()
            
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
        except Exception as e:
            logger.error(f"Authentication middleware error: {e}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Invalid token",
                    "message": str(e)
                }
            )
        
        # Process the request
        response = await call_next(request)
        return response

class RoleMiddleware(BaseHTTPMiddleware):
    """Optional middleware for role-based logging and monitoring."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        """Log role-based access attempts."""
        
        # Skip logging for public paths
        path = request.url.path
        is_public = any(re.match(pattern, path) for pattern in PUBLIC_PATHS)
        
        if not is_public and hasattr(request.state, "user"):
            user = request.state.user
            logger.debug(f"Access: {request.method} {path} by {user.email} (role: {user.role.value})")
        
        response = await call_next(request)
        return response