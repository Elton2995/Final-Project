from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_, desc
from datetime import datetime, timezone, timedelta

from app.crud.base import CRUDBase
from app.models.complaint import Complaint, ComplaintStatus, ComplaintPriority, ComplaintCategory
from app.models.user import User
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate

class CRUDComplaint(CRUDBase[Complaint, ComplaintCreate, ComplaintUpdate]):
    """Complaint CRUD operations."""
    
    def get_with_details(self, db: Session, id: int) -> Optional[Complaint]:
        """Get complaint with user and staff details."""
        return db.query(Complaint).options(
            joinedload(Complaint.user),
            joinedload(Complaint.assigned_staff)
        ).filter(
            Complaint.id == id,
            Complaint.deleted_at.is_(None)
        ).first()
    
    def get_by_complaint_id(self, db: Session, complaint_id: str) -> Optional[Complaint]:
        """Get complaint by user-friendly ID."""
        return db.query(Complaint).filter(
            Complaint.complaint_id == complaint_id,
            Complaint.deleted_at.is_(None)
        ).first()
    
    def get_by_user(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ComplaintStatus] = None
    ) -> List[Complaint]:
        """Get complaints for a specific user."""
        query = db.query(Complaint).filter(
            Complaint.user_id == user_id,
            Complaint.deleted_at.is_(None)
        )
        if status:
            query = query.filter(Complaint.status == status)
        return query.order_by(desc(Complaint.created_at)).offset(skip).limit(limit).all()
    
    def get_assigned_to_staff(
        self,
        db: Session,
        staff_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ComplaintStatus] = None
    ) -> List[Complaint]:
        """Get complaints assigned to a specific staff member."""
        query = db.query(Complaint).filter(
            Complaint.assigned_to == staff_id,
            Complaint.deleted_at.is_(None)
        )
        if status:
            query = query.filter(Complaint.status == status)
        return query.order_by(desc(Complaint.created_at)).offset(skip).limit(limit).all()
    
    def get_unassigned(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[Complaint]:
        """Get unassigned complaints."""
        return db.query(Complaint).filter(
            Complaint.assigned_to.is_(None),
            Complaint.status.in_([ComplaintStatus.OPEN, ComplaintStatus.IN_PROGRESS]),
            Complaint.deleted_at.is_(None)
        ).order_by(desc(Complaint.created_at)).offset(skip).limit(limit).all()
    
    def get_by_status(
        self,
        db: Session,
        status: ComplaintStatus,
        skip: int = 0,
        limit: int = 100
    ) -> List[Complaint]:
        """Get complaints by status."""
        return db.query(Complaint).filter(
            Complaint.status == status,
            Complaint.deleted_at.is_(None)
        ).order_by(desc(Complaint.created_at)).offset(skip).limit(limit).all()
    
    def get_stats(self, db: Session) -> Dict[str, Any]:
        """Get complaint statistics."""
        total = db.query(Complaint).filter(Complaint.deleted_at.is_(None)).count()
        
        status_counts = {}
        for status in ComplaintStatus:
            count = db.query(Complaint).filter(
                Complaint.status == status,
                Complaint.deleted_at.is_(None)
            ).count()
            status_counts[status.value] = count
        
        category_counts = {}
        for category in ComplaintCategory:
            count = db.query(Complaint).filter(
                Complaint.category == category,
                Complaint.deleted_at.is_(None)
            ).count()
            category_counts[category.value] = count
        
        priority_counts = {}
        for priority in ComplaintPriority:
            count = db.query(Complaint).filter(
                Complaint.priority == priority,
                Complaint.deleted_at.is_(None)
            ).count()
            priority_counts[priority.value] = count
        
        return {
            "total": total,
            "by_status": status_counts,
            "by_category": category_counts,
            "by_priority": priority_counts
        }
    
    def get_daily_stats(
        self,
        db: Session,
        days: int = 30
    ) -> Dict[str, List]:
        """Get daily complaint statistics for the last N days."""
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        # Daily new complaints
        daily_new = db.query(
            func.date(Complaint.created_at).label('date'),
            func.count(Complaint.id).label('count')
        ).filter(
            Complaint.created_at >= start_date,
            Complaint.deleted_at.is_(None)
        ).group_by(func.date(Complaint.created_at)).all()
        
        # Daily resolved complaints
        daily_resolved = db.query(
            func.date(Complaint.resolved_at).label('date'),
            func.count(Complaint.id).label('count')
        ).filter(
            Complaint.resolved_at >= start_date,
            Complaint.deleted_at.is_(None)
        ).group_by(func.date(Complaint.resolved_at)).all()
        
        return {
            "new": [{"date": str(d.date), "count": d.count} for d in daily_new],
            "resolved": [{"date": str(d.date), "count": d.count} for d in daily_resolved]
        }
    
    def assign_to_staff(
        self,
        db: Session,
        *,
        complaint: Complaint,
        staff_id: int
    ) -> Complaint:
        """Assign complaint to a staff member."""
        complaint.assigned_to = staff_id
        complaint.updated_at = datetime.now(timezone.utc)
        db.add(complaint)
        db.commit()
        db.refresh(complaint)
        return complaint
    
    def update_status(
        self,
        db: Session,
        *,
        complaint: Complaint,
        status: ComplaintStatus,
        resolution_notes: Optional[str] = None
    ) -> Complaint:
        """Update complaint status."""
        complaint.status = status
        complaint.updated_at = datetime.now(timezone.utc)
        
        if status == ComplaintStatus.RESOLVED:
            complaint.resolved_at = datetime.now(timezone.utc)
        elif status == ComplaintStatus.CLOSED:
            complaint.closed_at = datetime.now(timezone.utc)
            if not complaint.resolved_at:
                complaint.resolved_at = datetime.now(timezone.utc)
        
        if resolution_notes:
            complaint.resolution_notes = resolution_notes
        
        db.add(complaint)
        db.commit()
        db.refresh(complaint)
        return complaint
    
    def search_complaints(
        self,
        db: Session,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Complaint]:
        """Search complaints by title, description, or ID."""
        return db.query(Complaint).filter(
            Complaint.deleted_at.is_(None),
            or_(
                Complaint.title.ilike(f"%{query}%"),
                Complaint.description.ilike(f"%{query}%"),
                Complaint.complaint_id.ilike(f"%{query}%")
            )
        ).order_by(desc(Complaint.created_at)).offset(skip).limit(limit).all()

# Singleton instance
complaint_crud = CRUDComplaint(Complaint)