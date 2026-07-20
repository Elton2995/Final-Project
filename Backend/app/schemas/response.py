from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.schemas.user import User

class ResponseBase(BaseModel):
    message: str = Field(..., min_length=1)

class ResponseCreate(ResponseBase):
    complaint_id: Optional[int] = None
    request_id: Optional[int] = None

class ResponseUpdate(BaseModel):
    message: Optional[str] = Field(None, min_length=1)

class Response(ResponseBase):
    id: int
    user_id: int
    complaint_id: Optional[int] = None
    request_id: Optional[int] = None
    is_staff_response: bool = False
    is_system_response: bool = False
    created_at: datetime
    updated_at: datetime
    
    # Nested relations
    user: Optional[User] = None
    
    class Config:
        from_attributes = True

class ResponseListResponse(BaseModel):
    items: List[Response]
    total: int