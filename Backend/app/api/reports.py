from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import require_admin_or_staff, require_admin
from app.schemas.report import DashboardStats, MonthlyReport, ReportResponse
from app.crud.user import user_crud
from app.crud.complaint import complaint_crud
from app.crud.service_request import service_request_crud
from app.crud.feedback import feedback_crud
from app.crud.audit_log import audit_log_crud
from app.models.user import User, UserRole, UserStatus

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/reports/dashboard",
    response_model=DashboardStats,
    summary="Get dashboard statistics",
    description="Get real-time dashboard statistics. Admin or staff only."
)
async def get_dashboard_stats(
    current_user: User = Depends(require_admin_or_staff),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics."""
    # User counts
    total_users = user_crud.count(db)
    active_users = db.query(User).filter(
        User.status == UserStatus.ACTIVE,
        User.deleted_at.is_(None)
    ).count()
    
    # Staff online (simplified - in production, track active sessions)
    total_staff = db.query(User).filter(
        User.role.in_([UserRole.ADMIN, UserRole.STAFF]),
        User.status == UserStatus.ACTIVE,
        User.deleted_at.is_(None)
    ).count()
    
    # Complaint stats
    complaint_stats = complaint_crud.get_stats(db)
    
    # Request stats
    request_stats = service_request_crud.get_stats(db)
    
    # Feedback stats
    feedback_stats = feedback_crud.get_stats(db)
    
    return DashboardStats(
        total_users=total_users,
        active_users=active_users,
        total_complaints=complaint_stats["total"],
        open_complaints=complaint_stats["by_status"]["open"],
        in_progress_complaints=complaint_stats["by_status"]["inprogress"],
        resolved_complaints=complaint_stats["by_status"]["resolved"],
        closed_complaints=complaint_stats["by_status"]["closed"],
        total_requests=request_stats["total"],
        pending_requests=request_stats["by_status"]["open"],
        in_progress_requests=request_stats["by_status"]["inprogress"],
        completed_requests=request_stats["by_status"]["resolved"],
        total_feedback=feedback_stats["total"],
        average_rating=feedback_stats["average_rating"],
        staff_online=total_staff,
        total_staff=total_staff
    )

@router.get(
    "/reports/monthly",
    response_model=MonthlyReport,
    summary="Get monthly report",
    description="Get monthly statistics. Admin only."
)
async def get_monthly_report(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020, le=2030),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get monthly report."""
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    # New complaints
    new_complaints = db.query(Complaint).filter(
        Complaint.created_at >= start_date,
        Complaint.created_at < end_date,
        Complaint.deleted_at.is_(None)
    ).count()
    
    # Resolved complaints
    resolved_complaints = db.query(Complaint).filter(
        Complaint.resolved_at >= start_date,
        Complaint.resolved_at < end_date,
        Complaint.deleted_at.is_(None)
    ).count()
    
    # New requests
    new_requests = db.query(ServiceRequest).filter(
        ServiceRequest.created_at >= start_date,
        ServiceRequest.created_at < end_date,
        ServiceRequest.deleted_at.is_(None)
    ).count()
    
    # Completed requests
    completed_requests = db.query(ServiceRequest).filter(
        ServiceRequest.completed_at >= start_date,
        ServiceRequest.completed_at < end_date,
        ServiceRequest.deleted_at.is_(None)
    ).count()
    
    # New users
    new_users = db.query(User).filter(
        User.created_at >= start_date,
        User.created_at < end_date,
        User.deleted_at.is_(None)
    ).count()
    
    # Feedback
    feedback_count = db.query(Feedback).filter(
        Feedback.created_at >= start_date,
        Feedback.created_at < end_date,
        Feedback.deleted_at.is_(None)
    ).count()
    
    avg_rating = db.query(func.avg(Feedback.rating)).filter(
        Feedback.created_at >= start_date,
        Feedback.created_at < end_date,
        Feedback.deleted_at.is_(None)
    ).scalar() or 0
    
    return MonthlyReport(
        month=month,
        year=year,
        new_complaints=new_complaints,
        resolved_complaints=resolved_complaints,
        new_requests=new_requests,
        completed_requests=completed_requests,
        new_users=new_users,
        feedback_count=feedback_count,
        average_rating=round(float(avg_rating), 2)
    )