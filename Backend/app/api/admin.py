from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta
import logging

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import require_admin
from app.schemas.user import User, UserListResponse, UserRoleUpdate, UserStatusUpdate
from app.schemas.audit_log import AuditLog, AuditLogListResponse, AuditAction
from app.schemas.common import ResponseMessage
from app.crud.user import user_crud
from app.crud.audit_log import audit_log_crud
from app.crud.complaint import complaint_crud
from app.crud.service_request import service_request_crud
from app.crud.feedback import feedback_crudfrom app.models.user import User as UserModel, UserRole, UserStatus

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/admin/system-stats",
    response_model=dict,
    summary="Get system statistics",
    description="Get comprehensive system statistics. Admin only."
)
async def get_system_stats(
    current_user: UserModel = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get comprehensive system statistics."""
    # User stats
    total_users = user_crud.count(db)
    active_users = db.query(UserModel).filter(
        UserModel.status == UserStatus.ACTIVE,
        UserModel.deleted_at.is_(None)
    ).count()
    
    # Complaint stats
    complaint_stats = complaint_crud.get_stats(db)
    
    # Request stats
    request_stats = service_request_crud.get_stats(db)
    
    # Feedback stats
    feedback_stats = feedback_crud.get_stats(db)
    
    # Audit stats
    audit_stats = audit_log_crud.get_stats(db)
    
    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "by_role": user_crud.get_count_by_role(db),
            "by_status": user_crud.get_count_by_status(db)
        },
        "complaints": complaint_stats,
        "requests": request_stats,
        "feedback": feedback_stats,
        "audit": audit_stats,
        "generated_at": datetime.now().isoformat()
    }

@router.get(
    "/admin/audit-logs",
    response_model=AuditLogListResponse,
    summary="Get audit logs",
    description="Get audit logs with filtering. Admin only."
)
async def get_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    user_id: Optional[int] = None,
    action: Optional[AuditAction] = None,
    resource_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: UserModel = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get audit logs with filtering."""
    query = db.query(AuditLog)
    
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if action:
        query = query.filter(AuditLog.action == action)
    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)
    if start_date:
        query = query.filter(AuditLog.created_at >= start_date)
    if end_date:
        query = query.filter(AuditLog.created_at <= end_date)
    
    total = query.count()
    logs = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
    
    return AuditLogListResponse(
        items=logs,
        total=total,
        page=skip // limit + 1,
        per_page=limit,
        total_pages=(total + limit - 1) // limit
    )

@router.get(
    "/admin/recent-activity",
    response_model=List[dict],
    summary="Get recent activity",
    description="Get recent system activity. Admin only."
)
async def get_recent_activity(
    limit: int = Query(20, ge=1, le=100),
    current_user: UserModel = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get recent system activity."""
    recent_logs = audit_log_crud.get_recent(db, days=7, limit=limit)
    
    # Get user names for the logs
    user_ids = [log.user_id for log in recent_logs if log.user_id]
    users = db.query(UserModel).filter(UserModel.id.in_(user_ids)).all()
    user_map = {u.id: u.full_name for u in users}
    
    return [
        {
            "id": log.id,
            "user": user_map.get(log.user_id, "System"),
            "user_id": log.user_id,
            "action": log.action.value,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "details": log.details,
            "created_at": log.created_at.isoformat()
        }
        for log in recent_logs
    ]

@router.get(
    "/admin/users/export",
    response_model=List[dict],
    summary="Export users",
    description="Export user data. Admin only."
)
async def export_users(
    current_user: UserModel = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Export user data."""
    users = user_crud.get_multi(db, skip=0, limit=1000)
    
    return [
        {
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "phone": u.phone,
            "role": u.role.value,
            "status": u.status.value,
            "created_at": u.created_at.isoformat(),
            "last_login": u.last_login.isoformat() if u.last_login else None
        }
        for u in users
    ]

@router.get(
    "/admin/seed",
    response_model=ResponseMessage,
    summary="Seed initial data",
    description="Seed initial system data (admin, staff, settings). Admin only."
)
async def seed_data(
    current_user: UserModel = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Seed initial system data."""
    # Check if admin already exists
    admin = user_crud.get_by_email(db, "admin@servicedesk.com")
    if not admin:
        from app.schemas.user import UserCreate
        admin_data = UserCreate(
            full_name="System Administrator",
            email="admin@servicedesk.com",
            phone="+1 234 567 8900",
            password="Admin123!",
            confirm_password="Admin123!",
            role=UserRole.ADMIN
        )
        admin = user_crud.create(db, obj_in=admin_data)
    
    # Check if staff already exists
    staff = user_crud.get_by_email(db, "staff@servicedesk.com")
    if not staff:
        staff_data = UserCreate(
            full_name="Support Staff",
            email="staff@servicedesk.com",
            phone="+1 234 567 8901",
            password="Staff123!",
            confirm_password="Staff123!",
            role=UserRole.STAFF
        )
        staff = user_crud.create(db, obj_in=staff_data)
    
    # Check if test customer exists
    customer = user_crud.get_by_email(db, "customer@servicedesk.com")
    if not customer:
        customer_data = UserCreate(
            full_name="Test Customer",
            email="customer@servicedesk.com",
            phone="+1 234 567 8902",
            password="Customer123!",
            confirm_password="Customer123!",
            role=UserRole.CUSTOMER
        )
        customer = user_crud.create(db, obj_in=customer_data)
    
    logger.info("Seed data created successfully")
    
    return ResponseMessage(
        message="Seed data created successfully",
        success=True
    )