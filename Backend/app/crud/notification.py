from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from datetime import datetime, timezone

from app.crud.base import CRUDBase
from app.models.notification import Notification, NotificationType
from app.schemas.notification import NotificationCreate, NotificationUpdate

class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    """Notification CRUD operations."""
    
    def get_by_user(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        unread_only: bool = False
    ) -> List[Notification]:
        """Get notifications for a specific user."""
        query = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.deleted_at.is_(None)
        )
        if unread_only:
            query = query.filter(Notification.is_read == False)
        return query.order_by(desc(Notification.created_at)).offset(skip).limit(limit).all()
    
    def get_unread_count(self, db: Session, user_id: int) -> int:
        """Get unread notification count for a user."""
        return db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False,
            Notification.deleted_at.is_(None)
        ).count()
    
    def mark_as_read(
        self,
        db: Session,
        *,
        notification: Notification
    ) -> Notification:
        """Mark a notification as read."""
        notification.is_read = True
        notification.read_at = datetime.now(timezone.utc)
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification
    
    def mark_all_as_read(
        self,
        db: Session,
        user_id: int
    ) -> int:
        """Mark all notifications as read for a user."""
        count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False,
            Notification.deleted_at.is_(None)
        ).update({
            "is_read": True,
            "read_at": datetime.now(timezone.utc)
        })
        db.commit()
        return count
    
    def create_notification(
        self,
        db: Session,
        user_id: int,
        title: str,
        message: str,
        notification_type: NotificationType,
        data: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """Create a new notification."""
        return self.create(
            db,
            obj_in=NotificationCreate(
                title=title,
                message=message,
                type=notification_type,
                data=data,
                user_id=user_id
            )
        )
    
    def create_bulk(
        self,
        db: Session,
        user_ids: List[int],
        title: str,
        message: str,
        notification_type: NotificationType,
        data: Optional[Dict[str, Any]] = None
    ) -> List[Notification]:
        """Create notifications for multiple users."""
        notifications = []
        for user_id in user_ids:
            notification = self.create_notification(
                db, user_id, title, message, notification_type, data
            )
            notifications.append(notification)
        return notifications
    
    def delete_old(
        self,
        db: Session,
        days: int = 30
    ) -> int:
        """Delete notifications older than the specified days."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        count = db.query(Notification).filter(
            Notification.created_at < cutoff,
            Notification.deleted_at.is_(None)
        ).count()
        
        db.query(Notification).filter(
            Notification.created_at < cutoff
        ).delete()
        db.commit()
        return count

# Singleton instance
notification_crud = CRUDNotification(Notification)