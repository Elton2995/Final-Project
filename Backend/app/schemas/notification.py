from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    COMPLAINT_UPDATE = "complaint_update"
    REQUEST_UPDATE = "request_update"
    RESPONSE = "response"
    STATUS_CHANGE = "status_change"
    ASSIGNMENT = "assignment"
    REMINDER = "reminder"
    SYSTEM = "system"

class NotificationBase(BaseModel):
    title: str = Field(..., max_length=255)
    message: str
    type: NotificationType
    data: Optional[Dict[str, Any]] = None

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None

class Notification(NotificationBase):
    id: int
    user_id: int
    is_read: bool = False
    read_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class NotificationListResponse(BaseModel):
    items: List[Notification]
    total: int
    unread_count: int

class NotificationMarkRead(BaseModel):
    notification_ids: Optional[List[int]] = None
    mark_all: bool = False