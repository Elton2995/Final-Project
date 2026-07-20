from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

from app.schemas.user import User

class ComplaintStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "inprogress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class ComplaintPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class ComplaintCategory(str, Enum):
    TECHNICAL = "Technical Issue"
    BILLING = "Billing"
    SERVICE_OUTAGE = "Service Outage"
    ACCOUNT = "Account Management"
    PRODUCT_QUALITY = "Product Quality"
    CUSTOMER_SERVICE = "Customer Service"
    OTHER = "Other"

# Complaint Base Schema
class ComplaintBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=20)
    category: ComplaintCategory
    priority: ComplaintPriority = ComplaintPriority.MEDIUM

class ComplaintCreate(ComplaintBase):
    attachments: Optional[List[str]] = Field(default_factory=list)

class ComplaintUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=20)
    category: Optional[ComplaintCategory] = None
    priority: Optional[ComplaintPriority] = None
    status: Optional[ComplaintStatus] = None
    assigned_to: Optional[int] = None
    resolution_notes: Optional[str] = None

class ComplaintStatusUpdate(BaseModel):
    status: ComplaintStatus
    resolution_notes: Optional[str] = None

class ComplaintAssign(BaseModel):
    assigned_to: int

class ComplaintResponse(BaseModel):
    message: str
    complaint_id: int

# Complaint Response Schema
class Complaint(ComplaintBase):
    id: int
    complaint_id: str
    status: ComplaintStatus
    assigned_to: Optional[int] = None
    attachments: Optional[List[str]] = None
    resolution_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    # Nested relations
    user: Optional[User] = None
    assigned_staff: Optional[User] = None
    
    class Config:
        from_attributes = True

class ComplaintDetail(Complaint):
    responses: Optional[List['Response']] = None

# Complaint List Response
class ComplaintListResponse(BaseModel):
    items: List[Complaint]
    total: int
    page: int
    per_page: int
    total_pages: int

# Complaint Statistics
class ComplaintStats(BaseModel):
    total: int
    open: int
    in_progress: int
    resolved: int
    closed: int
    by_category: dict
    by_priority: dict
    daily_new: Optional[List[dict]] = None
    daily_resolved: Optional[List[dict]] = None

# Import for forward reference
from app.schemas.response import Response
ComplaintDetail.model_rebuild()