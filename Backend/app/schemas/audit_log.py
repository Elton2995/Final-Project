from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class AuditAction(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    SOFT_DELETE = "soft_delete"
    RESTORE = "restore"
    ROLE_CHANGE = "role_change"
    PERMISSION_CHANGE = "permission_change"
    STATUS_CHANGE = "status_change"
    ASSIGN = "assign"
    RESOLVE = "resolve"
    CLOSE = "close"

class AuditLogBase(BaseModel):
    action: AuditAction
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    details: Optional[Dict[str, Any]] = None

class AuditLogCreate(AuditLogBase):
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class AuditLog(AuditLogBase):
    id: int
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class AuditLogListResponse(BaseModel):
    items: List[AuditLog]
    total: int
    page: int
    per_page: int
    total_pages: int