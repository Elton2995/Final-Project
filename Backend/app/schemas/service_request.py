from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

from app.schemas.user import User

class RequestStatus(str, Enum):
    PENDING = "open"
    IN_PROGRESS = "inprogress"
    COMPLETED = "resolved"
    CANCELLED = "closed"

class RequestPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RequestCategory(str, Enum):
    INSTALLATION = "Installation"
    NEW_SERVICE = "New Service"
    UPGRADE = "Upgrade"
    REPAIR = "Repair"
    MAINTENANCE = "Maintenance"
    OTHER = "Other"

# Service Request Base Schema
class ServiceRequestBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=20)
    category: RequestCategory
    priority: RequestPriority = RequestPriority.MEDIUM
    preferred_date: Optional[datetime] = None
    preferred_time: Optional[str] = Field(None, max_length=50)

class ServiceRequestCreate(ServiceRequestBase):
    attachments: Optional[List[str]] = Field(default_factory=list)

class ServiceRequestUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=20)
    category: Optional[RequestCategory] = None
    priority: Optional[RequestPriority] = None
    status: Optional[RequestStatus] = None
    assigned_to: Optional[int] = None
    preferred_date: Optional[datetime] = None
    preferred_time: Optional[str] = None
    technician_name: Optional[str] = None
    completion_notes: Optional[str] = None

class ServiceRequestStatusUpdate(BaseModel):
    status: RequestStatus
    completion_notes: Optional[str] = None

class ServiceRequestAssign(BaseModel):
    assigned_to: int

# Service Request Response Schema
class ServiceRequest(ServiceRequestBase):
    id: int
    request_id: str
    status: RequestStatus
    assigned_to: Optional[int] = None
    attachments: Optional[List[str]] = None
    technician_name: Optional[str] = None
    completion_notes: Optional[str] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    # Nested relations
    user: Optional[User] = None
    assigned_staff: Optional[User] = None
    
    class Config:
        from_attributes = True

class ServiceRequestDetail(ServiceRequest):
    responses: Optional[List['Response']] = None

# Service Request List Response
class ServiceRequestListResponse(BaseModel):
    items: List[ServiceRequest]
    total: int
    page: int
    per_page: int
    total_pages: int

# Service Request Statistics
class ServiceRequestStats(BaseModel):
    total: int
    pending: int
    in_progress: int
    completed: int
    cancelled: int
    by_category: dict
    by_priority: dict

# Import for forward reference
from app.schemas.response import Response
ServiceRequestDetail.model_rebuild()