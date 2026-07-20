from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import Optional, List
import logging

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import (
    require_admin,
    require_admin_or_staff,
    require_customer,
    require_staff
)
from app.schemas.complaint import (
    Complaint,
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintStatusUpdate,
    ComplaintAssign,
    ComplaintDetail,
    ComplaintListResponse,
    ComplaintStats,
    ComplaintStatus,
    ComplaintPriority,
    ComplaintCategory
)
from app.schemas.response import ResponseCreate, Response
from app.schemas.common import ResponseMessage
from app.crud.complaint import complaint_crud
from app.crud.response import response_crud
from app.crud.notification import notification_crud
from app.crud.audit_log import audit_log_crud
from app.models.user import User, UserRole

logger = logging.getLogger(__name__)
router = APIRouter()

def generate_complaint_id(db: Session) -> str:
    """Generate a unique complaint ID."""
    count = db.query(Complaint).count() + 1
    return f"CMP-{count:03d}"

@router.post(
    "/complaints",
    response_model=Complaint,
    status_code=status.HTTP_201_CREATED,
    summary="Create a complaint",
    description="Submit a new complaint. Customer only."
)
async def create_complaint(
    complaint_data: ComplaintCreate,
    request: Request,
    current_user: User = Depends(require_customer),
    db: Session = Depends(get_db)
):
    """Create a new complaint."""
    complaint_id = generate_complaint_id(db)
    
    complaint = complaint_crud.create(
        db,
        obj_in=complaint_data,
        complaint_id=complaint_id,
        user_id=current_user.id,
        status=ComplaintStatus.OPEN
    )
    
    # Create notification for staff
    notification_crud.create_notification(
        db,
        user_id=current_user.id,
        title="Complaint Submitted",
        message=f"Your complaint '{complaint.title}' has been submitted successfully.",
        notification_type="complaint_update",
        data={"complaint_id": complaint.id}
    )
    
    # Notify admin/staff about new complaint
    staff_users = db.query(User).filter(
        User.role.in_([UserRole.ADMIN, UserRole.STAFF]),
        User.status == "active",
        User.deleted_at.is_(None)
    ).all()
    
    for staff in staff_users:
        notification_crud.create_notification(
            db,
            user_id=staff.id,
            title="New Complaint",
            message=f"New complaint '{complaint.title}' submitted by {current_user.full_name}",
            notification_type="complaint_update",
            data={"complaint_id": complaint.id}
        )
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="create",
        resource_type="complaint",
        resource_id=complaint.id,
        details={"complaint_id": complaint.complaint_id},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} created complaint {complaint.complaint_id}")
    
    return complaint

@router.get(
    "/complaints",
    response_model=ComplaintListResponse,
    summary="Get complaints",
    description="Get complaints with filtering. Access depends on user role."
)
async def get_complaints(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[ComplaintStatus] = None,
    priority: Optional[ComplaintPriority] = None,
    category: Optional[ComplaintCategory] = None,
    assigned_to: Optional[int] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get complaints with filtering."""
    filters = {}
    
    if current_user.role == UserRole.CUSTOMER:
        # Customers can only see their own complaints
        filters["user_id"] = current_user.id
    else:
        # Admin and staff can see all with filters
        if status:
            filters["status"] = status
        if priority:
            filters["priority"] = priority
        if category:
            filters["category"] = category
        if assigned_to:
            filters["assigned_to"] = assigned_to
    
    search_fields = ["title", "description", "complaint_id"] if search else None
    
    complaints = complaint_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        filters=filters,
        search=search,
        search_fields=search_fields
    )
    
    total = complaint_crud.count(
        db,
        filters=filters,
        search=search,
        search_fields=search_fields
    )
    
    return ComplaintListResponse(
        items=complaints,
        total=total,
        page=skip // limit + 1,
        per_page=limit,
        total_pages=(total + limit - 1) // limit
    )

@router.get(
    "/complaints/{complaint_id}",
    response_model=ComplaintDetail,
    summary="Get complaint by ID",
    description="Get a specific complaint's details."
)
async def get_complaint(
    complaint_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get complaint by user-friendly ID."""
    complaint = complaint_crud.get_by_complaint_id(db, complaint_id)
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.CUSTOMER and complaint.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Load responses
    responses = response_crud.get_by_complaint(db, complaint.id)
    complaint.responses = responses
    
    return complaint

@router.put(
    "/complaints/{complaint_id}",
    response_model=Complaint,
    summary="Update complaint",
    description="Update a complaint. Only the owner or admin can update."
)
async def update_complaint(
    complaint_id: str,
    complaint_data: ComplaintUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a complaint."""
    complaint = complaint_crud.get_by_complaint_id(db, complaint_id)
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.CUSTOMER and complaint.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    updated_complaint = complaint_crud.update(db, db_obj=complaint, obj_in=complaint_data)
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="update",
        resource_type="complaint",
        resource_id=complaint.id,
        details={"updated_fields": complaint_data.model_dump(exclude_unset=True)},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} updated complaint {complaint.complaint_id}")
    
    return updated_complaint

@router.patch(
    "/complaints/{complaint_id}/status",
    response_model=Complaint,
    summary="Update complaint status",
    description="Update complaint status. Staff or admin only."
)
async def update_complaint_status(
    complaint_id: str,
    status_data: ComplaintStatusUpdate,
    request: Request,
    current_user: User = Depends(require_admin_or_staff),
    db: Session = Depends(get_db)
):
    """Update complaint status."""
    complaint = complaint_crud.get_by_complaint_id(db, complaint_id)
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    old_status = complaint.status
    
    updated_complaint = complaint_crud.update_status(
        db,
        complaint=complaint,
        status=status_data.status,
        resolution_notes=status_data.resolution_notes
    )
    
    # Notify customer
    notification_crud.create_notification(
        db,
        user_id=complaint.user_id,
        title="Complaint Status Updated",
        message=f"Your complaint '{complaint.title}' status changed from {old_status.value} to {status_data.status.value}.",
        notification_type="status_change",
        data={"complaint_id": complaint.id}
    )
    
    # If resolved or closed, add system response
    if status_data.status in [ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED]:
        response_crud.create_for_complaint(
            db,
            complaint_id=complaint.id,
            user_id=current_user.id,
            message=f"Complaint marked as {status_data.status.value}. {status_data.resolution_notes or ''}",
            is_staff_response=True,
            is_system_response=True
        )
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="status_change",
        resource_type="complaint",
        resource_id=complaint.id,
        details={"old_status": old_status.value, "new_status": status_data.status.value},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} updated status of complaint {complaint.complaint_id} to {status_data.status.value}")
    
    return updated_complaint

@router.post(
    "/complaints/{complaint_id}/assign",
    response_model=Complaint,
    summary="Assign complaint",
    description="Assign complaint to staff member. Admin or staff only."
)
async def assign_complaint(
    complaint_id: str,
    assign_data: ComplaintAssign,
    request: Request,
    current_user: User = Depends(require_admin_or_staff),
    db: Session = Depends(get_db)
):
    """Assign complaint to a staff member."""
    complaint = complaint_crud.get_by_complaint_id(db, complaint_id)
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Verify staff exists
    staff = user_crud.get(db, assign_data.assigned_to)
    if not staff or staff.role not in [UserRole.ADMIN, UserRole.STAFF]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid staff member"
        )
    
    updated_complaint = complaint_crud.assign_to_staff(
        db,
        complaint=complaint,
        staff_id=assign_data.assigned_to
    )
    
    # Notify staff
    notification_crud.create_notification(
        db,
        user_id=assign_data.assigned_to,
        title="Complaint Assigned",
        message=f"Complaint '{complaint.title}' has been assigned to you.",
        notification_type="assignment",
        data={"complaint_id": complaint.id}
    )
    
    # Notify customer
    notification_crud.create_notification(
        db,
        user_id=complaint.user_id,
        title="Complaint Assigned",
        message=f"Your complaint '{complaint.title}' has been assigned to {staff.full_name}.",
        notification_type="assignment",
        data={"complaint_id": complaint.id}
    )
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="assign",
        resource_type="complaint",
        resource_id=complaint.id,
        details={"assigned_to": assign_data.assigned_to},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} assigned complaint {complaint.complaint_id} to {staff.email}")
    
    return updated_complaint

@router.post(
    "/complaints/{complaint_id}/responses",
    response_model=Response,
    status_code=status.HTTP_201_CREATED,
    summary="Add response to complaint",
    description="Add a response to a complaint."
)
async def add_complaint_response(
    complaint_id: str,
    response_data: ResponseCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a response to a complaint."""
    complaint = complaint_crud.get_by_complaint_id(db, complaint_id)
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.CUSTOMER and complaint.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    is_staff = current_user.role in [UserRole.ADMIN, UserRole.STAFF]
    
    response = response_crud.create_for_complaint(
        db,
        complaint_id=complaint.id,
        user_id=current_user.id,
        message=response_data.message,
        is_staff_response=is_staff,
        is_system_response=False
    )
    
    # Notify other party
    if is_staff:
        # Notify customer
        notification_crud.create_notification(
            db,
            user_id=complaint.user_id,
            title="New Response",
            message=f"Staff responded to your complaint '{complaint.title}': {response_data.message[:100]}...",
            notification_type="response",
            data={"complaint_id": complaint.id}
        )
    else:
        # Notify assigned staff
        if complaint.assigned_to:
            notification_crud.create_notification(
                db,
                user_id=complaint.assigned_to,
                title="New Response",
                message=f"Customer responded to complaint '{complaint.title}': {response_data.message[:100]}...",
                notification_type="response",
                data={"complaint_id": complaint.id}
            )
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="create",
        resource_type="response",
        resource_id=response.id,
        details={"complaint_id": complaint.complaint_id},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} added response to complaint {complaint.complaint_id}")
    
    return response

@router.get(
    "/complaints/stats",
    response_model=ComplaintStats,
    summary="Get complaint statistics",
    description="Get complaint statistics. Admin or staff only."
)
async def get_complaint_stats(
    current_user: User = Depends(require_admin_or_staff),
    db: Session = Depends(get_db)
):
    """Get complaint statistics."""
    stats = complaint_crud.get_stats(db)
    daily_stats = complaint_crud.get_daily_stats(db)
    
    return ComplaintStats(
        total=stats["total"],
        open=stats["by_status"]["open"],
        in_progress=stats["by_status"]["inprogress"],
        resolved=stats["by_status"]["resolved"],
        closed=stats["by_status"]["closed"],
        by_category=stats["by_category"],
        by_priority=stats["by_priority"],
        daily_new=daily_stats["new"],
        daily_resolved=daily_stats["resolved"]
    )