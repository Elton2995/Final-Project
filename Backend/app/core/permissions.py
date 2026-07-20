from typing import List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User, UserRole

def require_role(allowed_roles: List[UserRole]):
    """
    Factory function to create role-based permission dependencies.
    """
    async def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        """Check if current user has the required role."""
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    
    return role_checker

# Pre-defined role dependencies for easy use
async def require_admin(current_user: User = Depends(require_role([UserRole.ADMIN]))):
    """Require admin role."""
    return current_user

async def require_staff(current_user: User = Depends(require_role([UserRole.STAFF]))):
    """Require staff role."""
    return current_user

async def require_customer(current_user: User = Depends(require_role([UserRole.CUSTOMER]))):
    """Require customer role."""
    return current_user

async def require_admin_or_staff(
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """Require admin or staff role."""
    return current_user

# Resource ownership check
async def check_resource_ownership(
    resource_user_id: int,
    current_user: User = Depends(get_current_user)
) -> bool:
    """
    Check if current user owns the resource or is admin/staff.
    """
    if current_user.role in [UserRole.ADMIN, UserRole.STAFF]:
        return True
    return current_user.id == resource_user_id

def require_ownership_or_admin(resource_user_id: int):
    """
    Dependency to check if user owns the resource or is admin.
    """
    async def checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.role == UserRole.ADMIN:
            return current_user
        if current_user.id != resource_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource"
            )
        return current_user
    
    return checker