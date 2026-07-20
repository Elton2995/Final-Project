from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_, desc, and_
from datetime import datetime, timezone, timedelta

from app.crud.base import CRUDBase
from app.models.service_request import ServiceRequest, RequestStatus, RequestPriority, RequestCategory
from app.schemas.service_request import ServiceRequestCreate, ServiceRequestUpdate

class CRUDServiceRequest(CRUDBase[ServiceRequest, ServiceRequestCreate, ServiceRequestUpdate]):
    """Service Request CRUD operations."""
    
    def get_with_details(self, db: Session, id: int) -> Optional[ServiceRequest]:
        """Get service request with user and staff details."""
        return db.query(ServiceRequest).options(
            joinedload(ServiceRequest.user),
            joinedload(ServiceRequest.assigned_staff)
        ).filter(
            ServiceRequest.id == id,
            ServiceRequest.deleted_at.is_(None)
        ).first()
    
    def get_by_request_id(self, db: Session, request_id: str) -> Optional[ServiceRequest]:
        """Get service request by user-friendly ID."""
        return db.query(ServiceRequest).filter(
            ServiceRequest.request_id == request_id,
            ServiceRequest.deleted_at.is_(None)
        ).first()
    
    def get_by_user(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[RequestStatus] = None
    ) -> List[ServiceRequest]:
        """Get service requests for a specific user."""
        query = db.query(ServiceRequest).filter(
            ServiceRequest.user_id == user_id,
            ServiceRequest.deleted_at.is_(None)
        )
        if status:
            query = query.filter(ServiceRequest.status == status)
        return query.order_by(desc(ServiceRequest.created_at)).offset(skip).limit(limit).all()
    
    def get_assigned_to_staff(
        self,
        db: Session,
        staff_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[RequestStatus] = None
    ) -> List[ServiceRequest]:
        """Get service requests assigned to a specific staff member."""
        query = db.query(ServiceRequest).filter(
            ServiceRequest.assigned_to == staff_id,
            ServiceRequest.deleted_at.is_(None)
        )
        if status:
            query = query.filter(ServiceRequest.status == status)
        return query.order_by(desc(ServiceRequest.created_at)).offset(skip).limit(limit).all()
    
    def get_unassigned(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[ServiceRequest]:
        """Get unassigned service requests."""
        return db.query(ServiceRequest).filter(
            ServiceRequest.assigned_to.is_(None),
            ServiceRequest.status == RequestStatus.PENDING,
            ServiceRequest.deleted_at.is_(None)
        ).order_by(desc(ServiceRequest.created_at)).offset(skip).limit(limit).all()
    
    def get_by_status(
        self,
        db: Session,
        status: RequestStatus,
        skip: int = 0,
        limit: int = 100
    ) -> List[ServiceRequest]:
        """Get service requests by status."""
        return db.query(ServiceRequest).filter(
            ServiceRequest.status == status,
            ServiceRequest.deleted_at.is_(None)
        ).order_by(desc(ServiceRequest.created_at)).offset(skip).limit(limit).all()
    
    def get_stats(self, db: Session) -> Dict[str, Any]:
        """Get service request statistics."""
        total = db.query(ServiceRequest).filter(ServiceRequest.deleted_at.is_(None)).count()
        
        status_counts = {}
        for status in RequestStatus:
            count = db.query(ServiceRequest).filter(
                ServiceRequest.status == status,
                ServiceRequest.deleted_at.is_(None)
            ).count()
            status_counts[status.value] = count
        
        category_counts = {}
        for category in RequestCategory:
            count = db.query(ServiceRequest).filter(
                ServiceRequest.category == category,
                ServiceRequest.deleted_at.is_(None)
            ).count()
            category_counts[category.value] = count
        
        priority_counts = {}
        for priority in RequestPriority:
            count = db.query(ServiceRequest).filter(
                ServiceRequest.priority == priority,
                ServiceRequest.deleted_at.is_(None)
            ).count()
            priority_counts[priority.value] = count
        
        return {
            "total": total,
            "by_status": status_counts,
            "by_category": category_counts,
            "by_priority": priority_counts
        }
    
    def assign_to_staff(
        self,
        db: Session,
        *,
        request_obj: ServiceRequest,
        staff_id: int
    ) -> ServiceRequest:
        """Assign service request to a staff member."""
        request_obj.assigned_to = staff_id
        request_obj.updated_at = datetime.now(timezone.utc)
        db.add(request_obj)
        db.commit()
        db.refresh(request_obj)
        return request_obj
    
    def update_status(
        self,
        db: Session,
        *,
        request_obj: ServiceRequest,
        status: RequestStatus,
        completion_notes: Optional[str] = None
    ) -> ServiceRequest:
        """Update service request status."""
        request_obj.status = status
        request_obj.updated_at = datetime.now(timezone.utc)
        
        if status == RequestStatus.COMPLETED:
            request_obj.completed_at = datetime.now(timezone.utc)
        
        if completion_notes:
            request_obj.completion_notes = completion_notes
        
        db.add(request_obj)
        db.commit()
        db.refresh(request_obj)
        return request_obj
    
    def search_requests(
        self,
        db: Session,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[ServiceRequest]:
        """Search service requests by title, description, or ID."""
        return db.query(ServiceRequest).filter(
            ServiceRequest.deleted_at.is_(None),
            or_(
                ServiceRequest.title.ilike(f"%{query}%"),
                ServiceRequest.description.ilike(f"%{query}%"),
                ServiceRequest.request_id.ilike(f"%{query}%")
            )
        ).order_by(desc(ServiceRequest.created_at)).offset(skip).limit(limit).all()

# Singleton instance
service_request_crud = CRUDServiceRequest(ServiceRequest)