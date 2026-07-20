from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import require_admin
from app.schemas.notification import (
    Notification,
    NotificationListResponse,
    NotificationMarkRead
)
from app.schemas.common import ResponseMessage
from app.crud.notification import notification_crud
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/notifications",
    response_model=NotificationListResponse,
    summary="Get notifications",
    description="Get current user's notifications."
)
async def get_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    unread_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's notifications."""
    notifications = notification_crud.get_by_user(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        unread_only=unread_only
    )
    
    total = len(notifications)
    unread_count = notification_crud.get_unread_count(db, current_user.id)
    
    return NotificationListResponse(
        items=notifications,
        total=total,
        unread_count=unread_count
    )

@router.get(
    "/notifications/unread-count",
    response_model=dict,
    summary="Get unread count",
    description="Get current user's unread notification count."
)
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get unread notification count."""
    count = notification_crud.get_unread_count(db, current_user.id)
    return {"unread_count": count}

@router.patch(
    "/notifications/{notification_id}/read",
    response_model=Notification,
    summary="Mark notification as read",
    description="Mark a specific notification as read."
)
async def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark notification as read."""
    notification = notification_crud.get(db, notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    # Check ownership
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    updated_notification = notification_crud.mark_as_read(db, notification=notification)
    return updated_notification

@router.post(
    "/notifications/mark-all-read",
    response_model=ResponseMessage,
    summary="Mark all as read",
    description="Mark all notifications as read."
)
async def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark all notifications as read."""
    count = notification_crud.mark_all_as_read(db, current_user.id)
    
    return ResponseMessage(
        message=f"Marked {count} notifications as read",
        success=True
    )

@router.delete(
    "/notifications/old",
    response_model=ResponseMessage,
    summary="Delete old notifications",
    description="Delete notifications older than specified days. Admin only."
)
async def delete_old_notifications(
    days: int = Query(30, ge=1),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete old notifications."""
    count = notification_crud.delete_old(db, days)
    
    return ResponseMessage(
        message=f"Deleted {count} old notifications",
        success=True
    )