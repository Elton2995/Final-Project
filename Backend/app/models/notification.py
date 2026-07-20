from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Text, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base

class NotificationType(str, enum.Enum):
    """Notification type enum."""
    COMPLAINT_UPDATE = "complaint_update"
    REQUEST_UPDATE = "request_update"
    RESPONSE = "response"
    STATUS_CHANGE = "status_change"
    ASSIGNMENT = "assignment"
    REMINDER = "reminder"
    SYSTEM = "system"

class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = (
        Index('idx_notification_user', 'user_id'),
        Index('idx_notification_read', 'is_read'),
        Index('idx_notification_type', 'type'),
        Index('idx_notification_created', 'created_at'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Additional data (JSON)
    data = Column(Text, nullable=True)  # JSON string with additional data
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, read={self.is_read})>"
    
    def mark_as_read(self):
        """Mark notification as read."""
        from datetime import datetime, timezone
        self.is_read = True
        self.read_at = datetime.now(timezone.utc)