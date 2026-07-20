from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
import logging

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.core.dependencies import get_current_user
from app.schemas.user import (
    UserLogin,
    UserCreate,
    UserWithToken,
    RefreshTokenRequest,
    RefreshTokenResponse,
    User,
    UserUpdate
)
from app.schemas.common import ResponseMessage
from app.crud.user import user_crud
from app.crud.audit_log import audit_log_crud
from app.crud.notification import notification_crud
from app.models.user import User as UserModel
from app.models.refresh_token import RefreshToken

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=UserWithToken,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new customer account."
)
async def register(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    
    - **full_name**: Full name of the user
    - **email**: Valid email address
    - **phone**: Phone number (optional)
    - **password**: Password (min 8 characters)
    - **confirm_password**: Must match password
    """
    # Check if email already exists
    existing_user = user_crud.get_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = user_crud.create(db, obj_in=user_data)
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    # Store refresh token
    refresh_token_obj = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    )
    db.add(refresh_token_obj)
    db.commit()
    
    # Create welcome notification
    notification_crud.create_notification(
        db,
        user_id=user.id,
        title="Welcome to ServiceDesk!",
        message=f"Welcome {user.full_name}! Your account has been created successfully.",
        notification_type="system",
        data={"action": "welcome"}
    )
    
    # Log registration
    audit_log_crud.log_action(
        db,
        user_id=user.id,
        action="create",
        resource_type="user",
        resource_id=user.id,
        details={"action": "registration"},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"New user registered: {user.email}")
    
    return UserWithToken(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        role=user.role,
        status=user.status,
        avatar=user.avatar,
        last_login=user.last_login,
        created_at=user.created_at,
        updated_at=user.updated_at,
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post(
    "/login",
    response_model=UserWithToken,
    summary="Login to the system",
    description="Authenticate user and return JWT tokens."
)
async def login(
    login_data: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Login with email and password.
    
    - **email**: Registered email address
    - **password**: Account password
    """
    # Authenticate user
    user = user_crud.authenticate(
        db, email=login_data.email, password=login_data.password
    )
    if not user:
        audit_log_crud.log_action(
            db,
            user_id=None,
            action="login",
            resource_type="user",
            details={"email": login_data.email, "success": False},
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user = user_crud.update_last_login(db, user=user)
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    # Store refresh token (revoke old ones)
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user.id,
        RefreshToken.is_revoked == False
    ).update({"is_revoked": True})
    
    refresh_token_obj = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    )
    db.add(refresh_token_obj)
    db.commit()
    
    # Log login
    audit_log_crud.log_action(
        db,
        user_id=user.id,
        action="login",
        resource_type="user",
        resource_id=user.id,
        details={"email": user.email, "success": True},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User logged in: {user.email}")
    
    return UserWithToken(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        role=user.role,
        status=user.status,
        avatar=user.avatar,
        last_login=user.last_login,
        created_at=user.created_at,
        updated_at=user.updated_at,
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post(
    "/logout",
    response_model=ResponseMessage,
    summary="Logout user",
    description="Logout user and invalidate refresh token."
)
async def logout(
    request: Request,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout the current user."""
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        
        # Revoke refresh tokens
        db.query(RefreshToken).filter(
            RefreshToken.user_id == current_user.id,
            RefreshToken.is_revoked == False
        ).update({"is_revoked": True})
        db.commit()
    
    # Log logout
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="logout",
        resource_type="user",
        resource_id=current_user.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User logged out: {current_user.email}")
    
    return ResponseMessage(
        message="Logged out successfully",
        success=True
    )

@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    summary="Refresh access token",
    description="Get a new access token using a refresh token."
)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token.
    
    - **refresh_token**: Valid refresh token
    """
    try:
        # Verify refresh token
        payload = verify_token(refresh_data.refresh_token, token_type="refresh")
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Check if refresh token exists and is not revoked
        refresh_token_obj = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_data.refresh_token,
            RefreshToken.is_revoked == False
        ).first()
        
        if not refresh_token_obj:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or revoked refresh token"
            )
        
        # Check if token is expired
        if refresh_token_obj.is_expired:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )
        
        # Get user
        user = user_crud.get(db, int(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Create new access token
        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role.value}
        )
        
        logger.info(f"Access token refreshed for user: {user.email}")
        
        return RefreshTokenResponse(
            access_token=access_token
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.get(
    "/me",
    response_model=User,
    summary="Get current user",
    description="Get the currently authenticated user's information."
)
async def get_me(
    current_user: UserModel = Depends(get_current_user)
):
    """Get current user information."""
    return User(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        phone=current_user.phone,
        role=current_user.role,
        status=current_user.status,
        avatar=current_user.avatar,
        last_login=current_user.last_login,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

@router.put(
    "/me",
    response_model=User,
    summary="Update current user",
    description="Update the current user's profile."
)
async def update_me(
    user_data: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile."""
    # Check email uniqueness if changing
    if user_data.email and user_data.email != current_user.email:
        existing = user_crud.get_by_email(db, email=user_data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
    
    # Update user
    updated_user = user_crud.update(db, db_obj=current_user, obj_in=user_data)
    
    logger.info(f"User updated profile: {updated_user.email}")
    
    return User(
        id=updated_user.id,
        full_name=updated_user.full_name,
        email=updated_user.email,
        phone=updated_user.phone,
        role=updated_user.role,
        status=updated_user.status,
        avatar=updated_user.avatar,
        last_login=updated_user.last_login,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at
    )