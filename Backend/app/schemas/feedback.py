from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum

from app.schemas.user import User

class FeedbackCategory(str, Enum):
    OVERALL = "Overall Experience"
    SERVICE_QUALITY = "Service Quality"
    STAFF_PROFESSIONALISM = "Staff Professionalism"
    RESOLUTION_TIME = "Resolution Time"
    COMMUNICATION = "Communication"
    WEBSITE_USABILITY = "Website/App Usability"

class FeedbackBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    category: FeedbackCategory
    message: str = Field(..., min_length=20)
    suggestion: Optional[str] = None
    would_recommend: Optional[bool] = None

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    category: Optional[FeedbackCategory] = None
    message: Optional[str] = Field(None, min_length=20)
    suggestion: Optional[str] = None
    would_recommend: Optional[bool] = None

class Feedback(FeedbackBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    # Nested relations
    user: Optional[User] = None
    
    class Config:
        from_attributes = True

class FeedbackListResponse(BaseModel):
    items: List[Feedback]
    total: int
    average_rating: Optional[float] = None

class FeedbackStats(BaseModel):
    total: int
    average_rating: float
    rating_distribution: dict
    would_recommend: dict
    by_category: dict