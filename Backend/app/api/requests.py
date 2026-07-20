from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import (
    require_admin,
    require_admin_or_staff,
    require_customer,
    require_staff
)
from app.schemas.service_request import (
    ServiceRequest,
    ServiceRequestCreate,
    ServiceRequestUpdate,
    ServiceRequestStatusUpdate,
    ServiceRequestAssign,
    ServiceRequestDetail,
    ServiceRequestListResponse,
    ServiceRequestStats,
    RequestStatus,
    RequestPriority,
    RequestCategory
)
from app.schemas.response import ResponseCreate, Response
from app.schemas.common import ResponseMessage
from app.crud.service_request import service_request_crud
from app.crud.response import response_crud
from app.crud.notification import notification_crud
from app.crud.audit_log import audit_log_crud
from app.models.user import User, UserRole

logger = logging.getLogger(__name__)
router = APIRouter()

def generate_request_id(db: Session) -> str:
    """Generate a unique request ID."""
    count = db.query(ServiceRequest).count() + 1
    return f"REQ-{count:03d}"

@router.post(
    "/requests",
    response_model=ServiceRequest,
    status_code=status.HTTP_201_CREATED,
    summary="Create service request",
    description="Submit a new service request. Customer only."
)
async def create_service_request(
    request_data: ServiceRequestCreate,
    request: Request,
    current_user: User = Depends(require_customer),
    db: Session = Depends(get_db)
):
    """Create a new service request."""
    request_id = generate_request_id(db)
    
    service_request = service_request_crud.create(
        db,
        obj_in=request_data,
        request_id=request_id,
        user_id=current_user.id,
        status=RequestStatus.PENDING
    )
    
    # Create notification for customer
    notification_crud.create_notification(
        db,
        user_id=current_user.id,
        title="Service Request Submitted",
        message=f"Your service request '{service_request.title}' has been submitted successfully.",
        notification_type="request_update",
        data={"request_id": service_request.id}
    )
    
    # Notify admin/staff
    staff_users = db.query(User).filter(
        User.role.in_([UserRole.ADMIN, UserRole.STAFF]),
        User.status == "active",
        User.deleted_at.is_(None)
    ).all()
    
    for staff in staff_users:
        notification_crud.create_notification(
            db,
            user_id=staff.id,
            title="New Service Request",
            message=f"New service request '{service_request.title}' submitted by {current_user.full_name}",
            notification_type="request_update",
            data={"request_id": service_request.id}
        )
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="create",
        resource_type="service_request",
        resource_id=service_request.id,
        details={"request_id": service_request.request_id},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} created service request {service_request.request_id}")
    
    return service_request

@router.get(
    "/requests",
    response_model=ServiceRequestListResponse,
    summary="Get service requests",
    description="Get service requests with filtering. Access depends on user role."
)
async def get_service_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[RequestStatus] = None,
    priority: Optional[RequestPriority] = None,
    category: Optional[RequestCategory] = None,
    assigned_to: Optional[int] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get service requests with filtering."""
    filters = {}
    
    if current_user.role == UserRole.CUSTOMER:
        filters["user_id"] = current_user.id
    else:
        if status:
            filters["status"] = status
        if priority:
            filters["priority"] = priority
        if category:
            filters["category"] = category
        if assigned_to:
            filters["assigned_to"] = assigned_to
    
    search_fields = ["title", "description", "request_id"] if search else None
    
    requests = service_request_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        filters=filters,
        search=search,
        search_fields=search_fields
    )
    
    total = service_request_crud.count(
        db,
        filters=filters,
        search=search,
        search_fields=search_fields
    )
    
    return ServiceRequestListResponse(
        items=requests,
        total=total,
        page=skip // limit + 1,
        per_page=limit,
        total_pages=(total + limit - 1) // limit
    )

@router.get(
    "/requests/{request_id}",
    response_model=ServiceRequestDetail,
    summary="Get service request by ID",
    description="Get a specific service request's details."
)
async def get_service_request(
    request_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get service request by user-friendly ID."""
    service_request = service_request_crud.get_by_request_id(db, request_id)
    if not service_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.CUSTOMER and service_request.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Load responses
    responses = response_crud.get_by_request(db, service_request.id)
    service_request.responses = responses
    
    return service_request

@router.put(
    "/requests/{request_id}",
    response_model=ServiceRequest,
    summary="Update service request",
    description="Update a service request. Only the owner or admin can update."
)
async def update_service_request(
    request_id: str,
    request_data: ServiceRequestUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a service request."""
    service_request = service_request_crud.get_by_request_id(db, request_id)
    if not service_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.CUSTOMER and service_request.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    updated_request = service_request_crud.update(
        db,
        db_obj=service_request,
        obj_in=request_data
    )
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="update",
        resource_type="service_request",
        resource_id=service_request.id,
        details={"updated_fields": request_data.model_dump(exclude_unset=True)},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} updated service request {service_request.request_id}")
    
    return updated_request

@router.patch(
    "/requests/{request_id}/status",
    response_model=ServiceRequest,
    summary="Update service request status",
    description="Update service request status. Staff or admin only."
)
async def update_service_request_status(
    request_id: str,
    status_data: ServiceRequestStatusUpdate,
    request: Request,
    current_user: User = Depends(require_admin_or_staff),
    db: Session = Depends(get_db)
):
    """Update service request status."""
    service_request = service_request_crud.get_by_request_id(db, request_id)
    if not service_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found"
        )
    
    old_status = service_request.status
    
    updated_request = service_request_crud.update_status(
        db,
        request_obj=service_request,
        status=status_data.status,
        completion_notes=status_data.completion_notes
    )
    
    # Notify customer
    notification_crud.create_notification(
        db,
        user_id=service_request.user_id,
        title="Service Request Status Updated",
        message=f"Your service request '{service_request.title}' status changed from {old_status.value} to {status_data.status.value}.",
        notification_type="request_update",
        data={"request_id": service_request.id}
    )
    
    # If completed, add system response
    if status_data.status == RequestStatus.COMPLETED:
        response_crud.create_for_request(
            db,
            request_id=service_request.id,
            user_id=current_user.id,
            message=f"Service request marked as completed. {status_data.completion_notes or ''}",
            is_staff_response=True,
            is_system_response=True
        )
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="status_change",
        resource_type="service_request",
        resource_id=service_request.id,
        details={"old_status": old_status.value, "new_status": status_data.status.value},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} updated status of service request {service_request.request_id} to {status_data.status.value}")
    
    return updated_request

@router.post(
    "/requests/{request_id}/assign",
    response_model=ServiceRequest,
    summary="Assign service request",
    description="Assign service request to staff member. Admin or staff only."
)
async def assign_service_request(
    request_id: str,
    assign_data: ServiceRequestAssign,
    request: Request,
    current_user: User = Depends(require_admin_or_staff),
    db: Session = Depends(get_db)
):
    """Assign service request to a staff member."""
    service_request = service_request_crud.get_by_request_id(db, request_id)
    if not service_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found"
        )
    
    # Verify staff exists
    staff = user_crud.get(db, assign_data.assigned_to)
    if not staff or staff.role not in [UserRole.ADMIN, UserRole.STAFF]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid staff member"
        )
    
    updated_request = service_request_crud.assign_to_staff(
        db,
        request_obj=service_request,
        staff_id=assign_data.assigned_to
    )
    
    # Notify staff
    notification_crud.create_notification(
        db,
        user_id=assign_data.assigned_to,
        title="Service Request Assigned",
        message=f"Service request '{service_request.title}' has been assigned to you.",
        notification_type="assignment",
        data={"request_id": service_request.id}
    )
    
    # Notify customer
    notification_crud.create_notification(
        db,
        user_id=service_request.user_id,
        title="Service Request Assigned",
        message=f"Your service request '{service_request.title}' has been assigned to {staff.full_name}.",
        notification_type="assignment",
        data={"request_id": service_request.id}
    )
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="assign",
        resource_type="service_request",
        resource_id=service_request.id,
        details={"assigned_to": assign_data.assigned_to},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} assigned service request {service_request.request_id} to {staff.email}")
    
    return updated_request

@router.post(
    "/requests/{request_id}/responses",
    response_model=Response,
    status_code=status.HTTP_201_CREATED,
    summary="Add response to service request",
    description="Add a response to a service request."
)
async def add_request_response(
    request_id: str,
    response_data: ResponseCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a response to a service request."""
    service_request = service_request_crud.get_by_request_id(db, request_id)
    if not service_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.CUSTOMER and service_request.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    is_staff = current_user.role in [UserRole.ADMIN, UserRole.STAFF]
    
    response = response_crud.create_for_request(
        db,
        request_id=service_request.id,
        user_id=current_user.id,
        message=response_data.message,
        is_staff_response=is_staff,
        is_system_response=False
    )
    
    # Notify other party
    if is_staff:
        notification_crud.create_notification(
            db,
            user_id=service_request.user_id,
            title="New Response",
            message=f"Staff responded to your service request '{service_request.title}': {response_data.message[:100]}...",
            notification_type="response",
            data={"request_id": service_request.id}
        )
    else:
        if service_request.assigned_to:
            notification_crud.create_notification(
                db,
                user_id=service_request.assigned_to,
                title="New Response",
                message=f"Customer responded to service request '{service_request.title}': {response_data.message[:100]}...",
                notification_type="response",
                data={"request_id": service_request.id}
            )
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="create",
        resource_type="response",
        resource_id=response.id,
        details={"request_id": service_request.request_id},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} added response to service request {service_request.request_id}")
    
    return response

@router.get(
    "/requests/stats",
    response_model=ServiceRequestStats,
    summary="Get service request statistics",
    description="Get service request statistics. Admin or staff only."
)
async def get_request_stats(
    current_user: User = Depends(require_admin_or_staff),
    db: Session = Depends(get_db)
):
    """Get service request statistics."""
    stats = service_request_crud.get_stats(db)
    
    return ServiceRequestStats(
        total=stats["total"],
        pending=stats["by_status"]["open"],
        in_progress=stats["by_status"]["inprogress"],
        completed=stats["by_status"]["resolved"],
        cancelled=stats["by_status"]["closed"],
        by_category=stats["by_category"],
        by_priority=stats["by_priority"]
    )