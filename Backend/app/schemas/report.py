from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, date

class ReportFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    assigned_to: Optional[int] = None

class DashboardStats(BaseModel):
    total_users: int
    active_users: int
    total_complaints: int
    open_complaints: int
    in_progress_complaints: int
    resolved_complaints: int
    closed_complaints: int
    total_requests: int
    pending_requests: int
    in_progress_requests: int
    completed_requests: int
    total_feedback: int
    average_rating: float
    staff_online: int
    total_staff: int

class MonthlyReport(BaseModel):
    month: str
    year: int
    new_complaints: int
    resolved_complaints: int
    new_requests: int
    completed_requests: int
    new_users: int
    feedback_count: int
    average_rating: float

class ReportResponse(BaseModel):
    title: str
    generated_at: datetime
    data: Dict[str, Any]
    filters: Optional[Dict[str, Any]] = None