from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import require_admin, require_admin_or_staff
from app.schemas.user import (
    User,
    UserCreate,
    UserUpdate,
    UserRoleUpdate,
    UserStatusUpdate,
    UserListResponse,
    UserChangePassword
)
from app.schemas.common import ResponseMessage
from app.crud.user import user_crud
from app.crud.audit_log import audit_log_crud
from app.models.user import UserRole, UserStatus

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/users",
    response_model=UserListResponse,
    summary="Get all users",
    description="Get a list of all users with pagination. Admin only."
)
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    role: Optional[UserRole] = None,
    status: Optional[UserStatus] = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get all users with filtering and pagination."""
    filters = {}
    if role:
        filters["role"] = role
    if status:
        filters["status"] = status
    
    search_fields = ["full_name", "email"] if search else None
    
    users = user_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        filters=filters,
        search=search,
        search_fields=search_fields
    )
    
    total = user_crud.count(
        db,
        filters=filters,
        search=search,
        search_fields=search_fields
    )
    
    return UserListResponse(
        items=users,
        total=total,
        page=skip // limit + 1,
        per_page=limit,
        total_pages=(total + limit - 1) // limit
    )

@router.get(
    "/users/{user_id}",
    response_model=User,
    summary="Get user by ID",
    description="Get a specific user's information. Admin or staff only."
)
async def get_user(
    user_id: int,
    current_user: User = Depends(require_admin_or_staff),
    db: Session = Depends(get_db)
):
    """Get user by ID."""
    user = user_crud.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put(
    "/users/{user_id}",
    response_model=User,
    summary="Update user",
    description="Update a user's information. Admin only."
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update user information."""
    user = user_crud.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check email uniqueness if changing
    if user_data.email and user_data.email != user.email:
        existing = user_crud.get_by_email(db, email=user_data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
    
    updated_user = user_crud.update(db, db_obj=user, obj_in=user_data)
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="update",
        resource_type="user",
        resource_id=user_id,
        details={"updated_fields": user_data.model_dump(exclude_unset=True)},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} updated user {user.email}")
    
    return updated_user

@router.put(
    "/users/{user_id}/role",
    response_model=User,
    summary="Update user role",
    description="Update a user's role. Admin only."
)
async def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update user role."""
    user = user_crud.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from demoting themselves
    if user_id == current_user.id and role_data.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role"
        )
    
    updated_user = user_crud.update_role(db, user=user, role=role_data.role)
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="role_change",
        resource_type="user",
        resource_id=user_id,
        details={"old_role": user.role.value, "new_role": role_data.role.value},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} changed role for {user.email} to {role_data.role.value}")
    
    return updated_user

@router.put(
    "/users/{user_id}/status",
    response_model=User,
    summary="Update user status",
    description="Update a user's status (active/inactive/suspended). Admin only."
)
async def update_user_status(
    user_id: int,
    status_data: UserStatusUpdate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update user status."""
    user = user_crud.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deactivating themselves
    if user_id == current_user.id and status_data.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own status"
        )
    
    updated_user = user_crud.update_status(db, user=user, status=status_data.status)
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="status_change",
        resource_type="user",
        resource_id=user_id,
        details={"old_status": user.status.value, "new_status": status_data.status.value},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} changed status for {user.email} to {status_data.status.value}")
    
    return updated_user

@router.delete(
    "/users/{user_id}",
    response_model=ResponseMessage,
    summary="Delete user",
    description="Soft delete a user. Admin only."
)
async def delete_user(
    user_id: int,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Soft delete a user."""
    user = user_crud.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deleting themselves
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    user_crud.soft_delete(db, id=user_id)
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="soft_delete",
        resource_type="user",
        resource_id=user_id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} deleted user {user.email}")
    
    return ResponseMessage(
        message="User deleted successfully",
        success=True
    )

@router.post(
    "/users/{user_id}/restore",
    response_model=User,
    summary="Restore deleted user",
    description="Restore a soft-deleted user. Admin only."
)
async def restore_user(
    user_id: int,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Restore a soft-deleted user."""
    user = user_crud.restore(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or not deleted"
        )
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="restore",
        resource_type="user",
        resource_id=user_id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} restored user {user.email}")
    
    return user

@router.post(
    "/users/change-password",
    response_model=ResponseMessage,
    summary="Change password",
    description="Change current user's password."
)
async def change_password(
    password_data: UserChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password."""
    # Verify current password
    if not user_crud.authenticate(
        db, email=current_user.email, password=password_data.current_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    user_crud.update_password(db, user=current_user, new_password=password_data.new_password)
    
    logger.info(f"User {current_user.email} changed password")
    
    return ResponseMessage(
        message="Password updated successfully",
        success=True
    )

@router.get(
    "/users/stats",
    response_model=dict,
    summary="Get user statistics",
    description="Get user statistics. Admin only."
)
async def get_user_stats(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get user statistics."""
    return {
        "by_status": user_crud.get_count_by_status(db),
        "by_role": user_crud.get_count_by_role(db)
    }