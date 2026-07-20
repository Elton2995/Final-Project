from pydantic import BaseModel
from typing import Optional, Any, List
from datetime import datetime

class ResponseMessage(BaseModel):
    message: str
    success: bool = True
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    message: str
    success: bool = False
    errors: Optional[List[dict]] = None
    status_code: int

class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 10
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "asc"

class DateRangeFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None